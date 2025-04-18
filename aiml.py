import streamlit as st
import math
from queue import PriorityQueue
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Set page configuration
st.set_page_config(page_title="AI Experiments", layout="centered")

# Define tab names
tab_names = [
    "Tic Tac Toe (Human vs AI)",
    "Water Jug (Hill Climbing)",
    "8 Puzzle (Greedy Best FS)",
    "Find-S Algorithm",
    "Candidate Elimination"
]

# Initialize session state for tab selection
if 'active_tab' not in st.session_state:
    st.session_state['active_tab'] = tab_names[0]

# Create tabs
tabs = st.tabs(tab_names)

# Function to set active tab
def set_active_tab(tab_name):
    st.session_state['active_tab'] = tab_name
    st.rerun()

# Tic Tac Toe (Human vs AI)
with tabs[0]:
    st.header("Tic Tac Toe: Human vs AI")
    st.write("You are X and the AI is O. Click on a cell to make your move.")

    # Initialize game state if not present
    if "ttt_board" not in st.session_state:
        st.session_state.ttt_board = [""] * 9
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "message" not in st.session_state:
        st.session_state.message = ""

    HUMAN = "X"
    AI = "O"

    def check_winner(board):
        win_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
            (0, 4, 8), (2, 4, 6)              # diagonals
        ]
        for a, b, c in win_combinations:
            if board[a] == board[b] == board[c] and board[a] != "":
                return board[a]
        return None

    def is_board_full(board):
        return "" not in board

    def minimax(board, depth, is_maximizing):
        winner = check_winner(board)
        if winner == AI:
            return 1, None
        elif winner == HUMAN:
            return -1, None
        elif is_board_full(board):
            return 0, None

        if is_maximizing:
            best_score = -math.inf
            best_move = None
            for i in range(9):
                if board[i] == "":
                    board[i] = AI
                    score, _ = minimax(board, depth + 1, False)
                    board[i] = ""
                    if score > best_score:
                        best_score = score
                        best_move = i
            return best_score, best_move
        else:
            best_score = math.inf
            best_move = None
            for i in range(9):
                if board[i] == "":
                    board[i] = HUMAN
                    score, _ = minimax(board, depth + 1, True)
                    board[i] = ""
                    if score < best_score:
                        best_score = score
                        best_move = i
            return best_score, best_move

    def ai_move():
        _, move = minimax(st.session_state.ttt_board, 0, True)
        if move is not None:
            st.session_state.ttt_board[move] = AI

    def human_move(idx):
        if st.session_state.ttt_board[idx] == "" and not st.session_state.game_over:
            st.session_state.ttt_board[idx] = HUMAN
            winner = check_winner(st.session_state.ttt_board)
            if winner:
                st.session_state.game_over = True
                st.session_state.message = f"Player {winner} wins!"
            elif is_board_full(st.session_state.ttt_board):
                st.session_state.game_over = True
                st.session_state.message = "It's a draw!"
            else:
                ai_move()
                winner = check_winner(st.session_state.ttt_board)
                if winner:
                    st.session_state.game_over = True
                    st.session_state.message = f"Player {winner} wins!"
                elif is_board_full(st.session_state.ttt_board):
                    st.session_state.game_over = True
                    st.session_state.message = "It's a draw!"

    def reset_ttt():
        st.session_state.ttt_board = ["" for _ in range(9)]
        st.session_state.game_over = False
        st.session_state.message = ""

    # Render the Tic Tac Toe board and controls
    move_made = False
    for i in range(3):
        cols = st.columns(3)
        for j in range(3):
            idx = i * 3 + j
            cell = st.session_state.ttt_board[idx] if st.session_state.ttt_board[idx] != "" else " "
            if cols[j].button(cell, key=f"ttt_{idx}") and not st.session_state.game_over:
                human_move(idx)
                move_made = True

    if move_made:
        st.rerun()

    if st.session_state.message:
        st.success(st.session_state.message)

    if st.button("Reset Game", key="reset_game"):
        reset_ttt()
        st.rerun()

