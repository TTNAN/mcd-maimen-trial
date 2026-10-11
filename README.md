# 麦门审判 · mcd-maimen-trial

<p align="center"><img src="assets/poster.jpg" width="420" alt="麦门审判海报"></p>

> 你说你是麦门信徒？让数据说话。

<p align="center">
  <a href="https://ttnan.github.io/mcd-maimen-trial/"><img src="https://img.shields.io/badge/🍔_在线体验-开始审判-FFC72C?style=for-the-badge" alt="在线体验"></a>
  <a href="https://github.com/TTNAN/mcd-maimen-trial/stargazers"><img src="https://img.shields.io/github/stars/TTNAN/mcd-maimen-trial?style=for-the-badge&color=DA291C" alt="GitHub stars"></a>
</p>

<p align="center"><b>觉得好玩？点个 ⭐ Star 帮我冲榜！麦当劳程序员创意开发大赛按 Star 排名，冲进前 100 就有实物奖。</b></p>

🔒 **隐私承诺**：网页版零登录、答题数据不出你的手机；完整版的历史订单只在你本地读取，Token 只走环境变量，仓库里没有任何真实订单数据。

麦当劳程序员创意开发大赛参赛作品。把**麦门浓度测试**（quiz 答题）和**订单人格审判**（真实历史订单行为分析）结合在一起。

## 30 秒体验

| 方式 | 怎么玩 | 说明 |
| --- | --- | --- |
| 网页版 | https://ttnan.github.io/mcd-maimen-trial/ | 打开即玩，零登录 |
| 完整版演示 | `python trial.py --demo` | 脱敏示例数据，无需 Token，一次看完整流程 |
| 完整版真实 | `MCD_MCP_TOKEN=xxx python trial.py` | 你的真实订单审判 |

## 玩法

**第一步：答题。** 18 道题，12 道麦门知识 + 6 道习惯：

- 巨无霸里有几层牛肉饼？麦乐鸡块常规装几块？麦辣鸡腿堡是哪块肉？——答错直接开嘲讽
- 你吃麦当劳的频率？本命单品？深夜点过吗？——习惯题决定人格底色

**第二步：审判（完整版）。** 接入麦当劳官方 MCP，读取你的真实历史订单：下单时段、本命单品、客单价、门店离散度、0 元白嫖单——订单不会骗人。

**第三步：领判词。** 综合得分 = 答题分 × 0.4 + 行为分 × 0.6，生成你的段位、人格标签和毒舌判词，一键生成分享卡发朋友圈。

## 最好玩的部分：反差梗

- 题全对、一单没点过 → **「嘴强王者」**：麦门的理论家，实践的逃兵
- 题答得稀烂、订单拉满 → **「身体很诚实」**：麦门欢迎实干家

> 👉 把链接甩给那个自称「麦门信徒」的朋友，看看谁才是真祖师：https://ttnan.github.io/mcd-maimen-trial/

## 截图

| 首页 | 答题 | 审判结果 |
| --- | --- | --- |
| ![首页](assets/screenshots/hero.jpg) | ![答题](assets/screenshots/quiz.jpg) | ![审判结果](assets/screenshots/result.jpg) |

## 段位

| 分数 | 段位 | 判词 |
| --- | --- | --- |
| 80+ | 麦门祖师 | 你对麦当劳的了解已经超越了 99% 的人类 |
| 60-79 | 麦门长老 | 谈笑间，巨无霸灰飞烟灭 |
| 40-59 | 麦门信徒 | 虔诚，但还可以更虔诚 |
| <40 | 麦门路人 | 你路过麦当劳的次数比进去的次数多 |

## 人格标签（部分）

深夜党 / 早餐党 / 薯条教 / 白嫖怪 / 钉子户 / 漂泊党 / 薅羊毛党 / 肉食者 / 尝鲜党 / 快乐鸡 / 经典派 / 辣党 / 精打细算 / 堂食党 / 外卖党 / 原价战神……

## 两个版本

| | 网页版 `docs/index.html` | 完整版 `trial.py` |
| --- | --- | --- |
| 体验方式 | 在线即玩，无需登录 | 本地运行 |
| quiz 答题 | ✓（18 道） | ✓（18 道） |
| 真实订单分析 | ✗（用习惯题估算行为分） | ✓（`order-list` 拉历史订单） |
| 可领优惠券 | ✗ | ✓（`available-coupons`，顺手薅羊毛） |
| 下一单推荐 | ✗ | ✓（本命单品 × 当前可领券） |
| 分享卡 | Canvas 生成 PNG，可一键分享 | HTML 生成 |
| token | 不需要 | 需要 `MCD_MCP_TOKEN` 环境变量 |

## 本地运行完整版

```bash
# 仅依赖 Python 标准库，无需 pip install
# 1. 去 https://open.mcd.cn/mcp 用手机号登录，点"激活"拿到 Token
# 2. Token 只走环境变量，不会写入任何文件
MCD_MCP_TOKEN=你的token python trial.py
```

只答题不拉订单：`MCD_MCP_TOKEN=你的token python trial.py --no-orders`

跑单元测试：`python -m unittest discover tests`

## 示例

- [`sample_report.html`](sample_report.html) —— 完整版脱敏示例报告（合成数据，`python trial.py --demo` 一键生成）
- 分享卡示例（`report.html` 里点「📥 下载分享卡 PNG」可得）：

<p align="center"><img src="assets/share-card-sample.jpg" width="300" alt="分享卡示例"></p>

- [`assets/poster.jpg`](assets/poster.jpg) —— 宣传海报

## 目录结构

```
├── docs/index.html        # 网页版（GitHub Pages 在线体验）
├── trial.py               # 完整版主流程：答题 → 拉订单 → 分析 → 裁决 → 分享卡
├── quiz.json              # 题库（12 道知识题 + 6 道习惯题）
├── SKILL.md               # Skill 说明：Agent 如何调用审判能力
├── src/
│   ├── mcp.py             # 麦当劳 MCP 通用客户端
│   ├── analyzer.py        # 订单行为分析引擎
│   ├── personas.py        # 段位 / 反差梗 / 毒舌判词规则
│   ├── recommend.py       # 下一单推荐：本命单品 × 可领券
│   └── report.py          # 分享卡 HTML 生成
├── tests/                 # 单元测试
├── assets/poster.jpg      # 宣传海报
├── sample_report.html     # 脱敏示例报告
├── mcp-config.example.json# MCP 配置示例（脱敏）
├── MCP_INTEGRATION.md     # MCP 接入说明
└── CONTEST_DECLARATION.md # 参赛声明（官方原文，一字未改）
```

## 隐私说明

- 网页版不调用任何接口、不收集任何数据，答题全在本地完成。
- 完整版的历史订单仅在用户本地运行时读取，不上传任何服务器；Token 只走环境变量。
- 仓库中的示例报告为脱敏合成数据，不含任何真实订单信息。

## 目标用户

- 想测测自己麦门浓度的麦门信徒
- 想看朋友"嘴上说不要，身体很诚实"的乐子人
- 1024 程序员节，想整点好玩的程序员

## 参赛信息

- 活动：麦当劳程序员创意开发大赛
- 许可证：MIT

---

<p align="center"><b>🍟 玩得开心？Star 一下，帮麦门审判冲榜 → <a href="https://github.com/TTNAN/mcd-maimen-trial/stargazers">点我 Star</a> ⭐</b></p>
