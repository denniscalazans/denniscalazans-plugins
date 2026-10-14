#!/usr/bin/env node
/*
 * check_mermaid.cjs: render every Mermaid diagram of a document at phone width
 * and fail when a label is cut off, glued together, or too small to read.
 *
 * Why: a phone does not wrap Mermaid labels, so a long label is cut at the
 * node's edge. And Mermaid's strict mode drops "<br/>" inside a label, so the
 * words stick together ("imobiliáriassuecas"). Both pass a desktop glance and
 * fail the reader. This script renders the diagrams the way a published page
 * does (strict mode, base theme, natural width) on a 390px screen and reports
 * what the reader would see.
 *
 * Setup, once per working directory:
 *   npm install --no-save mermaid@11 playwright@1
 *   npx playwright install chromium
 *   (Or point CHROMIUM_PATH at an installed Chrome or Chromium binary.)
 *
 * Usage:
 *   node scripts/check_mermaid.cjs page.html [--width 390] [--min-font 12] [--max-label 25]
 *   node scripts/check_mermaid.cjs notes.md        (reads ```mermaid and ~~~mermaid fences)
 *   node scripts/check_mermaid.cjs --self-test     (checks the checker itself)
 *
 * Input: an HTML file with diagrams in <pre class="mermaid"> blocks (also
 * accepts <div class="mermaid"> and <code class="language-mermaid">), or a
 * Markdown file with mermaid fences.
 * Output: one FAIL line per problem, then "diagrams checked: N, problems: M".
 * Exit codes: 0 when every diagram passes, 1 when any problem is found,
 * 2 when the script cannot run (bad arguments, missing file or packages).
 */
'use strict';

const fs = require('fs');
const os = require('os');
const path = require('path');
const { pathToFileURL } = require('url');
const { createRequire } = require('module');

// Resolve mermaid and playwright from the working directory first, so the
// one-line npm install above is enough, then from this script's own folder.
function requireFrom(name, resolveOnly) {
  const roots = [process.cwd(), __dirname];
  for (const root of roots) {
    try {
      const req = createRequire(path.join(root, 'package.json'));
      return resolveOnly ? req.resolve(name) : req(name);
    } catch (e) { /* try the next root */ }
  }
  console.error(`Cannot find "${name}". Run: npm install --no-save mermaid@11 playwright@1`);
  process.exit(2);
}

// --- Arguments ------------------------------------------------------------------

function parseArgs(argv) {
  const opts = { width: 390, minFont: 12, maxLabel: 25, selfTest: false, input: null };
  const numeric = { '--width': 'width', '--min-font': 'minFont', '--max-label': 'maxLabel' };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--self-test') { opts.selfTest = true; continue; }
    if (a in numeric) {
      const v = Number(argv[++i]);
      if (!Number.isFinite(v)) { console.error(`${a} needs a number`); process.exit(2); }
      opts[numeric[a]] = v;
      continue;
    }
    if (a.startsWith('--')) { console.error(`Unknown option ${a}`); process.exit(2); }
    opts.input = a;
  }
  return opts;
}

const OPTS = parseArgs(process.argv.slice(2));
if (!OPTS.selfTest && !OPTS.input) {
  console.error('Usage: node check_mermaid.cjs <page.html | notes.md> [--width 390] [--min-font 12] [--max-label 25] | --self-test');
  process.exit(2);
}

// --- Input handling -------------------------------------------------------------

// Markdown: lift every mermaid fence into a plain page, so the same checks run.
// A fence opens with three or more backticks or tildes and closes with the same
// character, at least as many times. A mermaid fence inside another fence (a
// documentation block) is part of that fence, not a diagram.
function mermaidBlocksFromMarkdown(md) {
  const blocks = [];
  let fence = null; // { ch, len, mermaid, lines }
  for (const raw of md.split('\n')) {
    const open = raw.match(/^\s*(`{3,}|~{3,})\s*([\w-]*)/);
    if (fence) {
      const close = raw.match(/^\s*(`{3,}|~{3,})\s*$/);
      if (close && close[1][0] === fence.ch && close[1].length >= fence.len) {
        if (fence.mermaid) blocks.push(fence.lines.join('\n'));
        fence = null;
      } else if (fence.mermaid) {
        fence.lines.push(raw);
      }
      continue;
    }
    if (open) fence = { ch: open[1][0], len: open[1].length, mermaid: open[2].toLowerCase() === 'mermaid', lines: [] };
  }
  return blocks;
}

