import streamlit as st
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. 页面配置 & 视觉风格
# ==========================================
st.set_page_config(page_title="企业市场实验室", page_icon="🏭", layout="wide")

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
    
    /* 绿色主题头部 */
    .card-header {
        color: #064e3b;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 15px;
        border-left: 5px solid #10b981; 
        padding-left: 12px;
    }

    .page-banner {
        background: linear-gradient(135deg, #065f46 0%, #10b981 100%);
        color: white;
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .metric-value { font-size: 32px; font-weight: 800; color: #059669; }
    .metric-label { font-size: 16px; color: #64748b; font-weight: 500; }
    
    p, li, .stMarkdown { font-size: 16px !important; line-height: 1.6 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-banner">
    <div>
        <div style="font-size: 24px; font-weight: 800;">🏭 企业市场实验室 <span style="font-size:18px; opacity:0.8; font-weight:400;">(Market Lab)</span></div>
    </div>
    <div style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 14px;">
    </div>
</div>
""", unsafe_allow_html=True)

# 算法
def calc_derived_demand(capital, tech_type, prod_price):
    w = np.linspace(5, 100, 100)
    tech_factor = 1.5 if tech_type == "劳动互补型" else (0.6 if tech_type == "劳动替代型" else 1.0)
    demand = (prod_price * capital * tech_factor * 10) / w
    return w, demand

with st.sidebar:
    st.header("🎛️ 企业决策控制")
    with st.expander("🏭 生产要素 (Ch3)", expanded=True):
        capital = st.slider("资本存量 (K)", 10, 100, 50)
        prod_price = st.slider("产品价格指数 (P)", 1.0, 5.0, 2.0)
        tech_type = st.selectbox("技术进步类型", ["中性技术", "劳动替代型", "劳动互补型"])
    with st.expander("💰 薪酬激励 (Ch8)", expanded=True):
        pay_mode = st.radio("薪酬制度设计", ["计时工资", "计件工资", "效率工资"])

# --- 模块：派生需求 ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">📉 希克斯-马歇尔派生需求仿真</div>', unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])
w, d = calc_derived_demand(capital, tech_type, prod_price)

with col1:
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=d, y=w, name="劳动需求 D", line=dict(color='#10b981', width=4)))
    fig1.update_layout(xaxis_title="雇佣人数 (L)", yaxis_title="工资率 (W)", template="plotly_white", height=450, margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("##### 📊 关键参数")
    st.markdown(f"<div class='metric-label'>资本存量</div><div class='metric-value'>{capital}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-label'>技术类型</div>", unsafe_allow_html=True)
    
    if tech_type == "劳动替代型":
        st.error("📉 **预警**\n\n机器正在替代人工，需求曲线左移。")
    elif tech_type == "劳动互补型":
        st.success("📈 **繁荣**\n\n技术进步增加了劳动的边际产出。")
    else:
        st.info("⚖️ **平稳**\n\n技术对劳动需求无显著偏向。")

st.markdown('</div>', unsafe_allow_html=True)

# --- 模块：薪酬 ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">💰 薪酬激励制度设计</div>', unsafe_allow_html=True)
if pay_mode == "效率工资":
    st.info("### 📘 知识点：效率工资 (Efficiency Wage)")
    st.write("企业支付高于市场出清水平的工资，目的是减少员工偷懒（Solow Condition）和降低流失率。")
else:
    st.write(f"当前选择：**{pay_mode}**。这种模式下，工资通常等于劳动的边际产品价值 (W = VMP)。")
st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 4. 实验报告生成模块 (新增)
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">📝 实验报告生成</div>', unsafe_allow_html=True)

report_text = f"""
# 企业决策仿真实验报告
**实验时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**学生姓名**: ___________

## 一、 生产要素配置
- **资本存量**: {capital} 单位
- **产品价格**: {prod_price} 指数
- **技术类型**: {tech_type}

## 二、 实验结果分析
### 1. 派生需求分析
实验显示，{f'由于采用了{tech_type}，企业的劳动需求曲线显著外移，表明该技术与劳动呈互补关系。' if tech_type == '劳动互补型' else f'由于采用了{tech_type}，机器对劳动产生了明显的替代效应，需求收缩。' if tech_type == '劳动替代型' else '技术进步呈现中性特征，未对劳动需求产生偏向性影响。'}

### 2. 薪酬制度设计
当前选择的薪酬模式为 **{pay_mode}**。
{ '效率工资有助于解决信息不对称下的激励问题，但增加了企业的显性薪酬成本。' if pay_mode == '效率工资' else '计时/计件工资更依赖于企业的监督成本或产出可观测性。'}

## 三、 实验结论
本次仿真验证了希克斯-马歇尔派生需求定理，证明了技术进步的方向是影响劳动力需求弹性的关键变量。
"""

st.text_area("报告预览 (Markdown)", report_text, height=200)
st.download_button(
    label="📥 下载实验报告 (.md)",
    data=report_text,
    file_name=f"Market_Lab_Report_{datetime.now().strftime('%Y%m%d')}.md",
    mime="text/markdown",
    type="primary"
)
st.markdown('</div>', unsafe_allow_html=True)
