import random
import curses
import keyboard
import os

#intialise direction coordinates
UP = (0,-1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Food():
    def __init__(self, width, height, snake_body):
        self.width = width
        self.height = height
        self.position = self.generate_food(snake_body)
    
    def generate_food(self,snake_body):
        while True:
            x = random.randint(0,self.width - 1)
            y = random.randint(0,self.height - 1)

            #ensure the food is not generated in the snakes body
            if (x,y) not in snake_body:
                return (x,y)
            
    def respawn(self,snake_body):
        self.position = self.generate_food(snake_body)



class Snake():
    def __init__(self, body, direction):
        self.body = body
        self.direction = direction
    #take a step in the direction by removing the end of the snakes body and having the head be at the next 'tile' it is moving to
    def take_step(self, position):
        self.body = self.body[1:] + [position]
    
    def set_direction(self, direction):
        self.direction = direction
    
    def head(self):
        return self.body[-1]


class Game():
    def __init__(self, height,width):
        self.height = height
        self.width = width
        #empty at first can be easily changed in the main function
        self.board = []
        #Snake inital Position
        self.snake = Snake([(0, 1), (0, 2), (0, 3), (0, 4)], DOWN)
        self.food = Food(self.width,self.height,self.snake.body)
  
    
    
    
    

    def render(self, stdscr):
        stdscr.clear()

        # Draw borders
        for x in range(self.width + 2):
            stdscr.addstr(0, x, "#")
            stdscr.addstr(self.height + 1, x, "#")
        for y in range(self.height + 2):
            stdscr.addstr(y, 0, "#")
            stdscr.addstr(y, self.width + 1, "#")

        # Draw snake
        for x, y in self.snake.body[:-1]:
            stdscr.addstr(y + 1, x + 1, "o")
        head_x, head_y = self.snake.head()
        stdscr.addstr(head_y + 1, head_x + 1, "X")

        # Draw food
        fx, fy = self.food.position
        stdscr.addstr(fy + 1, fx + 1, "*")

        # Score display
        stdscr.addstr(self.height + 3, 0, f"Score: {len(self.snake.body) - 3}")
        stdscr.refresh()

    
    
    def move_snake(self):
        x,y = self.snake.direction
        head_x,head_y = self.snake.head()
        new_head = (head_x + x, head_y + y)
        #if the new head isnt within the boundaries or game over
        if not (0<= new_head[0] < self.width and 0 <= new_head[1] < self.height):
            print('You crashed into the wall. Game Over\n')
            return False
        if new_head in self.snake.body:
            print('You crashed into yourself. Game Over\n')
            return False
        #Snake grows by not removing its end and instead just changing the position of the head and everything else follows
        if new_head == self.food.position:
            self.snake.body.append(new_head)
            self.food.respawn(self.snake.body)
        else:
            self.snake.take_step(new_head)
        return True


def main(stdscr):    
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True) 
    stdscr.timeout(100)  # Refresh every 100 ms
    #May crash if terminal is not large enough. Command Prompt Reccomended. Change dimensions here if needed
    game = Game(height=20, width=20)
    key_map = {
        curses.KEY_UP: UP,
        curses.KEY_DOWN: DOWN,
        curses.KEY_LEFT: LEFT,
        curses.KEY_RIGHT: RIGHT
    }

    last_direction = game.snake.direction
    while True:
        key = stdscr.getch()
        new_direction = key_map.get(key)

        #Prevent backing into itself and game being over
        if new_direction and (new_direction[0] != -last_direction[0] or new_direction[1] != -last_direction[1]):
            game.snake.set_direction(new_direction)
            last_direction = new_direction

        if not game.move_snake():
            stdscr.addstr(game.height // 2, game.width // 2 - 5, "GAME OVER")
            stdscr.refresh()
            curses.napms(2000)
            break

        game.render(stdscr)

def run_game():
    #Run the game for 3 rounds
    round_counter = 0
    max_rounds = 3
    while round_counter < max_rounds:
        curses.wrapper(main)
        round_counter += 1
        print(f'{round_counter} ended\n')
        if round_counter < max_rounds:

            input('Press Enter to play another round\n')
        else: 
            print('Thanks for playing!')

run_game()