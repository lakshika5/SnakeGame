import tkinter as tk
import random


GAME_WIDTH = 700
GAME_HEIGHT = 500
SQUARE_SIZE = 20
SNAKE_COLOR = "purple"
FOOD_COLOR = "white"
BACKGROUND_COLOR = "black"


class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)

        self.canvas = tk.Canvas(master, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        self.score = 0
        self.direction = "Right"
        self.running = True

        self.snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake position
        self.food = self.place_food()

        self.draw_snake()
        self.draw_food()

        
        self.master.bind("<KeyPress-Up>", lambda event: self.change_direction("Up"))
        self.master.bind("<KeyPress-Down>", lambda event: self.change_direction("Down"))
        self.master.bind("<KeyPress-Left>", lambda event: self.change_direction("Left"))
        self.master.bind("<KeyPress-Right>", lambda event: self.change_direction("Right"))

        
        self.game_loop()

    def draw_snake(self):
        
        self.canvas.delete("snake")
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=SNAKE_COLOR, tags="snake"
            )

    def draw_food(self):
        
        self.canvas.delete("food")
        x, y = self.food
        self.canvas.create_rectangle(
            x, y, x + SQUARE_SIZE, y + SQUARE_SIZE, fill=FOOD_COLOR, tags="food"
        )

    def place_food(self):
        
        while True:
            x = random.randint(0, (GAME_WIDTH // SQUARE_SIZE) - 1) * SQUARE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SQUARE_SIZE) - 1) * SQUARE_SIZE
            if (x, y) not in self.snake:
                return x, y

    def change_direction(self, new_direction):
        
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if new_direction != opposites.get(self.direction, ""):
            self.direction = new_direction

    def move_snake(self):
        
        head_x, head_y = self.snake[0]
        if self.direction == "Up":
            head_y -= SQUARE_SIZE
        elif self.direction == "Down":
            head_y += SQUARE_SIZE
        elif self.direction == "Left":
            head_x -= SQUARE_SIZE
        elif self.direction == "Right":
            head_x += SQUARE_SIZE

        
        new_head = (head_x, head_y)
        self.snake = [new_head] + self.snake[:-1]

    def check_collision(self):
        """Check for collisions with walls, food, or itself."""
        head_x, head_y = self.snake[0]

        
        if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
            self.running = False

        
        if self.snake[0] in self.snake[1:]:
            self.running = False

        
        if self.snake[0] == self.food:
            self.snake.append(self.snake[-1])  
            self.food = self.place_food()  
            self.score += 1
            self.master.title(f"Snake Game - Score: {self.score}")

    def game_loop(self):
        
        if self.running:
            self.move_snake()
            self.check_collision()
            self.draw_snake()
            self.draw_food()
            self.master.after(100, self.game_loop)
        else:
            self.game_over()

    def game_over(self):
        
        self.canvas.create_text(
            GAME_WIDTH / 2,
            GAME_HEIGHT / 2,
            fill="white",
            font=("Arial", 24, "bold"),
            text=f"Game Over! Final Score: {self.score}",
        )



if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