# Water Jug with graphical UI
with tabs[1]:
    st.header("Water Jug Problem (Hill Climbing)")
    st.write("Enter the capacities for Jug 1 and Jug 2 and the target volume.")
    jug1 = st.number_input("Jug 1 Capacity", value=3, min_value=1)
    jug2 = st.number_input("Jug 2 Capacity", value=5, min_value=1)
    target = st.number_input("Target Volume", value=4, min_value=1)

    def plot_jugs(j1_cap, j1_amount, j2_cap, j2_amount):
        fig, ax = plt.subplots()
        # Jug1
        ax.add_patch(Rectangle((0, 0), 1, j1_cap, edgecolor='black', facecolor='none'))
        ax.add_patch(Rectangle((0, 0), 1, j1_amount, facecolor='blue'))
        ax.text(0.5, -0.5, f"Jug1: {j1_amount}/{j1_cap}", ha='center')
        # Jug2
        ax.add_patch(Rectangle((2, 0), 1, j2_cap, edgecolor='black', facecolor='none'))
        ax.add_patch(Rectangle((2, 0), 1, j2_amount, facecolor='blue'))
        ax.text(2.5, -0.5, f"Jug2: {j2_amount}/{j2_cap}", ha='center')
        ax.set_xlim(-1, 4)
        ax.set_ylim(-1, max(j1_cap, j2_cap) + 1)
        ax.set_aspect('equal')
        ax.axis('off')
        st.pyplot(fig)

    def hill_climbing(j1, j2, goal):
        visited = set()
        queue = [(0, 0)]
        path = []
        while queue:
            a, b = queue.pop(0)
            if (a, b) in visited:
                continue
            visited.add((a, b))
            path.append((a, b))
            if a == goal or b == goal:
                return path
            possible = [
                (j1, b),      # Fill Jug1
                (a, j2),      # Fill Jug2
                (0, b),       # Empty Jug1
                (a, 0),       # Empty Jug2
                (min(j1, a + b), b - (min(j1, a + b) - a)),  # Pour from Jug2 to Jug1
                (a - (min(j2, a + b) - b), min(j2, a + b))   # Pour from Jug1 to Jug2
            ]
            for state in possible:
                if state not in visited:
                    queue.append(state)
        return []

    if st.button("Solve Water Jug"):
        solution = hill_climbing(jug1, jug2, target)
        if solution:
            st.write("Solution Steps:")
            for idx, (a, b) in enumerate(solution):
                st.write(f"Step {idx + 1}: Jug1 = {a}, Jug2 = {b}")
                plot_jugs(jug1, a, jug2, b)
        else:
            st.error("No solution found.")

# 8 Puzzle with grid display
with tabs[2]:
    st.header("8 Puzzle Problem (Greedy Best First Search)")
    st.write("Enter the start and goal states as comma-separated 9 digits (use 0 for blank).")
    start_input = st.text_input("Start State", "1,2,3,4,5,6,7,8,0")
    goal_input = st.text_input("Goal State", "1,2,3,4,5,6,7,8,0")

    def display_puzzle(state):
        for i in range(3):
            cols = st.columns(3)
            for j in range(3):
                idx = i * 3 + j
                value = state[idx]
                if value == 0:
                    cols[j].write(" ")
                else:
                    cols[j].write(value)

    def heuristic(state, goal):
        return sum(1 for i in range(9) if state[i] != goal[i])

    def get_moves(pos):
        moves = []
        row, col = pos // 3, pos % 3
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 3 and 0 <= c < 3:
                moves.append(r * 3 + c)
        return moves

    def greedy_bfs(start, goal):
        visited = set()
        pq = PriorityQueue()
        pq.put((heuristic(start, goal), start, []))
        while not pq.empty():
            h, current, path = pq.get()
            if current == goal:
                return path + [current]
            visited.add(tuple(current))
            zero_pos = current.index(0)
            for move in get_moves(zero_pos):
                new_state = current[:]
                new_state[zero_pos], new_state[move] = new_state[move], new_state[zero_pos]
                if tuple(new_state) not in visited:
                    pq.put((heuristic(new_state, goal), new_state, path + [current]))
        return []

    if st.button("Solve Puzzle"):
        try:
            start_state = [int(i.strip()) for i in start_input.split(",")]
            goal_state = [int(i.strip()) for i in goal_input.split(",")]
            path = greedy_bfs(start_state, goal_state)
            if path:
                st.write("Solution Path:")
                for idx, state in enumerate(path):
                    st.write(f"Step {idx + 1}:")
                    display_puzzle(state)
            else:
                st.error("No solution found.")
        except Exception as e:
            st.error("Invalid input. Please enter 9 comma-separated numbers for each state.")

