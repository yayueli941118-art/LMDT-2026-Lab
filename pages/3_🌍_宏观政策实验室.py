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
        <div style="font-size: 16px; margin-top:5px; opacity:0.9;">西南交通大学希望学院 · 人力资源管理专业</div>
    </div>
    <div style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 14px;">
        👩‍🏫 课程负责人：黎雅月
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心算法修正：加入 ai_risk 变量
# ==========================================
def calc_beveridge(mismatch, policy_effect, ai_risk):
    u = np.linspace(0.5, 15, 100) # 避免 u=0 的除零错误
    
    # 核心修正逻辑：
    # 基础常数 k = 20
    # mismatch (0-2.0): 结构性错配系数，每增加0.1，k增加5
    # policy_effect (0/1): 政策修正，降低k
    # ai_risk (0-100): AI冲击每增加1%，k增加0.6。当拉到100%时，k增加60，效果非常剧烈！
    
    k = 20 + (mismatch * 50) + (ai_risk * 0.6) - (policy_effect * 15)
    
    v = k / u
    return u, v

with st.sidebar:
    st.header("🌍 宏观驾驶舱")
    st.subheader("⚠️ 风险监测")
    ai_risk = st.slider("AI 替代冲击 (%)", 0, 100, 30)
    mismatch = st.slider("技能错配度", 0.0, 2.0, 0.8)
    st.divider()
    st.subheader("🏛️ 政策工具箱")
    policy = st.multiselect("干预手段", ["最低工资调整", "技能重塑补贴(Reskilling)", "失业救济金"])

# --- 模块：结构性失业 ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">🧬 结构性失业诊断 (Beveridge Curve)</div>', unsafe_allow_html=True)

# 计算逻辑
policy_score = 1.0 if "技能重塑补贴(Reskilling)" in policy else 0

# 修正：调用函数时传入 ai_risk
u, v = calc_beveridge(mismatch, policy_score, ai_risk)
u_base, v_base = calc_beveridge(0, 0, 0) # 理想状态：无错配，无AI冲击

col1, col2 = st.columns([3, 1])
with col1:
    fig1 = go.Figure()
    # 理想曲线
    fig1.add_trace(go.Scatter(x=u_base, y=v_base, name="理想高效市场", line=dict(color='#cbd5e1', dash='dot')))
    # 当前曲线
    fig1.add_trace(go.Scatter(x=u, y=v, name="当前市场状态", line=dict(color='#8b5cf6', width=5)))
    
    # 增加一个注释，当 AI 冲击很高时显示
    if ai_risk > 80:
        fig1.add_annotation(
            x=8, y=20,
            text="AI 冲击导致剧烈外移",
            showarrow=True,
            arrowhead=1,
            ax=0, ay=-40,
            font=dict(color="red", size=14)
        )

    fig1.update_layout(
        xaxis_title="失业率 U (%)", 
        yaxis_title="职位空缺率 V (%)", 
        template="plotly_white", 
        height=450, 
        margin=dict(l=20, r=20, t=20, b=20),
        yaxis=dict(range=[0, 30]) # 固定Y轴范围，让位移看起来更明显
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("##### 📊 诊断结果")
    st.markdown(f"<div class='metric-label'>AI 冲击指数</div><div class='metric-value' style='color:{'#ef4444' if ai_risk > 50 else '#7c3aed'}'>{ai_risk}%</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 动态文案修正
    if ai_risk > 70:
        st.error(f"🚨 **极度危险**\n\nAI 技术大规模替代人工，贝弗里奇曲线显著外移，市场匹配效率崩塌。")
    elif mismatch > 1.0:
        st.warning("⚠️ **结构性失业**\n\n高失业与高空缺并存。")
    else:
        st.success("✅ **运行良好**\n\n市场主要为摩擦性失业。")
    
    if "技能重塑补贴(Reskilling)" in policy:
        st.info("✅ **政策生效**\n\n补贴降低了错配，曲线尝试回正。")

st.markdown('</div>', unsafe_allow_html=True)

# --- 模块：政策组合报告 ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">📝 政策组合拳模拟报告</div>', unsafe_allow_html=True)
if not policy:
    st.warning("当前未实施任何干预政策，市场处于自然演化状态。")
else:
    for p in policy:
        if p == "最低工资调整":
            st.write(f"- **{p}**：保障了低收入者权益，但可能导致低技能劳动力需求沿 D 曲线收缩。")
        elif p == "技能重塑补贴(Reskilling)":
            st.write(f"- **{p}**：降低了结构性错配，是应对 AI 冲击最有效的长期手段。")
        elif p == "失业救济金":
            st.write(f"- **{p}**：提供了社会安全网，但过高可能增加“保留工资”，降低就业意愿。")
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. 实验报告生成模块
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">📝 实验报告生成</div>', unsafe_allow_html=True)

report_text = f"""
# 宏观政策仿真实验报告
**实验时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**学生姓名**: ___________

## 一、 宏观风险监测
- **AI 替代冲击**: {ai_risk}%
- **技能错配指数**: {mismatch}

## 二、 实验结果分析
### 1. 结构性失业诊断
本次实验模拟了 **{ai_risk}%** 的 AI 技术替代冲击。
{ '在极端的 AI 冲击下，贝弗里奇曲线剧烈向右上方移动，表明旧技能劳动者被大规模淘汰，而新岗位招不到人，市场匹配效率严重下降。' if ai_risk > 70 else 'AI 冲击尚在可控范围内，市场通过自然调节维持了相对平衡。'}

### 2. 政策干预效果
本次实验采用了以下政策组合：{', '.join(policy) if policy else '无'}。
{ '技能重塑补贴有效促进了劳动力的技能升级，使贝弗里奇曲线向原点回归，缓解了 AI 带来的结构性冲击。' if '技能重塑补贴(Reskilling)' in policy else '缺乏针对性的培训政策，导致结构性错配难以在短期内自动修复。'}

## 三、 实验结论
本次仿真表明，面对技术冲击引发的结构性失业，单纯的需求侧刺激（如提高工资）效果有限，必须配合供给侧的技能重塑政策。
"""

st.text_area("报告预览 (Markdown)", report_text, height=200)
st.download_button(
    label="📥 下载实验报告 (.md)",
    data=report_text,
    file_name=f"Macro_Lab_Report_{datetime.now().strftime('%Y%m%d')}.md",
    mime="text/markdown",
    type="primary"
)
st.markdown('</div>', unsafe_allow_html=True)
