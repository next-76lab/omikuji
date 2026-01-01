import streamlit as st
import streamlit.components.v1 as components
import random
import time
import urllib.parse

# ========================================
# 2026年 新春おみくじアプリ (Streamlit版)
# 紅白のお正月デザイン
# ========================================

# ページ設定
st.set_page_config(
    page_title="🎍 2026年 新春おみくじ 🎍",
    page_icon="🐴",
    layout="centered"
)

# 共通CSS (紅白のお正月デザイン - iframeスクロールバー非表示)
COMMON_STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700;900&family=Zen+Maru+Gothic:wght@400;700&display=swap');

    :root {
        --aka: #C41E3A;
        --aka-light: #E04E6A;
        --shiro: #FFFAF0;
        --kin: #D4AF37;
        --kin-light: #F5E6A3;
        --kuro: #2B1B17;
        --midori: #2E8B57;
    }

    * {
        box-sizing: border-box;
    }

    html, body {
        margin: 0;
        padding: 0;
        font-family: 'Zen Maru Gothic', sans-serif;
        background: transparent;
        color: var(--kuro);
        overflow: hidden;
    }

    .result-card {
        background: linear-gradient(180deg, var(--shiro) 0%, #FFF5EE 100%);
        border: 3px solid var(--aka);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(196, 30, 58, 0.15), inset 0 0 60px rgba(212, 175, 55, 0.05);
        margin: 5px;
        position: relative;
        overflow: hidden;
    }

    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M30 0L60 30L30 60L0 30z' fill='none' stroke='%23C41E3A' stroke-opacity='0.05' stroke-width='1'/%3E%3C/svg%3E");
        pointer-events: none;
        opacity: 0.3;
    }

    .fortune-main {
        font-family: 'Noto Serif JP', serif;
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0.5rem 0;
        position: relative;
        z-index: 1;
    }

    .daikichi { color: var(--kin); text-shadow: 2px 2px 4px rgba(0,0,0,0.1), 0 0 20px rgba(212, 175, 55, 0.4); }
    .chuukichi { color: var(--aka); }
    .kichi { color: var(--midori); }
    .shoukichi { color: #4169E1; }
    .suekichi { color: #8B5CF6; }
    .kyou { color: #6B7280; }

    .detail-grid {
        display: grid;
        grid-template-columns: repeat(2, 1fr);
        gap: 10px;
        margin-top: 15px;
        position: relative;
        z-index: 1;
    }

    .detail-item {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,245,238,0.9));
        border: 1px solid rgba(196, 30, 58, 0.2);
        border-radius: 12px;
        padding: 10px 8px;
    }

    .detail-label {
        color: var(--aka);
        font-size: 0.8rem;
        margin-bottom: 2px;
        font-weight: 700;
    }

    .detail-stars {
        color: var(--kin);
        font-size: 0.9rem;
        letter-spacing: 1px;
    }

    .detail-comment {
        color: #555;
        font-size: 0.7rem;
        margin-top: 4px;
        line-height: 1.3;
    }

    .lucky-title {
        color: var(--aka);
        font-size: 0.9rem;
        margin: 20px 0 10px 0;
        border-top: 2px solid var(--aka);
        padding-top: 15px;
        position: relative;
        z-index: 1;
    }

    .lucky-flex {
        display: flex;
        justify-content: center;
        gap: 8px;
        flex-wrap: wrap;
        position: relative;
        z-index: 1;
    }

    .lucky-tag {
        background: linear-gradient(135deg, var(--aka) 0%, var(--aka-light) 100%);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        border: none;
        box-shadow: 0 2px 8px rgba(196, 30, 58, 0.3);
    }

    @media (max-width: 600px) {
        .fortune-main { font-size: 2.8rem; }
        .result-card { padding: 1.2rem 1rem; }
        .detail-grid { grid-template-columns: 1fr; gap: 8px; }
        .lucky-tag { font-size: 0.7rem; }
        p { font-size: 0.9rem !important; }
    }
</style>
"""

# Streamlit上のスタイル設定（紅白の背景）
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+JP:wght@400;700;900&family=Zen+Maru+Gothic:wght@400;700&display=swap');
    
    .stApp {
        background: linear-gradient(180deg, #FFFAF0 0%, #FFF5EE 50%, #FFE4E1 100%) !important;
    }
    
    .title-text {
        font-family: 'Noto Serif JP', serif;
        font-size: 2.5rem;
        font-weight: 900;
        text-align: center;
        color: #C41E3A;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle-text {
        color: #8B4513;
        text-align: center;
        font-size: 1rem;
        margin-bottom: 1.2rem;
        font-family: 'Zen Maru Gothic', sans-serif;
    }
    
    .year-badge {
        text-align: center;
        background: linear-gradient(135deg, #C41E3A 0%, #8B0000 100%);
        color: #F5E6A3;
        padding: 0.5rem 1.5rem;
        border-radius: 30px;
        font-weight: 700;
        width: fit-content;
        margin: 0 auto 1.5rem auto;
        box-shadow: 0 4px 15px rgba(196, 30, 58, 0.3);
        font-family: 'Noto Serif JP', serif;
    }
    
    .decoration {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    /* X共有ボタンのスタイル */
    .share-link {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        background: #000000;
        color: white !important;
        text-decoration: none !important;
        padding: 12px 24px;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        margin-top: 1rem;
    }
    
    .share-link:hover {
        background: #333;
        transform: translateY(-2px);
    }
    
    @media (max-width: 600px) {
        .title-text { font-size: 1.8rem; }
        .subtitle-text { font-size: 0.85rem; }
    }
</style>
""", unsafe_allow_html=True)

