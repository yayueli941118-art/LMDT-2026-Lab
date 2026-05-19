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
    
    .metric-value { font-size: 30px; font-weight: 800; color: #7c3aed; }
    .metric-label { font-size: 14px; color: #64748b; font-weight: 500; }
    
    p, li, .stMarkdown { font-size: 16px !important; line-height: 1.6 !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-banner">
    <div>
        <div style="font-size: 24px; font-weight: 800;">🌍 宏观政策实验室 <span style="font-size:18px; opacity:0.8; font-weight:400;">(Macro Lab)</span></div>
    </div>
    <div style="background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 14px;">
        《劳动经济学》数字孪生专属教具
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 2. 核心实验算法重构 (精确拟合教案数值)
# ==========================================
def calculate_uv_simulation(mismatch, min_wage, ubi, reskilling):
    """
    此算法精确拟合了教案中的数值轨迹：
    - 初始态(θ=0.2): U=3.1%, V=2.9%  (此时 φ ≈ 9.0)
    - 恶化态(θ=0.8): U=7.8%, V=5.15% (此时 φ ≈ 40.17)
    - 尝试A(+15%): U=8.1% (沿曲线移动)
    - 尝试B(+25%): φ 变大，曲线进一步外移
    - 尝试C(π=0.8): U=4.3%, V=3.5% (此时 φ ≈ 15.05，曲线回归)
    """
    # 1. 基础匹配效率常数 φ (通过 θ 线性映射)
    phi_base = 9.0 + 51.95 * (mismatch - 0.2)
    phi_base = max(1.0, phi_base)
    
    # 基础失业率 U_nom (通过 θ 线性映射)
    u_nom = 3.1 + 7.833 * (mismatch - 0.2)
    u_nom = max(0.5, u_nom)
    
    # 2. 引入尝试 B 效应 (失业救济金增加，导致保留工资上升，匹配效率 φ 变差)
    phi_final = phi_base + (ubi - 40) / 25.0 * 10.0
    
    # 3. 引入尝试 C 效应 (技能重塑补贴，抵消错配，匹配效率 φ 变好，U 降低)
    phi_final = phi_final - (reskilling / 0.8) * 25.12
    phi_final = max(4.0, phi_final)
    
    u_final = u_nom - (reskilling / 0.8) * 3.5
    u_final = max(1.0, u_final)
    
    # 4. 引入尝试 A 效应 (最低工资增加，需求收缩，沿曲线移动，U 上升)
    u_actual = u_final + (min_wage / 15.0) * 0.3
    v_actual = phi_final / u_actual
    
    # 生成整条 UV 曲线的数据点
    u_axis = np.linspace(0.5, 20, 200)
    v_axis = phi_final / u_axis
    
    return u_axis, v_axis, u_actual, v_actual, phi_final

# 生成前一次实验的基准浅色参考线（初始态 θ=0.2）
ref_u_axis, ref_v_axis, _, _, _ = calculate_uv_simulation(0.2, 0, 40, 0)

# ==========================================
# 3. 侧边栏：宏观驾驶舱
# ==========================================
with st.sidebar:
    st.header("🌍 宏观驾驶舱")
    
    st.subheader("⚠️ 风险监测：AI 技术冲击")
    # 默认为0.8，直接呈现案例中的"恶化状态"，或者由老师在课堂上从0.2拖至0.8
    mismatch = st.slider("技能错配度 (θ)", 0.0, 2.0, 0.8, step=0.1) 
    
    st.divider()
    
    st.subheader("🏛️ 政策工具箱")
    st.markdown("**尝试 A：提高最低工资**")
    min_wage_change = st.slider("最低工资标准上调 (%)", 0, 30, 0, step=5)
    
    st.markdown("**尝试 B：提高失业救济**")
    ubi_rate = st.slider("失业救济替代率 (%)", 40, 80, 40, step=5) 
    
    st.markdown("**尝试 C：技能重塑补贴**")
    reskilling_subsidy = st.slider("政策干预参数 (π)", 0.0, 1.0, 0.0, step=0.1)

# ==========================================
# 4. 核心高光环节：数字孪生实验推演
# ==========================================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<div class="card-header">🧬 结构性失业诊断沙盘 (Beveridge Curve)</div>', unsafe_allow_html=True)

# 核心计算
u, v, cur_u, cur_v, cur_phi = calculate_uv_simulation(mismatch, min_wage_change, ubi_rate, reskilling_subsidy)

col1, col2 = st.columns([2.5, 1.5])

with col1:
    fig1 = go.Figure()
    
    # 1. 轨迹叠加：浅色参考线 (对应教案"系统保留前一次实验的UV曲线为浅色参考线")
    fig1.add_trace(go.Scatter(x=ref_u_axis, y=ref_v_axis, name="初始态参考线 (θ=0.2)", line=dict(color='#cbd5e1', dash='solid', width=2)))
    
    # 2. 当前调参后的仿真曲线 (实色叠加)
    fig1.add_trace(go.Scatter(x=u, y=v, name="当前仿真演化曲线", line=dict(color='#8b5cf6', width=4)))
    
    # 3. 当前市场均衡点 (红色圆点)
    fig1.add_trace(go.Scatter(
        x=[cur_u], y=[cur_v], 
        mode='markers+text', 
        name='当前市场均衡点',
        marker=dict(color='#ef4444', size=14, line=dict(color='white', width=2)),
        text=[f"U:{cur_u:.1f}%, V:{cur_v:.2f}%"], 
        textposition="top right"
    ))
    
    # 动态视觉交互：复刻教案中的视觉轨迹提示
    if reskilling_subsidy >= 0.8:
        fig1.add_annotation(
            x=6, y=8,
            text="供给侧干预生效：UV 曲线向左下方回归原点",
            showarrow=True, arrowhead=2, arrowcolor="#22c55e",
            ax=30, ay=-40, font=dict(color="#22c55e", size=13)
        )
    elif mismatch >= 0.8:
        fig1.add_annotation(
            x=10, y=12,
            text="UV 曲线向右上方显著外移 (对比浅色轨迹)",
            showarrow=True, arrowhead=2, arrowcolor="#ef4444",
            ax=40, ay=-30, font=dict(color="#ef4444", size=13)
        )

    fig1.update_layout(
        xaxis_title="失业率 U (%)", 
        yaxis_title="岗位空缺率 V (%)", 
        template="plotly_white", 
        height=450, 
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(range=[0, 15]),
        yaxis=dict(range=[0, 15]),
        legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99)
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("##### 📊 实时量化面板")
    # 完美对齐教案：“同步刷新 U、V、φ 的具体数值”
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='metric-label'>失业率 (U)</div><div class='metric-value'>{cur_u:.1f}%</div>", unsafe_allow_html=True)
    with c2:
        st.markdown(f"<div class='metric-label'>空缺率 (V)</div><div class='metric-value' style='color:#f59e0b;'>{cur_v:.2f}%</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='metric-label'>匹配效率 (φ)</div><div class='metric-value' style='color:#3b82f6;'>{cur_phi:.2f}</div>", unsafe_allow_html=True)
    
    st.markdown("<hr style='margin:15px 0;'>", unsafe_allow_html=True)
    
    st.markdown("##### 🚨 诊断与系统评语")
    # 完全还原教案中设定的 100% 精确文本
    if min_wage_change >= 15 and reskilling_subsidy < 0.1:
        st.error("**【尝试 A】政策受挫**\n\n企业雇佣成本上升，劳动力需求曲线左移，登记失业率不降反升至 8.1%。\n\n**系统评语**：需求侧干预失效——提高价格下限无法解决技能错配的结构性问题。")
    elif ubi_rate >= 65 and reskilling_subsidy < 0.1:
        st.warning("**【尝试 B】政策受挫**\n\n保留工资上升，失业者求职强度下降，贝弗里奇曲线进一步外移。\n\n**系统评语**：纯需求侧补贴产生逆向激励——失业者等待更长时间才接受工作邀约。")
    elif reskilling_subsidy >= 0.8:
        st.success("**【尝试 C】政策成功**\n\n随着 π 值上升，匹配效率函数 φ 中政策效应逐渐抵消错配度的负面影响，UV 曲线开始向左下方回归原点。\n\n**系统评语**：供给侧结构性改革奏效——通过降低有效错配度，恢复市场匹配效率。")
    elif mismatch >= 0.8:
        st.error("**【状态诊断】高空缺与高失业并存**\n\n**系统预警文字**：诊断为典型的结构性失业——高空缺与高失业并存。")
    else:
        st.info("智能驾驶舱提示：请调节技能错配度模拟 AI 冲击，并测试市长政策沙盘的反事实反馈。")

st.markdown('</div>', unsafe_allow_html=True)
