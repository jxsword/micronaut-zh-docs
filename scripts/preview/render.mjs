#!/usr/bin/env node
// zh/ 全量 .adoc → 官方式单页静态站 + 多模块聚合（DR-005 + DR-006 M4）。
//
// 与官方站（docs.micronaut.io/5.2.x/<site>/，单页）同构：
//   官方由构建插件按 toc.yml 顺序把片段拼接为单页并插入页标题（片段文件本身无页标题）：
//     h1 = 章、h2 = 片段页（toc 树完整路径编号）、片段内容整体降一级（== → h3）。
//   本脚本复刻该算法：逐片段 convert（standalone:false）+ HTML 拼接——
//   片段间属性隔离，内部 <<锚>>/[[锚]] 引用拼接后天然成为页内跳转。
//   页锚 [[<site>-<basename>]] 与官方各模块页锚互通（core = core- 前缀）。
//
// M4 聚合（DR-006 §5）：读 config/modules.json（官方 /5.2.x/ 导航，2026-11-23 实抓）
//   - core → index.html（内容/锚与 DR-005 版零变化，仅新增顶部模块切换条）
//   - 模块（zh/modules/<site>/guide/toc.yml 存在即渲染）→ <site>.html
//     （idprefix <site>-、imagesdir modules/<site>/img/）
//   - landing.html：官方分组导航复刻（组 → 模块链接；外链模块指向官方站）
//   - 各单页顶部模块切换条（聚合导航 + 已上线模块页互链）
//
// 产物：build/site/{index.html, <site>.html × N, landing.html} + resources/。
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
const MODULES_JSON = path.resolve(argOf('--modules') ||
  path.join(REPO, 'config', 'modules.json'));

const OFFICIAL_BASE = 'https://docs.micronaut.io/5.2.x/';

// —— 片段级适配层（沿用多页版口径；site='core' 保持既有输出逐字节不变）——
function preprocessFragment(text, basename, site, modTitle) {
  const anchorPfx = `${site}-`;
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
      if (site === 'core') {
        const url = `${OFFICIAL_BASE}core/#core-${base || basename}`;
        out.push('.翻译溯源');
        out.push('[quote, micronaut-zh-docs, 非官方译文]');
        out.push(`本文翻译自 Micronaut Core v5.2.25 官方文档 ${url}[官方站对应章节]，翻译基线锁定于 2026-11-19；非官方译文，以英文原文为准。`);
      } else {
        // 模块基线为分支 HEAD（DR-006 §6）：从 zh 引用块提取分支/锁定日
        const bm = /（(\S+) 分支基线，(\d{4}-\d{2}-\d{2}) 锁定）/.exec(line);
        const branch = bm ? bm[1] : '5.2.x';
        const locked = bm ? bm[2] : '';
        const url = `${OFFICIAL_BASE}${site}/#${anchorPfx}${base || basename}`;
        out.push('.翻译溯源');
        out.push('[quote, micronaut-zh-docs, 非官方译文]');
        out.push(`本文翻译自 Micronaut ${modTitle} 官方文档（${branch} 分支基线${locked ? `，${locked} 锁定` : ''}） ${url}[官方站对应章节]；非官方译文，以英文原文为准。`);
      }
      i += next - 1;
      provenanceDone = true;
      continue;
    }
    if (/^(snippet::|source::|source\[\]|include::)/.test(line)) {
      if (!tipDone) {
        // core TIP 文案逐字节不变（DR-005 版）；模块用泛化措辞（上游仓各异）
        const tipText = site === 'core'
          ? '本段代码示例与配置属性表由上游构建期从 micronaut-core 模块源码注入，纯快照无法单独重建；请对照官方站对应章节阅读。'
          : '本段代码示例与配置属性表由上游构建期从模块源码注入，纯快照无法单独重建；请对照官方站对应章节阅读。';
        out.push('[TIP]');
        out.push('====');
        out.push(tipText);
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
      return `xref:#${anchorPfx}${rest.replace(/\.adoc$/, '')}`;
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
  if (!fs.existsSync(dir)) return res;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    const rel = base ? `${base}/${e.name}` : e.name;
    if (e.isDirectory()) res.push(...walk(p, rel));
    else if (e.name.endsWith('.adoc')) res.push(rel);
  }
  return res;
}

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

