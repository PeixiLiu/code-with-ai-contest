"""
╔══════════════════════════════════════════════════════════════╗
║           📡 5G SIGNAL NEXUS — 赛博朋克可视化看板             ║
║         Code with AI 海选赛 · 极致视觉升级版                  ║
╚══════════════════════════════════════════════════════════════╝

Features:
  🌃 Cyberpunk Dark Theme + Neon Glow
  🗺️ Multi-layer 3D/2D maps with pydeck
  💫 Animated background particles (CSS)
  📊 Interactive animated charts
  🎛️ Glassmorphism sidebar filters
  🔥 Real-time metric pulse indicators
"""

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ═══════════════════════════════════════════════════════════════
# 页面配置
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="📡 5G Signal Nexus",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════
# 自定义 CSS — 赛博朋克主题
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Global Dark Theme ── */
.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 30%, #0a0a1a 60%, #0d0d2b 100%);
    background-attachment: fixed;
}
.stMainBlockContainer {
    background: transparent !important;
}

/* ── Neon Glow Title ── */
h1 {
    background: linear-gradient(90deg, #00ffff, #ff00ff, #00ffff);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    font-weight: 900 !important;
    font-size: 3rem !important;
    text-shadow: none !important;
    filter: drop-shadow(0 0 20px rgba(0,255,255,0.5));
    letter-spacing: 2px !important;
}

h2 {
    color: #00ffff !important;
    font-weight: 700 !important;
    text-shadow: 0 0 10px rgba(0,255,255,0.3);
    border-bottom: 1px solid rgba(0,255,255,0.2);
    padding-bottom: 8px;
}

h3 {
    color: #ff00ff !important;
    font-weight: 600 !important;
}

/* ── Glassmorphism Cards ── */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(0,255,255,0.15) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), inset 0 1px 0 rgba(0,255,255,0.1) !important;
    transition: all 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(0,255,255,0.4) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4), 0 0 24px rgba(0,255,255,0.15), inset 0 1px 0 rgba(0,255,255,0.2) !important;
    transform: translateY(-2px);
}
[data-testid="stMetricValue"] {
    color: #00ffff !important;
    font-weight: 900 !important;
    font-size: 2rem !important;
}
[data-testid="stMetricDelta"] {
    color: #00ff88 !important;
    font-weight: 600 !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, rgba(10,10,30,0.98) 0%, rgba(20,0,40,0.98) 100%) !important;
    border-right: 1px solid rgba(0,255,255,0.1) !important;
    backdrop-filter: blur(20px) !important;
}
[data-testid="stSidebar"] .stMarkdown {
    color: #ccc !important;
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #ff00ff !important;
    text-shadow: 0 0 15px rgba(255,0,255,0.4);
}

/* ── Select/Slider Widgets ── */
.stSelectbox label, .stMultiselect label, .stSlider label {
    color: #00ffff !important;
    font-weight: 600 !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(0,255,255,0.1) !important;
    border-radius: 12px !important;
}

/* ── Buttons ── */
.stButton button {
    background: linear-gradient(135deg, #ff00ff, #00ffff) !important;
    border: none !important;
    border-radius: 12px !important;
    color: #000 !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    box-shadow: 0 0 20px rgba(255,0,255,0.3) !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase !important;
}
.stButton button:hover {
    box-shadow: 0 0 40px rgba(255,0,255,0.5), 0 0 80px rgba(0,255,255,0.2) !important;
    transform: scale(1.05) !important;
}

/* ── Divider ── */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(0,255,255,0.3), transparent) !important;
    margin: 24px 0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0a0a1a; }
::-webkit-scrollbar-thumb { background: linear-gradient(#00ffff, #ff00ff); border-radius: 3px; }

/* ── Animation: Pulse ── */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.pulse { animation: pulse 2s ease-in-out infinite; }

/* ── Animation: Glow ── */
@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(0,255,255,0.3); }
    50% { box-shadow: 0 0 40px rgba(0,255,255,0.6), 0 0 80px rgba(255,0,255,0.3); }
}
.glow-box {
    border: 2px solid rgba(0,255,255,0.3);
    border-radius: 16px;
    padding: 20px;
    background: rgba(10,10,30,0.6);
    animation: glow 3s ease-in-out infinite;
}

