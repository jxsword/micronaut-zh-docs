#!/usr/bin/env node
// zh/ 全量 .adoc → 官方式单页静态站（DR-005，替代 DR-004 的多页形态）。
//
// 与官方站（docs.micronaut.io/5.2.x/core/，11.4MB 单页）同构：
//   官方由构建插件按 toc.yml 顺序把片段拼接为单页并插入页标题（片段文件本身无页标题）：
//     h1 = 章（"1 Introduction"）、h2 = 片段页（"14.2.3.6 Provided Indicators"，
//     全部为 toc 树完整路径编号）、片段内容整体降一级（== → h3，内部标题不编号）。
//   本脚本复刻该算法：逐片段 convert（standalone:false）+ HTML 拼接——
//   片段间属性隔离，内部 <<锚>>/[[锚]] 引用拼接后天然成为页内跳转。
//   页锚 [[core-<basename>]] 与官方页锚互通。
//
// 产物：build/site/index.html（自包含单页：内联 asciidoctor.css + 侧栏 + scrollspy）
//      + resources/。
// 已知边界：构建期注入的代码/属性表按官方站 TIP 提示（DR-003 口径）；不做代码高亮。
import { createRequire } from 'module';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const require = createRequire(import.meta.url);
const adoc = require('@asciidoctor/core');
const yaml = require('js-yaml');

const args = process.argv.slice(2);
function argOf(name) {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : null;
}
const REPO = path.resolve(argOf('--repo') ||
  path.join(path.dirname(fileURLToPath(import.meta.url)), '..', '..'));
const SITE = path.resolve(argOf('--out') || path.join(REPO, 'build', 'site'));

// —— 片段级适配层（沿用多页版口径）——
function preprocessFragment(text, basename) {
  const lines = text.split('\n');
  const out = [];
  let provenanceDone = false;
  let tipDone = false;
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (!provenanceDone && line.startsWith('> 本文翻译自')) {
      const m = /upstream_file: (\S+)/.exec(lines[i + 1] || '');
      const base = m ? m[1].split('/').pop().replace(/\.adoc$/, '') : '';
      const next = lines[i + 2] === '' ? 3 : 2;
      const url = `https://docs.micronaut.io/5.2.x/core/#core-${base || basename}`;
      out.push('.翻译溯源');
      out.push('[quote, micronaut-zh-docs, 非官方译文]');
      out.push(`本文翻译自 Micronaut Core v5.2.25 官方文档 ${url}[官方站对应章节]，翻译基线锁定于 2026-11-19；非官方译文，以英文原文为准。`);
      i += next - 1;
      provenanceDone = true;
      continue;
    }
    if (/^(snippet::|source::|source\[\]|include::)/.test(line)) {
      if (!tipDone) {
        out.push('[TIP]');
        out.push('====');
        out.push('本段代码示例与配置属性表由上游构建期从 micronaut-core 模块源码注入，纯快照无法单独重建；请对照官方站对应章节阅读。');
        out.push('====');
        tipDone = true;
      }
      continue;
    }
    let l = line;
    // xref:guide/<rest>[label] → 页内锚（页锚或页内显式锚；label 在匹配外原样保留）
    l = l.replace(/xref:guide\/([^\[\s\]#]+)(#([^\[\]]+))?/g, (m0, rest, _a, an) => {
      if (/^https?:/.test(rest)) return m0;
      if (an) return `xref:#${an}`;
      return `xref:#core-${rest.replace(/\.adoc$/, '')}`;
    });
    // javadoc 宏族去宏化（含 ok(T) 等带参形态）
    l = l.replace(/(?:api|ann|rs|reactor|rx|sql):([^[\]]+)\[\]/g,
      (_, p) => p.split('.').pop());
    l = l.replace(/(?:api|ann|rs|reactor|rx|sql):[^[\]]+\[([^\]]+)\]/g, '$1');
    // dependency 宏 → 坐标行内码
    l = l.replace(/dependency::?([A-Za-z0-9._-]+)(?:\[[^\]]*\])?/g, (m0, art) => {
      const g = /groupId="([^"]+)"/.exec(m0);
      return '`' + (g ? `${g[1]}:${art}` : art) + '`';
    });
    out.push(l);
  }
  return out.join('\n');
}

