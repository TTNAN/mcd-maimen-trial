"""下一单推荐: 本命单品 x 当前可领优惠券 -> 一句人话推荐."""


def _keywords(name):
    kws = [name]
    kws += [name[i:i + 2] for i in range(0, len(name), 2) if len(name[i:i + 2]) == 2]
    return [k for k in kws if len(k) >= 2]


def recommend(profile, coupons):
    """profile: analyze() 结果; coupons: [{name,...}] 可领券列表. 返回推荐文案."""
    top = profile.get("stats", {}).get("top_products", [])
    fav = top[0][0] if top else ""
    names = [c.get("name", "") for c in coupons if c.get("name")]

    matched = []
    if fav:
        kws = _keywords(fav)
        for nm in names:
            if any(k in nm for k in kws):
                matched.append(nm)

    if matched:
        return f"本命「{fav}」配上「{matched[0]}」，干饭更香，冲！"
    if names:
        who = fav or "巨无霸"
        return f"先领「{names[0]}」，再点{who}，别和钱过不去。"
    if fav:
        return f"继续宠幸你的本命「{fav}」，专一是麦门美德。"
    return "从巨无霸开始吧，麦门入门第一课。"
