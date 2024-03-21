# noughtsandcrosses.py

import random
import os.path
import json
random.seed()

def draw_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)

def welcome(board):
    print("Welcome to Noughts and Crosses!")
    draw_board(board)

def initialise_board(board):
    for i in range(3):
        for j in range(3):
            board[i][j] = ' '
    return board

def get_player_move(board):
    while True:
        try:
            move = int(input("Enter the cell number (1-9): "))
            row = (move - 1) // 3
            col = (move - 1) % 3
            if 1 <= move <= 9 and board[row][col] == ' ':
                return row, col
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def choose_computer_move(board):
    # Simple implementation: choose a random empty cell

    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    return random.choice(empty_cells)

def check_for_win(board, mark):
    # Check rows, columns, and diagonals for a win
    for i in range(3):
        if all(board[i][j] == mark for j in range(3)) or all(board[j][i] == mark for j in range(3)):
            return True
    if all(board[i][i] == mark for i in range(3)) or all(board[i][2 - i] == mark for i in range(3)):
        return True
    return False

def check_for_draw(board):
    # Check if all cells are occupied
    return all(board[i][j] != ' ' for i in range(3) for j in range(3))

def play_game(board):
    # Initialize the board
    initialise_board(board)
    
    while True:
        # Get and draw the player's move
        player_row, player_col = get_player_move(board)
        board[player_row][player_col] = 'X'
        draw_board(board)

        # Check for player win or draw
        if check_for_win(board, 'X'):
            return 1
        elif check_for_draw(board):
            return 0

        # Get and draw the computer's move
        print("Computer_move")
        computer_row, computer_col = choose_computer_move(board)
        board[computer_row][computer_col] = 'O'
        draw_board(board)

        # Check for computer win or draw
        if check_for_win(board, 'O'):
            return -1
        elif check_for_draw(board):
            return 0

def menu():
    print("1 - Start Game")
    print("2 - Save score in 'leaderboard.txt'")
    print("3 - View Scores")
    print("q - End Game")
    return input("Enter your choice: ")

def load_scores():
    if os.path.isfile('leaderboard.txt'):
        with open('leaderboard.txt', 'r') as file:
            try:
                leaders = json.load(file)
            except json.JSONDecodeError:
                print("Error decoding leaderboard file. Creating a new one.")
                leaders = {}
    else:
        print("Leaderboard file not found. Creating a new one.")
        leaders = {}
    
    return leaders

def save_score(score):
    name = input("Enter your name: ")
    leaders = load_scores()
    leaders[name] = score
    with open('leaderboard.txt', 'w') as file:
        json.dump(leaders, file)
    print(f"Score {score} saved for {name}.")

def display_leaderboard(leaders):
    print("Leaderboard:")
    for name, score in leaders.items():
        print(f"{name}: {score}")

# Main game loop
if __name__ == '__main__':
    board = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9']]
    welcome(board)
    total_score = 0

    while True:
        choice = menu()

        if choice == '1':
            score = play_game(board)
            total_score += score
            print('Your current score is:', total_score)

        elif choice == '2':
            save_score(total_score)

        elif choice == '3':
            leader_board = load_scores()
            display_leaderboard(leader_board)

        elif choice == 'q':
            print('Thank you for playing the "Unbeatable Noughts and Crosses" game.')
            print('Goodbye')
            break
