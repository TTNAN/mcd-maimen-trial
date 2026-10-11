"""订单行为分析引擎: 从历史订单里扒出你的麦门画像."""
from collections import Counter
from datetime import datetime


def parse_time(s):
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except (ValueError, TypeError):
            continue
    return None


def analyze(orders):
    """orders: order-list 返回的 data.list. 返回画像 dict."""
    profile = {
        "order_count": len(orders),
        "tags": [],
        "stats": {},
    }
    if not orders:
        profile["tags"].append("云信徒")
        return profile

    amounts, hours, stores, products = [], [], [], []
    freebies = 0
    for o in orders:
        try:
            amounts.append(float(o.get("realTotalAmount") or 0))
        except (ValueError, TypeError):
            pass
        t = parse_time(o.get("createTime", ""))
        if t:
            hours.append(t.hour)
        if o.get("storeName"):
            stores.append(o["storeName"])
        for p in o.get("orderProductList", []) or []:
            name = p.get("productName", "")
            qty = p.get("quantity") or 1
            products.extend([name] * qty)
            # 组合子项也算
            for sub in p.get("comboItemList", []) or []:
                if sub.get("productName"):
                    products.append(sub["productName"])
        if float(o.get("realTotalAmount") or 0) == 0:
            freebies += 1

    # --- 基础统计 ---
    if amounts:
        profile["stats"]["avg_amount"] = round(sum(amounts) / len(amounts), 2)
        profile["stats"]["min_amount"] = min(amounts)
    hour_counter = Counter(h // 1 for h in hours)
    period = Counter()
    for h in hours:
        if 5 <= h < 10:
            period["早餐"] += 1
        elif 10 <= h < 15:
            period["午餐"] += 1
        elif 15 <= h < 22:
            period["下午茶/晚餐"] += 1
        else:
            period["深夜"] += 1
    profile["stats"]["period"] = dict(period)
    profile["stats"]["top_products"] = Counter(products).most_common(5)
    profile["stats"]["top_stores"] = Counter(stores).most_common(3)

    n = len(orders)
    tags = profile["tags"]

    # --- 人格标签 (行为派) ---
    if period.get("深夜", 0) >= max(1, n * 0.3):
        tags.append("深夜党")
    if period.get("早餐", 0) >= max(1, n * 0.3):
        tags.append("早餐党")
    all_names = " ".join(products)
    if "薯条" in all_names and sum(1 for p in products if "薯条" in p) >= n * 0.5:
        tags.append("薯条教")
    if freebies:
        tags.append("白嫖怪")
    if stores and Counter(stores).most_common(1)[0][1] >= max(2, n * 0.5):
        tags.append("钉子户")
    elif len(set(stores)) >= max(3, n * 0.6):
        tags.append("漂泊党")
    if "随心配" in all_names or "1+1" in all_names:
        tags.append("薅羊毛党")
    if any(k in all_names for k in ("安格斯", "双牛", "板烧", "厚牛")):
        tags.append("肉食者")
    if any(k in all_names for k in ("高达", "泰能打", "限定", "联名")):
        tags.append("尝鲜党")
    if "麦乐鸡" in all_names:
        tags.append("快乐鸡")
    if "巨无霸" in all_names:
        tags.append("经典派")
    if "麦辣" in all_names:
        tags.append("辣党")
    if profile["stats"].get("avg_amount", 0) and profile["stats"]["avg_amount"] < 15:
        tags.append("精打细算")
    if not tags:
        tags.append("随缘麦门")

    # --- 行为分 (0-100): 订单量/频率/广度 ---
    score = min(40, n * 8)  # 订单数, 5单封顶
    score += 20 if len(period) >= 3 else len(period) * 6  # 时段广度
    score += 20 if len(set(stores)) >= 3 else len(set(stores)) * 6  # 门店广度
    score += min(20, len(set(products)) * 2)  # 品类广度
    profile["behavior_score"] = round(min(100, score))

    return profile
