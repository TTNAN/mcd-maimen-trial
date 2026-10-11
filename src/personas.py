"""人格裁决: quiz 分 + 行为分 -> 段位 / 反差梗 / 毒舌点评."""

LEVELS = [
    (80, "麦门祖师", "你对麦当劳的了解已经超越了 99% 的人类，建议去应聘产品经理。"),
    (60, "麦门长老", "谈笑间，巨无霸灰飞烟灭。麦门有你，是麦门的福气。"),
    (40, "麦门信徒", "虔诚，但还可以更虔诚。你的修行之路才刚刚开始。"),
    (0, "麦门路人", "你路过麦当劳的次数比进去的次数多。麦门大门常打开，欢迎回头。"),
]

ROASTS = {
    "深夜党": "深夜的emo，一半是生活，一半是麦辣鸡翅。",
    "早餐党": "能为了猪柳蛋麦满分早起的人，干什么都能成。",
    "薯条教": "你的血管里流的不是血，是番茄酱。",
    "白嫖怪": "0 元订单？你薅的不是羊毛，是麦当劳的命。",
    "钉子户": "一家店吃到店员认识你，这叫专一。",
    "漂泊党": "南昌吃到上海，麦门没有边界。",
    "薅羊毛党": "1+1 随心配？你的数学一定很好。",
    "肉食者": "安格斯一入口，就知有没有。",
    "尝鲜党": "限定出了你必冲，麦当劳的市场部应该给你发工资。",
    "快乐鸡": "麦乐鸡蘸酱，你蘸的是童年。",
    "经典派": "巨无霸，永远的神，不接受反驳。",
    "辣党": "无辣不欢，麦辣鸡腿堡是你的本命没跑了。",
    "精打细算": "客单价不到 15 块，你是麦门审计署署长。",
    "嘴强王者": "题全对，单没点——麦门的理论家，实践的逃兵。",
    "身体很诚实": "题没答对几道，但订单不会骗人。麦门欢迎实干家。",
    "云信徒": "一次没点过？先点一单再回来审判。",
    "随缘麦门": "想起来才吃，吃的就是个随缘。",
    "干饭战士": "一周三刷以上，麦当劳你家开的？",
    "稳定输出": "细水长流，麦门需要你这样的中坚力量。",
    "自律党": "深夜从不点单，自制力拉满，respect。",
    "堂食党": "薯条必须现炸现吃，仪式感拉满。",
    "外卖党": "外卖能到的距离，都是你的麦门领地。",
    "自取党": "为了省配送费多走两步，精明的麦门人。",
    "原价战神": "原价吃麦当劳，真正的实力派。",
    "重度上瘾": "一天不吃浑身难受？麦门认证重度患者。",
    "中度依赖": "一周一单，剂量刚刚好。",
    "轻度想念": "一月一想，细水长流。",
}


def judge(quiz_score, quiz_max, profile, habit_tags):
    """返回 {level, title, roast, tags, scores}."""
    quiz_pct = (quiz_score / quiz_max * 100) if quiz_max else 0
    behavior = profile.get("behavior_score", 0)
    total = round(quiz_pct * 0.4 + behavior * 0.6)

    for threshold, level, _ in LEVELS:
        if total >= threshold:
            break

    tags = []
    # 反差梗优先
    if quiz_pct >= 70 and behavior < 40:
        tags.append("嘴强王者")
    elif quiz_pct < 40 and behavior >= 60:
        tags.append("身体很诚实")
    tags.extend(habit_tags[:2])
    for t in profile.get("tags", []):
        if t not in tags and len(tags) < 4:
            tags.append(t)

    roasts = [ROASTS.get(t, "") for t in tags[:2]]
    roast = " ".join(r for r in roasts if r)
    if not roast:
        roast = "麦门大门常打开，欢迎下次再来。"

    return {
        "level": level,
        "total_score": total,
        "quiz_score": round(quiz_pct),
        "behavior_score": behavior,
        "tags": tags,
        "roast": roast,
        "order_count": profile.get("order_count", 0),
        "stats": profile.get("stats", {}),
    }
