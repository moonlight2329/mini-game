import streamlit as st

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

st.title("🎮 Tic Tac Toe")

# --- STATE ---
if "board" not in st.session_state:
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.player = "X"
    st.session_state.mode = "2P"
    st.session_state.score = {"X": 0, "O": 0}
    st.session_state.game_over = False

# --- LOGIC ---

def wins_for(board, p):
    combos = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == p for i in c) for c in combos)


def is_draw(board):
    return " " not in board


def best_ai_move():
    b = st.session_state.board

    # 1. Win if possible
    for i in range(9):
        if b[i] == " ":
            b[i] = "O"
            if wins_for(b, "O"):
                b[i] = " "
                return i
            b[i] = " "

    # 2. Block player win
    for i in range(9):
        if b[i] == " ":
            b[i] = "X"
            if wins_for(b, "X"):
                b[i] = " "
                return i
            b[i] = " "

    # 3. Take center
    if b[4] == " ":
        return 4

    # 4. Take corners
    for i in [0,2,6,8]:
        if b[i] == " ":
            return i

    # 5. Take any side
    for i in [1,3,5,7]:
        if b[i] == " ":
            return i

    return None


def reset_board():
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.player = "X"
    st.session_state.game_over = False

# --- MODE ---
mode = st.radio("Mode", ["2 Player", "Play vs AI"], horizontal=True)
st.session_state.mode = "AI" if mode == "Play vs AI" else "2P"

st.markdown(f"### Score  \\n❌ X: {st.session_state.score['X']} &nbsp;&nbsp; ⭕ O: {st.session_state.score['O']}")

# --- STYLE ---
st.markdown("""
<style>
button[kind="secondary"] {
    height: 80px;
    font-size: 28px !important;
}
</style>
""", unsafe_allow_html=True)

# --- BOARD ---
for i in range(0, 9, 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j
        val = st.session_state.board[idx]

        display = "❌" if val == "X" else ("⭕" if val == "O" else " ")

        if cols[j].button(display, key=idx, use_container_width=True, disabled=st.session_state.game_over):
            if st.session_state.board[idx] == " " and not st.session_state.game_over:
                st.session_state.board[idx] = st.session_state.player

                if wins_for(st.session_state.board, st.session_state.player):
                    st.session_state.score[st.session_state.player] += 1
                    st.success(f"🎉 Player {st.session_state.player} wins!")
                    st.session_state.game_over = True

                elif is_draw(st.session_state.board):
                    st.warning("🤝 It's a draw!")
                    st.session_state.game_over = True

                else:
                    st.session_state.player = "O" if st.session_state.player == "X" else "X"

                    if st.session_state.mode == "AI" and st.session_state.player == "O":
                        ai = best_ai_move()
                        if ai is not None:
                            st.session_state.board[ai] = "O"

                            if wins_for(st.session_state.board, "O"):
                                st.session_state.score["O"] += 1
                                st.success("🤖 AI wins!")
                                st.session_state.game_over = True
                            elif is_draw(st.session_state.board):
                                st.warning("🤝 It's a draw!")
                                st.session_state.game_over = True
                            else:
                                st.session_state.player = "X"

# --- CONTROLS ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Restart Round"):
        reset_board()

with col2:
    if st.button("🧹 Reset Score"):
        st.session_state.score = {"X": 0, "O": 0}
        reset_board()

st.caption("Smarter AI: win → block → center → corners → sides")
