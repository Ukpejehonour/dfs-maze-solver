from turtle import Turtle, Screen
import random
import time

# --- Screen setup ---
screen = Screen()
screen.bgcolor("black")
screen.setup(800, 800)
screen.title("Maze Solver Robot")
screen.tracer(0)  # turn off automatic drawing

# --- Turtles ---
drawer = Turtle()
drawer.hideturtle()
drawer.speed(0)
drawer.pensize(2)
drawer.color("lime")

robot = Turtle()
robot.shape("turtle")
robot.color("red")
robot.penup()
robot.speed(0)

goal = Turtle()
goal.shape("circle")
goal.color("green")
goal.penup()
goal.speed(0)

# --- Maze setup ---
CELL_SIZE = 25
ROWS = 15
COLS = 15

maze = [[{"top": True, "bottom": True, "left": True, "right": True, "visited": False}
         for _ in range(COLS)] for _ in range(ROWS)]

# --- Draw a single cell ---
def draw_cell(x, y, cell):
    start_x = -COLS * CELL_SIZE // 2 + x * CELL_SIZE
    start_y = ROWS * CELL_SIZE // 2 - y * CELL_SIZE
    drawer.penup()
    drawer.goto(start_x, start_y)

    if cell["top"]:
        drawer.pendown()
        drawer.goto(start_x + CELL_SIZE, start_y)
        drawer.penup()
    drawer.goto(start_x + CELL_SIZE, start_y)

    if cell["right"]:
        drawer.pendown()
        drawer.goto(start_x + CELL_SIZE, start_y - CELL_SIZE)
        drawer.penup()
    drawer.goto(start_x + CELL_SIZE, start_y - CELL_SIZE)

    if cell["bottom"]:
        drawer.pendown()
        drawer.goto(start_x, start_y - CELL_SIZE)
        drawer.penup()
    drawer.goto(start_x, start_y - CELL_SIZE)

    if cell["left"]:
        drawer.pendown()
        drawer.goto(start_x, start_y)
        drawer.penup()

# --- Draw entire maze ---
def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            draw_cell(x, y, maze[y][x])
    screen.update()

# --- Maze generation using DFS ---
def generate_maze():
    store = []
    current = (0, 0)
    maze[0][0]["visited"] = True
    visited = 1
    total_cells = ROWS * COLS

    while visited < total_cells:
        x, y = current
        neighbors = []

        if y > 0 and not maze[y - 1][x]["visited"]:
            neighbors.append(("top", (x, y - 1)))
        if y < ROWS - 1 and not maze[y + 1][x]["visited"]:
            neighbors.append(("bottom", (x, y + 1)))
        if x > 0 and not maze[y][x - 1]["visited"]:
            neighbors.append(("left", (x - 1, y)))
        if x < COLS - 1 and not maze[y][x + 1]["visited"]:
            neighbors.append(("right", (x + 1, y)))

        if neighbors:
            direction, (nx, ny) = random.choice(neighbors)

            if direction == "top":
                maze[y][x]["top"] = False
                maze[ny][nx]["bottom"] = False
            elif direction == "bottom":
                maze[y][x]["bottom"] = False
                maze[ny][nx]["top"] = False
            elif direction == "left":
                maze[y][x]["left"] = False
                maze[ny][nx]["right"] = False
            elif direction == "right":
                maze[y][x]["right"] = False
                maze[ny][nx]["left"] = False

            store.append(current)
            current = (nx, ny)
            maze[ny][nx]["visited"] = True
            visited += 1
        elif store:
            current = store.pop()

# --- Robot helpers ---
def move_cell(x, y):
    rx = -COLS * CELL_SIZE // 2 + x * CELL_SIZE + CELL_SIZE / 2
    ry = ROWS * CELL_SIZE // 2 - y * CELL_SIZE - CELL_SIZE / 2
    robot.goto(rx, ry)

# --- Maze solving ---
def maze_solving():
    visited = set()
    path = [(0,0)]
    moves = 0
    start_time = time.time()

    while path:
        x, y = path[-1]
        visited.add((x, y)) 
        move_cell(x, y)
        robot.pendown()
        screen.update()
        time.sleep(0.05)

        if (x, y) == (COLS-1, ROWS-1):
            robot.color("gold")
            print(f"[GOAL] Reached in {moves} moves, {round(time.time() - start_time, 2)} seconds")
            screen.update()
            return

        cell = maze[y][x]
        moved = False
        directions = [
            ("right", (x+1, y)),
            ("bottom", (x, y+1)),
            ("left", (x-1, y)),
            ("top", (x, y-1))
        ]

        for direction, (nx, ny) in directions:
            if 0 <= nx < COLS and 0 <= ny < ROWS and (nx, ny) not in visited:
                if not cell[direction]:
                    print(f"[MOVE] Moving {direction}")
                    path.append((nx, ny))
                    moves += 1
                    moved = True
                    break

        if not moved:
            print("[BACKTRACK] Dead end. Returning...")
            path.pop()
            robot.penup()
            screen.update()

    print("[FAIL] No path found!")

# --- MAIN EXECUTION ---
generate_maze()
draw_maze()

# Place goal
goal_x = -COLS * CELL_SIZE // 2 + (COLS-1) * CELL_SIZE + CELL_SIZE/2
goal_y = ROWS * CELL_SIZE // 2 - (ROWS-1) * CELL_SIZE - CELL_SIZE/2
goal.goto(goal_x, goal_y)

# Place robot
move_cell(0,0)
robot.pendown()

# Solve the maze
maze_solving()

screen.exitonclick()
