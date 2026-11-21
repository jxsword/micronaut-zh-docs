# 交接文档（handoff-latest）

> 更新：2026-11-21 ｜ 会话：M3 全量收尾（**toc 专项 + sweep + 锚点专项 + 抽检 + sync drill + 豁免清零 + README + tag v1.0 全部完成**）｜ 下一会话任务：持续增量（周检测 → issue → 增量复译）

## 已完成清单（M3 会话，全部随收尾提交入库 + tag v1.0）

| 工作单元 | 说明 |
|---|---|
| toc.yml / toc-python.yml 翻译专项 | 385+301 条标题译出（handoff 旧口径「76 条」仅数 title 行）；键/注释逐字节保留；YAML 注释版溯源投影过 mark-current；新增 scripts/check_toc.py + 5 项 pytest；manifest 核销 current |
| 断链豁免 3 条收尾 | zh/guide/i18n.adoc 最小壳镜像（0 字节源 + `[[i18n]]` 锚）核销；clientConfiguration 回溯补注入 `[[_client_specific_configuration]]`；routing 的 `_uri_path_variables` B11 已在位。⑤ 豁免 **3 → 0** |
| check_anchors.py 增强 | 标题自动锚解析（第三优先级，idprefix/separator 均 `_`）；registry 重生成 121 → 123，unresolved 2 → 0，既有条目零变化 |
| 全量 sweep | spdlog 口径段级比对（4048 段）：errors 3（均为 B18 已文档化的 `////` 注释块误报）、warns 93（全部合法不译），**真漏译 0** |
| 锚点专项 | registry 123 条逐一 grep zh/：**123/123 实锚在位**，同 id 无歧义 |
| 抽检 ≥10% | 分层抽样（seed 20261121）39 文件（10.2%）五项机检 **39/39 PASS**；人工精读 4 文件（ideaSetup/producesAnnotation/methodInjection/pythonThreading）合格 |
| sync drill 八步 | --check 全量（上游 cca2a1ce：388 文件 0 变更）→ --file 单文件 → --apply --dry-run → 门控拒绝验证 → --collect-commits（already=388）→ --mark-current 幂等 → --check 复跑幂等 → tag 后门控解除验证（--apply 0 变更 no-op） |
| 术语滚动复核 | 57 组扫描：**14 条转正** glossary（advice/property source/event loop/service discovery/declarative client/health indicator/distributed tracing/circuit breaker/validation group/exception handler/error handler/camel-case/nullability annotations/data classes）；**advice 真缺陷 3 处修复**（whatsNew「重试建议」旧译、factories xref label 未译、constructorInjection 正文保留英文）；转正后 ③ 回流 387 文件 0 失败 |
| README 在线结构 | 新增「在线对照结构」节（#core-<basename> 对照、构建期注入边界、toc 校验、官方站未渲染三章说明）；基线节更新 v1.0；结构表 toc 路径勘误；B14 看板状态笔误修正 |
| tag `v1.0` | 指向 M3 收尾提交；`--apply` 门控（`v1.0^{commit}` 可解析即解禁）实测解除 |

## 状态快照（2026-11-21，M3 收尾）

- 分支 main；**远程 https://github.com/jxsword/micronaut-zh-docs（2026-11-21 建，SSH remote，push 走 SSH——见坑位 14）；在线阅读 https://jxsword.github.io/micronaut-zh-docs/（deploy-pages.yml 自动部署，DR-004）**；manifest：**388 条目 = 387 current + 1 skipped（appendix.adoc 0 字节壳，无引用）+ 0 missing**；全量 validate 387 文件 PASSED（0 警告 0 失败，⑤ 豁免清零）；pytest **100 绿**（+5 check_toc）
- anchor-registry：123 条（+2 标题自动锚），unresolved 0；toc 结构校验 `scripts/check_toc.py` PASSED（686 页）
- glossary：45 术语（31 → 45）+ 6 banned；三处 advice 旧译修复已入库
- **tag v1.0 已打标**——初译期基线锁定解除，进入持续增量模式（PLAN §8）：
  1. 周期性 `memgate 2048 python3 scripts/sync_upstream.py --check`（远程托管后由 sync-upstream.yml cron 驱动；本地无远程时手动/自动化均可）
  2. 检出变更 → 开 issue（`[upstream-sync] <sha>: 同步待处理`）
  3. issue 目标 48h 内响应：`--apply`（v1.0 后已解禁）→ 生成增量工作项 → 按 PLAN §5.1 SOP 走修订批次（只重译变更段，保留已译段）→ validate 全绿 → `--mark-current` → squash commit
- 退出码约定不变：0=无变更 / 1=有变更待翻译 / 2=环境错误

## 实测结论（M3 新增，继承 B01–B32 全部结论）

