

import pygame
import sys

pygame.init()

#CONSTANTS TO MAKE CODE EASIER
width, height = 700, 700
cell = 100
column, rows = 7, 6
rad = 45
y = (255, 215, 0)
b = (173, 216, 230)
w = (255, 255, 255)
bl = (0, 0, 0)
r = (255, 192, 203)



screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")

#GAME BOARD

grid = [
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " ", " ", " "],
]

rows = len(grid)
columns = len(grid[0])

gameboard = [row[:] for row in grid] 

#GAME BOARD INTERFACE
def draw_board(gameboard):
    screen.fill(w)
    for row in range(rows):
        for col in range(column):
            pygame.draw.rect(screen, b, (col * cell, row * cell + cell, cell, cell))
            color = w
            if gameboard[row][col] == "X":
                color = r
            elif gameboard[row][col] == "O":
                color = y
            pygame.draw.circle(screen, color, (col * cell + cell // 2, row * cell + cell + cell // 2), rad)
    pygame.display.update()


def insert_counter(gameboard, col, current_player):
    for row in range(rows - 1, -1, -1):
        if gameboard[row][col] == " ":
            gameboard[row][col] = current_player
            return True
    return False



def board_capacity(gameboard):
    return all(gameboard[0][col] != " " for col in range(column))

#CONNECT 4
def connect_4(gameboard):
  
    for row in range(rows):
        for col in range(column - 3):
            if gameboard[row][col] == gameboard[row][col + 1] == gameboard[row][col + 2] == gameboard[row][col + 3] != " ":
                return True

    for col in range(column):
        for row in range(rows - 3):
            if gameboard[row][col] == gameboard[row + 1][col] == gameboard[row + 2][col] == gameboard[row + 3][col] != " ":
                return True

    for row in range(rows - 3):
        for col in range(column - 3):
            if gameboard[row][col] == gameboard[row + 1][col + 1] == gameboard[row + 2][col + 2] == gameboard[row + 3][col + 3] != " ":
                return True

    for row in range(3, rows):
        for col in range(column - 3):
            if gameboard[row][col] == gameboard[row - 1][col + 1] == gameboard[row - 2][col + 2] == gameboard[row - 3][col + 3] != " ":
                return True

    return False

#WINNER
def end_game(winner):
    font = pygame.font.SysFont("Georgia", 75)
    label = font.render(f"{winner} wins!", 1, r if winner == "X" else y)
    screen.blit(label, (40, 10))
    pygame.display.update()
    pygame.time.wait(3000)

    font = pygame.font.SysFont("Georgia", 50, bold=True)  
    replay_label = font.render("REPLAY? (Y/N)", 1, bl)
    screen.blit(replay_label, (40, height // 2))
    pygame.display.update()

    waiting_for_response = True
    while waiting_for_response:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    waiting_for_response = False
                    return True  
                elif event.key == pygame.K_n:
                    pygame.quit()
                    sys.exit()


    return False  


#PLAYING THE GAME WITH INTERFACE
def play_game(gameboard):
    current_player = "X"
    game_over = False
    draw_board(gameboard)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, w, (0, 0, width, cell))
                posx = event.pos[0]
                if current_player == "X":
                    pygame.draw.circle(screen, r, (posx, cell // 2), rad)
                else:
                    pygame.draw.circle(screen, y, (posx, cell // 2), rad)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, w, (0, 0, width, cell))
                posx = event.pos[0]
                col = posx // cell

                if insert_counter(gameboard, col, current_player):
                    draw_board(gameboard)
                    if connect_4(gameboard):
                        game_over = True
                        if end_game(current_player):
                            
                            gameboard = [[" " for _ in range(column)] for _ in range(rows)]
                            play_game(gameboard) 
                        else:
                            pygame.quit()
                            sys.exit()

                    current_player = "O" if current_player == "X" else "X"

#START SCREEN

def main_menu():
    screen.fill(w)
    font = pygame.font.SysFont("Georgia", 75)
    title = font.render("Connect 4", 1, bl)
    screen.blit(title, (width // 4, height // 4))

    font = pygame.font.SysFont("Georgia", 50)
    play_label = font.render("Play (P)", 1, bl)
    rules_label = font.render("Rules (R)", 1, bl)
    quit_label = font.render("Quit (Q)", 1, bl)
    screen.blit(play_label, (width // 3, height // 2))
    screen.blit(rules_label, (width // 3, height // 2 + 60))
    screen.blit(quit_label, (width // 3, height // 2 + 120))
    pygame.display.update()

    waiting_for_response = True
    while waiting_for_response:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    waiting_for_response = False
                    play_game(gameboard)
                elif event.key == pygame.K_r:
                    waiting_for_response = False
                    rules_screen()
                elif event.key == pygame.K_q:
                    waiting_for_response = False
                    pygame.quit()
                    sys.exit()

#RULES
def rules_screen():
    screen.fill(w)
    font = pygame.font.SysFont("Georgia", 25)
    r = [
        "How to Play",
        "1. decide who will play first, players will alternate",
        "turns incerting a counter",
        "2. On your turn drop a counter on any slot",
        "3. the first to connect 4 either horrizontaly",
        "vertically or diagonally wins!",
        "",
        "(press any key to return)"
    ]
    for i, line in enumerate(r):
        label = font.render(line, 1, bl)
        screen.blit(label, (20, 20 + i * 30)) 
    pygame.display.update()

    waiting_for_response = True
    while waiting_for_response:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting_for_response = False
                main_menu()

#MAIN HOW EVERYTHING COMES TOGETHER
def main():
    main_menu()

if __name__ == "__main__":
    main()