function wrapPage(sources) {
  const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
  const pres = sources.map(s => `<pre class="mermaid">${esc(s)}</pre>`).join('\n');
  return `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">` +
    `<style>body{font-family:system-ui,sans-serif;margin:16px}</style></head><body>${pres}</body></html>`;
}

// The self-test: one diagram that fits a phone, one that breaks the rules the
// way a real page breaks them, with a literal <br/> tag and an unquoted long label.
const SELF_TEST_GOOD = 'flowchart TD\n  A["Cache"] --> B["Deploy"]\n  B --> C["Produção"]';
const SELF_TEST_BAD_HTML = '<pre class="mermaid">flowchart LR\n  A[Cache antes do deploy, sempre] --> B["Deploy<br/>em produção"]\n  B --> C["Resultado final medido por todos"]</pre>';

function prepareFile(opts) {
  const tmp = path.join(os.tmpdir(), `check_mermaid_${process.pid}.html`);
  if (opts.selfTest) {
    const page = wrapPage([SELF_TEST_GOOD]).replace('</body>', SELF_TEST_BAD_HTML + '</body>');
    fs.writeFileSync(tmp, page);
    return { file: tmp, cleanup: () => { try { fs.unlinkSync(tmp); } catch (e) { /* already gone */ } } };
  }
  const file = path.resolve(opts.input);
  if (!fs.existsSync(file)) { console.error(`No such file: ${file}`); process.exit(2); }
  if (/\.(md|markdown|mdx)$/i.test(file)) {
    fs.writeFileSync(tmp, wrapPage(mermaidBlocksFromMarkdown(fs.readFileSync(file, 'utf8'))));
    return { file: tmp, cleanup: () => { try { fs.unlinkSync(tmp); } catch (e) { /* already gone */ } } };
  }
  return { file, cleanup: () => {} };
}

// --- Browser --------------------------------------------------------------------

function findChromium() {
  if (process.env.CHROMIUM_PATH && fs.existsSync(process.env.CHROMIUM_PATH)) return process.env.CHROMIUM_PATH;
  const root = process.env.PLAYWRIGHT_BROWSERS_PATH;
  if (!root || !fs.existsSync(root)) return undefined; // let Playwright use its own default
  for (const d of fs.readdirSync(root).filter(d => /^chromium-\d+$/.test(d)).sort().reverse()) {
    for (const rel of ['chrome-linux/chrome', 'chrome-linux64/chrome', 'chrome-mac/Chromium.app/Contents/MacOS/Chromium', 'chrome-win/chrome.exe']) {
      const p = path.join(root, d, rel);
      if (fs.existsSync(p)) return p;
    }
  }
  return undefined;
}

// The three selectors a page may use for a diagram source.
const SOURCE_SELECTOR = 'pre.mermaid, div.mermaid, code.language-mermaid';