/* ── Footer ── */
.stCaption {
    color: rgba(255,255,255,0.3) !important;
    font-size: 0.8rem !important;
    text-align: center !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 数据加载
# ═══════════════════════════════════════════════════════════════
DATA_PATH = "data/signal_samples.csv"

@st.cache_data(ttl=3600)
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ["Latitude", "Longitude", "RSRP_dBm", "SINR_dB", "Download_Mbps"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df

df_raw = load_data(DATA_PATH)

# ═══════════════════════════════════════════════════════════════
# 颜色方案 — 赛博朋克霓虹
# ═══════════════════════════════════════════════════════════════
NEON_CYAN = [0, 255, 255]
NEON_MAGENTA = [255, 0, 255]
NEON_GREEN = [0, 255, 136]
NEON_ORANGE = [255, 136, 0]
NEON_RED = [255, 55, 85]
DEEP_PURPLE = [80, 0, 160]

def rsrp_neon_color(rsrp: float):
    """RSRP → 霓虹色映射"""
    if rsrp > -85:
        return NEON_CYAN               # 极强
    elif rsrp > -95:
        return NEON_GREEN              # 强
    elif rsrp > -105:
        return [255, 200, 50]          # 中 - 金色
    elif rsrp > -115:
        return NEON_ORANGE             # 弱
    else:
        return NEON_RED                # 极弱

def rsrp_hex(rsrp: float) -> str:
    r, g, b = rsrp_neon_color(rsrp)
    return f"#{r:02x}{g:02x}{b:02x}"

# ═══════════════════════════════════════════════════════════════
# 侧边栏 — 赛博朋克风格
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; margin-bottom:20px;">
        <div style="font-size:3rem;">📡</div>
        <div style="font-size:0.75rem; color:#666; letter-spacing:3px; margin-top:-10px;">SIGNAL NEXUS v2.0</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ 信号筛选器")
    
    available_bands = sorted(df_raw["Band"].unique())
    selected_bands = st.multiselect(
        "📶 频段 (Band)",
        options=available_bands,
        default=available_bands,
        help="选择5G频段：n28, n41, n78"
    )
    
    rsrp_min = int(df_raw["RSRP_dBm"].min()) - 1
    rsrp_max = int(df_raw["RSRP_dBm"].max()) + 1
    rsrp_range = st.slider(
        "📊 RSRP 范围 (dBm)",
        min_value=rsrp_min,
        max_value=rsrp_max,
        value=(rsrp_min, rsrp_max),
        step=1,
    )
    
    available_terminals = sorted(df_raw["TerminalType"].unique())
    selected_terminals = st.multiselect(
        "📱 终端类型",
        options=available_terminals,
        default=available_terminals,
    )
    
    st.markdown("---")
    st.markdown("### 🗺️ 地图模式")
    map_mode = st.radio(
        "选择视图",
        options=["🌍 2D 霓虹散点", "🏙️ 3D 赛博城市", "🔥 热力覆盖"],
        index=0,
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ 3D 参数")
    col_height_scale = st.slider("柱高灵敏度", 10, 200, 60, step=10, help="3D柱状图高度缩放")
    pitch_angle = st.slider("视角倾斜度", 0, 75, 50, step=5, help="地图倾斜角度")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size:0.7rem; color:#444; text-align:center; margin-top:20px;">
        ⚡ POWERED BY AI<br/>
        <span style="color:#00ffff;">OpenClaw + DeepSeek</span><br/>
        <span style="color:#ff00ff;">Code with AI 2026</span>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 数据筛选
# ═══════════════════════════════════════════════════════════════
mask = (
    df_raw["Band"].isin(selected_bands)
    & df_raw["RSRP_dBm"].between(rsrp_range[0], rsrp_range[1])
    & df_raw["TerminalType"].isin(selected_terminals)
)
df = df_raw[mask].copy()

# ═══════════════════════════════════════════════════════════════
# 页面标题
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="text-align:center; margin-bottom:10px;">
    <div style="font-size:0.8rem; color:#ff00ff; letter-spacing:8px; text-transform:uppercase; margin-bottom:-10px;">
        ⚡ Cyberpunk Dashboard
    </div>
</div>
""", unsafe_allow_html=True)

st.title("📡 5G SIGNAL NEXUS")
st.markdown("""
<div style="text-align:center; color:#666; margin-top:-10px; margin-bottom:30px; font-size:0.9rem;">
    实时 5G 路测数据可视化 · 赛博朋克主题 · AI 驱动分析
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# KPI 指标卡片
# ═══════════════════════════════════════════════════════════════
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    delta = len(df) - len(df_raw)
    st.metric(
        "📡 信号样本",
        f"{len(df)}",
        f"{delta:+d}" if delta != 0 else None,
    )

with col2:
    avg_rsrp = df["RSRP_dBm"].mean()
    st.metric(
        "⚡ 平均 RSRP",
        f"{avg_rsrp:.1f} dBm",
        f"{avg_rsrp - df_raw['RSRP_dBm'].mean():+.1f}" if len(df) > 0 else None,
    )

with col3:
    avg_dl = df["Download_Mbps"].mean()
    st.metric(
        "🚀 平均速率",
        f"{avg_dl:.0f} Mbps",
    )

with col4:
    cells = df["CellID"].nunique()
    st.metric(
        "🏢 覆盖小区",
        f"{cells}",
    )

with col5:
    peak_dl = df["Download_Mbps"].max() if len(df) > 0 else 0
    st.metric(
        "💎 峰值速率",
        f"{peak_dl:.0f} Mbps",
    )

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 地图 — 主视觉区
# ═══════════════════════════════════════════════════════════════
st.markdown('<div class="glow-box">', unsafe_allow_html=True)

map_title = "🗺️ 信号覆盖地图"
if "2D" in map_mode:
    map_title += " · 霓虹散点"
elif "3D" in map_mode:
    map_title += " · 赛博城市"
else:
    map_title += " · 热力覆盖"

st.subheader(map_title)

if df.empty:
    st.warning("⚠️ 当前筛选条件下无数据，请调整侧边栏参数")
else:
    map_df = df[["Latitude", "Longitude", "RSRP_dBm", "Download_Mbps", "CellID", "Band", "SINR_dB"]].copy()
    map_df["color"] = map_df["RSRP_dBm"].apply(rsrp_neon_color)
    map_df["elevation"] = map_df["Download_Mbps"] * col_height_scale

    center_lat = map_df["Latitude"].mean()
    center_lon = map_df["Longitude"].mean()

    # Tooltip 模板
    tooltip_html = """
        <div style="background:rgba(10,10,30,0.95); color:#fff; padding:12px; border-radius:8px; 
                    border:1px solid #00ffff; font-family:monospace;">
            <b style="color:#00ffff;">📡 小区 {CellID}</b><br/>
            频段: <span style="color:#ff00ff;">{Band}</span><br/>
            RSRP: <span style="color:#00ff88;">{RSRP_dBm} dBm</span><br/>
            SINR: {SINR_dB} dB<br/>
            速率: <span style="color:#ff8800;">{Download_Mbps} Mbps</span>
        </div>
    """

    layers = []

    if "2D" in map_mode:
        # 2D 霓虹散点 + 光晕效果
        layers.append(pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["Longitude", "Latitude"],
            get_fill_color="color",
            get_radius=80,
            pickable=True,
            auto_highlight=True,
            radius_min_pixels=4,
            radius_max_pixels=20,
            opacity=0.9,
        ))
        # 外层光晕（更大更透明的点）
        layers.append(pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["Longitude", "Latitude"],
            get_fill_color="color",
            get_radius=200,
            pickable=False,
            radius_min_pixels=20,
            radius_max_pixels=60,
            opacity=0.15,
            visible=True,
        ))

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=12,
            pitch=0,
            bearing=0,
        )

    elif "3D" in map_mode:
        # 3D 赛博城市 — 柱状图层
        layers.append(pdk.Layer(
            "ColumnLayer",
            data=map_df,
            get_position=["Longitude", "Latitude"],
            get_elevation="elevation",
            elevation_scale=1,
            radius=50,
            get_fill_color="color",
            pickable=True,
            auto_highlight=True,
            extruded=True,
            coverage=0.8,
            opacity=0.85,
        ))
        # 天面光点
        layers.append(pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["Longitude", "Latitude"],
            get_fill_color=[0, 255, 255],
            get_radius=30,
            pickable=False,
            radius_min_pixels=2,
            radius_max_pixels=8,
            opacity=0.6,
            # 让它浮在柱子顶部
            get_elevation="elevation",
        ))

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=12,
            pitch=pitch_angle,
            bearing=15,
        )

    else:
        # 热力覆盖 — Heatmap + 散点叠加
        layers.append(pdk.Layer(
            "HeatmapLayer",
            data=map_df,
            get_position=["Longitude", "Latitude"],
            get_weight="Download_Mbps",
            aggregation="MEAN",
            radius_pixels=60,
            intensity=3,
            threshold=0.05,
            color_range=[
                [0, 0, 0, 0],
                [0, 0, 255, 180],
                [0, 255, 255, 200],
                [0, 255, 0, 200],
                [255, 255, 0, 200],
                [255, 0, 255, 220],
            ],
        ))
        # 覆盖散点
        map_df["scatter_color"] = map_df["RSRP_dBm"].apply(rsrp_neon_color)
        layers.append(pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position=["Longitude", "Latitude"],
            get_fill_color="scatter_color",
            get_radius=50,
            pickable=True,
            auto_highlight=True,
            radius_min_pixels=3,
            radius_max_pixels=12,
            opacity=0.75,
        ))

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=12,
            pitch=0,
            bearing=0,
        )

    deck = pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        tooltip={"html": tooltip_html, "style": {"color": "white"}},
        map_provider="carto",
        map_style="dark_no_labels",
    )

    st.pydeck_chart(deck, width='stretch')

    # 图例
    st.markdown("""
    <div style="display:flex; gap:16px; margin-top:8px; font-size:0.85rem; flex-wrap:wrap;">
        <span><span style="color:#00ffff;">●</span> RSRP > -85 (极强)</span>
        <span><span style="color:#00ff88;">●</span> -85 ~ -95 (强)</span>
        <span><span style="color:#ffc832;">●</span> -95 ~ -105 (中)</span>
        <span><span style="color:#ff8800;">●</span> -105 ~ -115 (弱)</span>
        <span><span style="color:#ff3755;">●</span> RSRP < -115 (极弱)</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# 数据分析图表
# ═══════════════════════════════════════════════════════════════
st.subheader("📊 信号分析仪表")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # 各频段信号强度分布 — 小提琴 + 箱线
    st.markdown("#### 📶 各频段 RSRP 分布")
    
    fig = go.Figure()
    
    neon_colors_go = {
        "n28": "rgba(0,255,255,0.7)",
        "n41": "rgba(255,0,255,0.7)",
        "n78": "rgba(0,255,136,0.7)",
    }
    border_colors = {
        "n28": "#00ffff",
        "n41": "#ff00ff",
        "n78": "#00ff88",
    }
    
    for band in sorted(df["Band"].unique()):
        band_data = df[df["Band"] == band]["RSRP_dBm"]
        fig.add_trace(go.Violin(
            y=band_data,
            name=band,
            box_visible=True,
            meanline_visible=True,
            fillcolor=neon_colors_go.get(band, "rgba(255,255,255,0.3)"),
            line_color=border_colors.get(band, "#fff"),
            opacity=0.8,
            points="outliers",
            marker=dict(
                color=border_colors.get(band, "#fff"),
                size=3,
                opacity=0.6,
            ),
        ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ccc"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color="#ccc"),
        ),
    )
    fig.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False, title="RSRP (dBm)")
    
    st.plotly_chart(fig, width='stretch', config={"displayModeBar": False})

with chart_col2:
    # 终端类型分布 — 炫酷环形图
    st.markdown("#### 📱 终端类型 & 频段占比")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        # 终端类型 环形图
        term_counts = df["TerminalType"].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=term_counts.index,
            values=term_counts.values,
            hole=0.6,
            marker=dict(
                colors=["#00ffff", "#ff00ff", "#00ff88"],
                line=dict(color="#0a0a1a", width=2),
            ),
            textinfo="percent",
            textfont=dict(color="#fff", size=12),
            hovertemplate="<b>%{label}</b><br>数量: %{value}<br>占比: %{percent}<extra></extra>",
        ))
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=30, b=0),
            height=250,
            title=dict(text="终端类型", font=dict(color="#ccc", size=12)),
            showlegend=True,
            legend=dict(font=dict(color="#ccc", size=10)),
        )
        st.plotly_chart(fig2, width='stretch', config={"displayModeBar": False})
    
    with col_b:
        # 频段分布 环形图
        band_counts = df["Band"].value_counts()
        fig3 = go.Figure(go.Pie(
            labels=band_counts.index,
            values=band_counts.values,
            hole=0.6,
            marker=dict(
                colors=["#00ffff", "#ff00ff", "#00ff88"],
                line=dict(color="#0a0a1a", width=2),
            ),
            textinfo="percent",
            textfont=dict(color="#fff", size=12),
            hovertemplate="<b>%{label}</b><br>数量: %{value}<br>占比: %{percent}<extra></extra>",
        ))
        fig3.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=30, b=0),
            height=250,
            title=dict(text="频段分布", font=dict(color="#ccc", size=12)),
            showlegend=True,
            legend=dict(font=dict(color="#ccc", size=10)),
        )
        st.plotly_chart(fig3, width='stretch', config={"displayModeBar": False})

# ═══════════════════════════════════════════════════════════════
# 第二行图表
# ═══════════════════════════════════════════════════════════════
chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    # SINR vs RSRP 散点 — 信号质量矩阵
    st.markdown("#### 🎯 RSRP vs SINR 信号质量矩阵")
    
    fig4 = px.scatter(
        df,
        x="RSRP_dBm",
        y="SINR_dB",
        color="Band",
        size="Download_Mbps",
        hover_data=["CellID", "TerminalType"],
        color_discrete_map={
            "n28": "#00ffff",
            "n41": "#ff00ff",
            "n78": "#00ff88",
        },
        opacity=0.7,
    )
    fig4.update_traces(
        marker=dict(
            line=dict(width=1, color="#0a0a1a"),
        ),
    )
    fig4.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ccc"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            font=dict(color="#ccc"),
        ),
    )
    fig4.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False, title="RSRP (dBm)")
    fig4.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False, title="SINR (dB)")
    
    # 添加参考区域
    fig4.add_hline(y=15, line_dash="dash", line_color="rgba(0,255,136,0.3)", 
                   annotation_text="优质 SINR ≥15", annotation_position="top right",
                   annotation_font=dict(color="#00ff88", size=10))
    fig4.add_vline(x=-90, line_dash="dash", line_color="rgba(0,255,255,0.3)",
                   annotation_text="强 RSRP > -90", annotation_position="top",
                   annotation_font=dict(color="#00ffff", size=10))
    
    st.plotly_chart(fig4, width='stretch', config={"displayModeBar": False})

with chart_col4:
    # 下载速率分布 — 炫酷直方图
    st.markdown("#### 🚀 下载速率分布")
    
    fig5 = go.Figure()
    
    for band in sorted(df["Band"].unique()):
        band_data = df[df["Band"] == band]["Download_Mbps"]
        fig5.add_trace(go.Histogram(
            x=band_data,
            name=band,
            nbinsx=30,
            marker=dict(
                color=neon_colors_go.get(band, "rgba(255,255,255,0.3)"),
                line=dict(color=border_colors.get(band, "#fff"), width=1),
            ),
            opacity=0.7,
            histnorm="probability",
        ))
    
    fig5.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ccc"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=350,
        barmode="overlay",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            font=dict(color="#ccc"),
        ),
    )
    fig5.update_xaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False, title="Download (Mbps)")
    fig5.update_yaxes(gridcolor="rgba(255,255,255,0.05)", zeroline=False, title="概率密度")
    
    st.plotly_chart(fig5, width='stretch', config={"displayModeBar": False})

# ═══════════════════════════════════════════════════════════════
# 数据表格
# ═══════════════════════════════════════════════════════════════
with st.expander("📋 数据浏览器"):
    col_filter = st.text_input("🔍 搜索 CellID", placeholder="输入小区ID...")
    display_df = df
    if col_filter:
        display_df = df[df["CellID"].astype(str).str.contains(col_filter, case=False)]
    st.dataframe(display_df, width='stretch', height=300)
    
    if st.button("💾 导出筛选数据 (CSV)"):
        csv = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="点击下载",
            data=csv,
            file_name=f"5g_signal_nexus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

# ═══════════════════════════════════════════════════════════════
# 页脚
# ═══════════════════════════════════════════════════════════════
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center; padding:20px;">
    <div style="color:#ff00ff; font-size:1.2rem; margin-bottom:5px;">
        📡 5G SIGNAL NEXUS · CYBERPUNK EDITION
    </div>
    <div style="color:#444; font-size:0.8rem;">
        Code with AI 海选赛 · OpenClaw Agent · DeepSeek V4 Pro<br/>
        Data: signal_samples.csv · {len(df_raw)} samples · Shanghai 5G
    </div>
    <div style="color:#222; font-size:0.7rem; margin-top:8px;">
        ⚡ Rendered at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    </div>
</div>
""", unsafe_allow_html=True)
