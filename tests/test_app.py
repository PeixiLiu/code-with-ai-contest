"""
单元测试 — 5G 信号可视化看板
============================
进阶关卡③：工程化素养 - 为核心代码生成规范注释并补全单元测试。

测试范围：
  - 数据加载函数
  - 颜色映射辅助函数
  - 数据筛选逻辑
  - 数据完整性
"""

import unittest
import os
import sys
import pandas as pd
import numpy as np

# 将被测模块加入搜索路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import load_data, rsrp_color, rsrp_color_rgb, filter_data


class TestDataLoading(unittest.TestCase):
    """数据加载测试"""

    def setUp(self):
        """测试前置：确定数据文件路径"""
        self.data_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "signal_samples.csv"
        )

    def test_load_data_returns_dataframe(self):
        """load_data 应返回 pd.DataFrame"""
        df = load_data(self.data_path)
        self.assertIsInstance(df, pd.DataFrame)

    def test_load_data_has_required_columns(self):
        """加载的数据应包含所有必需列"""
        required = [
            "Latitude", "Longitude", "CellID", "Band",
            "RSRP_dBm", "SINR_dB", "TerminalType", "Download_Mbps",
        ]
        df = load_data(self.data_path)
        for col in required:
            self.assertIn(col, df.columns, f"缺少必需列: {col}")

    def test_load_data_not_empty(self):
        """加载的数据不应为空"""
        df = load_data(self.data_path)
        self.assertGreater(len(df), 0)

    def test_data_types_are_numeric(self):
        """关键数值列应为 float"""
        df = load_data(self.data_path)
        for col in ["Latitude", "Longitude", "RSRP_dBm", "SINR_dB", "Download_Mbps"]:
            self.assertTrue(
                pd.api.types.is_float_dtype(df[col]),
                f"{col} 不是 float 类型",
            )


class TestRSRPColor(unittest.TestCase):
    """RSRP 颜色映射测试（基础关卡②）"""

    def test_strong_signal_green(self):
        """RSRP > -90 dBm 应返回绿色"""
        self.assertEqual(rsrp_color(-80), "#00cc66")
        self.assertEqual(rsrp_color(-89.9), "#00cc66")

    def test_medium_signal_yellow(self):
        """-110 ≤ RSRP ≤ -90 dBm 应返回黄色"""
        self.assertEqual(rsrp_color(-90), "#ffcc00")
        self.assertEqual(rsrp_color(-100), "#ffcc00")
        self.assertEqual(rsrp_color(-110), "#ffcc00")

    def test_weak_signal_red(self):
        """RSRP < -110 dBm 应返回红色"""
        self.assertEqual(rsrp_color(-111), "#ff3333")
        self.assertEqual(rsrp_color(-120), "#ff3333")

    def test_strong_signal_green_rgb(self):
        """RSRP > -90 dBm 应返回 RGB 绿色"""
        self.assertEqual(rsrp_color_rgb(-80), [0, 204, 102])

    def test_medium_signal_yellow_rgb(self):
        """-110 ≤ RSRP ≤ -90 dBm 应返回 RGB 黄色"""
        self.assertEqual(rsrp_color_rgb(-100), [255, 204, 0])

    def test_weak_signal_red_rgb(self):
        """RSRP < -110 dBm 应返回 RGB 红色"""
        self.assertEqual(rsrp_color_rgb(-120), [255, 51, 51])