function walk(dir, base = '') {
  const res = [];
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    const rel = base ? `${base}/${e.name}` : e.name;
    if (e.isDirectory()) res.push(...walk(p, rel));
    else if (e.name.endsWith('.adoc')) res.push(rel);
  }
  return res;
}

// —— toc 树：顺序 + 编号 ——
const toc = yaml.load(fs.readFileSync(path.join(REPO, 'zh/guide/toc.yml'), 'utf-8'));
const FRAGMENTS = [];
function walkToc(node, prefix, nums, depth) {
  let idx = 0;
  for (const [k, v] of Object.entries(node)) {
    if (k === 'title' && typeof v !== 'object') continue;
    idx += 1;
    const num = [...nums, idx].join('.');
    const p = prefix ? `${prefix}.${k}` : k;
    const rel = p.replace(/\./g, '/') + '.adoc';
    if (typeof v === 'string') {
      FRAGMENTS.push({ basename: k, title: v, num, depth, chapter: depth === 0, rel });
    } else {
      FRAGMENTS.push({ basename: k, title: v.title || k, num, depth, chapter: depth === 0, rel });
      walkToc(v, p, [...nums, idx], depth + 1);
    }
  }
}
walkToc(toc, '', [], 0);

// —— 逐片段渲染 + 拼接 ——
fs.mkdirSync(SITE, { recursive: true });
fs.cpSync(path.join(REPO, 'source/resources'), path.join(SITE, 'resources'),
  { recursive: true });
const available = new Set(walk(path.join(REPO, 'zh/guide')));
const CONVERT_ATTRS = { 'idprefix': 'core-', 'idseparator': '-', 'imagesdir': 'resources/img/', 'lang': 'zh-CN' };

const t0 = Date.now();
let ok = 0;
const failures = [];
let missingChapter = 0;
const parts = [];
for (const f of FRAGMENTS) {
  let src;
  if (!available.has(f.rel)) {
    // skipped 壳（appendix.adoc 0 字节）：章页仅输出标题；非章缺失报错
    if (!f.chapter) { failures.push(`${f.rel}: zh 镜像缺失`); continue; }
    src = '';
    missingChapter += 1;
  } else {
    src = fs.readFileSync(path.join(REPO, 'zh/guide', f.rel), 'utf-8');
    src = preprocessFragment(src, f.basename);
  }
  // 章内容同样 +1 偏移：章页内小节标题（如 certificates/cli）提升后为页级 h2
  const page = f.chapter
    ? `[[core-${f.basename}]]\n== ${f.num} ${f.title}\n\n:leveloffset: +1\n\n${src.replace(/^\s+|\s+$/g, '')}\n`
    : `[[core-${f.basename}]]\n=== ${f.num} ${f.title}\n\n:leveloffset: +1\n\n${src.replace(/^\s+|\s+$/g, '')}\n`;
  try {
    const html = await adoc.convert(page, {
      standalone: false, safe: 'unsafe', attributes: { ...CONVERT_ATTRS },
    });
    parts.push(promote(html));
    ok += 1;
  } catch (e) {
    failures.push(`${f.rel}: ${String(e.message).split('\n')[0]}`);
  }
}

// 标题全局升位（章 == →h1、页 === →h2、内容 +1 偏移回正）：与官方 h1=章/h2=页/h3=内部对齐
function promote(html) {
  return html
    .replace(/<h([2-6])((?:\s[^>]*)?)>/g, (m, n, attrs) => `<h${+n - 1}${attrs}>`)
    .replace(/<\/h([2-6])>/g, (m, n) => `</h${+n - 1}>`)
    .replace(/class="sect([1-5])"/g, (m, n) => `class="sect${+n - 1}"`);
}

