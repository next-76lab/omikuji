import streamlit as st
import streamlit.components.v1 as components
import random
import time
import urllib.parse

# ========================================
# 2026年 新春おみくじアプリ (Streamlit版)
# ========================================

# ページ設定
st.set_page_config(
    page_title="🎍 2026年 新春おみくじ 🎍",
    page_icon="🐴",
    layout="centered"
)

# 共通CSS (スマホ対応メディアクエリを追加)
COMMON_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700;900&family=Zen+Maru+Gothic:wght@400;700&display=swap');

    :root {
        --gold: #D4AF37;
        --gold-light: #F5E6A3;
        --crimson: #C41E3A;
        --sakura: #FFB7C5;
        --midnight: #0a0a1a;
        --white: #fefefe;
        --x-color: #000000;
    }

    body {
        margin: 0;
        padding: 0;
        font-family: 'Zen Maru Gothic', sans-serif;
        background: transparent;
        color: white;
        overflow: hidden; /* iframe内でのスクロールを抑制 */
    }

    .result-card {
        background: rgba(30, 20, 50, 0.85);
        border: 2px solid var(--gold);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.2);
        margin: 5px;
    }

    .fortune-main {
        font-family: 'Noto Serif JP', serif;
        font-size: 3rem;
        font-weight: 900;
        margin: 0.2rem 0;
    }

    .daikichi { color: #FFD700; text-shadow: 0 0 20px rgba(255, 215, 0, 0.5); }
    .chuukichi { color: #FF8C00; }
    .kichi { color: #32CD32; }
    .shoukichi { color: #87CEEB; }
    .suekichi { color: #DDA0DD; }
    .kyou { color: #DC143C; }

    .detail-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 15px;
    }

    .detail-item {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 10px;
    }

    .detail-label {
        color: var(--gold);
        font-size: 0.8rem;
        margin-bottom: 2px;
    }

    .detail-stars {
        color: var(--gold-light);
        font-size: 1rem;
        letter-spacing: 1px;
    }

    .lucky-title {
        color: var(--sakura);
        font-size: 0.9rem;
        margin: 20px 0 10px 0;
        border-top: 1px solid rgba(212, 175, 55, 0.3);
        padding-top: 15px;
    }

    .lucky-flex {
        display: flex;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
    }

    .lucky-tag {
        background: rgba(212, 175, 55, 0.2);
        color: var(--gold-light);
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        border: 1px solid var(--gold);
    }

    /* 共有ボタンセクション */
    .share-container {
        margin-top: 25px;
    }

    .share-button {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: var(--x-color);
        color: white;
        text-decoration: none;
        padding: 10px 20px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.85rem;
        border: 1px solid rgba(255, 255, 255, 0.3);
        transition: all 0.3s ease;
    }

    .share-button:hover {
        background: #333;
        transform: translateY(-2px);
    }

    /* スマホ対応メディアクエリ */
    @media (max-width: 600px) {
        .fortune-main { font-size: 2.5rem; }
        .result-card { padding: 1.2rem 1rem; }
        .detail-grid { grid-template-columns: 1fr; gap: 8px; }
        .lucky-tag { font-size: 0.7rem; }
        p { font-size: 0.9rem !important; }
    }
</style>
"""

# Streamlit上のスタイル設定（背景など）
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a1a 0%, #1a0a2e 50%, #1a0520 100%) !important;
    }
    .title-text {
        font-family: 'Noto Serif JP', serif;
        font-size: 2.2rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #D4AF37 0%, #F5E6A3 50%, #D4AF37 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 10px rgba(212, 175, 55, 0.3));
    }
    .subtitle-text {
        color: #FFB7C5;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 1.2rem;
    }
    .year-badge {
        text-align: center;
        background: linear-gradient(135deg, #C41E3A, #8B0000);
        color: #F5E6A3;
        padding: 0.4rem 1.2rem;
        border-radius: 30px;
        font-weight: 700;
        width: fit-content;
        margin: 0 auto 1.5rem auto;
    }
    
    @media (max-width: 600px) {
        .title-text { font-size: 1.6rem; }
        .subtitle-text { font-size: 0.85rem; }
    }
</style>
""", unsafe_allow_html=True)

# データの定義
fortunes = [
    {"type": "大吉", "class": "daikichi", "msg": "最高の運勢です！2026年は天に昇る馬のように、何物もスピーディーに成就します。", "prob": 15},
    {"type": "中吉", "class": "chuukichi", "msg": "素晴らしい運勢です。周囲との連携を深めることで、より高みに到達できるでしょう。", "prob": 25},
    {"type": "吉", "class": "kichi", "msg": "良い運勢です。着実な一歩が大きな成果につながります。自信を持って進んでください。", "prob": 30},
    {"type": "小吉", "class": "shoukichi", "msg": "まずまずの運勢です。目先の利益にとらわれず、長期的な視点で行動すると吉です。", "prob": 20},
    {"type": "末吉", "class": "suekichi", "msg": "これからの運勢です。焦らず準備を整えることで、後半に大きなチャンスが訪れます。", "prob": 10},
]

categories = ["💕 恋愛運", "💼 仕事運", "🏃 健康運", "💰 金運", "📚 学業運", "✈️ 旅行運"]
lucky_items_pool = ["赤い手帳", "銀のブックマーク", "森林の香り", "新しいスニーカー", "クリスタルの置物", "ミントタブレット", "お守り", "特製お餅"]

# 初期化
if 'drawn' not in st.session_state:
    st.session_state.drawn = False
if 'result' not in st.session_state:
    st.session_state.result = None

# ヘッダー表示
st.markdown('<div class="title-text">🎍 新春おみくじ 🎍</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">今年の運勢を占いましょう</div>', unsafe_allow_html=True)
st.markdown('<div class="year-badge">🐴 2026年 午年 🐴</div>', unsafe_allow_html=True)

# メインコンテンツ
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if not st.session_state.drawn:
        st.write("")
        st.info("心を落ち着けてボタンを押してください")
        if st.button("🎋 おみくじを引く 🎋", use_container_width=True):
            with st.spinner('運勢を引き寄せています...'):
                time.sleep(1.2)
                st.session_state.result = random.choices(fortunes, weights=[f['prob'] for f in fortunes])[0]
                st.session_state.drawn = True
                st.rerun()
    else:
        res = st.session_state.result
        
        if res['type'] == "大吉":
            st.balloons()
            st.toast("おめでとうございます！大吉です！")
        
        # HTML 構築
        detail_items_list = []
        for cat in categories:
            sc = random.randint(3, 5)
            stars = "★" * sc + "☆" * (5 - sc)
            detail_items_list.append(f'<div class="detail-item"><div class="detail-label">{cat}</div><div class="detail-stars">{stars}</div></div>')
        detail_items_html = "".join(detail_items_list)

        lucky_tag_list = [
            f'<div class="lucky-tag">{random.choice(lucky_items_pool)}</div>',
            f'<div class="lucky-tag">カラー: {random.choice(["金", "赤", "白", "紫"])}</div>',
            f'<div class="lucky-tag">数字: {random.randint(1, 99)}</div>'
        ]
        lucky_tags_html = "".join(lucky_tag_list)

        # SNS共有用URL生成
        share_text = f"2026年のおみくじの結果は【{res['type']}】でした！🐴\\n{res['msg']}\\n#2026年おみくじ #午年"
        share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)

        full_html = f"""
        {COMMON_STYLE}
        <div class="result-card">
            <div class="fortune-main {res['class']}">{res['type']}</div>
            <p style="font-size: 1rem; line-height: 1.5; margin-bottom: 15px; color: white;">{res['msg']}</p>
            
            <div class="detail-grid">
                {detail_items_html}
            </div>
            
            <div class="lucky-title">✨ 今週のラッキーアイテム ✨</div>
            <div class="lucky-flex">
                {lucky_tags_html}
            </div>

            <div class="share-container">
                <a href="{share_url}" target="_top" class="share-button">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                    X で結果を共有する
                </a>
            </div>
        </div>
        """
        
        # iframeの高さを十分に確保し、見切れを防止
        components.html(full_html, height=750, scrolling=True)
        
        if st.button("🔄 もう一度引く", use_container_width=True):
            st.session_state.drawn = False
            st.rerun()

# フッター
st.markdown("""
<div style="text-align: center; color: rgba(255, 255, 255, 0.4); font-size: 0.8rem; margin-top: 3rem;">
    © 2026 新春おみくじ - 爽快に駆け抜けよう 🐴
</div>
""", unsafe_allow_html=True)