// 标题全局升位（章 == →h1、页 === →h2、内容 +1 偏移回正）：与官方 h1=章/h2=页/h3=内部对齐
function promote(html) {
  return html
    .replace(/<h([2-6])((?:\s[^>]*)?)>/g, (m, n, attrs) => `<h${+n - 1}${attrs}>`)
    .replace(/<\/h([2-6])>/g, (m, n) => `</h${+n - 1}>`)
    .replace(/class="sect([1-5])"/g, (m, n) => `class="sect${+n - 1}"`);
}

// —— 单模块单页渲染（DR-005 算法参数化；site='core' 输出与既有 index.html 对齐）——
async function renderModule(site, mod, cfg, links) {
  const prefix = site === 'core' ? '' : `modules/${site}`;
  const zhGuide = path.join(REPO, 'zh', prefix, 'guide');
  const tocPath = path.join(zhGuide, 'toc.yml');
  if (!fs.existsSync(tocPath)) {
    return null; // 模块未快照/未开译 → 不产页
  }
  const toc = yaml.load(fs.readFileSync(tocPath, 'utf-8'));
  const FRAGMENTS = [];
  function walkToc(node, prefixKeys, nums, depth) {
    let idx = 0;
    for (const [k, v] of Object.entries(node)) {
      if (k === 'title' && typeof v !== 'object') continue;
      idx += 1;
      const num = [...nums, idx].join('.');
      const p = prefixKeys ? `${prefixKeys}.${k}` : k;
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

  const available = new Set(walk(zhGuide));
  const anchorPfx = `${site}-`;
  const imagesdir = site === 'core' ? 'resources/img/' : `modules/${site}/img/`;
  const CONVERT_ATTRS = {
    'idprefix': anchorPfx, 'idseparator': '-', 'imagesdir': imagesdir,
    'lang': 'zh-CN',
  };

  const modTitle = (mod && mod.title) || site;
  const t0 = Date.now();
  let ok = 0;
  const failures = [];
  let missingChapter = 0;
  const parts = [];
  for (const f of FRAGMENTS) {
    let src;
    if (!available.has(f.rel)) {
      // skipped 壳（0 字节/纯 include）：章页仅输出标题；非章缺失报错
      if (!f.chapter) { failures.push(`${f.rel}: zh 镜像缺失`); continue; }
      src = '';
      missingChapter += 1;
    } else {
      src = fs.readFileSync(path.join(zhGuide, f.rel), 'utf-8');
      src = preprocessFragment(src, f.basename, site, modTitle);
    }
    // 章内容同样 +1 偏移：章页内小节标题提升后为页级 h2
    const page = f.chapter
      ? `[[${anchorPfx}${f.basename}]]\n== ${f.num} ${f.title}\n\n:leveloffset: +1\n\n${src.replace(/^\s+|\s+$/g, '')}\n`
      : `[[${anchorPfx}${f.basename}]]\n=== ${f.num} ${f.title}\n\n:leveloffset: +1\n\n${src.replace(/^\s+|\s+$/g, '')}\n`;
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

  // —— 组装单页（asciidoctor.css 内联 + 侧栏 + scrollspy + 模块切换条）——
  const baseCss = fs.readFileSync(
    path.join(path.dirname(fileURLToPath(import.meta.url)),
      'node_modules/@asciidoctor/core/data/asciidoctor-default.css'), 'utf-8');

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
      items += `<li data-depth="${depth}"><a href="#${anchorPfx}${k}">${label}</a>${child}</li>\n`;
    }
    return `<ul>${items}</ul>`;
  }

  const navTitle = site === 'core'
    ? 'Micronaut 中文文档'
    : `Micronaut ${esc(modTitle)} 中文文档`;
  const pageTitle = site === 'core'
    ? 'Micronaut Framework 中文文档（v5.2.25 基线，非官方译文）'
    : `Micronaut ${esc(modTitle)} 中文文档（${(mod && mod.branch) || '5.2.x'} 基线，非官方译文）`;
  const topNote = site === 'core'
    ? 'Micronaut Framework 官方文档社区非官方中文翻译（基线 v5.2.25，2026-11-19 锁定）；以英文原文为准。构建期注入的代码示例与配置属性表见各页「官方站对应章节」提示。本页为单页合集，左侧导航可在章节间直接跳转。'
    : `Micronaut ${esc(modTitle)} 官方文档社区非官方中文翻译（${(mod && mod.branch) || '5.2.x'} 分支基线${(mod && mod.locked_at) ? `，${mod.locked_at} 锁定` : ''}）；以英文原文为准。构建期注入的代码示例与配置属性表见各页「官方站对应章节」提示。本页为单页合集，左侧导航可在章节间直接跳转。`;

  const page = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${pageTitle}</title>
<style>${baseCss}</style>
<style>${navCss}</style>
</head>
<body id="top-anchor" class="article">
<nav id="doc-nav" aria-label="文档导航">
<div class="nav-title"><a href="#top-anchor">${navTitle}</a></div>
${navHtml(toc, [], 0)}
</nav>
<div id="doc-main">
${moduleBar(site, links)}
<div id="top-note">${topNote}</div>
${parts.join('\n')}
</div>
<div id="back-top"><a href="#top-anchor">顶部</a></div>
<script>${scrollJs(anchorPfx)}</script>
</body>
</html>`;
  const outFile = path.join(SITE, site === 'core' ? 'index.html' : `${site}.html`);
  fs.writeFileSync(outFile, page, 'utf-8');
  return {
    site, fragments: FRAGMENTS.length, rendered: ok, missingChapter,
    failures: failures.slice(0, 8), failureCount: failures.length,
    out: outFile, seconds: +((Date.now() - t0) / 1000).toFixed(1),
  };
}

// —— 模块切换条（DR-006 §5：各单页顶部；landing=聚合导航入口）——
function moduleBar(currentSite, links) {
  const items = links.map(l =>
    `<a href="${l.href}"${l.site === currentSite ? ' class="current"' : ''}>${esc(l.label)}</a>`)
    .join('');
  return `<nav id="module-bar" aria-label="模块切换">` +
    `<span class="mb-title">聚合站：</span>` +
    `<a href="landing.html">全部模块</a>${items}</nav>`;
}

// —— landing.html：官方 /5.2.x/ 分组导航复刻 ——
function renderLanding(cfg, linksBySite) {
  const baseCss = fs.readFileSync(
    path.join(path.dirname(fileURLToPath(import.meta.url)),
      'node_modules/@asciidoctor/core/data/asciidoctor-default.css'), 'utf-8');
  const groups = (cfg.groups || []).map(g => {
    const items = (g.modules || []).map(m => {
      const link = linksBySite[m];
      const mod = (cfg.modules || {})[m] || {};
      if (link) {
        return `<li><a href="${link.href}">${esc(mod.title || m)}</a></li>`;
      }
      if (mod.external && mod.url) {
        return `<li><a href="${mod.url}" rel="noopener">↗ ${esc(mod.title || m)}</a></li>`;
      }
      // 已注册未上线模块：灰态占位（无链接）
      return `<li class="todo">${esc(mod.title || m)}</li>`;
    }).join('\n');
    return `<section class="lg"><h2>${esc(g.title)}</h2><ul>${items}</ul></section>`;
  }).join('\n');
  const unplanned = (cfg.unplanned || []).map(u =>
    `<li>${esc(u.site)}（${esc(u.note || '未列入计划')}）</li>`).join('');
  const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Micronaut 中文文档 · 聚合导航（非官方译文）</title>
<style>${baseCss}</style>
<style>
body { max-width: 62em; margin: 0 auto; padding: 1em 1.2em 3em; }
h1 { border-bottom: 2px solid #e4e7f0; padding-bottom: .4em; }
.lg { display: inline-block; vertical-align: top; width: 19em; margin: 0 1em 1.2em 0; }
.lg h2 { font-size: 1.05em; border-bottom: 1px solid #e4e7f0; padding-bottom: .2em; }
.lg ul { list-style: none; padding-left: .2em; }
.lg li { margin: 2px 0; }
.lg a { color: #24325f; text-decoration: none; }
.lg a:hover { text-decoration: underline; }
.lg .todo { color: #999; }
#landing-note { color: #555; font-size: .92em; max-width: 62em; }
</style>
</head>
<body class="article">
<h1>Micronaut 中文文档 · 聚合导航</h1>
<div id="landing-note">Micronaut 官方文档（docs.micronaut.io /5.2.x/）社区非官方中文翻译。分组与官方导航一致（${esc(cfg.official_nav_captured || '')} 实抓）；灰色为未上线模块，↗ 为官方外链（不在翻译范围）。以英文原文为准。</div>
${groups}
<h2>说明</h2>
<ul>
<li>core 主指南：<a href="index.html">index.html</a></li>
${unplanned ? `<li>计划外条目：${unplanned}</li>` : ''}
</ul>
</body>
</html>`;
  fs.writeFileSync(path.join(SITE, 'landing.html'), html, 'utf-8');
}

// —— 样式与脚本（模块参数化；core 输出与 DR-005 版一致）——
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
#module-bar { max-width: 62em; margin: 0 auto 12px; padding: 7px 10px;
  background: #f7f8fa; border: 1px solid #e2e5ef; border-radius: 6px;
  font-size: 13px; display: flex; flex-wrap: wrap; gap: 4px 6px; align-items: center; }
