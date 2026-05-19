import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. 页面配置 & 视觉风格
# ==========================================
st.set_page_config(page_title="宏观政策实验室", page_icon="🌍", layout="wide")

st.markdown("""
<style>
    html, body, [class*="css"] { font-family: 'Microsoft YaHei', sans-serif !important; background-color: #f1f5f9; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 5rem !important; max-width: 98% !important; }
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }
    
    .card-header {
        color: #581c87;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        border-left: 5px solid #8b5cf6;
        padding-left: 12px;
    }

    .page-banner {
        background: linear-gradient(135deg, #4c1d95 0%, #8b5cf6 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .metric-value { font-size: 32px; font-weight: 800; color: #7c3aed; }
    .metric-label { font-size: 16px; color: #64748b; font-weight: 500; }
    
    p, li, .stMarkdown { font-size: 16px !important; line-height: 1.6 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-banner">
    <div>
        <div style="font-size: 24px; font-weight: 800;">🌍 宏观政策实验室 <span style="font-size:18px; opacity:0.8; font-weight:400;">(Macro Lab)</span></div>
    </div>
    <div style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 14px;">
        教学方案配套系统
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心实验算法重构 (内嵌案例因果链)
# ==========================================
def calc_beveridge_core(ai_risk, mismatch, min_wage_change, ubi_rate, reskilling_subsidy):
    u_axis = np.linspace(0.5, 20, 200) # 生成失业率自变量轴
    
    # 基础匹配效率常数 k0 = 20 
    # 尝试 B 的陷阱：提高失业救济金会降低求职强度，使匹配效率恶化，曲线向右上方外移
    ubi_effect = max(0, (ubi_rate - 40) * 0.8) 
    
    # 尝试 C 的正解：供给侧技能重塑补贴（干预参数π），直接消减AI冲击和技能错配
    policy_effect = reskilling_subsidy * 0.7 
    
    # 动态计算曲线匹配常数 K = f(mismatch, ai_risk, ubi, reskilling)
    k = 20 + (mismatch * 50) + (ai_risk * 0.6) + ubi_effect - (policy_effect * 100)
    k = max(5, k) # 约束下限
    
    # 计算当前政策环境下的基础空缺率 V
    v_axis = k / u_axis
    
    # 尝试 A 的陷阱：提高最低工资导致劳动需求沿 D 曲线收缩 
    # 模型表现为：当前市场均衡点在 UV 曲线向右下方滑动（失业率上升，空缺率下降）
    base_u = np.sqrt(k) # 当前市场自然均衡失业率
    
    # 最低工资每上升1%，失业率增加，空缺率沿曲线下降
    wage_shock = min_wage_change * 0.1
    current_u = base_u + wage_shock
    current_v = k / current_u
    
    return u_axis, v_axis, current_u, current_v

# ==========================================
# 3. 侧边栏：宏观驾驶舱
# ==========================================
with st.sidebar:
    st.header("🌍 宏观驾驶舱")
    
    st.subheader("⚠️ 风险监测")
    ai_risk = st.slider("AI 替代冲击 (%)", 0, 100, 40) # 对应案例设定：40%高风险 
    mismatch = st.slider("技能错配度 (θ)", 0.0, 2.0, 1.8) # 对应案例设定：1.8严重错配 
    
    st.divider()
    
    st.subheader("🏛️ 政策工具箱")
    st.markdown("**尝试 A：需求侧价格干预**")
    min_wage_change = st.slider("最低工资调整幅度 (%)", 0, 30, 0, step=5)
    
    st.markdown("**尝试 B：需求侧收入转移**")
    ubi_rate = st.slider("失业救济替代率 (%)", 40, 90, 40, step=5) # 基期为40% 
    
    st.markdown("**尝试 C：供给侧结构性改革**")
    reskilling_subsidy = st.slider("技能重塑补贴力度 (π)", 0.0, 1.0, 0.0, step=0.1)

# ==========================================
# 4. 核心高光环节：数字孪生实验推演
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">🧬 结构性失业诊断沙盘 (Beveridge Curve)</div>', unsafe_allow_html=True)

# 调用算法计算当前状态与基期状态
u, v, cur_u, cur_v = calc_beveridge_core(ai_risk, mismatch, min_wage_change, ubi_rate, reskilling_subsidy)
u_ideal, v_ideal, _, _ = calc_beveridge_core(0, 0, 0, 40, 0) # 理想状态

col1, col2 = st.columns([3, 1])

with col1:
    fig1 = go.Figure()
    
    # 1. 理想高效市场曲线（灰色虚线）
    fig1.add_trace(go.Scatter(x=u_ideal, y=v_ideal, name="理想高效市场", line=dict(color='#cbd5e1', dash='dot', width=2)))
    
    # 2. 当前调参后的仿真曲线（紫色实线）
    fig1.add_trace(go.Scatter(x=u, y=v, name="当前仿真演化曲线", line=dict(color='#8b5cf6', width=4)))
    
    # 3. 当前市场均衡点（红色定位核心）
    fig1.add_trace(go.Scatter(
        x=[cur_u], y=[cur_v], 
        mode='markers+text', 
        name='当前市场均衡点',
        marker=dict(color='#ef4444', size=14, line=dict(color='white', width=2)),
        text=[f"U:{cur_u:.1f}%, V:{cur_v:.1f}%"], # 已修复报错
        textposition="top right"
    ))
    
   # 动态视觉交互：当曲线因 AI 或 救济金 外移时，增加色块或标注 
    if ai_risk >= 40 or ubi_rate > 40:
        fig1.add_annotation(
            x=12, y=18,
            text="技术冲击/保留工资上升导致曲线外移（匹配效率恶化）",
            showarrow=True, arrowhead=2, arrowcolor="#ef4444", # 修改为 arrowcolor
            ax=40, ay=-30, font=dict(color="#ef4444", size=12)
        )
    if reskilling_subsidy > 0.4:
        fig1.add_annotation(
            x=4, y=6,
            text="供给侧干预生效：曲线向原点回归",
            showarrow=True, arrowhead=2, arrowcolor="#22c55e", # 修改为 arrowcolor
            ax=-30, ay=40, font=dict(color="#22c55e", size=12)
        )
    if reskilling_subsidy > 0.4:
        fig1.add_annotation(
            x=4, y=6,
            text="供给侧干预生效：曲线向原点回归",
            showarrow=True, arrowhead=2, arrowcolor="#22c55e", # 修改为 arrowcolor
            ax=-30, ay=40, font=dict(color="#22c55e", size=12)
        )
    if reskilling_subsidy > 0.4:
        fig1.add_annotation(
            x=4, y=6,
            text="供给侧干预生效：曲线向原点回归",
            showarrow=True, arrowhead=2, color="green",
            ax=-30, ay=40, font=dict(color="#22c55e", size=12)
        )

    fig1.update_layout(
        xaxis_title="失业 rate U (%)", 
        yaxis_title="岗位空缺 rate V (%)", 
        template="plotly_white", 
        height=500, 
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(range=[0, 22]),
        yaxis=dict(range=[0, 30]),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("##### 📊 沙盘实时量化指标")
    st.markdown(f"<div class='metric-label'>当前测算失业率 (U)</div><div class='metric-value'>{cur_u:.2f}%</div>", unsafe_allow_html=True) # 已修复报错
    st.markdown(f"<div class='metric-label'>当前岗位空缺率 (V)</div><div class='metric-value' style='color:#f59e0b;'>{cur_v:.2f}%</div>", unsafe_allow_html=True) # 已修复报错
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("##### 🚨 决策树即时诊断")
    # 完全还原案例中的 3 阶段认知冲突文案
    if min_wage_change >= 15 and reskilling_subsidy == 0:
        st.error("**尝试 A 反馈：**\n\n登记失业率不降反升！需求侧干预失效——提高价格下限无法解决技能错配的结构性问题。")
    elif ubi_rate >= 65 and reskilling_subsidy == 0:
        st.warning("**尝试 B 反馈：**\n\n贝弗里奇曲线进一步外移！纯需求侧补贴产生逆向激励——失业者等待更长时间才接受工作邀约（道德风险）。")
    elif reskilling_subsidy >= 0.6:
        st.success("**尝试 C 反馈：**\n\n供给侧结构性改革奏效！实施技能重塑补贴，曲线回归高效区间，匹配效率恢复。")
    else:
        st.info("智能驾驶舱提示：请依次在左侧测试尝试A、B价格补贴，并观察市长政策沙盘的反事实反馈。")

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 5. 动态生成：政策组合拳模拟报告
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">📝 政策决策链条诊断分析</div>', unsafe_allow_html=True)

# 动态捕捉学生的学习路径，并给予学术文献级评语
col_a, col_b, col_c = st.columns(3)

with col_a:
    st.markdown("项目 **尝试 A**（最低工资调整）")
    if min_wage_change > 0:
        st.caption(f"当前调增: +{min_wage_change}%")
        st.write("❌ **政策受挫**：保障了在职低收入者权益，但引发希克斯-马歇尔派生需求收缩。高技能错配下强行提高价格下限，直接挤出边缘低技能劳动力。")
    else:
        st.text("未激活此工具")

with col_b:
    st.markdown("项目 **尝试 B**（失业救济转移）")
    if ubi_rate > 40:
        st.caption(f"当前水平: {ubi_rate}% (基期40%)")
        st.write("❌ **政策受挫**：提供了短暂的社会兜底安全网，但拉高了市场“保留工资”。供给侧无新技能生成时，纯资金补贴加剧了劳动力市场道德风险。")
    else:
        st.text("未激活此工具")

with col_c:
    st.markdown("项目 **尝试 C**（技能重塑补贴）")
    if reskilling_subsidy > 0:
        st.caption(f"当前干预系数 π: {reskilling_subsidy}")
        st.write("🎯 **根本破解方案**：从供给侧直接干预市场匹配机制。通过财政补贴激活Reskilling，让旧技能劳动者适配AI时代新空缺，恢复系统本质均衡。")
    else:
        st.text("未激活此工具")

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. 自动化闭环：OBE 成果报告一键生成 
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">📥 自动化生成《宏观经济诊断报告》 (OBE 导向)</div>', unsafe_allow_html=True)

# 智能化合成Markdown文本
report_text = f"""# 《AI冲击下的结构性失业诊断与政策处方》
**实验时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**课程名称**: 劳动经济学 (第九章《结构性失业与宏观政策诊断》)
**系统运行 ID**: exp_macro_{datetime.now().strftime('%Y%m%d_%H%M%S')}

## 一、 宏观风险监测与仿真设定
- **AI 替代冲击 (Input Risk)**: {ai_risk}%
- **技能错配指数 (θ)**: {mismatch}

## 二、 反事实推理与决策链路记录
1. **需求侧价格冲击 (尝试 A)**: 最低工资变动了 **+{min_wage_change}%**。
   *结果反馈*: 均衡失业率移至 **{cur_u:.1f}%**。验证了单纯提高工资不仅无法解除技能错配，还会导致用工需求收缩。
2. **需求侧收入转移 (尝试 B)**: 失业救济替代率调至 **{ubi_rate}%**。
   *结果反馈*: 贝弗里奇曲线匹配常数发生变动。证明了过高的福利转移支付会产生逆向激励，引发道德风险。
3. **供给侧结构性改革 (尝试 C)**: 技能重塑补贴力度设定为 **{reskilling_subsidy}**。
   *结果反馈*: 匹配效率函数 $\phi(\theta, \pi)$ 得到修正，有效平移曲线回归高效区间。

## 三、 教师评阅标准与经济学结论
面对生成式 AI 技术浪潮对传统劳动力市场的解构，单纯的需求侧救济或行政限价（发钱、提薪）无法根治“高失业与高空缺并存”的结构性痼疾。政府宏观调控的唯一解是建立面向产业未来的技能重塑体系（Reskilling），通过向供给侧注入资源恢复劳动力市场的长期匹配效率。
"""

st.text_area("Markdown 报告底稿实时预览", report_text, height=220)
st.download_button(
    label="📥 一键导出并生成学术实验报告 (.md)",
    data=report_text,
    file_name=f"Macro_Lab_Report_{datetime.now().strftime('%Y%m%d')}.md",
    mime="text/markdown",
    type="primary"
)
st.markdown('</div>', unsafe_allow_html=True)

