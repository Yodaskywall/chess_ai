from board import Board
import pygame
from time import sleep, time
from minimax import minimax

BLACK_CLR = (107,61,15)
WHITE_CLR = (232,195,158)


pygame.init()
width = height = 500

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess mf")

def load_sprites():
    sprites = {

            }
    pieces = ["Bishop", "King", "Knight", "Pawn", "Queen", "Rook"]

    for piece in pieces:
        black = pygame.image.load(f"sprites/black/{piece}.png")
        black = pygame.transform.scale(black, (height // 8, width // 8))

        white = pygame.image.load(f"sprites/white/{piece}.png")
        white = pygame.transform.scale(white, (height // 8, width // 8))

        sprites[piece] = [black, white]

    circle = pygame.image.load("sprites/other/circle.png")
    circle = pygame.transform.scale(circle, (height // 8, width // 8))

    dot = pygame.image.load("sprites/other/dot.png")
    dot = pygame.transform.scale(dot, (height//8, width//8))

    sprites["dot"] = dot
    sprites["circle"] = circle

    return sprites


SPRITES = load_sprites()

def display_piece(screen, piece):
    if piece.colour == "White":
        colour = 1
    else:
        colour = 0

    sprite = SPRITES[piece.name][colour]
    x_cord = piece.x * (width // 8)
    y_cord = piece.y * (height // 8)

    screen.blit(sprite, [x_cord, y_cord])
    

class Square:
    width = width // 8
    height = height // 8


    def __init__(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.state = 0

        #self.cords = [self.width * self.x, height - (self.y * self.height)]
        self.cords = [self.width * self.x, self.y * self.height]

        if self.x % 2 and self.y % 2 or (not self.x % 2 and not self.y % 2):
            self.colour = WHITE_CLR
        else:
            self.colour = BLACK_CLR

    def display(self, screen, game):

        if self.state == 1:
            if self.colour == WHITE_CLR:
                colour = (232, 157, 0)

            else:
                colour = (108, 23, 0)

        else:
            colour = self.colour

        pygame.draw.rect(screen, colour, (self.cords[0], self.cords[1], self.width, self.height))

        if self.state == 2:
            screen.blit(SPRITES["dot"], [self.cords[0], self.cords[1]])

            if game.board.board[self.x][self.y] != 0:
                screen.blit(SPRITES["circle"], [self.cords[0], self.cords[1]])




    def __str__(self):
        return self.colour


class Game:
    def __init__(self):
        self.board = Board()
        self.squares = []
        self.piece_selected = None

        for i in range(8):
            for j in range(8):
                self.squares.append(Square([i,j]))
      
    def get_square(self, mouse_pos):
        x = mouse_pos[0] // (width // 8)
        y = mouse_pos[1] // (height // 8)
        
        return self.squares[x * 8 + y]

        
game = Game()

while game.board.winner is None:

    if game.board.player == "White":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                square = game.get_square(pygame.mouse.get_pos())
                piece = game.board.board[square.x][square.y]
                if piece != 0 and piece.colour == game.board.player:
                    if not(game.piece_selected is None):
                        game.squares[game.piece_selected.x * 8 + game.piece_selected.y].state = 0
                        for sq in game.squares:
                            if sq.state == 2:
                                sq.state = 0

                    square.state = 1
                    game.piece_selected = piece
                    for square_pos in piece.possible_moves():
                        game.squares[square_pos[0] * 8 + square_pos[1]].state = 2

                elif game.piece_selected and [square.x, square.y] in game.piece_selected.possible_moves():
                   game.board.move(game.piece_selected, [square.x, square.y]) 
                   for square in game.squares:
                       if square.state != 0:
                           square.state = 0
                   game.piece_selected = None

                elif game.piece_selected and [square.x, square.y] in [pito[:2] for pito in game.piece_selected.possible_moves()]:
                   for pito in game.piece_selected.possible_moves():
                       if pito[0] == square.x and pito[1] == square.y:
                           game.board.move(game.piece_selected, pito) 
                           for square in game.squares:
                               if square.state != 0:
                                   square.state = 0
                           game.piece_selected = None

                elif piece != 0 and piece.name == "Pawn":
                    pass


    else:
        pre_time = time()
        piece, pos = minimax(game.board, 3, -1000, 1000, False)[1]
        runtime = time() - pre_time
        #print(f"Runtime: {str(runtime)[:6]}s")
        game.board.move(piece, pos)


    for square in game.squares:
        square.display(screen, game)

    for piece in game.board.pieces:
        display_piece(screen, piece)
    
    pygame.display.update()

pygame.font.init()
myfont = pygame.font.SysFont("Times New Roman", 120)
if game.board.winner.upper() != "DRAW":
    text_surface = myfont.render(f"{game.board.winner.upper()}S WIN!", False, (0,0,0))

else:
    text_surface = myfont.render(f"DRAW!", False, (0,0,0))

pygame.draw.rect(screen, (255, 255, 255), (width // 9, height // 2.5, width - (width // 4.5), 150))
screen.blit(text_surface, (width // 9, height // 2.5))
pygame.display.update()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
