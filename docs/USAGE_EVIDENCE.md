# 部署与使用证据

这个文件用于重新提交时补充证据。上传 GitHub 后可以先保留模板；如果已经在 GenLayer Studio 操作过，把结果填进来。

## GenLayer Studio 部署

- Studio URL: https://studio.genlayer.com/contracts
- Contract file: `contracts/agent_milestone_auditor.py`
- Constructor args:

```json
[
  "AI Agent Delivery Milestone Audit",
  "Agent must deliver a runnable GenLayer milestone with contract logic, tests, frontend integration, deployment instructions, and evidence that the milestone was used end-to-end.",
  8500,
  5000,
  0
]
```

## submit_milestone 调用

调用参数由 `app/index.html` 生成，格式如下:

```json
[
  "M1: runnable GenLayer audit workflow",
  "{ evidence JSON string }",
  "sha256 evidence hash",
  100
]
```

## 运行结果记录

- 合约地址:
- submit_milestone 返回:
- latest_verdict 返回:
- progress 返回:
- 截图文件或链接:
