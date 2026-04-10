import streamlit as st
import random

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

st.title("🎮 Tic Tac Toe")

# Initialize state
if "board" not in st.session_state:
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.player = "X"
    st.session_state.mode = "2P"  # or 'AI'
    st.session_state.score = {"X": 0, "O": 0}
    st.session_state.game_over = False

# --- FUNCTIONS ---

def check_winner(board, player):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == player for i in combo) for combo in wins)


def check_draw(board):
    return " " not in board


def ai_move():
    empty = [i for i, spot in enumerate(st.session_state.board) if spot == " "]
    return random.choice(empty) if empty else None


def reset_board():
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.player = "X"
    st.session_state.game_over = False

# --- UI CONTROLS ---
st.subheader("Game Mode")
mode = st.radio("Choose mode:", ["2 Player", "Play vs AI"])
st.session_state.mode = "AI" if mode == "Play vs AI" else "2P"

st.markdown(f"**Score**  \\n❌ X: {st.session_state.score['X']} | ⭕ O: {st.session_state.score['O']}")

# --- BOARD UI ---
for i in range(0, 9, 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j
        label = st.session_state.board[idx] if st.session_state.board[idx] != " " else " "

        if cols[j].button(label, key=idx, use_container_width=True, disabled=st.session_state.game_over):
            if st.session_state.board[idx] == " " and not st.session_state.game_over:
                st.session_state.board[idx] = st.session_state.player

                # Check win
                if check_winner(st.session_state.board, st.session_state.player):
                    st.session_state.score[st.session_state.player] += 1
                    st.success(f"🎉 Player {st.session_state.player} wins!")
                    st.session_state.game_over = True

                # Check draw
                elif check_draw(st.session_state.board):
                    st.warning("🤝 It's a draw!")
                    st.session_state.game_over = True

                else:
                    # Switch player
                    st.session_state.player = "O" if st.session_state.player == "X" else "X"

                    # AI TURN
                    if st.session_state.mode == "AI" and st.session_state.player == "O":
                        ai_index = ai_move()
                        if ai_index is not None:
                            st.session_state.board[ai_index] = "O"

                            if check_winner(st.session_state.board, "O"):
                                st.session_state.score["O"] += 1
                                st.success("🤖 AI wins!")
                                st.session_state.game_over = True
                            elif check_draw(st.session_state.board):
                                st.warning("🤝 It's a draw!")
                                st.session_state.game_over = True
                            else:
                                st.session_state.player = "X"

# --- BUTTONS ---
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Restart Round"):
        reset_board()

with col2:
    if st.button("🧹 Reset Score"):
        st.session_state.score = {"X": 0, "O": 0}
        reset_board()

st.caption("Tip: Play vs AI or with a friend. Score persists until reset.")
