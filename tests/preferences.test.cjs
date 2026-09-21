const {test} = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/preferences.js'), 'utf8');

// Exercise the actual browser script at its DOM/storage/media boundaries.
function run(options = {}) {
  const data = {...options.saved};
  const writes = [];
  const icons = ['system', 'light', 'dark'].map(mode => ({dataset: {icon: mode}, toggleAttribute(_, hidden) {this.hidden = hidden;}}));
  const button = {hidden: true, setAttribute(key, value) {this[key] = value;}, querySelectorAll() {return icons;}, addEventListener(_, fn) {this.click = fn;}};
  const links = ['en', 'pt'].map(locale => ({dataset: {locale}, addEventListener(_, fn) {this.click = fn;}}));
  const root = {dataset: {entry: options.neutral ? 'neutral' : 'explicit'}, lang: options.lang || 'en'};
  const media = {matches: !!options.dark, addEventListener(_, fn) {this.change = fn;}};
  let ready;
  const location = {hash: options.hash || '', replace(url) {this.redirect = url;}};
  const context = {
    document: {documentElement: root, addEventListener(_, fn) {ready = fn;}, querySelector() {return button;}, querySelectorAll() {return links;}},
    navigator: {language: options.browserLocale},
    window: {location, ...(options.noDetection ? {} : {matchMedia() {return media;}})},
    localStorage: {getItem(key) {if (options.blockStorage) throw Error('blocked'); return data[key] ?? null;}, setItem(key, value) {if (options.blockStorage) throw Error('blocked'); writes.push([key, value]); data[key] = value;}}
  };
  vm.runInNewContext(source, context);
  ready();
  return {root, button, icons, links, media, location, writes, data};
}

test('System defaults, Light fallback, no implicit storage writes', () => {
  for (const options of [{}, {noDetection:true}, {blockStorage:true}, {saved:{'portfolio-theme':'invalid'}}]) {
    const s = run(options);
    assert.equal(s.root.dataset.themePreference, 'system');
    assert.equal(s.root.dataset.theme, 'light');
    assert.deepEqual(s.writes, []);
  }
  assert.equal(run({dark:true}).root.dataset.theme, 'dark');
});

test('cycle updates palette, localized labels, symbols, and saved preference', () => {
  const s = run({lang:'pt-BR'});
  for (const [mode, label] of [['light','claro'], ['dark','escuro'], ['system','sistema']]) {
    s.button.click();
    assert.equal(s.root.dataset.themePreference, mode);
    assert.match(s.button['aria-label'], new RegExp(`Tema: ${label}\\.`));
    assert.equal(s.icons.filter(i=>!i.hidden)[0].dataset.icon, mode);
    assert.equal(s.data['portfolio-theme'], mode);
  }
});

test('live system changes affect System only; blocked persistence is safe', () => {
  const s = run({blockStorage:true});
  s.media.matches = true; s.media.change();
  assert.equal(s.root.dataset.theme, 'dark');
  s.button.click();
  s.media.change();
  assert.equal(s.root.dataset.theme, 'light');
  s.button.click();
  s.media.matches = false; s.media.change();
  assert.equal(s.root.dataset.theme, 'dark');
  s.button.click();
  assert.equal(s.root.dataset.theme, 'light');
});

test('saved themes survive fresh page initialization independently of locale', () => {
  for (const lang of ['en', 'pt-BR']) {
    assert.equal(run({lang, saved:{'portfolio-theme':'dark'}, dark:false}).root.dataset.theme, 'dark');
    assert.equal(run({lang, saved:{'portfolio-theme':'light'}, dark:true}).root.dataset.theme, 'light');
  }
});

test('locale detection uses primary language and English fallback', () => {
  for (const [browserLocale, expected] of [['pt-BR','pt'], ['pt-PT','pt'], ['pt','pt'], ['en','en'], ['es','en'], ['fr-FR','en'], [undefined,'en']]) {
    assert.equal(run({neutral:true, browserLocale}).location.redirect, `/${expected}/`);
  }
});

test('explicit routes win; saved locale wins only at neutral entry', () => {
  const saved = {'portfolio-locale':'en'};
  assert.equal(run({browserLocale:'pt-BR',saved,neutral:true}).location.redirect, '/en/');
  assert.equal(run({lang:'pt-BR',saved}).location.redirect, undefined);
  assert.equal(run({neutral:true,browserLocale:'pt-PT',saved:{'portfolio-locale':'invalid'}}).location.redirect, '/pt/');
  assert.equal(run({neutral:true,browserLocale:'pt-BR',blockStorage:true}).location.redirect, '/pt/');
});

test('manual language choice saves independently and preserves current section', () => {
  const s = run({saved:{'portfolio-theme':'dark'}});
  s.location.hash = '#background';
  s.links[1].click();
  assert.equal(s.data['portfolio-locale'], 'pt');
  assert.equal(s.links[1].hash, '#background');
  assert.equal(s.data['portfolio-theme'], 'dark');
  assert.equal(run({neutral:true,hash:'#work'}).location.redirect, '/en/#work');
});
