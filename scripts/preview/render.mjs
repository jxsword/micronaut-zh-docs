#!/usr/bin/env node
// zh/ .adoc 全量渲染为多页静态站（本地预览与 GitHub Pages 共用同一脚本）。
//
// 数据流：zh/guide/**.adoc → 适配层预处理 → build/zh/**.adoc
//        → asciidoctor(safe=unsafe) → build/site/guide/**.html + index.html + resources/
//
// 适配层（预览级忠实度，见 reports/m3-final.md 与 README「在线对照结构」）：
//   1. 页头溯源块正规化为 quote 块 + 官方站链接（机读注释行剔除）；
//   2. Micronaut javadoc 宏族（api:/ann:/rs:/reactor:/rx:/sql:）去宏化为类简名；
//   3. dependency:: 宏坐标化为行内码；
//   4. snippet::/source::/include::（构建期代码与属性表注入）替换为官方站 TIP 提示
//      ——zh 语料实测所有 include:: 目标均为上游模块源码（无 .adoc 片段 include）；
//   5. 裸锚 <<id,label>> 经 config/anchor-registry.yml 改写为跨页链接
//      （上游按官方站单页口径书写，多页站需显式跨页）；
//   6. xref:guide/<rest> 按当前页深度改写为相对路径（同 5 的多页口径）；
//   7. :imagesdir: 按目录深度注入（site/resources/img/ 镜像）。
//
// 已知局限：registry 未登记的裸锚退化为页内 #id 跳转（当前 registry 123 条全登记）。
//
// 用法：node render.mjs [--repo <仓库根>] [--out <输出目录>]（默认 <repo>/build/site）
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
const BUILD_ZH = path.join(SITE, '..', 'zh-adoc-build');

const REGISTRY = yaml.load(
  fs.readFileSync(path.join(REPO, 'config/anchor-registry.yml'), 'utf-8'));
const ANCHOR_FILE = new Map();
for (const a of REGISTRY.anchors || []) {
  if (!ANCHOR_FILE.has(a.id)) ANCHOR_FILE.set(a.id, a.file);
}

// —— 相对路径工具：页面均位于 site/guide/<rel>.html ——
function relToGuideRoot(rel) {
  const depth = rel.split('/').length - 1; // 当前页相对 site/guide/ 的层级
  return '../'.repeat(depth);
}

function preprocess(text, rel) {
  const lines = text.split('\n');
  const out = [];
  let provenanceDone = false;
  let tipDone = false;
  const depth = rel.split('/').length - 1;
  const up = relToGuideRoot(rel);
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    // 1) 溯源块正规化
    if (!provenanceDone && line.startsWith('> 本文翻译自')) {
      const m = /upstream_file: (\S+)/.exec(lines[i + 1] || '');
      const base = m ? m[1].split('/').pop().replace(/\.adoc$/, '') : '';
      const next = lines[i + 2] === '' ? 3 : 2;
      const url = `https://docs.micronaut.io/5.2.x/core/#core-${base}`;
      out.push(`:imagesdir: ${up}../../resources/img/`);
      out.push('.翻译溯源');
      out.push('[quote, micronaut-zh-docs, 非官方译文]');
      out.push(`本文翻译自 Micronaut Core v5.2.25 官方文档 ${url}[官方站对应章节]，翻译基线锁定于 2026-11-19；非官方译文，以英文原文为准。`);
      i += next - 1;
      provenanceDone = true;
      continue;
    }
    // 4) 构建期注入类宏/指令 → 官方站 TIP（首个）
    if (/^snippet::/.test(line) || /^source::/.test(line) ||
        /^source\[\]/.test(line) || /^include::/.test(line)) {
      if (!tipDone) {
        out.push('[TIP]');
        out.push('====');
        const base = rel.split('/').pop().replace(/\.adoc$/, '');
        out.push(`本节代码示例与配置属性表由上游构建期从 micronaut-core 模块源码注入，纯快照无法单独重建；请对照 https://docs.micronaut.io/5.2.x/core/#core-${base}[官方站对应章节] 阅读。`);
        out.push('====');
        tipDone = true;
      }
      continue;
    }
    let l = line;
    // 5) 裸锚 <<id[,label]>> / <<file#anchor[,label]>> → registry 跨页链接
    l = l.replace(/<<([^>,\s]+)\s*(?:,\s*([^>]*))?>>/g, (m0, target, label) => {
      const [fp, an] = target.split('#');
      let file = null, anchor = an || null;
      if (fp && an !== undefined) {
        // <<file#anchor>>：file 形如 guide/xxx.adoc 或裸文件名
        file = fp.includes('/') ? fp : (ANCHOR_FILE.get(fp) ? null : null);
        if (!fp.includes('/')) { anchor = target; file = null; }
      } else {
        // 纯裸锚
        file = ANCHOR_FILE.get(fp) || null;
        anchor = fp;
      }
      if (file && file.startsWith('guide/')) {
        const t = `${up}${file.replace(/^guide\//, '').replace(/\.adoc$/, '')}.html`;
        return `xref:${t}${anchor ? '#' + anchor : ''}[${label || ''}]`;
      }
      return m0; // 未登记 → 保持原样（页内锚退化）
    });
    // 6) xref:guide/<rest> 多页相对化
    l = l.replace(/xref:guide\/([^\[\s\]]+)/g, (m0, rest) => {
      if (rest.startsWith('http')) return m0;
      return `xref:${up}${rest.replace(/\.adoc$/, '')}.html`;
    });
    // 2) javadoc 宏族去宏化（含 ok(T) 等带参形态）
    l = l.replace(/(?:api|ann|rs|reactor|rx|sql):([^[\]]+)\[\]/g,
      (_, p) => p.split('.').pop());
    l = l.replace(/(?:api|ann|rs|reactor|rx|sql):[^[\]]+\[([^\]]+)\]/g, '$1');
    // 3) dependency 宏 → 坐标行内码
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

// 1. 预处理全库
fs.rmSync(BUILD_ZH, { recursive: true, force: true });
fs.mkdirSync(BUILD_ZH, { recursive: true });
fs.mkdirSync(path.join(SITE, 'guide'), { recursive: true });
const files = walk(path.join(REPO, 'zh/guide'));
for (const rel of files) {
  const src = fs.readFileSync(path.join(REPO, 'zh/guide', rel), 'utf-8');
  const dst = path.join(BUILD_ZH, rel);
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.writeFileSync(dst, preprocess(src, rel), 'utf-8');
}

// 2. toc.yml → index.adoc（复用 M3 已译导航标题）
const toc = yaml.load(fs.readFileSync(path.join(REPO, 'zh/guide/toc.yml'), 'utf-8'));
function tocAdoc(node, prefix, depth) {
  let s = '';
  for (const [k, v] of Object.entries(node)) {
    if (k === 'title' && typeof v !== 'object') continue;
    const p = prefix ? `${prefix}.${k}` : k;
    const href = `guide/${p.replace(/\./g, '/')}.html`;
    if (typeof v === 'string') {
      s += `${'*'.repeat(depth + 1)} link:${href}[${v}]\n`;
    } else {
      s += `${'*'.repeat(depth + 1)} link:${href}[${v.title || k}]\n`;
      s += tocAdoc(v, p, depth + 1);
    }
  }
  return s;
}
fs.writeFileSync(path.join(BUILD_ZH, 'index.adoc'),
  `= Micronaut 官方文档中文翻译（v5.2.25 基线）\n\n` +
  `非官方译文，以英文原文为准；代码示例请对照官方站。\n\n` +
  tocAdoc(toc, '', 0), 'utf-8');

// 3. 图片镜像（site/resources/img/）
fs.cpSync(path.join(REPO, 'source/resources'), path.join(SITE, 'resources'),
  { recursive: true });

// 4. 渲染
const opts = {
  safe: 'unsafe',
  attributes: { 'source-highlighter': 'highlight.js', 'lang': 'zh-CN' },
};
let ok = 0;
const failures = [];
for (const rel of [...files, 'index.adoc']) {
  try {
    // asciidoctor.js v4：convert 返回 Promise
    const html = await adoc.convert(
      fs.readFileSync(path.join(BUILD_ZH, rel), 'utf-8'),
      { ...opts, standalone: true });
    const outRel = rel === 'index.adoc' ? 'index.html'
      : path.join('guide', rel.replace(/\.adoc$/, '.html'));
    const dst = path.join(SITE, outRel);
    fs.mkdirSync(path.dirname(dst), { recursive: true });
    fs.writeFileSync(dst, html, 'utf-8');
    ok++;
  } catch (e) {
    failures.push(`${rel}: ${String(e.message).split('\n')[0]}`);
  }
}
console.log(JSON.stringify({ rendered: ok, failed: failures.length,
  out: SITE, failures: failures.slice(0, 8) }));
process.exit(failures.length ? 1 : 0);