# データの定義
fortunes = [
    {"type": "大吉", "class": "daikichi", "msg": "最高の運勢です！2026年は天に昇る馬のように、何事もスピーディーに成就します。", "prob": 15},
    {"type": "中吉", "class": "chuukichi", "msg": "素晴らしい運勢です。周囲との連携を深めることで、より高みに到達できるでしょう。", "prob": 25},
    {"type": "吉", "class": "kichi", "msg": "良い運勢です。着実な一歩が大きな成果につながります。自信を持って進んでください。", "prob": 30},
    {"type": "小吉", "class": "shoukichi", "msg": "まずまずの運勢です。目先の利益にとらわれず、長期的な視点で行動すると吉です。", "prob": 20},
    {"type": "末吉", "class": "suekichi", "msg": "これからの運勢です。焦らず準備を整えることで、後半に大きなチャンスが訪れます。", "prob": 10},
]

# 各運勢カテゴリと一言コメントの定義
category_comments = {
    "💕 恋愛運": [
        "素直な気持ちを伝えて",
        "新しい出会いに期待",
        "パートナーとの時間を大切に",
        "自分磨きが吉",
        "積極的にアプローチを"
    ],
    "💼 仕事運": [
        "チームワークが鍵",
        "新企画にチャレンジ",
        "コツコツ努力が実る",
        "上司への相談が吉",
        "スキルアップの好機"
    ],
    "🏃 健康運": [
        "適度な運動を心がけて",
        "睡眠を十分に",
        "新しい習慣を始めよう",
        "ストレス発散が大切",
        "健康診断を忘れずに"
    ],
    "💰 金運": [
        "堅実な貯蓄が吉",
        "思わぬ臨時収入あり",
        "無駄遣いに注意",
        "投資は慎重に",
        "節約が幸運を呼ぶ"
    ],
    "📚 学業運": [
        "集中力アップの兆し",
        "新しい分野に挑戦",
        "復習が効果的",
        "仲間と学び合って",
        "資格取得に最適"
    ],
    "✈️ 旅行運": [
        "西方面が吉",
        "温泉旅行がおすすめ",
        "思い切って遠出を",
        "近場でリフレッシュ",
        "海外旅行に好機"
    ]
}

categories = list(category_comments.keys())
lucky_items_pool = ["赤い手帳", "銀のブックマーク", "森林の香り", "新しいスニーカー", "クリスタルの置物", "ミントタブレット", "お守り", "特製お餅"]

# 初期化
if 'drawn' not in st.session_state:
    st.session_state.drawn = False
if 'result' not in st.session_state:
    st.session_state.result = None

# 門松装飾
st.markdown('<div class="decoration">🎍🐴🎍</div>', unsafe_allow_html=True)

# ヘッダー表示
st.markdown('<div class="title-text">新春おみくじ</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-text">〜 今年の運勢を占いましょう 〜</div>', unsafe_allow_html=True)
st.markdown('<div class="year-badge">🐴 2026年 午年 🐴</div>', unsafe_allow_html=True)

# メインコンテンツ
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if not st.session_state.drawn:
        st.write("")
        st.info("🙏 心を落ち着けてボタンを押してください 🙏")
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
            st.toast("🎊 おめでとうございます！大吉です！🎊")
        
        # HTML 構築（コメント付き）
        detail_items_list = []
        for cat in categories:
            sc = random.randint(3, 5)
            stars = "★" * sc + "☆" * (5 - sc)
            comment = random.choice(category_comments[cat])
            detail_items_list.append(
                f'<div class="detail-item">'
                f'<div class="detail-label">{cat}</div>'
                f'<div class="detail-stars">{stars}</div>'
                f'<div class="detail-comment">{comment}</div>'
                f'</div>'
            )
        detail_items_html = "".join(detail_items_list)

        lucky_tag_list = [
            f'<div class="lucky-tag">{random.choice(lucky_items_pool)}</div>',
            f'<div class="lucky-tag">カラー: {random.choice(["金", "赤", "白", "紫"])}</div>',
            f'<div class="lucky-tag">数字: {random.randint(1, 99)}</div>'
        ]
        lucky_tags_html = "".join(lucky_tag_list)

        full_html = f"""
        {COMMON_STYLE}
        <div class="result-card">
            <div class="fortune-main {res['class']}">{res['type']}</div>
            <p style="font-size: 1rem; line-height: 1.6; margin-bottom: 15px; color: #2B1B17;">{res['msg']}</p>
            
            <div class="detail-grid">
                {detail_items_html}
            </div>
            
            <div class="lucky-title">✨ 今週のラッキーアイテム ✨</div>
            <div class="lucky-flex">
                {lucky_tags_html}
            </div>
        </div>
        """
        
        # iframeの高さを十分に確保（コメント追加のため高さを増加）
        components.html(full_html, height=850, scrolling=False)
        
        # X共有ボタンをiframe外（Streamlit側）で表示
        share_text = f"2026年のおみくじの結果は【{res['type']}】でした！🐴\n{res['msg']}\n#2026年おみくじ #午年"
        share_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(share_text)
        
        st.markdown(f'''
        <div style="text-align: center; margin-top: 1rem;">
            <a href="{share_url}" target="_blank" class="share-link">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                X で結果を共有する
            </a>
        </div>
        ''', unsafe_allow_html=True)
        
        st.write("")
        if st.button("🔄 もう一度引く", use_container_width=True):
            st.session_state.drawn = False
            st.rerun()

# フッター
st.markdown("""
<div style="text-align: center; color: #8B4513; font-size: 0.8rem; margin-top: 3rem; opacity: 0.7;">
    © 2026 新春おみくじ - 爽快に駆け抜けよう 🐴
</div>
""", unsafe_allow_html=True)
