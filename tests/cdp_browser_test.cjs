const { spawn } = require('node:child_process');
const http = require('node:http');

const CHROME_PATH = process.env.BROWSER_BIN || 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = parseInt(process.env.CDP_PORT || '9223', 10);

async function getJson(url) {
  return new Promise((resolve, reject) => {
    http.get(url, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(JSON.parse(data)));
    }).on('error', reject);
  });
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

class CDPClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.id = 0;
    this.callbacks = new Map();
    this.eventListeners = new Map();
  }

  async init() {
    return new Promise((resolve, reject) => {
      this.ws.onopen = resolve;
      this.ws.onerror = reject;
      this.ws.onmessage = msg => {
        const res = JSON.parse(msg.data);
        if (res.id && this.callbacks.has(res.id)) {
          const { resolve, reject } = this.callbacks.get(res.id);
          this.callbacks.delete(res.id);
          if (res.error) reject(new Error(res.error.message));
          else resolve(res.result);
        } else if (res.method && this.eventListeners.has(res.method)) {
          const listeners = this.eventListeners.get(res.method);
          listeners.forEach(fn => fn(res.params));
        }
      };
    });
  }

  once(event) {
    return new Promise(resolve => {
      if (!this.eventListeners.has(event)) {
        this.eventListeners.set(event, new Set());
      }
      const cb = (params) => {
        this.eventListeners.get(event).delete(cb);
        resolve(params);
      };
      this.eventListeners.get(event).add(cb);
    });
  }

  send(method, params = {}) {
    return new Promise((resolve, reject) => {
      const id = ++this.id;
      this.callbacks.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }

  async evaluate(expression) {
    const res = await this.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise: true });
    if (res.exceptionDetails) {
      throw new Error(JSON.stringify(res.exceptionDetails));
    }
    return res.result.value;
  }

  async setViewport(width, height) {
    await this.send('Emulation.setDeviceMetricsOverride', {
      width,
      height,
      deviceScaleFactor: 1,
      mobile: width < 768
    });
  }

  async navigate(url) {
    const loadPromise = this.once('Page.loadEventFired');
    await this.send('Page.navigate', { url });
    await loadPromise;
    for (let i = 0; i < 40; i++) {
      const ready = await this.evaluate(`location.href !== 'about:blank' && document.readyState === 'complete'`);
      if (ready) break;
      await sleep(100);
    }
    await sleep(100);
  }

  close() {
    this.ws.close();
  }
}

