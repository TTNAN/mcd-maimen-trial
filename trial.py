#!/usr/bin/env python3
"""麦门审判: quiz 答题 + 真实订单行为分析 -> 段位/人格/分享卡.

用法:
    MCD_MCP_TOKEN=xxx python trial.py                 # 交互答题
    MCD_MCP_TOKEN=xxx python trial.py --answers B,B,B,B,B,B,B,A,A,A
    MCD_MCP_TOKEN=xxx python trial.py --no-orders      # 只答题, 不拉订单
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))
from mcp import connect, call_tool
from analyzer import analyze
from personas import judge
from report import render

ROOT = os.path.dirname(os.path.abspath(__file__))


def ask_quiz(preset=None):
    quiz = json.load(open(os.path.join(ROOT, "quiz.json"), encoding="utf-8"))
    score, max_score, habit_tags = 0, 0, []
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
                print(f"   ✓ {q['explain']}")
            else:
                print(f"   ✗ {q['explain']}")
        else:
            if 0 <= pick < len(q["tags"]):
                habit_tags.append(q["tags"][pick])
                print(f"   → 已记录")
        print()
    return score, max_score, habit_tags


def fetch_orders(session):
    payload, _ = call_tool(session, "order-list", {})
    data = payload.get("data", payload) if isinstance(payload, dict) else {}
    orders = data.get("list", []) if isinstance(data, dict) else []
    return [o for o in orders if isinstance(o, dict)]


def main():
    args = sys.argv[1:]
    preset = next((a.split("=", 1)[1] for a in args if a.startswith("--answers=")), None)
    # 兼容 --answers B,B 形式
    if not preset and "--answers" in args:
        i = args.index("--answers")
        preset = args[i + 1] if i + 1 < len(args) else None
    no_orders = "--no-orders" in args

    score, max_score, habit_tags = ask_quiz(preset)

    orders = []
    if not no_orders:
        try:
            session = connect()
            orders = fetch_orders(session)
            print(f"已拉取 {len(orders)} 笔历史订单\n")
        except Exception as e:
            print(f"订单拉取失败 ({e})，仅按答题出结果。\n")

    profile = analyze(orders)
    result = judge(score, max_score, profile, habit_tags)

    print("=" * 40)
    print(f"  审判结果：{result['level']}")
    print(f"  综合 {result['total_score']} 分（答题 {result['quiz_score']} / 行为 {result['behavior_score']}）")
    print(f"  标签：{' / '.join(result['tags'])}")
    print(f"  判词：{result['roast']}")
    print("=" * 40)

    out = os.path.join(ROOT, "report.html")
    render(result, out)
    print(f"\n分享卡已生成：{out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
