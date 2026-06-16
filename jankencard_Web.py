import streamlit as st
import random

# ページの設定
st.set_page_config(page_title="じゃんけんカードゲーム" , layout="wide")

# セッションがまだ作られていない場合
if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.game_over = False

    # 15枚の山札
    deck = ["グー ✊"] * 5 + ["チョキ ✌"] * 5 + ["パー ✋"] * 5

    # 山札をシャッフル
    random.shuffle(deck)

    # 山札を1枚ずつ取り出して、手札に配る
    st.session_state.player_hand = [deck.pop() , deck.pop() , deck.pop()]
    st.session_state.computer_hand = [deck.pop() , deck.pop() , deck.pop()]

    # 残った9枚を山札として記憶
    st.session_state.deck = deck

    # カウント用
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.round_count = 1
    st.session_state.history = []           # 試合結果表示

# 画面を1対3に分割
col_history, col_main = st.columns([1, 3])

# ============================================
# 左側エリア：これまでの勝負結果＆山札の残り枚数
# ============================================
with col_history:
    st.subheader("試合結果📝")
    st.write(f"**山札の残り:** あと {len(st.session_state.deck)}枚")
    st.write("---")

    # 履歴が空のとき
    if not st.session_state.history:
        st.caption(" ")
    else:
        for hist in reversed(st.session_state.history):
            st.write(hist)

