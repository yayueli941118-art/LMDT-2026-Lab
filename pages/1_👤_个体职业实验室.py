import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. 页面配置 & 视觉风格
# ==========================================
st.set_page_config(page_title="个体职业实验室", page_icon="👤", layout="wide")

st.markdown("""
<style>
    /* 全局字体与布局 */
    html, body, [class*="css"] { font-family: 'Microsoft YaHei', sans-serif !important; background-color: #f1f5f9; }
    .block-container { padding-top: 3.5rem !important; padding-bottom: 5rem !important; max-width: 98% !important; }
    
    /* 隐藏默认头部 */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* 卡片式容器 */
    .card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s;
    }
    .card:hover { transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    
    /* 蓝色主题头部 */
    .card-header {
        color: #1e3a8a;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        border-left: 5px solid #3b82f6;
        padding-left: 12px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* 顶部 Banner */
    .page-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .metric-value { font-size: 32px; font-weight: 800; color: #2563eb; }
    .metric-label { font-size: 16px; color: #64748b; font-weight: 500; }
    
    p, li, .stMarkdown { font-size: 16px !important; line-height: 1.6 !important; }
</style>
""", unsafe_allow_html=True)

# 顶部 Banner
st.markdown("""
<div class="page-banner">
    <div>
        <div style="font-size: 24px; font-weight: 800;">👤 个体职业发展实验室 <span style="font-size:18px; opacity:0.8; font-weight:400;">(Micro Lab)</span></div>
        <div style="font-size: 16px; margin-top:5px; opacity:0.9;">西南交通大学希望学院 · 人力资源管理专业</div>
    </div>
    <div style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 14px;">
        👩‍🏫 课程负责人：黎雅月
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. 算法引擎
# ==========================================
def calc_mincer(edu, exp, gen_t, spec_t, disc):
    base = 7.0
    r = 0.08 + (0.004 * gen_t) + (0.002 * spec_t)
    ln_w = base + r * edu + 0.05 * exp - 0.0006 * (exp**2)
    wage = np.exp(ln_w)
    wage_disc = wage * (1 - disc/100)
    return wage, wage_disc

def calc_migration_npv(w_home, w_city, cost_move, cost_psych, years=20):
    t = np.arange(1, years+1)
    benefit = (w_city - w_home) * 12
    costs = np.array([cost_move + cost_psych] + [cost_psych]*(years-1))
    net = benefit - costs
    cum_npv = np.cumsum(net / (1.05 ** t))
    return t, cum_npv

# ==========================================
# 3. 控制台与界面
# ==========================================
with st.sidebar:
    st.header("🎛️ 参数控制台")
    with st.expander("🎓 人力资本 (Ch5)", expanded=True):
        edu = st.slider("受教育年限", 9, 22, 16)
        gen_t = st.slider("一般培训投入", 0, 10, 5)
        spec_t = st.slider("特殊培训投入", 0, 10, 3)
    with st.expander("🧭 流动决策 (Ch6)", expanded=False):
        w_diff = st.slider("城乡月薪差 (k)", 1, 30, 8)
        c_move = st.number_input("搬迁成本 (k)", 0, 100, 20)
        c_psych = st.slider("心理成本 (k/年)", 0, 50, 10)
    with st.expander("⚖️ 歧视系数 (Ch7)", expanded=False):
        disc = st.slider("市场歧视程度 (%)", 0, 40, 15)

# --- 模块一：职业画像 ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">💎 模块一：职业生涯工资画像 (Wage-Age Profile)</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
exp_vec = np.linspace(0, 40, 100)
w_base, _ = calc_mincer(12, exp_vec, 0, 0, 0) # 基准
w_exp, w_disc = calc_mincer(edu, exp_vec, gen_t, spec_t, disc)

with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=exp_vec, y=w_base, name='对照组 (高中)', line=dict(color='#cbd5e1', dash='dash')))
    fig1.add_trace(go.Scatter(x=exp_vec, y=w_exp, name=f'实验组 ({edu}年)', line=dict(color='#3b82f6', width=4)))
    if disc > 0:
        fig1.add_trace(go.Scatter(x=exp_vec, y=w_disc, name='歧视后工资', line=dict(color='#ef4444')))
        fig1.add_trace(go.Scatter(x=exp_vec, y=w_exp, fill='tonexty', fillcolor='rgba(239, 68, 68, 0.1)', line=dict(width=0), showlegend=False))
    
    fig1.update_layout(xaxis_title="工龄 (Year)", yaxis_title="工资指数", template="plotly_white", height=400, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("##### 📊 关键指标")
    st.markdown(f"<div class='metric-label'>起薪预测</div><div class='metric-value'>{w_exp[0]:.1f}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    premium = ((w_exp[20]/w_base[20])-1)*100
    st.markdown(f"<div class='metric-label'>教育溢价</div><div class='metric-value' style='color:{'#10b981' if premium>0 else '#ef4444'}'>+{premium:.1f}%</div>", unsafe_allow_html=True)
    if disc > 0:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-label'>歧视损失</div><div class='metric-value' style='color:#ef4444'>-{disc}%</div>", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# --- 模块二：迁移决策 ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">🚀 模块二：劳动力流动回报分析 (Migration NPV)</div>', unsafe_allow_html=True)

col3, col4 = st.columns([3, 1])
years, npv = calc_migration_npv(5, 5+w_diff, c_move, c_psych)
breakeven = np.where(npv > 0)[0]

with col3:
    fig2 = go.Figure(go.Bar(x=years, y=npv, marker_color=['#ef4444' if v<0 else '#10b981' for v in npv]))
    fig2.update_layout(xaxis_title="年份", yaxis_title="累计净收益 (k)", template="plotly_white", height=350, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

with col4:
    st.markdown("##### 💡 决策建议")
    if len(breakeven) > 0:
        st.success(f"✅ **值得迁移**\n\n预计在第 **{breakeven[0]+1}** 年收回成本并开始盈利。")
    else:
        st.error("❌ **不值得迁移**\n\n心理成本过高，长期收益无法覆盖成本。")

st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. 实验报告生成模块 (新增)
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">📝 实验报告生成</div>', unsafe_allow_html=True)

report_text = f"""
# 个体职业发展仿真实验报告
**实验时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**学生姓名**: ___________

## 一、 实验参数设定
- **受教育年限**: {edu} 年
- **培训投入**: 一般培训 ({gen_t}) / 特殊培训 ({spec_t})
- **流动决策**: 城乡工资差 {w_diff}k, 搬迁成本 {c_move}k, 心理成本 {c_psych}k

## 二、 实验结果分析
### 1. 人力资本回报
根据明瑟收入方程模拟，在当前教育投入下，预计职业中期的教育溢价率为 **{premium:.1f}%**。
{f'同时，由于市场存在 **{disc}%** 的歧视系数，导致了显著的非生产率工资差异。' if disc > 0 else '市场环境公平，无显著歧视损失。'}

### 2. 劳动力流动决策
基于净现值(NPV)模型计算，{f'迁移是理性的选择，预计在第 **{breakeven[0]+1}** 年实现盈亏平衡。' if len(breakeven) > 0 else '迁移是非理性的，因为高昂的心理成本或搬迁成本导致长期净收益为负。'}

## 三、 实验结论
通过本次数字孪生仿真，验证了教育投资的边际递减规律以及心理成本对劳动力流动的阻碍作用。
"""

st.text_area("报告预览 (Markdown)", report_text, height=200)
st.download_button(
    label="📥 下载实验报告 (.md)",
    data=report_text,
    file_name=f"Micro_Lab_Report_{datetime.now().strftime('%Y%m%d')}.md",
    mime="text/markdown",
    type="primary"
)
st.markdown('</div>', unsafe_allow_html=True)
