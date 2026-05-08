# 🤖 AI 交互日志 (AI_PROMPTS.md)

> **Code with AI 海选赛 — 5G 信号可视化看板**
> 使用 AI：DeepSeek V4 Flash (通过 OpenClaw CLI)
> 构建方式：端到端 AI 编码，无手工代码输入

---

## 会话记录

### Step 1: 理解需求与数据探索

**Human:**
> 这是 BESA 2026 Code with AI 海选赛的题目，请帮我完成。
> 仓库地址：https://github.com/besa-2026/code-with-ai-contest

**AI:**
首先获取仓库信息，了解赛题要求和数据结构：

- 比赛要求构建 5G 信号可视化看板，使用 Streamlit + pydeck
- 数据为 `data/signal_samples.csv`，包含 500 条上海地区 5G 路测数据
- 包括字段：Latitude, Longitude, CellID, Band, RSRP_dBm, SINR_dB, TerminalType, Download_Mbps
- 需要完成基础关卡（数据加载、散点地图、概览图表）和进阶关卡（侧边栏筛选、3D 地图、工程化）

**数据探索结果：**
```
总行数: 500
频段分布: n28=164, n78=161, n41=175
终端类型: Smartphone=148, CPE=184, IoT=168
RSRP 范围: -119.9 ~ -70.0 dBm
下载速率: 13.1 ~ 998.8 Mbps
```

---

### Step 2: 构建核心 app.py

**Human:**
> 请构建完整的 app.py，包含以下功能：

**AI 构建策略：**

1. **数据加载** — pandas 读取 CSV，带缓存装饰器
2. **2D 散点地图** — pydeck ScatterplotLayer，RSRP 颜色映射（绿> -90, 黄-90~-110, 红< -110）
3. **3D 柱状图** — pydeck ColumnLayer，柱高随下载速率变化
4. **数据概览** — bar_chart（频段分布）+ matplotlib pie chart（终端类型占比）
5. **侧边栏联动筛选** — multiselect 频段、slider RSRP 范围、multiselect 终端类型
6. **地图模式切换** — radio button 切换 2D/3D

**关键代码：**

```python
# 颜色映射函数
def rsrp_color(rsrp):
    if rsrp > -90: return "#00cc66"  # 绿 - 强信号
    elif rsrp >= -110: return "#ffcc00"  # 黄 - 中信号
    else: return "#ff3333"  # 红 - 弱信号
```

---

### Step 3: 补全工程化要求

**Human:**
> 请添加完整的类型注释、文档字符串，并编写单元测试覆盖所有核心功能

**AI 添加了：**
- `load_data()` 函数 — 类型注释 + docstring
- `rsrp_color()` / `rsrp_color_rgb()` — 颜色映射文档
- `filter_data()` — 筛选逻辑
- `tests/test_app.py` — 包含 4 个测试类、15 个测试用例
  - `TestDataLoading` — 数据加载正确性
  - `TestRSRPColor` — 颜色边界条件
  - `TestFilterData` — 筛选逻辑（组合条件、空集、全集）
  - `TestDataIntegrity` — 数据质量验证

---

### Step 4: 编写 README + AI_PROMPTS

**Human:**
> 请生成 README.md 和 AI_PROMPTS.md

**AI:**
生成完整的项目文档，包括功能说明、运行方法、数据结构说明、项目结构等。

---

## 使用的 AI 工具链

| 工具 | 用途 |
|------|------|
| DeepSeek V4 Flash | 主要编码与推理引擎 |
| OpenClaw CLI | AI Coding Agent 框架 |
| Streamlit | Web 应用框架 |
| pydeck | 地图可视化 |
| pandas | 数据处理 |
| unittest | 测试框架 |

## 构建时间线

| 阶段 | 时间 | 说明 |
|------|------|------|
| 需求分析 | ~3 min | 读取赛题说明，数据探索 |
| 核心编码 | ~5 min | app.py 构建 |
| 测试编写 | ~3 min | 单元测试 |
| 文档完善 | ~3 min | README + AI_PROMPTS |

**总计：约 14 分钟**（纯 AI 驱动，无需手工编写一行代码）