async function run() {
  console.log('Launching headless Chrome for release candidate verification...');
  const chrome = spawn(CHROME_PATH, [
    '--headless=new',
    `--remote-debugging-port=${PORT}`,
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--user-data-dir=' + require('node:os').tmpdir() + '\\chrome-test-' + Date.now()
  ]);

  let cdp;
  try {
    // Wait for Chrome remote debugging endpoint
    let version;
    for (let i = 0; i < 30; i++) {
      await sleep(200);
      try {
        version = await getJson(`http://127.0.0.1:${PORT}/json/version`);
        if (version.webSocketDebuggerUrl) break;
      } catch {}
    }

    if (!version || !version.webSocketDebuggerUrl) {
      throw new Error('Could not connect to Chrome debugging endpoint');
    }

    // Get a page target
    const targets = await getJson(`http://127.0.0.1:${PORT}/json/list`);
    const pageTarget = targets.find(t => t.type === 'page') || targets[0];
    cdp = new CDPClient(pageTarget.webSocketDebuggerUrl);
    await cdp.init();
    await cdp.send('Page.enable');
    await cdp.send('Runtime.enable');

    console.log('Connected to Chrome via CDP.');

    const BASE = process.env.TARGET_URL || 'http://127.0.0.1:4173';
    console.log(`Testing target: ${BASE}`);

    const widths = [360, 390, 768, 1440];
    const routes = [
      '/en/',
      '/pt/',
      '/en/work/mgs/',
      '/pt/work/mgs/',
      '/en/work/mapa/',
      '/pt/work/mapa/',
      '/404.html'
    ];

    console.log('\n--- 1. Testing responsive overflow at 360, 390, 768, 1440px ---');
    for (const width of widths) {
      await cdp.setViewport(width, 900);
      for (const route of routes) {
        await cdp.navigate(`${BASE}${route}`);
        const result = await cdp.evaluate(`({
          path: location.pathname,
          innerWidth: window.innerWidth,
          scrollWidth: document.documentElement.scrollWidth,
          overflow: document.documentElement.scrollWidth > window.innerWidth,
          h1Count: document.querySelectorAll('h1').length
        })`);

        if (result.overflow) {
          throw new Error(`Overflow detected at width ${width}px on route ${route}: scrollWidth=${result.scrollWidth}, innerWidth=${result.innerWidth}`);
        }
        if (result.h1Count !== 1) {
          throw new Error(`Expected exactly 1 h1 on route ${route}, found ${result.h1Count}`);
        }
      }
      console.log(`✓ All 7 routes fit cleanly without horizontal overflow at ${width}px`);
    }

    console.log('\n--- 2. Testing theme cycle and keyboard interactivity ---');
    await cdp.setViewport(1440, 900);
    await cdp.navigate(`${BASE}/en/`);

    // Initial theme: system (resolves to light or dark)
    let themeState = await cdp.evaluate(`({
      theme: document.documentElement.dataset.theme,
      pref: document.documentElement.dataset.themePreference,
      label: document.querySelector('.theme-toggle')?.getAttribute('aria-label')
    })`);
    console.log('Initial state:', themeState);

    // Click 1: switch to light
    await cdp.evaluate(`document.querySelector('.theme-toggle').click()`);
    themeState = await cdp.evaluate(`({
      theme: document.documentElement.dataset.theme,
      pref: document.documentElement.dataset.themePreference,
      label: document.querySelector('.theme-toggle').getAttribute('aria-label')
    })`);
    if (themeState.pref !== 'light' || themeState.theme !== 'light') {
      throw new Error(`Expected light theme, got ${JSON.stringify(themeState)}`);
    }
    console.log('✓ Cycled to light:', themeState);

    // Click 2: switch to dark
    await cdp.evaluate(`document.querySelector('.theme-toggle').click()`);
    themeState = await cdp.evaluate(`({
      theme: document.documentElement.dataset.theme,
      pref: document.documentElement.dataset.themePreference,
      label: document.querySelector('.theme-toggle').getAttribute('aria-label')
    })`);
    if (themeState.pref !== 'dark' || themeState.theme !== 'dark') {
      throw new Error(`Expected dark theme, got ${JSON.stringify(themeState)}`);
    }
    console.log('✓ Cycled to dark:', themeState);

    // Click 3: return to system
    await cdp.evaluate(`document.querySelector('.theme-toggle').click()`);
    themeState = await cdp.evaluate(`({
      theme: document.documentElement.dataset.theme,
      pref: document.documentElement.dataset.themePreference
    })`);
    if (themeState.pref !== 'system') {
      throw new Error(`Expected system theme, got ${JSON.stringify(themeState)}`);
    }
    console.log('✓ Returned to system:', themeState);

    console.log('\n--- 3. Testing case study cross-navigation ---');
    // Navigate from /en/work/mapa/ to Portuguese equivalent
    await cdp.navigate(`${BASE}/en/work/mapa/`);
    const ptLink = await cdp.evaluate(`document.querySelector('a[data-locale="pt"]').getAttribute('href')`);
    if (ptLink !== '/pt/work/mapa/') {
      throw new Error(`Expected ptLink to be /pt/work/mapa/, got ${ptLink}`);
    }
    await cdp.navigate(`${BASE}${ptLink}`);
    const heading = await cdp.evaluate(`document.querySelector('h1').innerText`);
    if (!heading.includes('Transformando planilhas')) {
      throw new Error(`Expected Portuguese heading for Mapa da Bella, got ${heading}`);
    }
    console.log('✓ Cross-locale case navigation verified:', { ptLink, heading });

    // Navigate to homepage via back link
    await cdp.evaluate(`document.querySelector('.arrow[href$="#work"]').click()`);
    await sleep(200);
    const homeUrl = await cdp.evaluate(`location.pathname + location.hash`);
    console.log('✓ Returned to home from case study:', homeUrl);

    console.log('\n--- 4. Testing interactive collapsible FAQ ---');
    await cdp.navigate(`${BASE}/en/`);
    let faqState = await cdp.evaluate(`(() => {
      const items = Array.from(document.querySelectorAll('.faq-item')).map(item => ({
        question: item.querySelector('.faq-question')?.innerText?.trim() || '',
        answer: item.querySelector('.faq-answer')?.textContent?.trim() || '',
        open: item.open || false
      }));
      return {
        count: items.length,
        items
      };
    })()`);

    if (faqState.count !== 3) {
      throw new Error(`Expected 3 FAQ items on /en/, got ${faqState.count}`);
    }
    if (faqState.items.some(i => i.open)) {
      throw new Error('All FAQ questions should start collapsed by default');
    }
    if (!faqState.items[0].question.includes('What agentic tools do you use?')) {
      throw new Error(`Unexpected FAQ question 1: ${faqState.items[0].question}`);
    }
    if (!faqState.items[0].answer.includes('Antigravity, Claude Code, Codex, Grok Build, and OpenCode')) {
      throw new Error(`Unexpected FAQ answer 1: ${faqState.items[0].answer}`);
    }
    if (!faqState.items[1].question.includes('Where did you learn to use AI?')) {
      throw new Error(`Unexpected FAQ question 2: ${faqState.items[1].question}`);
    }
    if (!faqState.items[1].answer.includes('certified AI professional through Google')) {
      throw new Error(`Unexpected FAQ answer 2: ${faqState.items[1].answer}`);
    }
    if (!faqState.items[2].question.includes('Where did you learn English?')) {
      throw new Error(`Unexpected FAQ question 3: ${faqState.items[2].question}`);
    }
    if (!faqState.items[2].answer.includes('CNA') || !faqState.items[2].answer.includes('C2 by EF SET')) {
      throw new Error(`Unexpected FAQ answer 3: ${faqState.items[2].answer}`);
    }
    console.log('✓ All 3 FAQ items start collapsed with expected question and answer content');

    // Click item 1 to expand
    await cdp.evaluate(`document.querySelectorAll('.faq-question')[0].click()`);
    let isItem1Open = await cdp.evaluate(`document.querySelectorAll('.faq-item')[0].open`);
    if (!isItem1Open) {
      throw new Error('FAQ item 1 failed to expand on click');
    }
    console.log('✓ FAQ item 1 expands on user click');

    // Click item 3 to expand
    await cdp.evaluate(`document.querySelectorAll('.faq-question')[2].click()`);
    let isItem3Open = await cdp.evaluate(`document.querySelectorAll('.faq-item')[2].open`);
    if (!isItem3Open) {
      throw new Error('FAQ item 3 failed to expand on click');
    }
    console.log('✓ FAQ item 3 expands on user click');

    // Click item 1 again to collapse
    await cdp.evaluate(`document.querySelectorAll('.faq-question')[0].click()`);
    isItem1Open = await cdp.evaluate(`document.querySelectorAll('.faq-item')[0].open`);
    if (isItem1Open) {
      throw new Error('FAQ item 1 failed to collapse on second click');
    }
    console.log('✓ FAQ item 1 collapses cleanly on subsequent click');

    console.log('\n--- 5. Testing in-page tab navigation and browser history behavior ---');
    await cdp.navigate(`${BASE}/en/`);
    const initialHist = await cdp.evaluate(`({
      length: history.length,
      canGoBack: window.navigation ? window.navigation.canGoBack : null
    })`);
    console.log('Initial page history state:', initialHist);

    const sections = ['work', 'background', 'faq', 'availability', 'contact'];
    for (const sec of sections) {
      await cdp.evaluate(`document.querySelector('.sections a[href*="#${sec}"]').click()`);
      await sleep(150);

      const navState = await cdp.evaluate(`({
        hash: location.hash,
        length: history.length,
        canGoBack: window.navigation ? window.navigation.canGoBack : null,
        top: Math.round(document.getElementById('${sec}').getBoundingClientRect().top)
      })`);

      if (navState.hash !== `#${sec}`) {
        throw new Error(`Expected hash #${sec}, got ${navState.hash}`);
      }
      if (navState.length !== initialHist.length) {
        throw new Error(`History length expanded on tab #${sec} click: expected ${initialHist.length}, got ${navState.length}`);
      }
      if (initialHist.canGoBack === false && navState.canGoBack !== false) {
        throw new Error(`Browser back button became enabled after clicking in-page tab #${sec}`);
      }
      console.log(`✓ Tab #${sec} updated URL without history expansion:`, navState);
    }

    // Click brand link to return to top
    await cdp.evaluate(`document.querySelector('a.brand').click()`);
    await sleep(150);
    const brandState = await cdp.evaluate(`({
      hash: location.hash,
      length: history.length,
      scrollY: window.scrollY
    })`);
    if (brandState.hash !== '' || brandState.scrollY !== 0 || brandState.length !== initialHist.length) {
      throw new Error(`Brand click failed to return to top or expanded history: ${JSON.stringify(brandState)}`);
    }
    console.log('✓ Brand click returned to top without history expansion:', brandState);

    console.log('\n======================================');
    console.log('ALL BROWSER VALIDATION CHECKS PASSED!');
    console.log('======================================\n');
  } finally {
    if (cdp) cdp.close();
    chrome.kill();
  }
}

run().catch(err => {
  console.error('Test failed:', err);
  process.exit(1);
});
