import pygame
import random
import columns_functions
from pygame.locals import QUIT

fps = 30
jewels = ['S', 'T', 'V', 'W', 'X', 'Y', 'Z']

def jewel_color(jewel: str) -> tuple:
    '''
    Given a jewel (letter) returns a color
    '''
    if jewel == 'S':
        return (255, 0, 0) #Red
    elif jewel == 'T':
        return (255, 165, 0) #Orange
    elif jewel == 'V':
        return (255, 255, 0) #Yellow
    elif jewel == 'W':
        return (0, 128, 0) #Green
    elif jewel == 'X':
        return (0, 255, 255) #Cyan
    elif jewel == 'Y':
        return (75, 0, 130) #Purple
    elif jewel == 'Z':
        return (139, 69, 19) #Brown

class ColumnState:
    def __init__(self, col: int, row: int) -> None:
        self._game = columns_functions.GameState(col, row)

        self._running = True
        self._paused = False
        self._over = False
        self._status = ''
        self._background_color = pygame.Color(0, 0, 0)
        self._count = 0

        self._surface = None

    def run(self) -> None:
        '''
        Starts up the pygame interface
        '''
        try:
            pygame.init()
            self._surface = pygame.display.set_mode((300, 650))
            self._surface.fill(self._background_color)

            running = True
            pause = False
            clock = pygame.time.Clock()

            nextTick = fps

            while running:
                clock.tick(fps)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    elif self._over:
                        self._paused = True
                        self._status = 'GAME OVER'
                    elif event.type == pygame.KEYDOWN:

                        if event.key == pygame.K_SPACE:
                            self._game.rotate_faller()
                            self._paused = False
                        elif event.key == pygame.K_LEFT:
                            self._game.move_faller_left()
                            self._paused = False
                        elif event.key == pygame.K_RIGHT:
                            self._game.move_faller_right()
                            self._paused = False
                        elif event.key == pygame.K_p:
                            self._paused = True
                            self._status = "Paused"
                        else:
                            self._paused = False
                            self._status = ""

                nextTick -= 1

                if nextTick == 0:
                    if not self._paused:
                        if self._game.game_tick():
                            self._status = "Game Over"
                            self._over = True
                            self._running = False
                            self._paused = True

                        if not self._game._faller.active:
                            contents = random.sample(jewels, 3)
                            column = random.randint(1, self._game.columns())
                            self._game.create_faller(column, contents)

                    if not self._paused:
                        self._count += 1
                    nextTick = 30
                
                self.update_board()
        finally:
            pygame.quit()

    def update_board(self):
        '''
        Updates the squares in the board to their right color
        '''
        board = self._game.get_board()
        for row in range(self._game.rows()):
            for column in range(self._game.columns()):

                jewel = board[column][row]
                state = self._game.get_cell_state(column, row)
                rawColor = None

                if state == columns_functions.MATCHED_CELL:
                    rawColor = (255, 255, 255)
                elif state == columns_functions.EMPTY_CELL:
                    rawColor = (0, 0, 0)
                else:
                    rawColor = jewel_color(jewel)
                
                rect = pygame.Rect(column*50, row*50, 50, 50)

                pygame.draw.rect(self._surface, rawColor, rect, 0)

                if state == columns_functions.FALLER_STOPPED_CELL:
                    pygame.draw.rect(self._surface, pygame.Color(255, 255, 255), rect, 2)

        self.paused()
        pygame.display.flip()
    
    def paused(self) -> None:
        '''
        Sets up the game over, paused, and non paused text
        '''
        green = (0,255,127)
        red = (255,0,0)
        if (self._over):
            myfont2 = pygame.font.SysFont("comicsansms", 40)
            text2 = myfont2.render("GAME OVER", 50, green)
            text2_center = (40,300)
            self._surface.blit(text2, text2_center)
            myfont = pygame.font.SysFont("comicsansms", 40)
            text1 = myfont.render('Score: ' + str(self._count), 100, red)
            text_center = (40, 500)
            self._surface.blit(text1, text_center)

        elif (self._paused):
            myfont = pygame.font.SysFont("comicsansms", 20)
            myfont2 = pygame.font.SysFont("comicsansms", 20)
            text1 = myfont.render(self._status, 100, red)
            text_center = ((self._surface.get_width()/2 - 20),(self._surface.get_height()/2))
            self._surface.blit(text1, text_center)
            text2 = myfont2.render("Press any key to continue", 100, red)
            text2_center = (40, 400)
            self._surface.blit(text2, text2_center)
            
        else:
            myfont2 = pygame.font.SysFont("comicsansms", 20)
            text2 = myfont2.render("Press 'p' to pause", 50, green)
            text2_center = (10,10)
            self._surface.blit(text2, text2_center)

if __name__ == '__main__':
    '''
    Initializes the game if this file is being run as the main file
    '''
    game = ColumnState(6, 13)
    game.run()