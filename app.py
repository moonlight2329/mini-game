import streamlit as st
import random

st.set_page_config(page_title="Mini Game Hub", layout="centered")

st.title("🎮 Mini Game Hub")

# ================= MENU =================
game = st.sidebar.selectbox(
    "Choose a game",
    ["Tic Tac Toe", "Number Guessing", "Rock Paper Scissors"]
)

# ================= TIC TAC TOE =================
def run_tic_tac_toe():
    st.header("Tic Tac Toe")

    if "ttt_board" not in st.session_state:
        st.session_state.ttt_board = [" " for _ in range(9)]
        st.session_state.ttt_player = "X"
        st.session_state.ttt_score = {"X": 0, "O": 0}
        st.session_state.ttt_game_over = False

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
        b = st.session_state.ttt_board

        for i in range(9):
            if b[i] == " ":
                b[i] = "O"
                if wins_for(b, "O"):
                    b[i] = " "
                    return i
                b[i] = " "

        for i in range(9):
            if b[i] == " ":
                b[i] = "X"
                if wins_for(b, "X"):
                    b[i] = " "
                    return i
                b[i] = " "

        if b[4] == " ": return 4
        for i in [0,2,6,8]:
            if b[i] == " ": return i
        for i in [1,3,5,7]:
            if b[i] == " ": return i

    mode = st.radio("Mode", ["2 Player", "AI"], horizontal=True)

    st.write(f"Score → X: {st.session_state.ttt_score['X']} | O: {st.session_state.ttt_score['O']}")

    for i in range(0, 9, 3):
        cols = st.columns(3)
        for j in range(3):
            idx = i + j
            val = st.session_state.ttt_board[idx]
            label = "❌" if val == "X" else ("⭕" if val == "O" else " ")

            if cols[j].button(label, key=f"ttt_{idx}", use_container_width=True, disabled=st.session_state.ttt_game_over):
                if val == " ":
                    st.session_state.ttt_board[idx] = st.session_state.ttt_player

                    if wins_for(st.session_state.ttt_board, st.session_state.ttt_player):
                        st.session_state.ttt_score[st.session_state.ttt_player] += 1
                        st.success(f"🎉 {st.session_state.ttt_player} wins!")
                        st.session_state.ttt_game_over = True

                    elif is_draw(st.session_state.ttt_board):
                        st.warning("Draw!")
                        st.session_state.ttt_game_over = True

                    else:
                        st.session_state.ttt_player = "O" if st.session_state.ttt_player == "X" else "X"

                        if mode == "AI" and st.session_state.ttt_player == "O":
                            ai = best_ai_move()
                            if ai is not None:
                                st.session_state.ttt_board[ai] = "O"

                                if wins_for(st.session_state.ttt_board, "O"):
                                    st.session_state.ttt_score["O"] += 1
                                    st.success("🤖 AI wins!")
                                    st.session_state.ttt_game_over = True
                                elif is_draw(st.session_state.ttt_board):
                                    st.warning("Draw!")
                                    st.session_state.ttt_game_over = True
                                else:
                                    st.session_state.ttt_player = "X"

    if st.button("Restart Tic Tac Toe"):
        st.session_state.ttt_board = [" " for _ in range(9)]
        st.session_state.ttt_player = "X"
        st.session_state.ttt_game_over = False

# ================= NUMBER GUESSING =================
def run_number_guessing():
    st.header("Number Guessing Game")

    if "target" not in st.session_state:
        st.session_state.target = random.randint(1, 100)
        st.session_state.attempts = 0

    guess = st.number_input("Enter your guess (1-100)", 1, 100)

    if st.button("Guess"):
        st.session_state.attempts += 1

        if guess == st.session_state.target:
            st.success(f"🎉 Correct! Attempts: {st.session_state.attempts}")
        elif guess < st.session_state.target:
            st.info("Too low")
        else:
            st.info("Too high")

    if st.button("Restart Number Game"):
        st.session_state.target = random.randint(1, 100)
        st.session_state.attempts = 0

# ================= ROCK PAPER SCISSORS =================
def run_rps():
    st.header("Rock Paper Scissors")

    choices = ["Rock", "Paper", "Scissors"]
    player = st.selectbox("Choose", choices)

    if st.button("Play"):
        ai = random.choice(choices)
        st.write(f"AI chose: {ai}")

        if player == ai:
            st.warning("Draw")
        elif (player == "Rock" and ai == "Scissors") or \
             (player == "Paper" and ai == "Rock") or \
             (player == "Scissors" and ai == "Paper"):
            st.success("You win!")
        else:
            st.error("AI wins!")

# ================= ROUTER =================
if game == "Tic Tac Toe":
    run_tic_tac_toe()
elif game == "Number Guessing":
    run_number_guessing()
else:
    run_rps()