// —— 组装单页（asciidoctor.css 内联 + 侧栏 + scrollspy）——
const baseCss = fs.readFileSync(
  path.join(path.dirname(fileURLToPath(import.meta.url)),
    'node_modules/@asciidoctor/core/data/asciidoctor-default.css'), 'utf-8');

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}
function navHtml(node, nums, depth) {
  let idx = 0;
  let items = '';
  for (const [k, v] of Object.entries(node)) {
    if (k === 'title' && typeof v !== 'object') continue;
    idx += 1;
    const num = [...nums, idx].join('.');
    const title = typeof v === 'string' ? v : (v.title || k);
    const label = `${num} ${esc(title)}`;
    const child = typeof v === 'object' ? navHtml(v, [...nums, idx], depth + 1) : '';
    items += `<li data-depth="${depth}"><a href="#core-${k}">${label}</a>${child}</li>\n`;
  }
  return `<ul>${items}</ul>`;
}
const navCss = `
#doc-nav { position: fixed; top: 0; left: 0; bottom: 0; width: 300px; overflow-y: auto;
  box-sizing: border-box; padding: 14px 10px 40px; background: #f7f8fa;
  border-right: 1px solid #ddd; font-size: 12.5px; z-index: 10; }
#doc-nav ul { list-style: none; margin: 0; padding-left: 13px; }
#doc-nav li { margin: 1px 0; }
#doc-nav a { color: #24325f; text-decoration: none; display: block; padding: 2px 6px;
  border-radius: 3px; line-height: 1.35; }
#doc-nav a:hover { background: #e3e7f2; }
#doc-nav a.active { background: #2a3f8f; color: #fff; }
#doc-nav li[data-depth="0"] > a { font-weight: 600; margin-top: 4px; }
#doc-nav .nav-title { font-weight: 700; margin: 2px 6px 10px; font-size: 14px; }
#doc-nav .nav-title a { color: #1a2a55; }
@media (min-width: 1000px) {
  #doc-main { margin-left: 312px; }
}
@media (max-width: 999px) { #doc-nav { display: none; } #doc-main { margin: 0 12px; } }
#back-top { position: fixed; right: 18px; bottom: 18px; z-index: 20; }
#back-top a { display: inline-block; padding: 6px 10px; background: #2a3f8f; color: #fff;
  border-radius: 4px; text-decoration: none; font-size: 13px; }
#top-note { max-width: 62em; margin: 0 auto 18px; color: #555; font-size: 0.9em; }
.sect0 { margin-top: 2.8em; padding-top: 0.8em; border-top: 2px solid #e4e7f0; }
.sect0:first-of-type { border-top: none; }
`;
const scrollJs = `
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('#doc-nav a'));
  var byId = {};
  links.forEach(function (a) { var id = (a.getAttribute('href') || '').slice(1); if (id) byId[id] = a; });
  var targets = Array.prototype.slice.call(document.querySelectorAll('[id^="core-"]'));
  var last = null;
  function onScroll() {
    var cur = null;
    for (var i = 0; i < targets.length; i++) {
      if (targets[i].getBoundingClientRect().top <= 90) cur = targets[i];
      else break;
    }
    if (!cur || cur.id === last) return;
    last = cur.id;
    links.forEach(function (a) { a.classList.remove('active'); });
    var a = byId[cur.id];
    while (a) {
      a.classList.add('active');
      var li = a.closest('li');
      a = li && li.parentElement && li.parentElement.closest('li')
        ? li.parentElement.closest('li').querySelector(':scope > a') : null;
    }
    var act = document.querySelector('#doc-nav a.active');
    if (act) act.scrollIntoView({ block: 'nearest' });
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
`;
const page = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Micronaut Framework 中文文档（v5.2.25 基线，非官方译文）</title>
<style>${baseCss}</style>
<style>${navCss}</style>
</head>
<body id="top-anchor" class="article">
<nav id="doc-nav" aria-label="文档导航">
<div class="nav-title"><a href="#top-anchor">Micronaut 中文文档</a></div>
${navHtml(toc, [], 0)}
</nav>
<div id="doc-main">
<div id="top-note">Micronaut Framework 官方文档社区非官方中文翻译（基线 v5.2.25，2026-11-19 锁定）；以英文原文为准。构建期注入的代码示例与配置属性表见各页「官方站对应章节」提示。本页为单页合集，左侧导航可在章节间直接跳转。</div>
${parts.join('\n')}
</div>
<div id="back-top"><a href="#top-anchor">顶部</a></div>
<script>${scrollJs}</script>
</body>
</html>`;
fs.writeFileSync(path.join(SITE, 'index.html'), page, 'utf-8');

const dt = ((Date.now() - t0) / 1000).toFixed(1);
console.log(JSON.stringify({
  mode: 'single-page-merged', fragments: FRAGMENTS.length, rendered: ok,
  missingChapter, failures: failures.slice(0, 8), failureCount: failures.length,
  out: path.join(SITE, 'index.html'),
  sizeMB: +(fs.statSync(path.join(SITE, 'index.html')).size / 1048576).toFixed(1),
  seconds: +dt,
}));
process.exit(failures.length ? 1 : 0);
