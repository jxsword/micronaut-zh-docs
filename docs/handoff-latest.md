# 交接文档（handoff-latest）

> 更新：2026-11-20 ｜ 会话：M0 余项 + M1 基建会话 ｜ 下一会话任务：M2 分批翻译（B01 起）

## 已完成清单（全部已提交，main 分支）

| 工作单元 | 提交 | 说明 |
|---|---|---|
| M0 余项 | `67fd538` | README（TASL/基线锚定/结构表）/ LICENSE（MIT）/ LICENSE_TRANSLATION.md（Apache-2.0 署名） |
| segment_adoc.py | `2fb7425` | asciidoc 分段器 + 18 测试 |
| protect_untranslatable.py | `24299ce` | 占位符保护/还原 + 16 测试 |
| sync_upstream.py | `eaf4bc1` | 账本同步（--init/--check/--apply 门控/--mark-current/--collect-commits）+ 24 测试 |
| validate_translation.py | `d2fd429` | 七项硬门禁 + 17 测试 |
| check_anchors.py | `ebb18a4`+`060f3fa` | 裸锚点全域解析（116 锚点/2 unresolved） |
| progress.py | `cdc49b5` | 进度报表 + 3 测试 |
| config | `d390b61` | glossary 17 术语 + 6 banned；style-guide |
| prompts | `96437bb` | translate.md.j2 + review.md |
| CI | `1c7fe96` | validate.yml + sync-upstream.yml（预备件） |
| 快照 | `758608f` | v5.2.25 快照 + manifest 388 条目 + 演练产出 |
| 切分 | `758608f` 后续 | inventory-5.2.25.md（32 批）+ 看板 + 采集完成（388/388） |

## 状态快照

- 分支 main；快照基线 `0b46d27afdfa`（tag v5.2.25，2026-11-17 发布）
- manifest：388 条目 = 386 missing + 2 skipped（guide/appendix.adoc、guide/i18n.adoc 纯 include 壳）
- 验收演练全过：`--check` 对照 5.2.x HEAD（cca2a1ce83cd）0 变更退出码 0；pytest 86 绿；validate 空库通过
- 批次：32 批（双指标 非代码词 ≤3500 / 总词 ≤5500 实测达标），非代码词 99,722 / 总词 100,312 / 总段 5,573

## 实测结论（M1 验证的关键事实）

1. **toc.yml 含显示标题**（嵌套 dict），键路径 `guide/<键路径>.adoc` 即阅读顺序；toc.yml/toc-python.yml 已入账本，翻译时只译标题值（YAML 键不译）
2. 上游 xref 惯例：**裸锚点跨页引用**（`<<anchor,Label>>`），锚 id = include 文件 basename；check_anchors 据此解析 116 个被引锚点，2 个 unresolved（M3 清零跟踪）
3. 上游 5.2.x HEAD 与 v5.2.25 之间 src/main/docs 无差异（基线与分支头一致）

## 待办（下一会话）

1. **M2 分批翻译**：按看板 B01 起串行执行（启动提示词见 `docs/新会话启动提示词.md`，可直接粘贴）
2. `upstream_commit` 采集：**已完成**（388/388 成功，0 延后；per-file commit 已入 manifest）；
   后续新文件或 --apply 后需补采：
   `memgate 2048 python3 scripts/sync_upstream.py --collect-commits --ref 5.2.x`（缓存续跑不重复请求）
3. M3+：断链豁免清零、抽检、sync 全链路 drill、tag v1.0

## 调试经验与坑位

1. **长输出损坏**：本会话多次出现工具调用内容损坏（长文件写入退化），已全部读回修复并全绿；
   复发时的处置：立即读回文件 → 修损坏行 → pytest 全绿 → 再提交
2. gh api commits?path= 必须用全仓路径（`src/main/docs/<rel>`），传相对路径会返回空数组（exit 0 无输出）
3. 网络直连 github.com 失败，git clone 走 `HTTPS_PROXY=http://192.168.33.1:10808`；gh api 直连可用
4. `--init` 退出码 1 = 386 missing 待翻译（符合 §4.2「1=有变更待翻译」约定）
5. apply 门控：`MZD_ALLOW_APPLY=1` 仅供测试；生产解禁条件 = git tag v1.0 存在

## 硬性纪律清单（继承）

1. `docs/翻译计划.md` 为唯一权威规范；改架构走 decision_log（DR-004 起递增）
2. 所有脚本 memgate 包裹；`source/` 只读；`manifest.yml` 禁人工直改
3. 门禁硬性化，禁止 `|| true`
4. 每批次 squash commit + 批次报告；决策类提交末行 `Decision: DR-编号`
5. agent 并发上限 = 串行 1；上下文过半立即交接