#module-bar a { color: #24325f; text-decoration: none; padding: 2px 9px;
  border-radius: 4px; }
#module-bar a:hover { background: #e3e7f2; }
#module-bar a.current { background: #2a3f8f; color: #fff; }
#module-bar .mb-title { color: #666; font-weight: 600; }
.sect0 { margin-top: 2.8em; padding-top: 0.8em; border-top: 2px solid #e4e7f0; }
.sect0:first-of-type { border-top: none; }
`;
function scrollJs(anchorPfx) {
  return `
(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('#doc-nav a'));
  var byId = {};
  links.forEach(function (a) { var id = (a.getAttribute('href') || '').slice(1); if (id) byId[id] = a; });
  var targets = Array.prototype.slice.call(document.querySelectorAll('[id^="${anchorPfx}"]'));
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
}

// —— 图片镜像：core 沿用 resources/；模块 → modules/<site>/img/（DR-006 §5）——
function walkAll(dir, base = '') {
  const res = [];
  if (!fs.existsSync(dir)) return res;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    const rel = base ? `${base}/${e.name}` : e.name;
    if (e.isDirectory()) res.push(...walkAll(p, rel));
    else res.push(rel);
  }
  return res;
}

function copyImages(site) {
  const prefix = site === 'core' ? '' : `modules/${site}`;
  const srcRoot = path.join(REPO, 'source', prefix, 'resources');
  if (!fs.existsSync(srcRoot)) return 0;
  if (site === 'core') {
    const dest = path.join(SITE, 'resources');
    fs.cpSync(srcRoot, dest, { recursive: true });
    return walkAll(dest).length;
  }
  // 模块：resources/** 摊平进 img/（resources/img/x.png → img/x.png，
  // resources/foo.png → img/foo.png），imagesdir=modules/<site>/img/
  const dest = path.join(SITE, 'modules', site, 'img');
  let n = 0;
  for (const rel of walkAll(srcRoot)) {
    const under = rel.startsWith('img/') ? rel.slice(4) : rel;
    const target = path.join(dest, under);
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.copyFileSync(path.join(srcRoot, rel), target);
    n += 1;
  }
  return n;
}

