import streamlit as st

st.title("🎮 Tic Tac Toe")

if "board" not in st.session_state:
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.player = "X"

def check_winner(board, player):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(board[i] == player for i in combo) for combo in wins)

def check_draw(board):
    return " " not in board

for i in range(0, 9, 3):
    cols = st.columns(3)
    for j in range(3):
        idx = i + j

        if cols[j].button(st.session_state.board[idx] or "-", key=idx):
            if st.session_state.board[idx] == " ":
                st.session_state.board[idx] = st.session_state.player

                # Check win
                if check_winner(st.session_state.board, st.session_state.player):
                    st.success(f"🎉 Player {st.session_state.player} wins!")
                    st.stop()

                # Check draw
                if check_draw(st.session_state.board):
                    st.warning("🤝 It's a draw!")
                    st.stop()

                # Switch player
                st.session_state.player = "O" if st.session_state.player == "X" else "X"


if st.button("🔄 Restart Game"):
    st.session_state.board = [" " for _ in range(9)]
    st.session_state.player = "X"
