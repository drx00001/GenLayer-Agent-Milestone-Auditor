# GenLayer Agent Milestone Auditor

一个更完整的 GenLayer 项目: AI 代理交付物里程碑审计与付款释放判定。

项目不是单一 prompt demo，而是一个端到端工作流: 买家定义验收要求，代理提交里程碑证据包，前端生成 evidence JSON、证据 hash 和确定性预评分，GenLayer validators 再用 AI 共识判断里程碑是否 `accepted`、`revision`、`rejected` 或 `disputed`。

## 为什么适合作为项目里程碑

- 更深入的合约逻辑: 阈值校验、提交计数、验收统计、证据 hash、状态机和 AI 共识复核。
- 测试: `tests/test_policy.py` 覆盖验收评分规则。
- 集成: `app/index.html` 生成部署参数和合约调用参数。
- 部署/使用证据: `docs/USAGE_EVIDENCE.md` 提供 GenLayer Studio 部署和调用记录模板。
- 明确进度: `docs/MILESTONES.md` 写明 M1-M4 交付内容。

## 文件结构

```text
contracts/agent_milestone_auditor.py  GenLayer Intelligent Contract
app/index.html                        前端参数生成器
tests/test_policy.py                   本地评分规则测试
docs/MILESTONES.md                     项目里程碑
docs/USAGE_EVIDENCE.md                 部署与使用证据模板
```

## 合约功能

`AgentMilestoneAuditor` 支持:

- `submit_milestone(milestone_name, evidence_json, evidence_hash, deterministic_score)`
- `latest_verdict()`
- `progress()`

合约会检查:

- 付款阈值是否有效。
- `deterministic_score` 是否在 0 到 100。
- `evidence_hash` 是否足够长。
- AI 共识返回的 `status`、`score`、`release_bps` 是否合理。
- `accepted` 结果是否达到释放阈值。

## 本地测试

```bash
cd 02-GenLayer-Agent-Milestone-Auditor
python3 tests/test_policy.py
```

预期输出:

```text
policy tests passed
```

## GenLayer Studio 部署

1. 打开 https://studio.genlayer.com/contracts
2. 新建或导入 `contracts/agent_milestone_auditor.py`
3. Constructor args:

```json
[
  "AI Agent Delivery Milestone Audit",
  "Agent must deliver a runnable GenLayer milestone with contract logic, tests, frontend integration, deployment instructions, and evidence that the milestone was used end-to-end.",
  8500,
  5000,
  0
]
```

4. 打开 `app/index.html`，点击“生成调用参数”。
5. 复制 `submit_milestone args` 到 GenLayer Studio 调用合约。
6. 把返回结果记录到 `docs/USAGE_EVIDENCE.md`。

## 示例证据包

```json
{
  "contract": true,
  "tests": true,
  "frontend": true,
  "deployment_steps": true,
  "screenshots_or_logs": true,
  "notes": "Contract deployed in GenLayer Studio and submit_milestone returned accepted."
}
```

## 里程碑状态

当前完成:

- M1 可运行合约
- M2 前端集成
- M3 本地测试
- M4 部署与使用证据模板
