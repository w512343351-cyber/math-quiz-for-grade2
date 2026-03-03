# -*- coding: utf-8 -*-
import streamlit as st
import random
from datetime import datetime

# -------------------------------
# ページ設定（かわいいアイコンとタイトル）
st.set_page_config(
    page_title="わくわく算数ランド", 
    page_icon="🧸", 
    layout="wide"
)

# -------------------------------
# カスタムCSSでフォントや色を一気にポップに！
st.markdown("""
<style>
    /* 全体のフォントを丸くてかわいく */
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Comic Neue', cursive;
    }
    /* タイトルを虹色に */
    .rainbow-title {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    /* サブタイトル */
    .sub-title {
        font-size: 1.5rem;
        color: #ff9f43;
        text-align: center;
        margin-top: 0;
    }
    /* サイドバーを明るく */
    .css-1d391kg {
        background-color: #fff9e6;
    }
    /* ボタンをポップに */
    .stButton > button {
        background-color: #ff9ff3;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 50px;
        border: 3px solid #f368e0;
        padding: 0.5rem 2rem;
        box-shadow: 0 5px 0 #b13a9b;
        transition: 0.1s;
    }
    .stButton > button:hover {
        transform: translateY(3px);
        box-shadow: 0 2px 0 #b13a9b;
    }
    /* 問題カード */
    .question-card {
        background-color: #fff3e6;
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 10px solid #ff9ff3;
        font-size: 1.3rem;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    /* 答えカード */
    .answer-card {
        background-color: #e3f0ff;
        border-radius: 20px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 10px solid #48dbfb;
        font-size: 1.3rem;
    }
    /* フッター */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# ヘッダー部分（かわいい絵文字いっぱい）
st.markdown('<p class="rainbow-title">🧸 わくわく算数ランド 🎈</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ あそびながらさんすうにちょうせん！ ✨</p>', unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# サイドバー（カラフルな設定パネル）
with st.sidebar:
    st.markdown("## 🎮 ゲームせってい")
    st.markdown("---")
    
    # 問題数（スライダーを星で飾る）
    num_questions = st.slider(
        "⭐ もんだいすう", 
        min_value=1, max_value=30, value=10,
        help="いくつもんだいをとくかえらんでね"
    )
    
    st.markdown("---")
    st.markdown("### 🧮 どんなけいさん？")
    
    # カラフルなチェックボックス
    col1, col2 = st.columns(2)
    with col1:
        calc_addition = st.checkbox("➕ たしざん", value=True)
        calc_multiplication = st.checkbox("✖️ かけざん", value=True)
        calc_length = st.checkbox("📏 ながさ", value=False)
    with col2:
        calc_subtraction = st.checkbox("➖ ひきざん", value=True)
        calc_compare = st.checkbox("⚖️ くらべっこ", value=False)
        calc_time = st.checkbox("⏰ とけい", value=False)
    
    st.markdown("---")
    st.markdown("### 🎯 むずかしさ")
    
    # 難易度を動物で表現
    difficulty = st.radio(
        "レベルをえらんでね",
        options=["🐣 かんたん", "🐼 ふつう", "🦁 むずかしい"],
        index=1,
        horizontal=True
    )
    # 選択内容をコード内で使いやすい形に変換
    if difficulty == "🐣 かんたん":
        diff_level = "1桁のみ"
    elif difficulty == "🐼 ふつう":
        diff_level = "2桁（繰り上がり・繰り下がりなし）"
    else:
        diff_level = "2桁（あり）"
    
    st.markdown("---")
    # 答え表示スイッチ（かわいいトグル）
    show_answers = st.toggle("✨ こたえをみる", value=True)
    
    st.markdown("---")
    st.markdown("💡 **つかいかた**: ボタンをおすとしゅつだい！")

# -------------------------------
# 問題生成関数（前回と同じ内容）
def generate_question(types, difficulty):
    q_type = random.choice(types)
    
    # 足し算
    if q_type == "addition":
        if difficulty == "1桁のみ":
            a = random.randint(1, 9)
            b = random.randint(1, 9)
        elif difficulty == "2桁（繰り上がり・繰り下がりなし）":
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            while (a // 10 + b // 10) >= 10:
                a = random.randint(10, 99)
                b = random.randint(10, 99)
        else:
            a = random.randint(10, 99)
            b = random.randint(10, 99)
        return f"{a} + {b} = ?", str(a + b)
    
    # 引き算
    elif q_type == "subtraction":
        if difficulty == "1桁のみ":
            a = random.randint(1, 9)
            b = random.randint(1, a)
        elif difficulty == "2桁（繰り上がり・繰り下がりなし）":
            a = random.randint(10, 99)
            b_ten = random.randint(0, a // 10)
            b_unit = random.randint(0, a % 10)
            b = b_ten * 10 + b_unit
        else:
            a = random.randint(10, 99)
            b = random.randint(1, a)
        return f"{a} - {b} = ?", str(a - b)
    
    # 掛け算
    elif q_type == "multiplication":
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        return f"{a} × {b} = ?", str(a * b)
    
    # 比較
    elif q_type == "compare":
        a = random.randint(1, 100)
        b = random.randint(1, 100)
        if random.choice([True, False]) and a == b:
            b = a + random.choice([-1, 1]) if a > 1 else a + 1
        op = random.choice([">", "<", "="])
        if op == ">":
            if a <= b:
                a, b = b + 1, b
        elif op == "<":
            if a >= b:
                a, b = b - 1, b
        else:
            b = a
        return f"{a} □ {b} （にあてはまる記号 >, <, = を答えましょう）", op
    
    # 長さ
    elif q_type == "length":
        if random.choice([True, False]):
            meters = random.randint(1, 5)
            return f"{meters} m = □ cm", str(meters * 100)
        else:
            cm = random.choice([100, 200, 300, 400, 500, 600, 700, 800, 900])
            return f"{cm} cm = □ m", str(cm // 100) if cm % 100 == 0 else f"{cm/100:.1f}"
    
    # 時間
    elif q_type == "time":
        hour = random.randint(1, 12)
        minute = random.choice([0, 15, 30, 45])
        return f"時計の針が {hour} 時 {minute} 分をさしています。時刻は？", f"{hour}時{minute}分"

# -------------------------------
# 問題リスト生成
def generate_worksheet():
    selected_types = []
    if calc_addition:
        selected_types.append("addition")
    if calc_subtraction:
        selected_types.append("subtraction")
    if calc_multiplication:
        selected_types.append("multiplication")
    if calc_compare:
        selected_types.append("compare")
    if calc_length:
        selected_types.append("length")
    if calc_time:
        selected_types.append("time")
    
    if not selected_types:
        st.warning("⚠️ 1つ以上のけいさんをえらんでね！")
        return [], []
    
    questions, answers = [], []
    for _ in range(int(num_questions)):
        q, a = generate_question(selected_types, diff_level)
        questions.append(q)
        answers.append(a)
    return questions, answers

# -------------------------------
# メインエリア：生成ボタン（どーんと大きく）
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🎲 もんだいをつくる！ 🎲"):
        questions, answers = generate_worksheet()
        if questions:
            st.session_state["questions"] = questions
            st.session_state["answers"] = answers
            st.balloons()  # バルーンでお祝い！
    st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------
# 問題表示エリア
if "questions" in st.session_state and st.session_state["questions"]:
    st.markdown("---")
    st.markdown("## 📚 きょうのもんだい")
    
    # 問題をカード形式で表示
    for i, q in enumerate(st.session_state["questions"], 1):
        st.markdown(f'<div class="question-card">🔹 {i}. {q}</div>', unsafe_allow_html=True)
    
    # 答え表示
    if show_answers:
        st.markdown("## 🔍 こたえあわせ")
        for i, a in enumerate(st.session_state["answers"], 1):
            st.markdown(f'<div class="answer-card">✅ {i}. {a}</div>', unsafe_allow_html=True)
    
    # ダウンロードボタン（かわいく）
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        text_content = "【わくわく算数ランド】\n\n"
        for i, q in enumerate(st.session_state["questions"], 1):
            text_content += f"{i}. {q}\n"
        if show_answers:
            text_content += "\n【こたえ】\n"
            for i, a in enumerate(st.session_state["answers"], 1):
                text_content += f"{i}. {a}\n"
        
        st.download_button(
            label="📥 プリントにほぞん",
            data=text_content,
            file_name=f"wakuwaku_math_{datetime.now().strftime('%Y%m%d')}.txt",
            mime="text/plain"
        )
else:
    # 初期表示（かわいいイラスト風）
    st.markdown("## 🎈 はじめよう！")
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
        ### ようこそ！
        
        🌟 **わくわく算数ランド**へようこそ！  
        おんなじ　ほうほうで　さんすうの　れんしゅうが　できるよ。
        
        1. 👈 ひだりの　サイドバーで　もんだいの　しゅるいを　えらんでね
        2. 🎲 「もんだいをつくる！」ボタンを　ぽちっ！
        3. 📝 もんだいを　といて　こたえあわせ
        
        さあ、たのしく　べんきょうしよう！
        """)
        st.markdown("---")
        st.markdown("🎉 **それでは、レッツ　チャレンジ！**")

# -------------------------------
# フッター
st.markdown("---")
st.markdown("""
<div class="footer">
    🧸 わくわく算数ランド | まいにちあそんでさんすうマスター！<br>
    © 2025 げんきっず
</div>
""", unsafe_allow_html=True)