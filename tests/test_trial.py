"""analyzer / personas / recommend 单元测试: python -m unittest discover tests"""
import os
import sys
import unittest
from datetime import datetime, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from analyzer import analyze
from personas import judge
from recommend import recommend


def order(amount="25.0", dt=None, store="测试店", products=("麦辣鸡腿堡",)):
    return {
        "realTotalAmount": amount,
        "createTime": (dt or datetime.now()).strftime("%Y-%m-%d %H:%M:%S"),
        "storeName": store,
        "orderProductList": [
            {"productName": p, "quantity": 1, "comboItemList": []} for p in products
        ],
    }


class TestAnalyzer(unittest.TestCase):
    def test_empty(self):
        p = analyze([])
        self.assertIn("云信徒", p["tags"])
        self.assertEqual(p["order_count"], 0)

    def test_night_owl(self):
        orders = [order(dt=datetime(2026, 1, 1, 23, 30) - timedelta(days=i))
                  for i in range(4)]
        p = analyze(orders)
        self.assertIn("深夜党", p["tags"])

    def test_freebie(self):
        p = analyze([order(amount="0")])
        self.assertIn("白嫖怪", p["tags"])

    def test_fries_cult(self):
        orders = [order(products=("薯条", "可乐")) for _ in range(3)]
        p = analyze(orders)
        self.assertIn("薯条教", p["tags"])

    def test_score_bounds(self):
        orders = [order(dt=datetime.now() - timedelta(days=i),
                        products=("巨无霸", "薯条", "麦乐鸡"))
                  for i in range(10)]
        p = analyze(orders)
        self.assertGreaterEqual(p["behavior_score"], 0)
        self.assertLessEqual(p["behavior_score"], 100)
        self.assertIn("recent_30d", p["stats"])

    def test_stable_amount(self):
        orders = [order(amount="20.0") for _ in range(4)]
        p = analyze(orders)
        self.assertIn("稳定输出", p["tags"])

    def test_abnormal_orders(self):
        orders = [
            {},
            {"realTotalAmount": "abc", "createTime": "not-a-time",
             "orderProductList": None},
            {"realTotalAmount": None, "storeName": "x", "createTime": None},
            {"orderProductList": [{"productName": None, "quantity": None}]},
        ]
        p = analyze(orders)  # 不崩即可
        self.assertGreaterEqual(p["behavior_score"], 0)
        self.assertLessEqual(p["behavior_score"], 100)


class TestPersonas(unittest.TestCase):
    def _profile(self, behavior, tags=()):
        return {"behavior_score": behavior, "tags": list(tags),
                "order_count": 5, "stats": {}}

    def test_king_of_talk(self):
        r = judge(120, 120, self._profile(20), [])
        self.assertEqual(r["tags"][0], "嘴强王者")
        self.assertTrue(r["roast"])  # 有判词即可

    def test_honest_body(self):
        r = judge(20, 120, self._profile(80), [])
        self.assertEqual(r["tags"][0], "身体很诚实")

    def test_levels(self):
        self.assertEqual(judge(120, 120, self._profile(90), [])["level"], "麦门祖师")
        # quiz 75分*0.4=30 + 行为70*0.6=42 -> 72 长老
        self.assertEqual(judge(90, 120, self._profile(70), [])["level"], "麦门长老")
        self.assertEqual(judge(0, 120, self._profile(0), [])["level"], "麦门路人")

    def test_habit_tags_kept(self):
        r = judge(60, 120, self._profile(50), ["薯条教", "深夜党"])
        self.assertIn("薯条教", r["tags"])


class TestRecommend(unittest.TestCase):
    def _profile(self, fav="麦辣鸡腿堡"):
        return {"stats": {"top_products": [(fav, 5)]}}

    def test_matched_coupon(self):
        rec = recommend(self._profile(), [{"name": "麦辣鸡腿堡单人餐优惠券"}])
        self.assertIn("麦辣鸡腿堡", rec)
        self.assertIn("优惠券", rec)

    def test_no_coupon(self):
        rec = recommend(self._profile(), [])
        self.assertIn("麦辣鸡腿堡", rec)

    def test_no_data(self):
        rec = recommend({"stats": {}}, [])
        self.assertIn("巨无霸", rec)


if __name__ == "__main__":
    unittest.main()