async function run(opts) {
  const { chromium } = requireFrom('playwright');
  const mermaidPath = requireFrom('mermaid/dist/mermaid.min.js', true);
  const { file, cleanup } = prepareFile(opts);
  let browser;
  try {
    browser = await chromium.launch({ executablePath: findChromium() });
    const page = await browser.newPage({ viewport: { width: opts.width, height: 844 }, colorScheme: 'dark' });
    await page.goto(pathToFileURL(file).href);

    // Read each source the way Mermaid's own run() does: innerHTML with entities
    // decoded. A literal <br/> in the page survives as a tag string here, while
    // textContent would already have lost it. Then the static checks.
    const problems = await page.evaluate(({ selector, maxLabel }) => {
      const out = [];
      const decode = html => { const t = document.createElement('textarea'); t.innerHTML = html; return t.value; };
      const sources = [];
      document.querySelectorAll(selector).forEach((el, i) => {
        const src = decode(el.innerHTML);
        sources.push(src);
        if (/<br\s*\/?>/i.test(src)) out.push(`diagram ${i}: "<br/>" inside a label (strict mode drops it and glues the words together)`);
        // Node labels, quoted or not: A["text"], A[text], A(text), A{text}, A>text], A([text]), A[[text]], A{{text}}.
        const labelRe = /[\[\(\{>]{1,2}\s*"?([^"\[\]\(\)\{\}<>|]+?)"?\s*[\]\)\}]{1,2}/g;
        src.split('\n').forEach(line => {
          if (/^\s*(?:%%|flowchart|graph|sequenceDiagram|classDiagram|stateDiagram|erDiagram|subgraph|end\b|style\b|classDef\b|click\b|linkStyle\b)/.test(line)) return;
          let m;
          while ((m = labelRe.exec(line))) {
            const t = m[1].trim();
            if (t && t.length > maxLabel) out.push(`diagram ${i}: label longer than ${maxLabel} characters: "${t}"`);
          }
        });
      });
      window.__sources = sources;
      return out;
    }, { selector: SOURCE_SELECTOR, maxLabel: opts.maxLabel });

    // Render like a published page: strict, base theme, natural width, body font.
    await page.addScriptTag({ path: mermaidPath });
    await page.evaluate(async (selector) => {
      const font = getComputedStyle(document.body).fontFamily || 'sans-serif';
      const nat = { useMaxWidth: false };
      mermaid.initialize({ startOnLoad: false, securityLevel: 'strict', theme: 'base', flowchart: nat,
        sequence: nat, state: nat, class: nat, er: nat, themeVariables: { fontSize: '16px', fontFamily: font } });
      const els = [...document.querySelectorAll(selector)];
      for (let i = 0; i < els.length; i++) {
        const el = els[i];
        let svg;
        try { ({ svg } = await mermaid.render('chk' + i, window.__sources[i])); }
        catch (e) { svg = `<svg data-error="${String(e && e.message || e).replace(/"/g, "'")}"></svg>`; }
        const mount = document.createElement('div'); mount.className = 'mermaid-diagram'; mount.innerHTML = svg;
        el.parentNode.insertBefore(mount, el); el.style.display = 'none';
      }
    }, SOURCE_SELECTOR);
    await page.addStyleTag({ content: '.mermaid-diagram svg{display:block;margin:0 auto;max-width:100%;height:auto}' +
      '.mermaid-diagram foreignObject *{white-space:nowrap!important}' });
    await page.waitForTimeout(1500);

    const rendered = await page.evaluate((minFont) => {
      const out = [];
      document.querySelectorAll('.mermaid-diagram svg').forEach((svg, i) => {
        const err = svg.getAttribute('data-error');
        if (err) { out.push(`diagram ${i}: does not render: ${err}`); return; }
        const vb = svg.viewBox.baseVal; const w = svg.getBoundingClientRect().width;
        const scale = vb && vb.width ? w / vb.width : 1;
        const label = svg.querySelector('.nodeLabel');
        const fs = label ? parseFloat(getComputedStyle(label).fontSize) : 16;
        if (fs * scale < minFont) out.push(`diagram ${i}: labels shrink to ${(fs * scale).toFixed(1)}px on a phone (minimum ${minFont}px). Make it narrower (at most 2 nodes side by side, prefer TD) or let it scroll: .mermaid-diagram{overflow-x:auto} .mermaid-diagram svg{max-width:none!important}`);
        svg.querySelectorAll('foreignObject').forEach(fo => {
          const d = fo.firstElementChild; const t = fo.textContent.trim(); if (!d || !t) return;
          if (d.scrollWidth > fo.width.baseVal.value + 1) out.push(`diagram ${i}: label cut off on a phone: "${t}"`);
        });
      });
      const doc = document.documentElement;
      if (doc.scrollWidth > innerWidth + 1) out.push(`the page scrolls sideways (${doc.scrollWidth}px on a ${innerWidth}px screen)`);
      return { out, count: document.querySelectorAll('.mermaid-diagram svg').length };
    }, opts.minFont);

    return { problems: problems.concat(rendered.out), count: rendered.count };
  } finally {
    if (browser) await browser.close();
    cleanup();
  }
}

run(OPTS).then(({ problems, count }) => {
  if (OPTS.selfTest) {
    // Diagram 0 must pass. Diagram 1 must fail on the literal <br/>, on the unquoted
    // long label, and on the rendered cut, because that is what a real page does.
    const bad = problems.filter(p => p.startsWith('diagram 1:'));
    const good = problems.filter(p => p.startsWith('diagram 0:'));
    const ok = count === 2 && good.length === 0 &&
      bad.some(p => p.includes('<br/>')) &&
      bad.some(p => p.includes('Cache antes do deploy, sempre') && p.includes(`longer than ${OPTS.maxLabel}`)) &&
      bad.some(p => p.includes('cut off'));
    console.log(`self-test: ${ok ? 'PASS' : 'FAIL'} (diagrams: ${count}, diagram 0 problems: ${good.length}, diagram 1 problems: ${bad.length})`);
    problems.forEach(p => console.log('  ' + p));
    process.exit(ok ? 0 : 1);
  }
  console.log(`diagrams checked: ${count}, problems: ${problems.length}`);
  problems.forEach(p => console.log('  FAIL ' + p));
  process.exit(problems.length ? 1 : 0);
}).catch(err => { console.error(err && err.stack || err); process.exit(2); });
