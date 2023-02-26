import pygame
import sys
import time


##### CONFIG ###########
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_desktop_sizes()[0]

BAR_COLOR = pygame.Color(0,128,255) # blue
BAR_WIDTH = WINDOW_WIDTH * 0.9 * 0.05
BAR_HEIGHT = WINDOW_HEIGHT * 0.9 * 0.9
BAR_X = WINDOW_WIDTH * 0.9 * 0.05
BAR_Y = WINDOW_HEIGHT * 0.9 * 0.05

NOTE_COLOR = pygame.Color(0,255, 162) # green
NOTE_WIDTH = 5
NOTE_HEIGHT = 5
NOTE_START_X = WINDOW_WIDTH + 1

CURSOR_COLOR = pygame.Color(255, 255, 255) # white
CURSOR_WIDTH = BAR_WIDTH + 30
CURSOR_HEIGHT = 150
CURSOR_START_Y = BAR_Y + BAR_HEIGHT - CURSOR_HEIGHT

#### END OF CONFIG #####

class Cursor:
    def __init__(self) -> None:
        self.obj = pygame.Rect(BAR_X-15, CURSOR_START_Y, CURSOR_WIDTH, CURSOR_HEIGHT)
    
    def cursor_move(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_UP] and self.obj.top > BAR_Y:
           self.obj = self.obj.move(0, -dist)
        if key[pygame.K_DOWN] and self.obj.top + self.obj.height < BAR_Y + BAR_HEIGHT:
           self.obj = self.obj.move(0, dist)

        print(self.obj.top, BAR_Y)
    
    def get_obj(self):
        return self.obj

class Notes:

    x_pos = -1
    
    def __init__(self, y) -> None:
        self.obj = pygame.Rect(Notes.x_pos, y)
        
    def move(self):
        self.obj.move(-1, 0)

    def get_obj(self) -> pygame.Rect:
        return self.obj

class RhythmGame:
    
    def __init__(self) -> None:
        self.window_width = 0.9 * WINDOW_WIDTH
        self.window_height = 0.9 * WINDOW_HEIGHT

        # self.screen = None
        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

        self.cursor = Cursor()
        self.notes = []

    def update_screen(self) -> None:
        self.screen.fill((0, 0, 0)) # black
        # draw focus bar
        self.draw_focus_bar()
        # draw cursor
        self.draw_cursor(self.cursor.get_obj())
        # draw all notes to the current frame
        for note in self.notes:
            # get the note's obj(rect)
            self.draw_note(note.get_obj())
            
 
    def display(self) -> None:
        self.update_screen()
        pygame.display.flip()
    
    def draw_focus_bar(self) -> None:
        rectangle = pygame.Rect(BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT)
        pygame.draw.rect(self.screen, BAR_COLOR, rectangle, 0, border_radius=1)
    
    def draw_cursor(self, cursor_obj) -> None:
        pygame.draw.rect(self.screen, CURSOR_COLOR, cursor_obj, 5, border_radius=1)

    def draw_note(self, note_obj) -> None:
        pygame.draw.rect(self.screen, NOTE_COLOR, note_obj)

def main():
    game = RhythmGame()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        
        game.cursor.cursor_move()
        game.display()
        
if __name__ == "__main__":
    main()
        