# 项目里程碑

## M1 - 可运行合约

- 完成 `AgentMilestoneAuditor` GenLayer Intelligent Contract。
- 支持初始化项目名、买家要求、付款阈值。
- 支持 `submit_milestone` 提交证据包、证据 hash、确定性预评分。
- 支持 `latest_verdict` 和 `progress` 查询验收状态。

## M2 - 证据与评分集成

- 前端 `app/index.html` 生成 constructor args。
- 前端生成 `submit_milestone` 参数。
- 浏览器内计算 SHA-256 evidence hash。
- 评分规则覆盖合约、测试、前端、部署步骤和使用证据。

## M3 - 测试与验证

- `tests/test_policy.py` 覆盖完整、缺测试、薄 demo 三类证据。
- 可用 `python3 tests/test_policy.py` 本地运行。
- README 提供 GenLayer Studio 部署和调用步骤。

## M4 - 重新提交证据

- 上传 GitHub 后，提交仓库链接。
- 若已部署到 GenLayer Studio，把合约地址、交易或截图补到 `docs/USAGE_EVIDENCE.md`。