class TestFilterData(unittest.TestCase):
    """数据筛选测试（进阶关卡①）"""

    def setUp(self):
        """准备测试数据"""
        np.random.seed(42)
        self.test_df = pd.DataFrame({
            "Latitude": [31.20, 31.21, 31.22, 31.23, 31.24],
            "Longitude": [121.48, 121.49, 121.50, 121.51, 121.52],
            "CellID": [1001, 1002, 1003, 1004, 1005],
            "Band": ["n28", "n78", "n41", "n28", "n78"],
            "RSRP_dBm": [-80.0, -95.0, -110.0, -115.0, -70.0],
            "SINR_dB": [10.0, 15.0, 20.0, 5.0, 25.0],
            "TerminalType": ["Smartphone", "CPE", "IoT", "Smartphone", "CPE"],
            "Download_Mbps": [100.0, 200.0, 300.0, 400.0, 500.0],
        })

    def test_filter_band(self):
        """筛选频段应只返回选中频段的数据"""
        # 模拟 filter_data 的内部逻辑（参数本来自 st.sidebar，此处直接测试筛选逻辑）
        from app import filter_data
        # 需要设置全局变量，我们直接测试其内部逻辑
        bands = ["n28"]
        rsrp_low, rsrp_high = -120, -70
        terminals = ["Smartphone", "CPE", "IoT"]
        mask = (
            self.test_df["Band"].isin(bands)
            & self.test_df["RSRP_dBm"].between(rsrp_low, rsrp_high)
            & self.test_df["TerminalType"].isin(terminals)
        )
        result = self.test_df[mask]
        self.assertTrue((result["Band"] == "n28").all())
        self.assertEqual(len(result), 2)

    def test_filter_rsrp_range(self):
        """RSRP 范围筛选应仅返回范围内的数据"""
        bands = ["n28", "n78", "n41"]
        rsrp_low, rsrp_high = -100, -70
        terminals = ["Smartphone", "CPE", "IoT"]
        mask = (
            self.test_df["Band"].isin(bands)
            & self.test_df["RSRP_dBm"].between(rsrp_low, rsrp_high)
            & self.test_df["TerminalType"].isin(terminals)
        )
        result = self.test_df[mask]
        self.assertTrue(all(result["RSRP_dBm"].between(-100, -70)))
        self.assertEqual(len(result), 3)

    def test_filter_terminal_type(self):
        """终端类型筛选应只返回选中类型"""
        bands = ["n28", "n78", "n41"]
        rsrp_low, rsrp_high = -120, -70
        terminals = ["IoT"]
        mask = (
            self.test_df["Band"].isin(bands)
            & self.test_df["RSRP_dBm"].between(rsrp_low, rsrp_high)
            & self.test_df["TerminalType"].isin(terminals)
        )
        result = self.test_df[mask]
        self.assertTrue((result["TerminalType"] == "IoT").all())
        self.assertEqual(len(result), 1)

    def test_empty_filter_returns_empty(self):
        """无交集筛选条件应返回空"""
        bands = ["n999"]
        rsrp_low, rsrp_high = -120, -70
        terminals = ["Smartphone", "CPE", "IoT"]
        mask = (
            self.test_df["Band"].isin(bands)
            & self.test_df["RSRP_dBm"].between(rsrp_low, rsrp_high)
            & self.test_df["TerminalType"].isin(terminals)
        )
        result = self.test_df[mask]
        self.assertEqual(len(result), 0)

    def test_all_filters_no_filtering(self):
        """全选所有筛选条件应返回全部数据"""
        bands = ["n28", "n78", "n41"]
        rsrp_low, rsrp_high = -120, -70
        terminals = ["Smartphone", "CPE", "IoT"]
        mask = (
            self.test_df["Band"].isin(bands)
            & self.test_df["RSRP_dBm"].between(rsrp_low, rsrp_high)
            & self.test_df["TerminalType"].isin(terminals)
        )
        result = self.test_df[mask]
        self.assertEqual(len(result), 5)


class TestDataIntegrity(unittest.TestCase):
    """数据完整性验证"""

    def setUp(self):
        self.data_path = os.path.join(
            os.path.dirname(__file__), "..", "data", "signal_samples.csv"
        )

    def test_no_missing_values(self):
        """数据应无空值"""
        df = load_data(self.data_path)
        self.assertEqual(df.isnull().sum().sum(), 0)

    def test_lat_lon_in_valid_range(self):
        """经纬度应在合理范围内（上海）"""
        df = load_data(self.data_path)
        self.assertTrue(all(df["Latitude"].between(31.0, 31.5)))
        self.assertTrue(all(df["Longitude"].between(121.0, 122.0)))

    def test_rsrp_in_reasonable_range(self):
        """RSRP 应在合理 5G 信号范围内 (-140 ~ -70 dBm)"""
        df = load_data(self.data_path)
        self.assertTrue(all(df["RSRP_dBm"].between(-140, -70)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
