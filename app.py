# -*- coding: utf-8 -*-
import streamlit as st
import random
import math
from datetime import datetime

# -------------------------------
# ページ設定
st.set_page_config(
    page_title="わくわく算数ランド", 
    page_icon="🧸", 
    layout="wide"
)

# -------------------------------
# カスタムCSS（かわいく）
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Comic+Neue:wght@400;700&display=swap');
    html, body, [class*="css"]  {
        font-family: 'Comic Neue', cursive;
    }
    .rainbow-title {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(45deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .sub-title {
        font-size: 1.5rem;
        color: #ff9f43;
        text-align: center;
        margin-top: 0;
    }
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
    .question-box {
        background-color: #fff3e6;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border-left: 15px solid #ff9ff3;
        font-size: 2rem;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .correct-msg {
        background-color: #d4edda;
        color: #155724;
        border-radius: 10px;
        padding: 0.5rem;
        text-align: center;
        font-size: 1.5rem;
    }
    .wrong-msg {
        background-color: #f8d7da;
        color: #721c24;
        border-radius: 10px;
        padding: 0.5rem;
        text-align: center;
        font-size: 1.5rem;
    }
    .puzzle-container {
        background-color: #faf0e6;
        border-radius: 30px;
        padding: 20px;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .puzzle-grid {
        display: grid;
        gap: 10px;
        justify-content: center;
        margin: 10px 0;
    }
    .puzzle-cell {
        background-color: #f5f5f5;
        border-radius: 15px;
        padding: 15px;
        text-align: center;
        font-size: 2.5rem;
        border: 3px solid #ff9ff3;
        min-width: 80px;
        min-height: 80px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    .puzzle-cell.filled {
        background-color: #fff3e6;
        transform: scale(1.05);
    }
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# タイトル
st.markdown('<p class="rainbow-title">🧸 わくわく算数ランド 🎈</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">✨ えらんで といて まるつけ！ ✨</p>', unsafe_allow_html=True)
st.markdown("---")

# -------------------------------
# サイドバー（設定）
with st.sidebar:
    st.markdown("## 🎮 ゲームせってい")
    st.markdown("---")
    
    # モード選択
    mode = st.radio(
        "あそびかたをえらんでね",
        options=["📋 れんしゅうモード（いちらんひょうじ）", "🎯 チャレンジモード（1もんずつこたえる）"],
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
    # 練習モード用：答え表示
    if "れんしゅう" in mode:
        show_answers = st.toggle("✨ こたえをみる", value=True)

# -------------------------------
# 絵文字リスト（パズルピースに使う）
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

# -------------------------------
# 問題生成関数（変更なし）
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
        return f"{a} + {b} = ?", str(a + b)
    
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
    
    elif q_type == "multiplication":
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        return f"{a} × {b} = ?", str(a * b)
    
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
    
    elif q_type == "length":
        if random.choice([True, False]):
            meters = random.randint(1, 5)
            return f"{meters} m = □ cm", str(meters * 100)
        else:
            cm = random.choice([100, 200, 300, 400, 500, 600, 700, 800, 900])
            return f"{cm} cm = □ m", str(cm // 100) if cm % 100 == 0 else f"{cm/100:.1f}"
    
    elif q_type == "time":
        hour = random.randint(1, 12)
        minute = random.choice([0, 15, 30, 45])
        return f"時計の針が {hour} 時 {minute} 分をさしています。時刻は？", f"{hour}時{minute}分"

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
# セッション状態の初期化
if "questions" not in st.session_state:
    st.session_state["questions"] = []
    st.session_state["answers"] = []
    st.session_state["current_q"] = 0
    st.session_state["score"] = 0
    st.session_state["answered"] = [False] * 30
    st.session_state["puzzle_pieces"] = []   # 各ピースの絵文字（問題数分）
    st.session_state["puzzle_filled"] = []   # 各ピースが埋まったかどうか

# -------------------------------
# メイン処理
if "questions" not in st.session_state:
    st.session_state["questions"] = []
    st.session_state["answers"] = []
    st.session_state["current_q"] = 0
    st.session_state["score"] = 0
    st.session_state["answered"] = [False] * 30
    st.session_state["puzzle_pieces"] = []
    st.session_state["puzzle_filled"] = []

# 新規作成ボタン
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🎲 もんだいをあたらしくつくる"):
        q_list, a_list = generate_worksheet()
        if q_list:
            st.session_state["questions"] = q_list
            st.session_state["answers"] = a_list
            st.session_state["current_q"] = 0
            st.session_state["score"] = 0
            st.session_state["answered"] = [False] * len(q_list)
            
            # パズル用のデータを初期化
            n = len(q_list)
            # 問題数分の異なる絵文字をランダムに選ぶ（重複なし）
            available_emojis = EMOJI_LIST.copy()
            random.shuffle(available_emojis)
            st.session_state["puzzle_pieces"] = available_emojis[:n]
            st.session_state["puzzle_filled"] = [False] * n
            
            if "チャレンジ" in mode:
                st.rerun()

# -------------------------------
# モード分岐
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

else:
    # ---------- チャレンジモード（1問ずつ回答＋パズル）----------
    if not st.session_state["questions"]:
        st.info("🎲 もんだいをつくってはじめよう！")
    else:
        q_list = st.session_state["questions"]
        a_list = st.session_state["answers"]
        total = len(q_list)
        current = st.session_state["current_q"]
        filled = st.session_state["puzzle_filled"]
        pieces = st.session_state["puzzle_pieces"]
        
        # 進捗表示
        st.progress(current / total, text=f"もんだい {current+1} / {total}")
        st.markdown(f"### せいかいすう: {st.session_state['score']} / {total}")
        
        # -------------------------------
        # パズル表示（問題数に合わせてグリッドサイズを計算）
        if total > 0:
            # グリッドの列数を決める（できるだけ正方形に近く）
            cols = math.ceil(math.sqrt(total))
            rows = math.ceil(total / cols)
            
            st.markdown("### 🧩 あつめてね！パズル")
            with st.container():
                st.markdown('<div class="puzzle-container">', unsafe_allow_html=True)
                
                # CSSでグリッドを定義
                grid_style = f"""
                <style>
                .puzzle-grid-{total} {{
                    display: grid;
                    grid-template-columns: repeat({cols}, 1fr);
                    gap: 10px;
                    justify-content: center;
                }}
                </style>
                """
                st.markdown(grid_style, unsafe_allow_html=True)
                
                # グリッドを描画
                html = f'<div class="puzzle-grid puzzle-grid-{total}">'
                for i in range(total):
                    cell_class = "puzzle-cell filled" if filled[i] else "puzzle-cell"
                    content = pieces[i] if filled[i] else "❓"
                    html += f'<div class="{cell_class}">{content}</div>'
                # 余ったセルは空白で埋める（グリッドを整えるため）
                for i in range(total, rows * cols):
                    html += f'<div class="puzzle-cell" style="visibility: hidden;"></div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        # -------------------------------
        # 現在の問題
        if current < total:
            st.markdown(f'<div class="question-box">🔢 {q_list[current]}</div>', unsafe_allow_html=True)
            
            # 回答入力
            if "□" in q_list[current] and "記号" in q_list[current]:
                user_answer = st.radio(
                    "ふごうをえらんでね",
                    options=[">", "<", "="],
                    horizontal=True,
                    key=f"q_{current}"
                )
            else:
                user_answer = st.text_input("こたえをにゅうりょくしてね", key=f"q_{current}", value="")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ こたえる", key=f"btn_{current}"):
                    if user_answer:
                        # 正誤判定
                        is_correct = False
                        if "記号" in q_list[current]:
                            is_correct = (user_answer == a_list[current])
                        else:
                            user_clean = user_answer.strip().replace(" ", "")
                            correct_clean = a_list[current].strip().replace(" ", "")
                            is_correct = (user_clean == correct_clean)
                        
                        if is_correct:
                            # 正解処理
                            st.session_state["score"] += 1
                            st.session_state["puzzle_filled"][current] = True  # 現在の問題のピースを埋める
                            st.markdown('<div class="correct-msg">🎉 せいかい！ すごい！</div>', unsafe_allow_html=True)
                            
                            # 全問正解チェック
                            if all(st.session_state["puzzle_filled"]):
                                st.balloons()
                                st.markdown('<div class="correct-msg" style="font-size:2rem;">🌈✨ パズルかんせい！ やったね！ ✨🌈</div>', unsafe_allow_html=True)
                            
                            # 次の問題へ
                            if current + 1 < total:
                                st.session_state["current_q"] += 1
                                st.rerun()
                        else:
                            st.markdown(f'<div class="wrong-msg">😢 ざんねん... ただしいこたえは {a_list[current]}</div>', unsafe_allow_html=True)
                            
                            # 間違えても次の問題に進める（再挑戦できるように）
                            # 必要ならここで再試行させてもよいが、今回は進むだけにする
                            # if current + 1 < total:
                            #     st.session_state["current_q"] += 1
                            #     st.rerun()
                    else:
                        st.warning("こたえをにゅうりょくしてね")
            
            with col2:
                if st.button("⏩ とばす"):
                    if current + 1 < total:
                        st.session_state["current_q"] += 1
                        st.rerun()
        else:
            # 全問終了
            st.balloons()
            if all(st.session_state["puzzle_filled"]):
                st.markdown("## 🎊 おめでとう！ ぜんもんせいかい！")
            else:
                st.markdown(f"## 🎊 おわり！ せいかいすう: {st.session_state['score']} / {total}")
            if st.button("🔄 もういちど"):
                st.session_state["current_q"] = 0
                st.session_state["score"] = 0
                st.session_state["answered"] = [False] * total
                st.session_state["puzzle_filled"] = [False] * total
                st.rerun()

# -------------------------------
st.markdown("---")
st.markdown('<div class="footer">🧸 わくわく算数ランド | たのしくまなぼう！</div>', unsafe_allow_html=True)