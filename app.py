"""
📡 5G 信号可视化看板 (5G Signal Visualization Dashboard)
=========================================================
Code with AI 海选赛 — 基础关卡 + 进阶关卡完整实现

功能特性：
  - 数据加载：pandas 读取 CSV 数据
  - 交互地图：2D 散点图（RSRP 颜色编码） + 3D 柱状图（高度=下载速率）
  - 数据概览：频段分布柱状图、终端类型饼图
  - 侧边栏联动筛选：频段、RSRP 范围、终端类型
  - 工程化：类型注释、文档字符串、单元测试

作者：AI Coding Agent (OpenClaw)
"""

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# ---------------------------------------------------------------------------
# 页面配置
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="5G 信号可视化看板",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# 数据加载 — 基础关卡①
# ---------------------------------------------------------------------------
DATA_PATH = "data/signal_samples.csv"


@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    """
    从 CSV 文件读取 5G 路测数据。

    Returns
    -------
    pd.DataFrame
        包含经纬度、小区ID、频段、RSRP、SINR、终端类型、下载速率的 DataFrame。
    """
    df = pd.read_csv(path)
    # 确保数值列为 float
    for col in ["Latitude", "Longitude", "RSRP_dBm", "SINR_dB", "Download_Mbps"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


df_raw = load_data(DATA_PATH)

# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------


def rsrp_color(rsrp: float) -> str:
    """
    根据 RSRP 值返回颜色（用于 2D 散点图）。

    规则：
      - RSRP > -90 dBm → 绿色 (信号强)
      - -110 ≤ RSRP ≤ -90 dBm → 黄色 (信号中等)
      - RSRP < -110 dBm → 红色 (信号弱)
    """
    if rsrp > -90:
        return "#00cc66"  # 绿
    elif rsrp >= -110:
        return "#ffcc00"  # 黄
    else:
        return "#ff3333"  # 红


def rsrp_color_rgb(rsrp: float):
    """
    返回 [R, G, B] 格式的颜色值，用于 pydeck 图层。
    """
    if rsrp > -90:
        return [0, 204, 102]
    elif rsrp >= -110:
        return [255, 204, 0]
    else:
        return [255, 51, 51]


# ---------------------------------------------------------------------------
# 侧边栏 — 进阶关卡①：联动筛选
# ---------------------------------------------------------------------------
st.sidebar.title("📡 筛选面板")
st.sidebar.markdown("使用下方筛选器实时过滤地图与图表数据。")

# 频段筛选
available_bands = sorted(df_raw["Band"].unique())
selected_bands = st.sidebar.multiselect(
    "频段 (Band)",
    options=available_bands,
    default=available_bands,
    help="选择一个或多个 5G 频段进行筛选",
)

# RSRP 范围筛选
rsrp_min, rsrp_max = int(df_raw["RSRP_dBm"].min()), int(df_raw["RSRP_dBm"].max())
rsrp_range = st.sidebar.slider(
    "RSRP 范围 (dBm)",
    min_value=rsrp_min,
    max_value=rsrp_max,
    value=(rsrp_min, rsrp_max),
    step=1,
    help="拖动滑动条筛选信号强度范围",
)

# 终端类型筛选
available_terminals = sorted(df_raw["TerminalType"].unique())
selected_terminals = st.sidebar.multiselect(
    "终端类型 (Terminal)",
    options=available_terminals,
    default=available_terminals,
    help="选择一个或多个终端类型",
)

# 地图类型切换
map_mode = st.sidebar.radio(
    "地图模式",
    options=["2D 散点图", "3D 柱状图"],
    index=0,
    help="2D: 颜色编码信号强度; 3D: 柱高表示下载速率",
)

# ---------------------------------------------------------------------------
# 数据筛选（应用侧边栏条件）
# ---------------------------------------------------------------------------
def filter_data(df: pd.DataFrame) -> pd.DataFrame:
    """根据侧边栏选择条件筛选数据。"""
    mask = (
        df["Band"].isin(selected_bands)
        & df["RSRP_dBm"].between(rsrp_range[0], rsrp_range[1])
        & df["TerminalType"].isin(selected_terminals)
    )
    return df[mask].copy()


df = filter_data(df_raw)

# ---------------------------------------------------------------------------
# 页面主体
# ---------------------------------------------------------------------------
st.title("📡 5G 信号可视化看板")
st.markdown(
    "**Code with AI 海选赛** · 基于 Streamlit + pydeck 构建的交互式 5G 路测数据看板。"
)

# 数据概览指标
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("样本总数", f"{len(df)}", f"{len(df) - len(df_raw):+d}")
with col2:
    st.metric(
        "平均 RSRP",
        f"{df['RSRP_dBm'].mean():.1f} dBm",
        f"{df['RSRP_dBm'].mean() - df_raw['RSRP_dBm'].mean():.1f}" if len(df) > 0 else "—",
    )
with col3:
    st.metric("平均下载速率", f"{df['Download_Mbps'].mean():.1f} Mbps")
with col4:
    st.metric("覆盖小区", f"{df['CellID'].nunique()}")

# ---------------------------------------------------------------------------
# 交互地图 — 基础关卡② + 进阶关卡②
# ---------------------------------------------------------------------------
st.subheader("🗺️ 信号覆盖地图")

if df.empty:
    st.warning("当前筛选条件下没有数据，请调整侧边栏筛选条件。")
else:
    # 准备地图数据
    map_df = df[["Latitude", "Longitude", "RSRP_dBm", "Download_Mbps", "CellID", "Band", "SINR_dB"]].copy()
    map_df["color"] = map_df["RSRP_dBm"].apply(rsrp_color)
    map_df["color_rgb"] = map_df["RSRP_dBm"].apply(rsrp_color_rgb)

    # 判断使用 2D 还是 3D
    if map_mode == "2D 散点图":
        # --- 2D 散点图（基础关卡②） ---
        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["Longitude", "Latitude"],
            get_color="color_rgb",
            get_radius=30,
            pickable=True,
            auto_highlight=True,
            radius_min_pixels=3,
            radius_max_pixels=15,
        )

        view_state = pdk.ViewState(
            latitude=map_df["Latitude"].mean(),
            longitude=map_df["Longitude"].mean(),
            zoom=12,
            pitch=0,
        )

        tooltip = {
            "html": (
                "<b>小区 ID:</b> {CellID}<br/>"
                "<b>频段:</b> {Band}<br/>"
                "<b>RSRP:</b> {RSRP_dBm} dBm<br/>"
                "<b>SINR:</b> {SINR_dB} dB<br/>"
                "<b>下载速率:</b> {Download_Mbps} Mbps"
            ),
            "style": {"backgroundColor": "rgba(0,0,0,0.8)", "color": "white"},
        }

        deck = pdk.Deck(
            layers=[scatter_layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_provider="carto",
            map_style="light",
        )

        st.pydeck_chart(deck, width='stretch')

        # 图例
        st.markdown(
            """
            <div style="display:flex; gap:20px; margin-top:5px;">
                <span style="color:#00cc66;">●</span> RSRP > -90 dBm (强)
                <span style="color:#ffcc00; margin-left:15px;">●</span> -110 ~ -90 dBm (中)
                <span style="color:#ff3333; margin-left:15px;">●</span> RSRP < -110 dBm (弱)
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        # --- 3D 柱状图（进阶关卡②） ---
        # 将柱高映射到合适的缩放范围
        height_scale = 500  # 缩放因子
        map_df["height"] = map_df["Download_Mbps"] * height_scale

        # 可选的柱高范围控制
        col_height_min = st.number_input(
            "柱高基数 (m)", value=100, step=50,
            help="所有柱子的基础高度（米），叠加下载速率映射高度。"
        )
        map_df["height"] = col_height_min + map_df["Download_Mbps"] * height_scale / 100

        column_layer = pdk.Layer(
            "ColumnLayer",
            data=map_df,
            get_position=["Longitude", "Latitude"],
            get_elevation="height",
            elevation_scale=1,
            radius=30,
            get_fill_color="color_rgb",
            pickable=True,
            auto_highlight=True,
            extruded=True,
            coverage=0.8,
        )

        view_state_3d = pdk.ViewState(
            latitude=map_df["Latitude"].mean(),
            longitude=map_df["Longitude"].mean(),
            zoom=12,
            pitch=45,
            bearing=0,
        )

        tooltip_3d = {
            "html": (
                "<b>小区 ID:</b> {CellID}<br/>"
                "<b>频段:</b> {Band}<br/>"
                "<b>RSRP:</b> {RSRP_dBm} dBm<br/>"
                "<b>下载速率:</b> {Download_Mbps} Mbps<br/>"
                "<b>柱高:</b> {height:.0f} m"
            ),
            "style": {"backgroundColor": "rgba(0,0,0,0.8)", "color": "white"},
        }

        deck_3d = pdk.Deck(
            layers=[column_layer],
            initial_view_state=view_state_3d,
            tooltip=tooltip_3d,
            map_provider="carto",
            map_style="light",
        )

        st.pydeck_chart(deck_3d, width='stretch')

        st.info(
            "💡 3D 柱状图：柱子颜色表示 RSRP 信号强度（绿=强，黄=中，红=弱），"
            "柱子高度表示下载速率（越高越快）。拖动鼠标旋转/缩放查看。"
        )

# ---------------------------------------------------------------------------
# 数据概览图表 — 基础关卡③
# ---------------------------------------------------------------------------
st.subheader("📊 数据概览")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # 各频段基站数量柱状图
    st.markdown("**各频段基站数量**")
    band_counts = df["Band"].value_counts().reset_index()
    band_counts.columns = ["Band", "Count"]
    st.bar_chart(band_counts.set_index("Band"), color="#0066ff", width='stretch')

with chart_col2:
    # 各终端类型占比饼图（使用 st.write 配合自定义 CSS 绘制饼图）
    st.markdown("**各终端类型占比**")
    term_counts = df["TerminalType"].value_counts()

    # 使用 Streamlit 原生饼图
    term_df = term_counts.reset_index()
    term_df.columns = ["TerminalType", "Count"]

    # 配色方案
    term_colors = {"Smartphone": "#00cc66", "CPE": "#0066ff", "IoT": "#ffcc00"}

    # 用 st.bar_chart 展示占比方便比较，但需求要求饼图——用 pyplot 绘制
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    colors = [term_colors.get(t, "#999999") for t in term_counts.index]
    wedges, texts, autotexts = ax.pie(
        term_counts.values,
        labels=term_counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
        textprops={"fontsize": 12},
    )
    ax.set_title("", fontsize=14)
    st.pyplot(fig, width='stretch')

# ---------------------------------------------------------------------------
# 数据预览表
# ---------------------------------------------------------------------------
with st.expander("📋 查看原始数据"):
    st.dataframe(df, width='stretch')
    st.download_button(
        label="💾 下载筛选后数据 (CSV)",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_signal_data.csv",
        mime="text/csv",
    )

# ---------------------------------------------------------------------------
# 页脚说明
# ---------------------------------------------------------------------------
st.markdown("---")
st.caption(
    "📡 5G 信号可视化看板 · Code with AI 海选赛 · "
    "数据来源: `data/signal_samples.csv`"
)