// —— 主流程：core + 已快照模块逐个渲染 + landing ——
const cfg = JSON.parse(fs.readFileSync(MODULES_JSON, 'utf-8'));
fs.mkdirSync(SITE, { recursive: true });

const t0 = Date.now();
const results = [];

// 切换条/落地页链接集合：core + 已快照模块（按 modules.json 组序）
function siteAvailable(site) {
  const prefix = site === 'core' ? '' : `modules/${site}`;
  return fs.existsSync(path.join(REPO, 'zh', prefix, 'guide', 'toc.yml'));
}
const availSites = ['core'];
for (const g of cfg.groups || []) {
  for (const m of g.modules || []) {
    const mod = (cfg.modules || {})[m] || {};
    if (mod.external || m === 'core' || availSites.includes(m)) continue;
    if (siteAvailable(m)) availSites.push(m);
  }
}
const links = availSites.map(s => ({
  site: s,
  label: s === 'core' ? 'Core' : ((cfg.modules[s] || {}).title || s),
  href: s === 'core' ? 'index.html' : `${s}.html`,
}));

for (const site of availSites) {
  const r = await renderModule(site, cfg.modules[site], cfg, links);
  if (r) {
    r.images = copyImages(site);
    results.push(r);
  }
}
renderLanding(cfg, Object.fromEntries(links.map(l => [l.site, l])));

const dt = ((Date.now() - t0) / 1000).toFixed(1);
const failures = results.flatMap(r => r.failures);
console.log(JSON.stringify({
  mode: 'aggregate-multi-module',
  pages: results.map(r => ({
    site: r.site, fragments: r.fragments, rendered: r.rendered,
    missingChapter: r.missingChapter, failureCount: r.failureCount,
    images: r.images, seconds: r.seconds,
    sizeMB: +(fs.statSync(r.out).size / 1048576).toFixed(1),
  })),
  landing: path.join(SITE, 'landing.html'),
  failureCount: failures.length,
  failures: failures.slice(0, 8),
  seconds: +dt,
}, null, 1));
process.exit(failures.length ? 1 : 0);