# ============================================
# 右側エリア：メイン画面
# ============================================
with col_main:
    
    st.html("""
        <style>
            .stApp {
                background-color: #f0f2f5 !important;
            }
            /* 左側の試合結果エリアや文字の背景も馴染ませる設定 */
            div[data-testid="stSidebar"], div[data-testid="stVerticalBlock"] {
                background-color: transparent !important;
            }
        </style>
    """)
    
    st.title("♠♡じゃんけんカードゲーム♢♣")

    # スコア表示
    st.markdown(f"### 【第 {st.session_state.round_count} 戦目】")
    score_col1, score_col2 = st.columns(2) # 💡score_sol2を修正
    score_col1.metric("🤖 コンピューター", f"{st.session_state.computer_score}勝")
    score_col2.metric("👦 プレイヤー", f"{st.session_state.player_score}勝")

    st.write("---")

    # コンピューターの手札
    st.write("#### 🤖 コンピューターの手札")
    card_html = """
    <div style="
        display: inline-block;
        width: 80px;
        height: 120px;
        background: linear-gradient(135deg, #1e3a8a 25%, #3b82f6 25%, #3b82f6 50%, #1e3a8a 50%, #1e3a8a 75%, #3b82f6 75%, #3b82f6 100%);
        background-size: 12px 12px;
        border: 3px solid #ffffff;
        border-radius: 10px;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.3);
        margin: 0 8px;
    "></div>
    """

    c_cards = "".join([card_html] * len(st.session_state.computer_hand))
    c_display = f"""
    <div style="text-align: center; width: 100%; padding: 10px 0;">
        {c_cards}
    </div>
    """
    st.markdown(c_display, unsafe_allow_html=True)

    st.write(" ")

    # \\\\中段：バトルゾーン////
    st.write("#### ⚔ BATTLE ⚔")
    with st.container(border=True):
        b_col_c, b_col_vs, b_col_p = st.columns([5, 2, 5])

        # コンピューター側のバトルゾーン
        with b_col_c:
            st.markdown("<div style='text-align: center; color: gray;'>🤖 コンピューター</div>" , unsafe_allow_html=True) # 💡centerに修正
            if "last_c_card" in st.session_state:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.last_c_card} </h2>" , unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='text-align: center; color: #ddd;'>🂟</h2>", unsafe_allow_html=True)
            
        # VSの文字と勝敗結果
        with b_col_vs:
            st.markdown("<h2 style='text-align: center; color: red; margin-top: 10px;'>VS</h2>", unsafe_allow_html=True) # 💡</h2>に修正
            if "round_result" in st.session_state:
                st.markdown(f"<p style='text-align: center; font-weight: bold;'>{st.session_state.round_result}</p>", unsafe_allow_html=True)

        # プレイヤーのバトルゾーン
        with b_col_p:
            st.markdown("<div style='text-align: center; color: gray;'>👦 プレイヤー</div>" , unsafe_allow_html=True) # 💡centerに修正
            if "last_p_card" in st.session_state:
                st.markdown(f"<h2 style='text-align: center;'>{st.session_state.last_p_card} </h2>" , unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='text-align: center; color: #ddd;'>🂟</h2>", unsafe_allow_html=True)
    
    st.write(" ")

    # プレイヤーの手札のボタン
    if not st.session_state.game_over:
        st.markdown("<h4 style='text-align: center; color: gray;'>👦 あなたの手札（出すカードを1枚選択）</h4>", unsafe_allow_html=True)

        p_side1, p_main_col, p_side2 = st.columns([2, 6, 2])
        with p_main_col:
            hand_cols = st.columns(len(st.session_state.player_hand))

            for idx, card in enumerate(st.session_state.player_hand):
                with hand_cols[idx]:

                    st.html("""
                        <style>
                            div[data-testid="stButton"] button {
                                background-color: #ffffff !important;
                                color: #333333 !important;
                                border: 3px solid #3b82f6 !important;
                                border-radius: 10px !important;
                                height: 120px !important;  /* 💡相手のトランプと同じ縦の長さに！ */
                                font-size: 20px !important; /* 💡中の絵文字（✊など）を大きく！ */
                                font-weight: bold !important;
                                box-shadow: 3px 3px 8px rgba(0,0,0,0.2) !important;
                                transition: 0.2s;
                            }
                            div[data-testid="stButton"] button:hover {
                                border-color: #1e3a8a !important; /* マウスを乗せると青が濃くなるよ！ */
                                transform: translateY(-4px);      /* ちょっと上に浮き上がるオシャレ演出！ */
                            }
                        </style>
                    """)

                    if st.button(f"{card}", key=f"card_{idx}", use_container_width=True):
                                        
                        # 1. プレイヤーが選んだカードを手札から出す
                        p_card = st.session_state.player_hand.pop(idx)

                        # 2. コンピューターも手札からランダムに1枚出す
                        c_idx = random.randint(0, len(st.session_state.computer_hand) - 1)
                        c_card = st.session_state.computer_hand.pop(c_idx)

                        # 3. 出したカードをバトルゾーンに表示するため、セッションに記憶
                        st.session_state.last_p_card = p_card
                        st.session_state.last_c_card = c_card

                        # 4. 勝ち負けの判定
                        if p_card == c_card:
                            res = "あいこ"
                            res_emoji = "🤝"
                        elif (p_card =="グー ✊" and c_card == "チョキ ✌") or \
                            (p_card == "チョキ ✌" and c_card == "パー ✋") or \
                            (p_card == "パー ✋" and c_card == "グー ✊"): # 💡「チョ定」を「チョキ」に修正！
                            res = "あなたの勝ち！"
                            res_emoji = "🎊🎊"
                            st.session_state.player_score += 1
                        else:
                            res = "あなたの負け…"
                            res_emoji = "😭"
                            st.session_state.computer_score += 1
                    
                        # 判定結果を記憶
                        st.session_state.round_result = f"{res_emoji}{res}"

                        # 画面左側に今回の勝負結果を保存
                        hist_text = f"**{st.session_state.round_count}戦目:** 👦{p_card} vs 🤖{c_card} → **{res}**"
                        st.session_state.history.append(hist_text)

                        # 手札の補充＆サドンデス・試合終了判定
                        if st.session_state.round_count >= 3 and st.session_state.player_score != st.session_state.computer_score:
                            st.session_state.game_over = True
                        else:
                            # 同点の場合、サドンデスフラグON
                            if st.session_state.round_count >= 3:
                                st.session_state.sudden_death = True
                        
                            # 山札に2枚以上残っていたら、1枚ずつ引く
                            if len(st.session_state.deck) >= 2:
                                st.session_state.player_hand.append(st.session_state.deck.pop())
                                st.session_state.computer_hand.append(st.session_state.deck.pop())
                            else:
                                # 山札が空になったら終了
                                st.session_state.game_over = True

                        # ラウンド数を増やす
                        st.session_state.round_count += 1
                            
                        st.rerun()

# ============
# 最終結果発表
# ============
    else:
        st.write("---")
        st.subheader("🏆 最終結果発表")

        p_score = st.session_state.player_score
        c_score = st.session_state.computer_score

        if p_score > c_score:
            st.balloons()
            st.success(f"### 👑 おめでとうございます✨ {p_score}対{c_score}であなたの勝利です！！🎊")
        elif c_score > p_score:
            st.error(f"### 😭 残念… {c_score}対{p_score} でコンピューターの勝利です…また挑戦してね！🔥")
        else:
            st.warning(f"### 🤝 {p_score}対{c_score} で引き分けです。とてもいい勝負でした！")

        # コンティニューボタン（💡st.buttonに修正、st.rerun()を追加したよ！）
        if st.button("🎮もう一度遊ぶ🎮", type="primary"):
            st.session_state.clear()
            st.rerun()