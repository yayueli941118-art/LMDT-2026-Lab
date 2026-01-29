import streamlit as st
from PIL import Image

# ==========================================
# 1. 门户配置
# ==========================================
st.set_page_config(
    page_title="LMDT - 黎雅月老师教学平台",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. 视觉重构引擎 (解决字小、空、丑的问题)
# ==========================================
st.markdown("""
<style>
    /* --- 字体与全局布局优化 --- */
    html, body, [class*="css"] {
        font-family: 'Microsoft YaHei', 'Heiti SC', sans-serif !important; /* 强制使用微软雅黑 */
        color: #0f172a;
    }
    
    /* 解决"页面空白太多"：强制减少顶部留白 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important; /* 让内容撑满屏幕宽度的95% */
    }

    /* 解决"字太小"：全局字号放大 */
    p, .stMarkdown, li {
        font-size: 18px !important; /* 正文从16px提到18px */
        line-height: 1.7 !important;
    }
    
    /* 标题大加粗 */
    h1 { font-size: 42px !important; font-weight: 900 !important; color: #1e3a8a !important; letter-spacing: 2px; }
    h2 { font-size: 32px !important; font-weight: 800 !important; color: #1e40af !important; border-left: 8px solid #3b82f6; padding-left: 15px; }
    h3 { font-size: 24px !important; font-weight: 700 !important; }

    /* --- 专属署名 Header --- */
    .school-banner {
        background: linear-gradient(120deg, #1e3a8a 0%, #2563eb 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }
    .school-name { font-size: 22px; opacity: 0.9; font-weight: 400; letter-spacing: 1px; }
    .system-title { font-size: 48px; font-weight: 900; margin: 10px 0; letter-spacing: 2px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .author-badge { 
        background-color: rgba(255,255,255,0.2); 
        padding: 8px 15px; 
        border-radius: 50px; 
        font-size: 16px; 
        border: 1px solid rgba(255,255,255,0.4);
    }

    /* --- 卡片样式优化 --- */
    .nav-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
        height: 100%;
    }
    .nav-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08);
        transform: translateY(-5px);
    }
    .card-icon { font-size: 40px; margin-bottom: 15px; display: block; }
    .card-title { font-size: 24px; font-weight: 800; color: #1e3a8a; display: block; margin-bottom: 10px; }
    .card-desc { font-size: 16px; color: #64748b; margin-bottom: 15px; }
    .card-tag { 
        display: inline-block; 
        background: #eff6ff; 
        color: #2563eb; 
        padding: 4px 10px; 
        border-radius: 4px; 
        font-size: 14px; 
        font-weight: bold; 
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 专属定制 Banner (解决署名问题)
# ==========================================
st.markdown("""
<div class="school-banner">
    <div>
        <div class="school-name">🏛️ 西南交通大学希望学院 · 商学院</div>
        <div class="system-title">劳动力市场数字孪生实验平台</div>
        <div style="font-size: 20px; font-weight: 600; margin-top:10px;">
            Designed for: <span style="border-bottom: 2px solid #fbbf24;">人力资源管理专业 (HRM)</span>
        </div>
    </div>
    <div style="text-align: right;">
        <div class="author-badge">👩‍🏫 课程负责人：黎雅月</div>
        <div style="margin-top:10px; font-size:14px; opacity:0.8;">第七届全国高校教师技能创新大赛参赛作品</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 4. 核心导航区 (解决内容空洞问题)
# ==========================================

st.markdown("## 📍 请选择实验模块")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="nav-card">
        <span class="card-icon">👤</span>
        <span class="card-title">个体职业实验室</span>
        <p class="card-desc">
            模拟劳动者从求学、求职到流动的全生命周期。探索<b>人力资本投资</b>回报与<b>职业流动</b>决策。
        </p>
        <div style="margin-top:20px;">
            <span class="card-tag">第1/2章 供给</span>
            <span class="card-tag">第5章 人力资本</span>
            <span class="card-tag">第6章 流动</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="nav-card">
        <span class="card-icon">🏭</span>
        <span class="card-title">企业市场实验室</span>
        <p class="card-desc">
            扮演企业管理者，进行<b>生产要素配置</b>与<b>薪酬制度设计</b>。体验派生需求与效率工资理论。
        </p>
        <div style="margin-top:20px;">
            <span class="card-tag">第3章 需求</span>
            <span class="card-tag">第4章 均衡</span>
            <span class="card-tag">第8章 薪酬</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="nav-card">
        <span class="card-icon">🌍</span>
        <span class="card-title">宏观政策实验室</span>
        <p class="card-desc">
            扮演政府决策者，应对<b>AI技术冲击</b>，诊断<b>结构性失业</b>，并制定宏观干预政策。
        </p>
        <div style="margin-top:20px;">
            <span class="card-tag">第9章 失业</span>
            <span class="card-tag">AI 冲击</span>
            <span class="card-tag">政策沙盘</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# 5. 底部教学理念 (增加页面厚度)
# ==========================================
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 20px;">
    <h4>🎓 教学理念：Data-Driven Learning (DDL)</h4>
    <p>本平台旨在通过<b>数字孪生技术</b>，将抽象的经济学模型转化为可视化、可交互的实验场景。</p>
    <p>让 HR 专业的学生从“死记硬背公式”转向“理解市场逻辑”，培养数据洞察力与决策思维。</p>
</div>
""", unsafe_allow_html=True)

# 侧边栏补充信息
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/teacher.png", width=80)
    st.markdown("### 👩‍🏫 课程负责人：黎雅月")
    st.info("**西南交通大学希望学院**\n\n人力资源管理专业核心课\n《劳动经济学》教学团队")
    
    st.divider()
    st.markdown("#### 📌 实验进度")
    st.progress(0, text="当前处于：门户首页")