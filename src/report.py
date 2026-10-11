"""生成麦门审判分享卡 (单文件 HTML, 深色麦当劳风)."""
import html


def _esc(s):
    return html.escape(str(s))


def render(result, out_path):
    tags = "".join(f'<span class="tag">{_esc(t)}</span>' for t in result["tags"])
    stats = result.get("stats", {})
    period = stats.get("period", {})
    period_str = " / ".join(f"{k}×{v}" for k, v in period.items()) or "暂无"
    top = stats.get("top_products", [])
    top_str = "、".join(f"{_esc(n)}×{c}" for n, c in top[:3]) or "暂无"
    avg = stats.get("avg_amount", "-")

    page = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>麦门审判 · {result['level']}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d0d0d;color:#f5f5f5;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;display:flex;justify-content:center;padding:24px}}
.card{{width:100%;max-width:420px;background:linear-gradient(160deg,#1a0505,#2b0a06 60%,#120404);border:1px solid #5a1f12;border-radius:20px;padding:32px 28px;box-shadow:0 12px 48px rgba(228,0,43,.25)}}
.kicker{{color:#f5c518;letter-spacing:.35em;font-size:12px;text-align:center}}
h1{{text-align:center;font-size:38px;margin:10px 0 4px;background:linear-gradient(90deg,#ffcf3f,#e4002b);-webkit-background-clip:text;background-clip:text;color:transparent}}
.score{{text-align:center;color:#999;font-size:13px;margin-bottom:18px}}
.tags{{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:16px 0}}
.tag{{background:rgba(228,0,43,.16);border:1px solid #e4002b;color:#ffb3c0;border-radius:999px;padding:6px 14px;font-size:14px}}
.roast{{background:rgba(245,197,24,.08);border-left:3px solid #f5c518;padding:12px 14px;border-radius:0 10px 10px 0;font-size:15px;line-height:1.7;margin:18px 0;color:#ffe9a8}}
.rows{{margin-top:6px;font-size:14px;color:#bbb;line-height:2}}
.rows b{{color:#fff}}
.foot{{margin-top:22px;text-align:center;color:#666;font-size:12px}}
.foot b{{color:#f5c518}}
</style></head><body>
<div class="card">
<div class="kicker">麦 门 审 判</div>
<h1>{result['level']}</h1>
<div class="score">综合 {result['total_score']} 分 · 答题 {result['quiz_score']} 分 · 行为 {result['behavior_score']} 分</div>
<div class="tags">{tags}</div>
<div class="roast">{_esc(result['roast'])}</div>
<div class="rows">
<b>在册订单</b>：{result['order_count']} 单<br>
<b>时段画像</b>：{_esc(period_str)}<br>
<b>本命单品</b>：{top_str}<br>
<b>客单价</b>：{avg} 元
</div>
<div class="foot">数据来源：麦当劳官方 MCP · <b>麦门审判 mcd-maimen-trial</b></div>
</div></body></html>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    return out_path