# Find-S with intermediary hypotheses
with tabs[3]:
    st.header("Find-S Algorithm")
    st.write("Enter positive examples (one per line, attributes comma-separated). Example:")
    st.code("sunny,warm,normal,strong,yes")
    find_s_input = st.text_area("Enter positive examples:")
    if st.button("Run Find-S"):
        try:
            lines = [line.split(',') for line in find_s_input.splitlines() if line.strip() and line.strip().lower().endswith("yes")]
            if not lines:
                st.error("Please enter at least one positive example ending with 'yes'.")
            else:
                hypothesis = lines[0][:-1]
                st.write("Initial Hypothesis:")
                st.table([hypothesis])
                for ex in lines[1:]:
                    for i in range(len(hypothesis)):
                        if hypothesis[i] != ex[i]:
                            hypothesis[i] = "?"
                    st.write(f"After example {ex[:-1]}:")
                    st.table([hypothesis])
                st.write("Final Hypothesis:")
                st.table([hypothesis])
        except Exception as e:
            st.error("Error processing input. Ensure the format is correct.")

# Candidate Elimination with intermediary S and G
with tabs[4]:
    st.header("Candidate Elimination Algorithm")
    st.write("Enter examples (one per line, attributes comma-separated, last value as yes/no).")
    st.code("sunny,warm,normal,strong,yes\nsunny,cold,high,strong,no")
    ce_input = st.text_area("Enter dataset:")
    if st.button("Run Candidate Elimination"):
        try:
            lines = [line.split(',') for line in ce_input.splitlines() if line.strip()]
            if not lines:
                st.error("Please enter some examples.")
            else:
                n_attrs = len(lines[0]) - 1
                S = ["∅" for _ in range(n_attrs)]
                G = [["?" for _ in range(n_attrs)]]
                st.write("Initial Specific Hypothesis (S):")
                st.table([S])
                st.write("Initial General Hypothesis (G):")
                st.table([G])
                for ex in lines:
                    attrs, label = ex[:-1], ex[-1].strip().lower()
                    if label == "yes":
                        for i in range(n_attrs):
                            if S[i] == "∅":
                                S[i] = attrs[i]
                            elif S[i] != attrs[i]:
                                S[i] = "?"
                        G = [g for g in G if all(g[i] == "?" or g[i] == attrs[i] for i in range(n_attrs))]
                    elif label == "no":
                        G_new = []
                        for g in G:
                            if any(g[i] == "?" or g[i] == attrs[i] for i in range(n_attrs)):
                                for j in range(n_attrs):
                                    if g[j] == "?" and attrs[j] != S[j]:
                                        new_g = g[:]
                                        new_g[j] = S[j]
                                        G_new.append(new_g)
                        G = G_new
                    st.write(f"After example {ex}:")
                    st.write("Specific Hypothesis (S):")
                    st.table([S])
                    st.write("General Hypotheses (G):")
                    if G:
                        st.table(G)
                    else:
                        st.write("No general hypotheses.")
                st.write("Final Specific Hypothesis (S):")
                st.table([S])
                st.write("Final General Hypotheses (G):")
                if G:
                    st.table(G)
                else:
                    st.write("No general hypotheses.")
        except Exception as e:
            st.error("Error processing dataset. Ensure the format is correct.")