1. **源片段 .adoc 无 H1**：页题只存在于 toc.yml（上游构建特性）；toc 标题翻译是对外显示的唯一标题来源。
2. **toc 标题口径**：385 条 = 76 `title:` 行 + 309 标量叶子；toc-python 与 toc 同键同值（多 1 条 overloads 页）。YAML 文件溯源投影写为 `#` 注释（RE_PROVENANCE 在注释行内匹配，YAML 仍合法）。
3. **标题自动锚解析**：check_anchors 第三优先级 `idprefix="_"/idseparator="_"`（Micronaut 构建实测）；未来上游新增 auto-id 引用可直接解析，不再进 unresolved。
4. **sweep 误报三源**：上游 `////` 注释块（B18 纪律保留）、dependency/snippet 宏行、路径型 block title 与行内码列表段——人工分诊时按类豁免。
5. **术语转正回流纪律**：转正前先统计「源文出现文件数 × zh 译名命中」，缺口文件逐一核对语境（API 名/宏/普通行文 → 不动；真旧译 → 先修再转正）；转正后必须全量 validate（③ 回流）。本次 advice 转正抓出 3 处 B01/B02 早期旧译——术语复核确有实效。
6. **glossary 不宜全量收录低频词**：provider/codec/aspect/connection pool 等存在 API 名或普通行文误触面，保持语境括注；specification 规范/规约两译为语境分工（Bean Validation 规范 vs 协议规约），不统一。
7. **drill 八步**（PLAN §8「演练八步全通」落地口径，见 reports/m3-final.md §5）：前置盘点 → --check 全量 → --check --file → --apply --dry-run → 门控拒绝验证 → --collect-commits → --mark-current 幂等 → --check 复跑幂等 + 产物出树确认；tag 后补 --apply 解除验证。
8. **0 字节壳文件的断链处置**：被 xref 引用的壳页建最小 zh 镜像（投影块 + basename 锚）；validate ①–⑦ 全过；未被引用的壳页维持 skipped。

## 待办（下一会话：持续增量阶段）

1. **周检测例行**：跑 `--check`；有变更则开 issue 并按 §5.1 SOP 走增量复译批次（首批可顺带把 B 系列批次报告的目录索引补进 reports/ 便于追溯）。
2. 远程仓库托管时（另议）：README 免责与 Pages 配置一并做；CI workflows（validate.yml / sync-upstream.yml）本地门禁迁 CI。
3. 5.3.x 正式发布时的基线切换：届时按重大决策走 decision_log（DR-004 起）。
4. 二期 guides（CC-BY-4.0）开工前须新决策。

## 调试经验与坑位（M3 增补）

9. **validate 全量循环**：validate_translation.py 仅 `--file` 单参数，全量跑用 python 循环 subprocess（387 文件约 1 分钟）；subprocess 每文件冷启动可接受。
10. **check_toc 白名单机制**：标题值含 CJK 即视为已译；纯 API/产品名条目进 ALLOWLIST（31 条）；「与源逐字节相同」仅对含 CJK 的值报警（防漏译）。
11. **YAML 行级变换**：`key:` 节点行/注释行/空行原样保留，仅替换 `key: value` 叶值；带引号值保留引号风格；替换值与原值相同则整行不动（`'@Blocking'`）。
12. **临时脚本沿用纪律**：Write 工具创建 + py_compile 先行 + memgate 包裹；sweep/抽检/术语扫描脚本口径已固化进 reports/m3-final.md，需要复跑时按报告口径重建即可。
13. **--apply 会改写 source/_upstream_commit**（脚本 apply 收尾写入检测时上游 HEAD，sync_upstream.py:583）：0 变更演练后该文件会偏离基线 sha——M3 收尾时已还原（0b46d27a 与 manifest baseline_commit 一致）；真实增量 apply 后出现此变化属预期行为，配套同步报告会记录当次 HEAD，不必回滚。
14. **git push 必须走 SSH**：gh OAuth token 无 `workflow` scope，https push 含 workflow 文件的提交会被拒（`gh auth setup-git` 也无效）；本机 SSH key（id_ed25519_github3）已认证 jxsword，remote 已设 `git@github.com:jxsword/micronaut-zh-docs.git`，直连可达。
15. **本地预览必须走 HTTP**：沙箱 Firefox 经 xdg-desktop-portal 打开 file:// 时 URL 被重映射到 /run/user/1000/doc/<id>/，portal 只授权用户手动打开的单个文件，页内相对链接全部 404（开发者工具却显示 200）——多文件站点一律 `python3 -m http.server` / 静态服务器提供。起服务用 `setsid memgate … & disown`（nohup 子 shell 与 systemd-run 组合会 hang）。
16. **actions/deploy-pages 偶发 "Found 0 artifact(s)"**：artifact 已上传成功但同 run 内查询为空（GitHub 侧瞬时延迟），重跑 workflow 即可（实测第 2 次 success）。

## 硬性纪律清单（继承，持续有效）

1. `docs/翻译计划.md` 为唯一权威规范；改架构走 decision_log（DR-004 起递增）
2. 所有脚本 memgate 包裹；`source/` 只读（仅 sync 写入）；`manifest.yml` 禁人工直改（--mark-current 除外）
3. 门禁硬性化，禁止 `|| true`
4. 每批次 squash commit + 批次报告；决策类提交末行 `Decision: DR-编号`
5. agent 并发上限 = 串行 1；上下文过半立即交接；里程碑收尾主动建议开新会话
