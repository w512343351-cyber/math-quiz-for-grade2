# -*- coding: utf-8 -*-
import streamlit as st
import random
import math
import re
from datetime import datetime

# -------------------------------
# ページ設定
st.set_page_config(
    page_title="わくわく算数ランド",
    page_icon="🧸",
    layout="wide",
    initial_sidebar_state="auto"
)

# -------------------------------
# カスタムCSS（全面最適化 + モバイル対応）
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Mochiy+Pop+One&display=swap');

    * { box-sizing: border-box; }

    html, body, [class*="css"]  {
        font-family: 'Mochiy Pop One', 'Comic Neue', cursive, sans-serif;
        background-color: #fef9e6;
    }

    .main > .block-container {
        padding: 1rem 1rem 2rem 1rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .rainbow-title {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 0 0 0.2rem 0;
        text-shadow: 2px 2px 0 rgba(0,0,0,0.1);
    }

    .sub-title {
        font-size: 1.2rem;
        color: #ff9f43;
        text-align: center;
        margin-top: 0;
        font-weight: normal;
    }

    /* ボタン全体のスタイル（大きくポップに） */
    .stButton > button {
        background: linear-gradient(145deg, #ff9ff3, #feca57);
        color: white;
        font-size: 2rem !important;
        font-weight: bold;
        border-radius: 60px !important;
        border: 3px solid white;
        padding: 0.3rem 0.1rem !important;
        box-shadow: 0 8px 0 #b13a9b, 0 10px 20px rgba(0,0,0,0.1);
        transition: 0.1s ease;
        width: 100%;
        height: 4rem !important;
        line-height: 1.2 !important;
        letter-spacing: 2px;
    }
    .stButton > button:hover {
        transform: translateY(4px);
        box-shadow: 0 4px 0 #b13a9b, 0 10px 20px rgba(0,0,0,0.1);
    }

    /* 水平方向の列の間隔を縮める（数字キーボードのボタン間隔を狭くする） */
    .row-widget.stHorizontal {
        gap: 3px !important;
        margin-bottom: 5px !important;
        flex-wrap: wrap !important;
    }

    /* モバイル対応：画面幅が600px以下の場合 */
    @media (max-width: 600px) {
        .rainbow-title { font-size: 2.2rem; }
        .sub-title { font-size: 1rem; }
        .stButton > button {
            font-size: 1.5rem !important;
            height: 3.2rem !important;
        }
        .question-box { font-size: 1.5rem; padding: 1rem; }
        .answer-display { font-size: 2rem; padding: 10px; }
        .character-emoji { font-size: 5rem; padding: 15px; }
        .character-name { font-size: 1.8rem; }
        .puzzle-cell { font-size: 2rem; min-width: 60px; min-height: 60px; }
        .collection-box { font-size: 1.2rem; padding: 8px 12px; }
    }

    /* サイドバー */
    .css-1d391kg, .css-12oz5g7 {
        background: linear-gradient(180deg, #fff9e6, #fff2d9);
        border-radius: 30px 0 0 30px;
        padding: 20px 15px;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.8), 0 4px 10px rgba(0,0,0,0.05);
    }

    /* キャラクターカード */
    .character-container {
        background: linear-gradient(135deg, #fff9ef, #ffe6f0);
        border-radius: 50px;
        padding: 20px;
        margin: 20px 0 30px 0;
        border: 5px solid #ffb6c1;
        box-shadow: 0 20px 30px rgba(255, 105, 180, 0.2);
        display: flex;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
        position: relative;
        overflow: hidden;
    }

    .character-container::before {
        content: "✨⭐✨";
        position: absolute;
        top: 10px;
        right: 20px;
        font-size: 2rem;
        opacity: 0.2;
        rotate: 10deg;
    }

    .character-emoji {
        font-size: 7rem;
        background: white;
        border-radius: 50%;
        padding: 20px;
        box-shadow: 0 10px 0 #ffb6c1, 0 15px 30px rgba(0,0,0,0.1);
        display: inline-block;
        line-height: 1;
        animation: bounce 2s infinite;
    }

    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }

    .character-info {
        flex: 1;
        min-width: 200px;
    }

    .character-name {
        font-size: 2.5rem;
        color: #ff1493;
        font-weight: bold;
        margin-bottom: 5px;
        text-shadow: 2px 2px 0 #ffe0f0;
    }

    .character-message {
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 15px;
        background: rgba(255,255,255,0.7);
        padding: 5px 15px;
        border-radius: 30px;
        display: inline-block;
    }

    .exp-bar {
        width: 100%;
        height: 25px;
        background-color: #f0f0f0;
        border-radius: 30px;
        overflow: hidden;
        margin: 10px 0;
        border: 2px solid white;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.1);
    }

    .exp-fill {
        height: 100%;
        background: linear-gradient(90deg, #ffd700, #ffb347);
        transition: width 0.5s;
        border-radius: 30px;
    }

    .level-badge {
        background: linear-gradient(45deg, #ff1493, #ff69b4);
        color: white;
        padding: 8px 20px;
        border-radius: 40px;
        display: inline-block;
        font-size: 1.2rem;
        box-shadow: 0 5px 0 #b13a9b;
    }

    .evolution-text {
        text-align: center;
        color: #ff69b4;
        font-size: 1.2rem;
        background: rgba(255,255,255,0.8);
        padding: 8px 20px;
        border-radius: 40px;
        margin-top: 10px;
        border: 2px dashed #ffb6c1;
    }

    /* 問題カード */
    .question-box {
        background: #fff3e6;
        border-radius: 60px;
        padding: 2rem;
        margin: 1.5rem 0;
        border: 5px solid #ff9ff3;
        font-size: 2rem;
        text-align: center;
        box-shadow: 0 15px 0 #b13a9b, 0 20px 30px rgba(0,0,0,0.1);
    }

    /* 答案显示框 */
    .answer-display {
        background: #fff9e6;
        border: 5px solid #ff9ff3;
        border-radius: 30px;
        font-size: 2.5rem;
        text-align: center;
        padding: 15px;
        margin: 15px 0;
    }

    .correct-msg {
        background: #b5e7a0;
        color: #1e5f1e;
        border-radius: 40px;
        padding: 1rem;
        text-align: center;
        font-size: 2rem;
        border: 3px solid white;
        box-shadow: 0 5px 0 #5f9e5f;
        margin: 20px 0;
    }

    .wrong-msg {
        background: #f8d7da;
        color: #9e2a2a;
        border-radius: 40px;
        padding: 1rem;
        text-align: center;
        font-size: 1.5rem;
        border: 3px solid white;
        box-shadow: 0 5px 0 #b02a2a;
        margin: 20px 0;
    }

    /* パズルエリア */
    .puzzle-container {
        background: #fef2e7;
        border-radius: 60px;
        padding: 20px;
        margin: 20px 0;
        border: 5px solid #feca57;
        box-shadow: 0 10px 0 #b38f40, 0 15px 25px rgba(0,0,0,0.1);
    }

    .puzzle-grid {
        display: grid;
        gap: 8px;
        justify-content: center;
    }

    .puzzle-cell {
        background: #fff;
        border-radius: 20px;
        padding: 8px;
        font-size: 2.5rem;
        border: 3px solid #ff9ff3;
        min-width: 70px;
        min-height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 0 #b13a9b, 0 8px 15px rgba(0,0,0,0.1);
        transition: 0.2s;
    }

    .puzzle-cell.filled {
        background: #ffe6f0;
        transform: scale(1.05);
        border-color: #ff69b4;
    }

    /* ご褒美シール */
    @keyframes shine {
        0% { box-shadow: 0 0 20px gold; }
        50% { box-shadow: 0 0 40px orange; }
        100% { box-shadow: 0 0 20px gold; }
    }

    .sticker {
        background: linear-gradient(145deg, #ffd700, #ffb347);
        border-radius: 50%;
        width: 180px;
        height: 180px;
        margin: 20px auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 0 10px 20px rgba(0,0,0,0.3), inset 0 -5px 10px rgba(0,0,0,0.2);
        border: 5px solid white;
        animation: shine 1.5s infinite;
    }

    .sticker-text {
        font-size: 1.5rem;
        color: white;
        text-shadow: 2px 2px 0 #b37400;
    }

    /* 右下キャラクターコレクション */
    .collection-box {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 50px;
        padding: 8px 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        border: 3px solid #ffb6c1;
        backdrop-filter: blur(10px);
        z-index: 1000;
        display: flex;
        align-items: center;
        gap: 5px;
        font-size: 1.5rem;
        max-width: 80vw;
        overflow-x: auto;
        white-space: nowrap;
        cursor: pointer;
        transition: 0.3s;
    }

    .collection-box:hover {
        transform: scale(1.05);
        background: white;
    }

    .collection-box span {
        display: inline-block;
        filter: drop-shadow(0 2px 3px rgba(0,0,0,0.2));
    }

    /* アニメーション：スター */
    @keyframes starPop {
        0% { transform: scale(0) rotate(0deg); opacity: 0; }
        50% { transform: scale(3) rotate(180deg); opacity: 1; }
        100% { transform: scale(0) rotate(360deg); opacity: 0; }
    }
    .star-animation {
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 5rem;
        animation: starPop 0.8s ease-out forwards;
        pointer-events: none;
        z-index: 9999;
    }

    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.8rem;
        margin-top: 4rem;
        padding: 1rem;
        background: #fff9e6;
        border-radius: 50px 50px 0 0;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# タイトル
st.markdown('<p class="rainbow-title">🧸 わくわく算数ランド 🎈</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ キャラクターをそだてながら さんすうれんしゅう！ ✨</p>', unsafe_allow_html=True)
st.markdown("---")

# ==============================================
# キャラクター育成設定
# ==============================================
CHARACTERS = {
    "たまご": {"emoji": "🥚", "next_level": 5, "message": "まだうまれたて..."},
    "ひよこ": {"emoji": "🐣", "next_level": 15, "message": "ぴよぴよ！ げんきいっぱい！"},
    "にわとり": {"emoji": "🐤", "next_level": 30, "message": "こけこっこー！ まいにもれんしゅう！"},
    "おおきなにわとり": {"emoji": "🐔", "next_level": 50, "message": "かっこいいでしょ！ さんすうはかせ！"},
    "フェニックス": {"emoji": "🦅", "next_level": 100, "message": "でんせつのとり！ もうこわいものなし！"},
}

def get_character_by_exp(exp):
    if exp < 5:
        return "たまご", CHARACTERS["たまご"]
    elif exp < 15:
        return "ひよこ", CHARACTERS["ひよこ"]
    elif exp < 30:
        return "にわとり", CHARACTERS["にわとり"]
    elif exp < 50:
        return "おおきなにわとり", CHARACTERS["おおきなにわとり"]
    else:
        return "フェニックス", CHARACTERS["フェニックス"]

def get_next_level_exp(exp):
    if exp < 5:
        return 5
    elif exp < 15:
        return 15
    elif exp < 30:
        return 30
    elif exp < 50:
        return 50
    else:
        return 100

# ==============================================
# サイドバー（設定）
# ==============================================
with st.sidebar:
    st.markdown("## 🎮 ゲームせってい")
    st.markdown("---")

    mode = st.radio(
        "あそびかたをえらんでね",
        options=["📋 れんしゅうモード", "🎯 チャレンジモード"],
        index=0
    )

    st.markdown("---")
    num_questions = st.slider("⭐ もんだいすう", min_value=1, max_value=30, value=10)

    st.markdown("---")
    st.markdown("### 🧮 どんなけいさん？")

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
    difficulty = st.radio(
        "レベルをえらんでね",
        options=["🐣 かんたん", "🐼 ふつう", "🦁 むずかしい"],
        index=1,
        horizontal=True
    )
    if difficulty == "🐣 かんたん":
        diff_level = "1桁のみ"
    elif difficulty == "🐼 ふつう":
        diff_level = "2桁（繰り上がり・繰り下がりなし）"
    else:
        diff_level = "2桁（あり）"

    st.markdown("---")
    if "れんしゅう" in mode:
        show_answers = st.toggle("✨ こたえをみる", value=True)

# ==============================================
# 絵文字リスト（パズルピース用）
# ==============================================
EMOJI_LIST = [
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐸",
    "🐒", "🐔", "🐧", "🐦", "🐤", "🐣", "🐥", "🐺", "🐗", "🐴",
    "🦄", "🐝", "🐛", "🐌", "🐞", "🐜", "🦗", "🕷️", "🦂", "🐢",
    "🐍", "🦎", "🐙", "🦑", "🦐", "🦞", "🐠", "🐟", "🐡", "🐬",
    "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🐘",
    "🦛", "🦏", "🐪", "🐫", "🦒", "🦘", "🦡", "🐃", "🐂", "🐄",
    "🐎", "🐖", "🐏", "🐑", "🦙", "🐐", "🦌", "🐕", "🐩", "🐈",
    "🕊️", "🐇", "🦝", "🦔", "🦦", "🦥", "🐁", "🐀", "🐿️", "🦔",
    "🍎", "🍐", "🍊", "🍋", "🍌", "🍉", "🍇", "🍓", "🫐", "🍈",
    "🍒", "🍑", "🥭", "🍍", "🥥", "🥝", "🍅", "🍆", "🥑", "🥦",
    "🥬", "🥒", "🌶️", "🫑", "🌽", "🥕", "🫒", "🧄", "🧅", "🥔",
    "🍠", "🥐", "🥯", "🍞", "🥖", "🥨", "🧀", "🥚", "🍳", "🧈",
    "🥞", "🧇", "🥓", "🥩", "🍗", "🍖", "🦴", "🌭", "🍔", "🍟",
    "🍕", "🫓", "🥪", "🥙", "🧆", "🌮", "🌯", "🫔", "🥗", "🥘",
    "🫕", "🥫", "🍝", "🍜", "🍲", "🍛", "🍣", "🍱", "🥟", "🍤",
    "🍙", "🍚", "🍘", "🍥", "🥠", "🥮", "🍡", "🍧", "🍨", "🍦",
    "🍰", "🎂", "🧁", "🍫", "🍬", "🍭", "🍮", "🍯", "🍼", "🥛"
]

# ==============================================
# 問題生成関数
# ==============================================
def generate_question(types, difficulty):
    q_type = random.choice(types)

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
        return f"{a} + {b} = ?", str(a + b), "number"

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
        return f"{a} - {b} = ?", str(a - b), "number"

    elif q_type == "multiplication":
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        return f"{a} × {b} = ?", str(a * b), "number"

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
        return f"{a} □ {b} （にあてはまる記号 >, <, = を答えましょう）", op, "compare"

    elif q_type == "length":
        if random.choice([True, False]):
            meters = random.randint(1, 5)
            return f"{meters} m = □ cm", str(meters * 100), "number"
        else:
            cm = random.choice([100, 200, 300, 400, 500, 600, 700, 800, 900])
            return f"{cm} cm = □ m", str(cm // 100) if cm % 100 == 0 else f"{cm/100:.1f}", "number"

    elif q_type == "time":
        hour = random.randint(1, 12)
        minute = random.choice([0, 15, 30, 45])
        return f"時計の針が {hour} 時 {minute} 分をさしています。時刻は？", f"{hour}時{minute}分", "time"

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
        return [], [], []

    questions, answers, qtypes = [], [], []
    for _ in range(int(num_questions)):
        q, a, t = generate_question(selected_types, diff_level)
        questions.append(q)
        answers.append(a)
        qtypes.append(t)
    return questions, answers, qtypes

# ==============================================
# セッション状態の初期化
# ==============================================
if "questions" not in st.session_state:
    st.session_state["questions"] = []
    st.session_state["answers"] = []
    st.session_state["qtypes"] = []
    st.session_state["current_q"] = 0
    st.session_state["score"] = 0
    st.session_state["answered"] = [False] * 30
    st.session_state["puzzle_pieces"] = []
    st.session_state["puzzle_filled"] = []
    st.session_state["all_correct"] = False

    # キャラクター育成用
    st.session_state["exp"] = 0
    st.session_state["prev_character"] = "たまご"

    # キャラクター図鑑（庭）用
    st.session_state["character_collection"] = {
        "たまご": 0,
        "ひよこ": 0,
        "にわとり": 0,
        "おおきなにわとり": 0,
        "フェニックス": 0
    }

# ==============================================
# 現在のキャラクター情報取得・表示
# ==============================================
current_char, char_info = get_character_by_exp(st.session_state["exp"])
next_level_exp = get_next_level_exp(st.session_state["exp"])
exp_percentage = min(100, (st.session_state["exp"] / next_level_exp) * 100)

# レベルアップチェック＆図鑑登録
if current_char != st.session_state["prev_character"]:
    st.balloons()
    st.session_state["character_collection"][current_char] += 1
    st.session_state["prev_character"] = current_char

# メインキャラクターカード表示
with st.container():
    st.markdown('<div class="character-container">', unsafe_allow_html=True)
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(f'<div class="character-emoji">{char_info["emoji"]}</div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="character-name">✨ {current_char} ✨</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="character-message">{char_info["message"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="level-badge">レベル {st.session_state["exp"]} / {next_level_exp}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="exp-bar"><div class="exp-fill" style="width: {exp_percentage}%;"></div></div>', unsafe_allow_html=True)

        # 進化までの残り問題数を表示
        remaining = next_level_exp - st.session_state["exp"]
        if remaining > 0:
            st.markdown(f'<div class="evolution-text">あと <b>{remaining}</b> もんせいかいで しんか！</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="evolution-text">✨ つぎのしんかまで あとちょっと！ ✨</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ==============================================
# 新規作成ボタン（古い入力をリセット）
# ==============================================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎲 もんだいをあたらしくつくる"):
        q_list, a_list, t_list = generate_worksheet()
        if q_list:
            st.session_state["questions"] = q_list
            st.session_state["answers"] = a_list
            st.session_state["qtypes"] = t_list
            st.session_state["current_q"] = 0
            st.session_state["score"] = 0
            st.session_state["answered"] = [False] * len(q_list)
            st.session_state["all_correct"] = False

            # パズル用のデータを初期化
            n = len(q_list)
            available_emojis = EMOJI_LIST.copy()
            random.shuffle(available_emojis)
            st.session_state["puzzle_pieces"] = available_emojis[:n]
            st.session_state["puzzle_filled"] = [False] * n

            # 以前の入力値をすべてクリア
            keys_to_delete = [key for key in st.session_state.keys() if key.startswith("input_")]
            for key in keys_to_delete:
                del st.session_state[key]

            if "チャレンジ" in mode:
                st.rerun()

# ==============================================
# モード分岐
# ==============================================
if "れんしゅう" in mode:
    # ---------- 練習モード（一覧表示）----------
    if st.session_state["questions"]:
        st.markdown("## 📚 きょうのもんだい")
        for i, q in enumerate(st.session_state["questions"], 1):
            st.markdown(f"**{i}.** {q}")

        if show_answers:
            st.markdown("## 🔍 こたえ")
            for i, a in enumerate(st.session_state["answers"], 1):
                st.markdown(f"**{i}.** {a}")

        # ダウンロード
        text_content = "【れんしゅうもんだい】\n\n"
        for i, q in enumerate(st.session_state["questions"], 1):
            text_content += f"{i}. {q}\n"
        if show_answers:
            text_content += "\n【こたえ】\n"
            for i, a in enumerate(st.session_state["answers"], 1):
                text_content += f"{i}. {a}\n"

        st.download_button("📥 プリントにほぞん", text_content, file_name="renshu.txt")
    else:
        st.info("👈 もんだいをつくってね")

else:  # チャレンジモード
    if not st.session_state["questions"]:
        st.info("🎲 もんだいをつくってはじめよう！")
    else:
        q_list = st.session_state["questions"]
        a_list = st.session_state["answers"]
        t_list = st.session_state["qtypes"]
        total = len(q_list)
        current = st.session_state["current_q"]
        filled = st.session_state["puzzle_filled"]
        pieces = st.session_state["puzzle_pieces"]

        # 進捗表示
        st.progress(current / total, text=f"もんだい {current+1} / {total}")
        st.markdown(f"### せいかいすう: {st.session_state['score']} / {total}")

        # パズル表示
        if total > 0:
            cols = math.ceil(math.sqrt(total))
            rows = math.ceil(total / cols)

            st.markdown("### 🧩 あつめてね！パズル")
            with st.container():
                st.markdown('<div class="puzzle-container">', unsafe_allow_html=True)

                grid_style = f"""
                <style>
                .puzzle-grid-{total} {{
                    display: grid;
                    grid-template-columns: repeat({cols}, 1fr);
                    gap: 8px;
                    justify-content: center;
                }}
                </style>
                """
                st.markdown(grid_style, unsafe_allow_html=True)

                html = f'<div class="puzzle-grid puzzle-grid-{total}">'
                for i in range(total):
                    cell_class = "puzzle-cell filled" if filled[i] else "puzzle-cell"
                    content = pieces[i] if filled[i] else "❓"
                    html += f'<div class="{cell_class}">{content}</div>'
                for i in range(total, rows * cols):
                    html += f'<div class="puzzle-cell" style="visibility: hidden;"></div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)

        # 現在の問題
        if current < total:
            st.markdown(f'<div class="question-box">🔢 {q_list[current]}</div>', unsafe_allow_html=True)

            qtype = t_list[current]
            correct_answer = a_list[current]

            # ---------- 比較題（＞＜＝） ----------
            if qtype == "compare":
                user_answer = st.radio(
                    "ふごうをえらんでね",
                    options=[">", "<", "="],
                    horizontal=True,
                    key=f"q_{current}"
                )
                col_ans, col_skip = st.columns([1, 1])
                with col_ans:
                    if st.button("✅ こたえる", key=f"btn_{current}"):
                        if user_answer:
                            if user_answer == correct_answer:
                                st.session_state["score"] += 1
                                st.session_state["puzzle_filled"][current] = True
                                st.session_state["exp"] += 1
                                st.markdown('<div class="star-animation">⭐</div>', unsafe_allow_html=True)
                                if all(st.session_state["puzzle_filled"]):
                                    st.session_state["all_correct"] = True
                                    st.balloons()
                                    st.markdown(f'<div class="correct-msg" style="font-size:2rem;">🌈✨ パズルかんせい！ ✨🌈</div>', unsafe_allow_html=True)
                                    st.session_state["current_q"] = total
                                    st.rerun()
                                else:
                                    st.markdown('<div class="correct-msg">🎉 せいかい！ すごい！</div>', unsafe_allow_html=True)
                                    if current + 1 < total:
                                        st.session_state["current_q"] += 1
                                        st.rerun()
                            else:
                                st.markdown(f'<div class="wrong-msg">😢 ざんねん... ただしいこたえは {correct_answer}</div>', unsafe_allow_html=True)
                        else:
                            st.warning("ふごうをえらんでね")
                with col_skip:
                    if st.button("⏩ とばす", key=f"skip_{current}"):
                        if current + 1 < total:
                            st.session_state["current_q"] += 1
                            st.rerun()

            # ---------- 時間題（选项按钮 - 最终稳定版） ----------
            elif qtype == "time":
                # 生成选项函数（确保正确答案始终在选项中）
                def generate_time_options(correct):
                    options = [correct]  # 始终包含正确答案
                    match = re.match(r'(\d+)時(\d+)分', correct)
                    if not match:
                        return options
                    hour = int(match.group(1))
                    minute = int(match.group(2))
                    minute_choices = [0, 15, 30, 45]
                    other_hours = [h for h in range(1, 13) if h != hour]
                    other_minutes = [m for m in minute_choices if m != minute]
                    distractors = set()
                    # 同小时不同分钟
                    for m in other_minutes:
                        distractors.add(f"{hour}時{m}分")
                    # 不同小时同分钟
                    for h in random.sample(other_hours, min(2, len(other_hours))):
                        distractors.add(f"{h}時{minute}分")
                    # 如果不足3个，补充不同小时不同分钟
                    while len(distractors) < 3:
                        h = random.choice(other_hours)
                        m = random.choice(other_minutes)
                        distractors.add(f"{h}時{m}分")
                    # 随机取3个干扰项
                    dist_list = list(distractors)
                    random.shuffle(dist_list)
                    options.extend(dist_list[:3])
                    # 最终打乱顺序
                    random.shuffle(options)
                    return options

                # 为当前问题存储选项列表，避免每次rerun重新生成
                options_key = f"time_options_{current}"
                if options_key not in st.session_state:
                    st.session_state[options_key] = generate_time_options(correct_answer)
                time_options = st.session_state[options_key]

                # 将选项排成2列
                for i in range(0, len(time_options), 2):
                    row_cols = st.columns(2)
                    for j in range(2):
                        idx = i + j
                        if idx < len(time_options):
                            with row_cols[j]:
                                if st.button(time_options[idx], key=f"time_opt_{current}_{idx}", use_container_width=True):
                                    if time_options[idx] == correct_answer:
                                        st.session_state["score"] += 1
                                        st.session_state["puzzle_filled"][current] = True
                                        st.session_state["exp"] += 1
                                        st.markdown('<div class="star-animation">⭐</div>', unsafe_allow_html=True)
                                        if all(st.session_state["puzzle_filled"]):
                                            st.session_state["all_correct"] = True
                                            st.balloons()
                                            st.markdown(f'<div class="correct-msg" style="font-size:2rem;">🌈✨ パズルかんせい！ ✨🌈</div>', unsafe_allow_html=True)
                                            st.session_state["current_q"] = total
                                            # 清理存储
                                            if options_key in st.session_state:
                                                del st.session_state[options_key]
                                            st.rerun()
                                        else:
                                            st.markdown('<div class="correct-msg">🎉 せいかい！ すごい！</div>', unsafe_allow_html=True)
                                            if current + 1 < total:
                                                st.session_state["current_q"] += 1
                                                # 清理存储
                                                if options_key in st.session_state:
                                                    del st.session_state[options_key]
                                                st.rerun()
                                    else:
                                        st.markdown(f'<div class="wrong-msg">😢 ざんねん... ただしいこたえは {correct_answer}</div>', unsafe_allow_html=True)
                if st.button("⏩ とばす", key=f"skip_time_{current}"):
                    if current + 1 < total:
                        st.session_state["current_q"] += 1
                        # 清理存储
                        if options_key in st.session_state:
                            del st.session_state[options_key]
                        st.rerun()

            # ---------- 数值题（优化后的数字键盘） ----------
            else:
                input_key = f"input_{current}"
                if input_key not in st.session_state:
                    st.session_state[input_key] = ""

                st.markdown(f'<div class="answer-display">{st.session_state[input_key] or "?"}</div>', unsafe_allow_html=True)

                # 数字键盘 1-9 (3x3)
                rows = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
                for row in rows:
                    cols = st.columns(3)
                    for idx, num in enumerate(row):
                        with cols[idx]:
                            if st.button(str(num), key=f"num_{current}_{num}", use_container_width=True):
                                st.session_state[input_key] += str(num)
                                st.rerun()

                # 0 单独一行居中
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("0", key=f"num_{current}_0", use_container_width=True):
                        st.session_state[input_key] += "0"
                        st.rerun()

                # 操作按钮
                col_del, col_clear, col_submit = st.columns(3)
                with col_del:
                    if st.button("⌫ けす", key=f"del_{current}", use_container_width=True):
                        st.session_state[input_key] = st.session_state[input_key][:-1]
                        st.rerun()
                with col_clear:
                    if st.button("🗑 すべてけす", key=f"clear_{current}", use_container_width=True):
                        st.session_state[input_key] = ""
                        st.rerun()
                with col_submit:
                    if st.button("✅ こたえる", key=f"submit_{current}", use_container_width=True):
                        user_answer = st.session_state[input_key]
                        if user_answer:
                            if user_answer == correct_answer:
                                st.session_state["score"] += 1
                                st.session_state["puzzle_filled"][current] = True
                                st.session_state["exp"] += 1
                                st.markdown('<div class="star-animation">⭐</div>', unsafe_allow_html=True)
                                if all(st.session_state["puzzle_filled"]):
                                    st.session_state["all_correct"] = True
                                    st.balloons()
                                    st.markdown(f'<div class="correct-msg" style="font-size:2rem;">🌈✨ パズルかんせい！ ✨🌈</div>', unsafe_allow_html=True)
                                    st.session_state["current_q"] = total
                                    st.rerun()
                                else:
                                    st.markdown('<div class="correct-msg">🎉 せいかい！ すごい！</div>', unsafe_allow_html=True)
                                    if current + 1 < total:
                                        st.session_state["current_q"] += 1
                                        st.rerun()
                            else:
                                st.markdown(f'<div class="wrong-msg">😢 ざんねん... ただしいこたえは {correct_answer}</div>', unsafe_allow_html=True)
                        else:
                            st.warning("こたえをにゅうりょくしてね")

                # 跳过按钮
                if st.button("⏩ とばす", key=f"skip_num_{current}"):
                    if current + 1 < total:
                        st.session_state["current_q"] += 1
                        st.rerun()

        else:
            # 全問終了画面
            if st.session_state.get("all_correct", False):
                st.balloons()
                st.markdown("""
                <div class="sticker">
                    <div style="font-size: 4rem;">🏆</div>
                    <div class="sticker-text">よくできました！</div>
                    <div style="font-size: 1.5rem; color: white;">⭐⭐⭐</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("## 🎊 ぜんもんせいかい！ おめでとう！ 🎊")
            else:
                st.markdown(f"## 🎊 おわり！ せいかいすう: {st.session_state['score']} / {total}")

            if st.button("🔄 もういちど"):
                st.session_state["current_q"] = 0
                st.session_state["score"] = 0
                st.session_state["answered"] = [False] * total
                st.session_state["puzzle_filled"] = [False] * total
                st.session_state["all_correct"] = False
                st.rerun()

# ==============================================
# 右下キャラクターコレクション
# ==============================================
unlocked_emojis = []
for name, data in CHARACTERS.items():
    if st.session_state["character_collection"].get(name, 0) > 0:
        unlocked_emojis.append(data["emoji"])
if not unlocked_emojis:
    unlocked_emojis = ["🥚"]

emojis_html = "".join([f'<span>{emoji}</span>' for emoji in unlocked_emojis])
st.markdown(f"""
<div class="collection-box">
    {emojis_html}
</div>
""", unsafe_allow_html=True)

# ==============================================
# フッター
# ==============================================
st.markdown("---")
st.markdown('<div class="footer">🧸 わくわく算数ランド | キャラクターをそだてよう！</div>', unsafe_allow_html=True)