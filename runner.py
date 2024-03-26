from minesweeper import Minesweeper, MinesweeperAI
import time


# Game configuration
HEIGHT, WIDTH, MINES = 10, 10, 20


# Initialize game and AI
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH)
flagged_cells = set()


def print_board():
    """Function to print the current board state to the console."""
    # Print column numbers
    print("   ", end="")
    for j in range(WIDTH):
        print(f"{j:^3}", end="")
    print("\n  " + "----" * WIDTH)


    for i in range(HEIGHT):
        # Print row number
        print(f"{i:^2}|", end="")
        for j in range(WIDTH):
            if (i, j) in flagged_cells:
                print(f"{'F':^3}", end="")
            elif (i, j) in ai.moves_made:
                if game.is_mine((i, j)):
                    print(f"{'X':^3}", end="")
                else:
                    print(f"{game.nearby_mines((i, j)):^3}", end="")
            else:
                print(f"{'*':^3}", end="")
        print()


    print()




game_over = False


while not game_over:
    print("Minesweeper")
    print_board()


    user_input = input("Enter your move (row col), 'ai' for AI move, 'flag row col' to mark a location, or 'exit' to quit: ")


    if user_input.lower() == 'exit':
        break
    elif user_input.lower() == 'ai':
        move = ai.make_safe_move() or ai.make_random_move()
        if move is None:
            print("No moves left.")
            break
        else:
            print(f"AI move: {move}")
            if game.is_mine(move):
                print("AI hit a mine! Game over.")
                game_over = True
            else:
                ai.add_knowledge(move, game.nearby_mines(move))
    elif user_input.lower().startswith('flag'):
      try:
          _, row, col = user_input.split()
          row, col = int(row), int(col)
          # Add the flagged cell to the set
          flagged_cells.add((row, col))
      except ValueError:
          print("Invalid input. Please enter a valid move or flag.")


    else:
        try:
            row, col = map(int, user_input.split())
            if game.is_mine((row, col)):
                print("Mine hit! Game over.")
                game_over = True
            else:
                ai.add_knowledge((row, col), game.nearby_mines((row, col)))
                print(ai.knowledge)
        except ValueError:
            print("Invalid input. Please enter a valid move.")


    if game.won():
        print("Congratulations! You have won!")
        game_over = True


    time.sleep(1)
