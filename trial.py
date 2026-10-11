#!/usr/bin/env python3
"""麦门审判: quiz 答题 + 真实订单行为分析 -> 段位/人格/分享卡.

用法:
    MCD_MCP_TOKEN=xxx python trial.py                 # 交互答题
    MCD_MCP_TOKEN=xxx python trial.py --answers B,B,B,B,B,B,B,A,A,A
    MCD_MCP_TOKEN=xxx python trial.py --no-orders      # 只答题, 不拉订单
    python trial.py --demo                            # 演示模式: 脱敏示例数据, 无需 Token
"""
import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from mcp import connect, call_tool
from analyzer import analyze
from personas import judge
from recommend import recommend
from report import render

ROOT = os.path.dirname(os.path.abspath(__file__))

# 终端颜色 (不支持时自动降级为空)
def _colors():
    if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
        return {k: "" for k in ("gold", "red", "green", "bold", "dim", "reset")}
    return {"gold": "\033[33m", "red": "\033[31m", "green": "\033[32m",
            "bold": "\033[1m", "dim": "\033[2m", "reset": "\033[0m"}

C = _colors()


def ask_quiz(preset=None):
    quiz = json.load(open(os.path.join(ROOT, "quiz.json"), encoding="utf-8"))
    score, max_score, habit_tags = 0, 0, []
    correct, kcount = 0, len(quiz["knowledge"])
    answers = (preset.split(",") if preset else [])
    ai = 0
    print(f"\n=== {quiz['title']} ===\n")
    for idx, q in enumerate(quiz["knowledge"] + quiz["habit"]):
        is_knowledge = idx < len(quiz["knowledge"])
        print(f"{idx+1}. {q['q']}")
        for i, opt in enumerate(q["options"]):
            print(f"   {chr(65+i)}. {opt}")
        if ai < len(answers):
            ans = answers[ai].strip().upper()
            ai += 1
            print(f"   > {ans} (预设)")
        else:
            ans = input("   你的选择: ").strip().upper()
        pick = ord(ans) - 65 if len(ans) == 1 and "A" <= ans <= "Z" else -1
        if is_knowledge:
            max_score += q["points"]
            if pick == q["answer"]:
                score += q["points"]
                correct += 1
                print(f"   {C['green']}✓{C['reset']} {q['explain']}")
            else:
                print(f"   {C['red']}✗{C['reset']} {q['explain']}")
        else:
            if 0 <= pick < len(q["tags"]):
                habit_tags.append(q["tags"][pick])
                print(f"   → 已记录")
        print()
    return score, max_score, habit_tags, correct, kcount


def load_demo():
    """演示模式: 脱敏合成订单 + 示例券, 时间按 daysAgo 换算成最近日期."""
    d = json.load(open(os.path.join(ROOT, "demo_orders.json"), encoding="utf-8"))
    now = datetime.now()
    orders = []
    for o in d.get("orders", []):
        t = (now - timedelta(days=o.get("daysAgo", 0))).replace(
            hour=o.get("hour", 12), minute=30, second=0)
        orders.append({
            "realTotalAmount": o.get("amount", "0"),
            "createTime": t.strftime("%Y-%m-%d %H:%M:%S"),
            "storeName": o.get("store", ""),
            "orderProductList": [
                {"productName": p, "quantity": 1, "comboItemList": []}
                for p in o.get("products", [])
            ],
        })
    coupons = [{"name": c.get("name", "")} for c in d.get("coupons", [])]
    return orders, coupons


DEMO_ANSWERS = "B,B,A,B,C,A,B,A,B,C,A,B,A,A,B,A,B,A"  # 演示用预设答案


def fetch_orders(session):
    payload, _ = call_tool(session, "order-list", {})
    data = payload.get("data", payload) if isinstance(payload, dict) else {}
    orders = data.get("list", []) if isinstance(data, dict) else []
    return [o for o in orders if isinstance(o, dict)]


def extract_coupons(payload):
    """从 available-coupons 返回里抠出券名列表, 结构防御式解析."""
    data = payload.get("data", payload) if isinstance(payload, dict) else {}
    items = []
    if isinstance(data, dict):
        for key in ("list", "coupons", "records", "items"):
            if isinstance(data.get(key), list):
                items = data[key]
                break
    elif isinstance(data, list):
        items = data
    out = []
    for it in items:
        if not isinstance(it, dict):
            continue
        name = it.get("couponName") or it.get("name") or it.get("title") or ""
        status = it.get("status") or it.get("state") or ""
        if name:
            out.append({"name": str(name), "status": str(status)})
    return out


def main():
    args = sys.argv[1:]
    preset = next((a.split("=", 1)[1] for a in args if a.startswith("--answers=")), None)
    # 兼容 --answers B,B 形式
    if not preset and "--answers" in args:
        i = args.index("--answers")
        preset = args[i + 1] if i + 1 < len(args) else None
    no_orders = "--no-orders" in args
    demo = "--demo" in args
    if demo and not preset:
        preset = DEMO_ANSWERS
        print("演示模式：预设答案 + 脱敏示例订单（含示例券），无需 Token。\n")

    score, max_score, habit_tags, correct, kcount = ask_quiz(preset)

    orders = []
    coupons = []
    if demo:
        orders, coupons = load_demo()
        print(f"演示模式：载入 {len(orders)} 笔脱敏示例订单，{len(coupons)} 张示例券\n")
    elif not no_orders:
        try:
            session = connect()
            orders = fetch_orders(session)
            print(f"已拉取 {len(orders)} 笔历史订单")
            try:
                payload, _ = call_tool(session, "available-coupons", {})
                coupons = extract_coupons(payload)
                print(f"发现 {len(coupons)} 张可领优惠券\n")
            except Exception as e:
                print(f"优惠券查询失败 ({e})，跳过。\n")
        except Exception as e:
            print(f"订单拉取失败 ({e})，仅按答题出结果。\n")

    profile = analyze(orders)
    if coupons:
        profile["stats"]["coupon_count"] = len(coupons)
        if len(coupons) >= 5 and "薅羊毛党" not in profile["tags"]:
            profile["tags"].append("薅羊毛党")
    result = judge(score, max_score, profile, habit_tags)
    result["recommend"] = recommend(profile, coupons)
    result["quiz_detail"] = f"{correct}/{kcount} 答对"

    print("=" * 44)
    print(f"  {C['gold']}{C['bold']}审判结果：{result['level']}{C['reset']}")
    print(f"  综合 {C['bold']}{result['total_score']}{C['reset']} 分"
          f"（答题 {result['quiz_score']} / 行为 {result['behavior_score']}）")
    print(f"  标签：{C['red']}{' / '.join(result['tags'])}{C['reset']}")
    print(f"  判词：{C['gold']}{result['roast']}{C['reset']}")
    print(f"  {C['green']}下一单：{result['recommend']}{C['reset']}")
    print("=" * 44)

    out = os.path.join(ROOT, "report.html")
    render(result, out)
    print(f"\n分享卡已生成：{out}")
    print("在浏览器打开后：手机长按卡片保存图片，或点「📥 下载分享卡 PNG」按钮。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
