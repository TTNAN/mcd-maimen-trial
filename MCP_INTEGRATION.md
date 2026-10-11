# 麦当劳 MCP 接入说明

## 双版本说明

本项目有两个版本，分工如下：

- **网页版**（`docs/index.html`，[在线体验](https://ttnan.github.io/mcd-maimen-trial/)）：纯前端 quiz，**不调用任何 MCP 接口**，行为分用习惯题答案估算。无需登录、无 token，零隐私风险。
- **完整版**（`trial.py`）：调用下方 MCP Tool 拉取真实历史订单做行为分析，需要用户自备 `MCD_MCP_TOKEN`。

## 使用的 MCP Server（完整版）

- **Server**：麦当劳中国官方 MCP Server
- **接入地址**：`https://mcp.mcd.cn`
- **传输协议**：Streamable HTTP（JSON-RPC over HTTP POST）
- **鉴权**：请求头 `Authorization: Bearer <MCD_MCP_TOKEN>`

## 使用的 Tool

| Tool | 用途 |
| --- | --- |
| `order-list` | 拉取用户历史订单（下单时间、门店、商品清单、实付金额），是人格审判的核心数据源 |
| `now-time-info` | 校准当前时间（备用） |

> 实际 Tool 名以官方 MCP 文档为准。

## 调用流程

```
initialize（建连）
  → 交互式 quiz（7 道知识题 + 3 道习惯题，本地题库 quiz.json）
  → order-list → 历史订单
  → analyzer.py：时段分布 / 本命单品 / 客单价 / 门店离散度 / 白嫖记录 → 行为画像 + 行为分
  → personas.py：quiz 分 × 0.4 + 行为分 × 0.6 → 段位；反差规则 → 嘴强王者 / 身体很诚实；标签 → 毒舌判词
  → report.py：生成单文件 HTML 分享卡
```

## 业务价值

把"我觉得我是麦门信徒"变成可验证的数据结论：quiz 测知识、订单看行为，两者互相印证或打脸。分享卡形态天然适合社交传播，让更多人了解麦当劳 MCP 能做什么。

## 安全说明

- MCP Token 仅通过环境变量 `MCD_MCP_TOKEN` 传入，不写入代码、日志或 Git 仓库；
- 历史订单属于个人隐私数据，仅在用户本地运行时读取，不上传任何服务器；
- 仓库中的示例报告为**脱敏合成数据**，不含任何真实订单信息。
