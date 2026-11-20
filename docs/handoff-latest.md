# 交接文档（handoff-latest）

> 更新：2026-11-20 ｜ 会话：M2 分批翻译（B01 完成）｜ 下一会话任务：M2 继续分批翻译（B02 起）

## 已完成清单（全部已提交，main 分支）

| 工作单元 | 提交 | 说明 |
|---|---|---|
| M0 余项 | `67fd538` | README / LICENSE / LICENSE_TRANSLATION.md |
| M1 基建（六脚本+tests+config+CI+快照+切分） | `2fb7425`…`e72d9ef` | 见 M1 收尾报告；pytest 86 绿 |
| **B01 翻译批次** | 本次提交 | 19 文件（Introduction 3 + Quick Start 10 + IoC 前 6 节）全绿核销；词数 3355（与 inventory 一致）/ 段落 190；报告见 `reports/batch-B01.md` |
| B01 附带缺陷修复 | 同上提交 | M1 缺陷×4 + segment snippet:: 补录 + 新增 assemble_zh.py；pytest 94 绿 |

## 状态快照（2026-11-20，B01 收尾）

- 分支 main；基线 v5.2.25（`0b46d27afdfa`，快照日期 2026-11-20）；批次期间冻结窗口遵守（未跑 --apply）
- manifest：388 条目 = 367 missing + 2 skipped + **19 current**（进度 4.9%）
- 看板：B01 = current，其余 31 批 pending
- anchor-registry：121 条（116→121，http 前缀裸锚点修复后重新生成）；unresolved 2 条不变
- validate 全量跑：PASSED（28 条 ⑤ 豁免警告 = 未译目标，M3 清零）
- zh/resources/img 13 张图镜像已建立（字节复制）
- B01 页头溯源投影：页名=toc 英文原题、URL=`https://docs.micronaut.io/5.2.x/core/#core-<basename>`（官方站实测锚点格式）、基线锁定日期 2026-11-19、translated_at=2026-11-20

## 实测结论（本会话新增）

1. **官方站单页锚点 = `core-<basename>`**：docs.micronaut.io/5.2.x/guide/index.html 302 → /5.2.x/core/（保留 hash）；单页标题 id 形如 `core-introduction`、`core-_upgrading_between_…`（子标题 auto-id 前缀/分隔符均为 `_`）；curl 直连超时须走代理（11.4MB 大页）。
2. **上游怪癖**：guide/httpServer.adoc、guide/httpClient.adoc、guide/certificates.adoc 三章在源码与 toc.yml 存在，但官方站未渲染（站内无对应锚点/导航）；相关裸锚点译文原样保留，validate 正常通过。后续批次遇到这三章时页头 URL 注明站内不可达。
3. **validate/分段器缺陷已修**（详见 reports/batch-B01.md「M1 缺陷修复」）：
   - check_anchors URL 过滤误吞 `http*` 开头裸锚点（已修，registry 116→121）
   - validate ⑤ 裸锚点当文件路径误报（已修：登记表全域解析）
   - validate ⑤ `reg_ids` 放行使注入机检恒真（已收紧：必须存在 `[[id]]`/`[#id]` 字面）
   - 禁繁体表混入简繁共用字（行/息/主/境/景/常）大面积误报（已收紧为繁体独有字）
   - segment_adoc `snippet::` 未列为指令行（已补，B01 含 8 行）
4. **新增 scripts/assemble_zh.py**：溯源投影装配（从 manifest 读双哈希注入页头，杜绝手抄）；后续批次直接复用：
   `memgate 2048 python3 scripts/assemble_zh.py --file <rel...>`（输入为 workdir/protect 下 -restored.txt）
5. 校验链固化：protect → translate（占位符逐字节保留）→ restore（哈希完整性）→ assemble_zh → validate --file → reviewer 段落对照（剔除页头后 paragraph 数相等 + 停用词漏译检测）→ --mark-current。

## 待办（下一会话）

1. **M2 继续**：B02 起（12 文件，非代码词 3049），看板改 in-progress 后按 §5.1 SOP + 上节固化校验链执行；B01 收尾提示词见 `docs/新会话启动提示词.md`（其中批次号改为下一批即可）
2. 术语滚动：qualifier/eager initialization/context propagation 等首现括注是否转正 glossary，由后续批次按频次复核
3. M3+：断链豁免清零（当前 28 条）、抽检、sync drill、tag v1.0

## 调试经验与坑位（累计）

1. 长输出损坏处置：立即读回文件 → 修损坏行 → pytest 全绿 → 再提交（M1 经验，本会话未复发）
2. gh api commits?path= 须用全仓路径 `src/main/docs/<rel>`
3. 网络直连 github.com 失败 → git/curl 走 `http://192.168.33.1:10808`；gh api 直连可用；**11MB 级大页 curl 直连会超时截断（3MB 处 28 超时），必须代理 + 后台跑**
4. validate ⑤ 段落对照做机检时，zh 侧须剔除页头溯源段（引用行+注释行合并为一段，恒 +1 偏差）
5. PreToolUse hook 拒绝 Bash 直写源码/测试文件（heredoc/append）→ 一律 Write/Edit 提交
6. zh 译文页头 `> ` 引用行与 `<!-- -->` 注释行不参与 ⑦/③ 校验（strip_code 豁免），溯源字段以 ⑥/manifest 对账为准

## 硬性纪律清单（继承）

1. `docs/翻译计划.md` 为唯一权威规范；改架构走 decision_log（DR-004 起递增）
2. 所有脚本 memgate 包裹；`source/` 只读；`manifest.yml` 禁人工直改（--mark-current 除外）
3. 门禁硬性化，禁止 `|| true`
4. 每批次 squash commit + 批次报告；决策类提交末行 `Decision: DR-编号`
5. agent 并发上限 = 串行 1；上下文过半立即交接
