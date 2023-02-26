import pygame
import sys
import random
import time
import math
import testRecorded

##### CONFIG ###########
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = pygame.display.get_desktop_sizes()[0]

BAR_COLOR = pygame.Color(0,128,255) # blue
BAR_WIDTH = WINDOW_WIDTH * 0.9 * 0.05
BAR_HEIGHT = WINDOW_HEIGHT * 0.9 * 0.89
BAR_X = WINDOW_WIDTH * 0.9 * 0.05
BAR_Y = WINDOW_HEIGHT * 0.9 * 0.05

NOTE_COLOR = pygame.Color(0,255, 162) # green
NOTE_WIDTH = 20
NOTE_HEIGHT = 20
NOTE_START_X = WINDOW_WIDTH + 1

CURSOR_COLOR = pygame.Color(255, 255, 255) # white
CURSOR_WIDTH = BAR_WIDTH + 30
CURSOR_HEIGHT = 150
CURSOR_START_Y = BAR_Y + BAR_HEIGHT - CURSOR_HEIGHT

#### END OF CONFIG #####

class Cursor:
    def __init__(self) -> None:
        self.obj = pygame.Rect(BAR_X-15, CURSOR_START_Y, CURSOR_WIDTH, CURSOR_HEIGHT)
    
    def move(self):
        key = pygame.key.get_pressed()
        dist = 1
        if key[pygame.K_UP] and self.obj.top > BAR_Y:
           self.obj = self.obj.move(0, -dist)
        if key[pygame.K_DOWN] and self.obj.top + self.obj.height < BAR_Y + BAR_HEIGHT:
           self.obj = self.obj.move(0, dist)
    
    def eeg_move(self, power):
        self.obj = self.obj.move(0, power*5)
    
    def get_obj(self):
        return self.obj
    
    def get_x(self):
        return self.obj.left

    def get_y(self):
        return self.obj.top

class Note:
    
    def __init__(self, x, y) -> None:
        self.obj = pygame.Rect(x, y, NOTE_WIDTH, NOTE_HEIGHT)
        
    def move(self):
        self.obj = self.obj.move(-1, 0)

    def get_obj(self) -> pygame.Rect:
        return self.obj

    def get_x(self) -> int:
        return self.obj.left

    def get_y(self) -> int:
        return self.obj.top

    def is_touching_cursor(self, cursor_x, cursor_y):
        if self.get_x() == (cursor_x + CURSOR_WIDTH)//2:
            if self.get_y() >= cursor_y and self.get_y() <= cursor_y + CURSOR_HEIGHT:
                return True
        return False

class RhythmGame:

    unit_time = 250
    notes_distance = 1000
    min_notes = 10
    max_notes = 20
    
    def __init__(self) -> None:
        self.window_width = 0.9 * WINDOW_WIDTH
        self.window_height = 0.9 * WINDOW_HEIGHT

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)

        self.cursor = Cursor()
        self.notes = []
        self.hit_effects = []

    def add_hit_effect(self, note: Note):
        obj = note.get_obj()
        effect = pygame.draw.circle(self.screen, NOTE_COLOR, 
                                    (obj.centerx, obj.centery), 10, 5)
        self.hit_effects.append(effect)
        
    def update_screen(self) -> None:
        self.screen.fill((0, 0, 0)) # black
        # draw focus bar
        self.draw_focus_bar()
        # draw cursor
        self.cursor.move()
        self.draw_cursor(self.cursor.get_obj())
        # draw all notes to the current frame
        self.handle_notes()
        for note in self.notes:
            # get the note's obj(rect)
            self.draw_note(note.get_obj())

        # handle notes
        for note in self.notes:
            note.move()
            if note.is_touching_cursor(self.cursor.get_x(), self.cursor.get_y()): # hit
                self.add_hit_effect(note)
            if note.get_x() < 0: # miss
                self.notes.remove(note)
        
        # render hit effects
        for i in range(len(self.hit_effects)):
            effect = self.hit_effects[i]
            radius = effect.height//2
            if radius < 100:
                effect = pygame.draw.circle(self.screen, NOTE_COLOR,
                                            (effect.centerx, effect.centery), 
                                            radius+1, 5)
                self.hit_effects[i] = effect
            else:
                self.hit_effects.remove(effect)
                
            if effect.top <= 1 or effect.left <= 1:
                self.hit_effects.remove(effect)
            
    def display(self) -> None:
        pygame.display.flip()
    
    def draw_focus_bar(self) -> None:
        rectangle = pygame.Rect(BAR_X, BAR_Y, BAR_WIDTH, BAR_HEIGHT)
        pygame.draw.rect(self.screen, BAR_COLOR, rectangle, 0, border_radius=1)
    
    def draw_cursor(self, cursor_obj) -> None:
        pygame.draw.rect(self.screen, CURSOR_COLOR, cursor_obj, 5, border_radius=1)

    def draw_note(self, note_obj) -> None:
        pygame.draw.rect(self.screen, NOTE_COLOR, note_obj)

    def handle_notes(self):
        if len(self.notes) == 0:
            prev_note_x = NOTE_START_X
            prev_note_y = random.randint(math.ceil(BAR_Y + BAR_HEIGHT/2), math.ceil(BAR_Y + BAR_HEIGHT - NOTE_HEIGHT))

        if len(self.notes) < RhythmGame.min_notes:
            note_y = random.randint(math.ceil(BAR_Y), math.ceil(BAR_Y +
                BAR_HEIGHT - NOTE_HEIGHT))
            if len(self.notes) > 0:
                prev_note_x = self.notes[-1].get_x()
                prev_note_y = self.notes[-1].get_y()
                RhythmGame.notes_distance = RhythmGame.unit_time * random.randint(1, 4)
                note_x = prev_note_x + RhythmGame.notes_distance
            else:
                note_x = NOTE_START_X

            if self.is_valid_note(note_x, note_y, prev_note_x, prev_note_y):
                self.create_note(note_x, note_y)
            else:
                rv = random.randint(1, 4) # 1, 2, 3, 4
                if (rv == 1):
                    # increase x 25%
                    note_x += RhythmGame.notes_distance * random.randint(1, 2)    
                else:
                    # or decrease y 75%
                    offset = prev_note_y - note_y
                    note_y += offset*0.25*random.randint(2, 4)
                self.create_note(note_x, note_y)

    def create_note(self, x, y) -> None:
        self.notes.append(Note(x, y))

    def is_valid_note(self, x, y, prev_x, prev_y) -> bool:
        if abs(x - prev_x) <= 750 and abs(y - prev_y) >= 100:
            return False
        return True

def main():
    game = RhythmGame()
    
    # create a random number generator
    random.seed(time.time())
    
    recorder, trigger, receiver = testRecorded.init_stream(bufsize=0.1, winsize=0.1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        filtered_data = testRecorded.filter_data(receiver=receiver, seconds_sleep=0, padlen=2)
        average_voltage = testRecorded.average_voltage(filtered_data)
        print("ave_volt:", average_voltage)
        game.cursor.eeg_move(average_voltage)

        game.update_screen()
        game.display()
        
if __name__ == "__main__":
    main()
        