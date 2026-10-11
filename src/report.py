"""生成麦门审判分享卡 (单文件 HTML, 深色麦当劳风, 内嵌 Canvas 可下载 PNG)."""
import html
import json


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
    rec = result.get("recommend", "")
    rec_row = f"<b>下一单推荐</b>：{_esc(rec)}<br>\n" if rec else ""
    quiz_detail = result.get("quiz_detail", "")
    quiz_row = f"<b>知识题</b>：{_esc(quiz_detail)}<br>\n" if quiz_detail else ""

    # 内嵌给 Canvas 用的数据
    rdata = {
        "level": result["level"],
        "total": result["total_score"],
        "quiz": result["quiz_score"],
        "behavior": result["behavior_score"],
        "quiz_detail": quiz_detail,
        "tags": result["tags"],
        "roast": result["roast"],
        "order_count": result.get("order_count", 0),
        "period": period_str,
        "top": "、".join(f"{n}×{c}" for n, c in top[:3]) or "暂无",
        "avg": str(avg),
        "recommend": rec,
    }
    rdata_json = json.dumps(rdata, ensure_ascii=False).replace("</", "<\\/")

    page = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>麦门审判 · {result['level']}</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#0d0d0d;color:#f5f5f5;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;display:flex;flex-direction:column;align-items:center;padding:24px}}
.tip{{width:100%;max-width:420px;background:rgba(245,197,24,.1);border:1px solid #f5c518;border-radius:12px;padding:12px 16px;font-size:14px;line-height:1.7;color:#ffe9a8;margin-bottom:16px}}
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
.dl{{display:block;width:100%;max-width:420px;margin-top:16px;padding:15px;border:0;border-radius:14px;font-size:16px;font-weight:700;cursor:pointer;background:linear-gradient(90deg,#f5c518,#ff9d00);color:#2b0a06}}
</style></head><body>
<div class="tip">📸 <b>分享小贴士</b>：手机长按上方卡片可保存图片，或点下方按钮直接下载 PNG 分享卡，发朋友圈更方便。</div>
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
<b>客单价</b>：{avg} 元<br>
{quiz_row}{rec_row}</div>
<div class="foot">数据来源：麦当劳官方 MCP · <b>麦门审判 mcd-maimen-trial</b></div>
</div>
<button class="dl" onclick="dlCard()">📥 下载分享卡 PNG</button>
<script id="rdata" type="application/json">{rdata_json}</script>
<script>
function rr(x,px,py,w,h,r){{x.beginPath();x.moveTo(px+r,py);x.arcTo(px+w,py,px+w,py+h,r);x.arcTo(px+w,py+h,px,py+h,r);x.arcTo(px,py+h,px,py,r);x.arcTo(px,py,px+w,py,r);x.closePath()}}
function wrap(x,text,px,py,maxW,lh){{
  let line="",lines=[];
  for(const ch of text){{ if(x.measureText(line+ch).width>maxW){{lines.push(line);line=ch}}else line+=ch }}
  lines.push(line);
  lines.forEach((l,i)=>x.fillText(l,px,py+i*lh));
}}
function dlCard(){{
  const R=JSON.parse(document.getElementById("rdata").textContent);
  const W=900,H=1400,c=document.createElement("canvas");c.width=W;c.height=H;
  const x=c.getContext("2d"),F='-apple-system,"PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif';
  const g=x.createLinearGradient(0,0,W,H);g.addColorStop(0,"#1a0505");g.addColorStop(.6,"#2b0a06");g.addColorStop(1,"#120404");
  x.fillStyle=g;x.fillRect(0,0,W,H);
  x.strokeStyle="#5a1f12";x.lineWidth=3;x.strokeRect(30,30,W-60,H-60);
  x.textAlign="center";
  x.fillStyle="#f5c518";x.font=`28px ${{F}}`;x.fillText("麦 门 审 判",W/2,120);
  const tg=x.createLinearGradient(200,0,700,0);tg.addColorStop(0,"#ffcf3f");tg.addColorStop(1,"#e4002b");
  x.fillStyle=tg;x.font=`bold 120px ${{F}}`;x.fillText(R.level,W/2,280);
  x.fillStyle="#FFC72C";x.font=`bold 44px ${{F}}`;x.fillText(`综合 ${{R.total}} 分`,W/2,360);
  x.fillStyle="#aaa";x.font=`30px ${{F}}`;
  const sub=`知识题 ${{R.quiz_detail||R.quiz+"分"}} · 行为 ${{R.behavior}} 分`;
  x.fillText(sub,W/2,410);
  // tags
  x.font=`32px ${{F}}`;
  const ws=R.tags.map(t=>x.measureText(t).width+56),gap=16;
  let tx=(W-(ws.reduce((a,b)=>a+b,0)+gap*(ws.length-1)))/2;const ty=470;
  R.tags.forEach((t,i)=>{{
    x.fillStyle="rgba(228,0,43,.18)";x.strokeStyle="#e4002b";x.lineWidth=2;
    rr(x,tx,ty,ws[i],64,32);x.fill();x.stroke();
    x.fillStyle="#ffb3c0";x.fillText(t,tx+ws[i]/2,ty+43);tx+=ws[i]+gap;
  }});
  // roast
  x.fillStyle="rgba(245,197,24,.08)";x.fillRect(90,580,W-180,220);
  x.fillStyle="#f5c518";x.fillRect(90,580,8,220);
  x.textAlign="left";x.fillStyle="#ffe9a8";x.font=`36px ${{F}}`;
  wrap(x,"「"+R.roast+"」",130,650,W-260,58);
  // rows
  x.fillStyle="#bbb";x.font=`30px ${{F}}`;let ry=880;
  [["在册订单",R.order_count+" 单"],["时段画像",R.period],["本命单品",R.top],["客单价",R.avg+" 元"]]
    .forEach(([k,v])=>{{ x.fillStyle="#fff";x.fillText(k+"：",150,ry);x.fillStyle="#bbb";
      x.textAlign="left";x.fillText(String(v).slice(0,20),150+x.measureText(k+"：").width,ry);x.textAlign="center";ry+=52; }});
  if(R.recommend){{ x.fillStyle="#7CFC98";x.font=`30px ${{F}}`;
    wrap(x,"下一单："+R.recommend,90,ry+10,W-180,48); }}
  // hook
  x.fillStyle="#ddd";x.font=`34px ${{F}}`;x.textAlign="center";
  x.fillText(`我是${{R.level}}，你敢来审判吗？`,W/2,H-160);
  x.fillStyle="#666";x.font=`24px ${{F}}`;
  x.fillText("麦门审判 mcd-maimen-trial · 麦当劳程序员创意开发大赛参赛作品",W/2,H-100);
  const a=document.createElement("a");
  a.href=c.toDataURL("image/png");a.download="麦门审判-"+R.level+".png";a.click();
}}
</script>
</body></html>"""
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(page)
    return out_path
