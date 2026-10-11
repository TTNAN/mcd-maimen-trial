# 麦门审判 Skill

> 麦门浓度测试 × 真实订单人格审判。让人（或 Agent）回答 18 道题，拉取麦当劳官方 MCP 的历史订单，输出段位、人格标签、毒舌判词和下一单推荐。

## 两种使用方式

### 1. 给人玩：网页版（零登录）

https://ttnan.github.io/mcd-maimen-trial/

手机打开即玩：18 道题（12 知识 + 6 习惯）→ 段位 → Canvas 分享卡 → 一键分享。
行为分用习惯题估算，不调用任何 MCP 接口，数据不出手机。

### 2. 给 Agent 用：Python 完整版

```bash
MCD_MCP_TOKEN=xxx python trial.py --answers B,B,A,C,A,A,B,A,A,B,A,C,A,A,B,A,B,A
# --answers: 18 个选项(A/B/C)，跳过交互直接出结果
# --no-orders: 只答题，不拉订单（无 token 时用）
```

也可以当库调用：

```python
from src.analyzer import analyze      # orders -> 画像 {tags, behavior_score, stats}
from src.personas import judge        # (quiz分, 行为分) -> {level, tags, roast}
from src.recommend import recommend  # (画像, 可领券) -> 下一单推荐文案
```

## MCP 工具（完整版，均为只读）

| 工具 | 用途 |
| --- | --- |
| `order-list` | 历史订单：时段 / 本命单品 / 客单价 / 门店离散度 / 0 元单 |
| `available-coupons` | 当前可领券：实锤「薅羊毛党」，参与下一单推荐 |

## 计分规则

- 综合分 = quiz 答题分 × 0.4 + 订单行为分 × 0.6
- 行为分（0-100）：订单数 30 + 时段广度 15 + 门店广度 15 + 品类广度 10 + 近 30 天活跃 15 + 深夜浓度 10 + 客单价稳定 5
- 反差梗：quiz ≥ 70 且行为 < 40 →「嘴强王者」；quiz < 40 且行为 ≥ 60 →「身体很诚实」

## 段位

80+ 麦门祖师 / 60+ 麦门长老 / 40+ 麦门信徒 / 40 以下麦门路人

## 下一单推荐逻辑

`recommend(profile, coupons)`：取订单统计里的本命单品（top_products[0]），
在可领券里按关键词匹配相关券；有券配本命 → 直接推荐组合；
只有券 → 先领券再点本命；都没 → 从巨无霸入门。

## 隐私

- Token 只走 `MCD_MCP_TOKEN` 环境变量，不落盘。
- 订单数据仅在本地进程内使用，不上传任何服务器。
- 仓库示例报告为脱敏合成数据。
