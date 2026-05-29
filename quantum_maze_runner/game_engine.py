import turtle
import time

from config import *
from maze import Maze
from player import Player
from ghost import Ghost

RESTART_DELAY = 10  # seconds


class GameEngine:

    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Quantum Maze Runner")
        self.screen.bgcolor(BG_COLOR)
        self.screen.setup(WIN_W, WIN_H)
        self.screen.tracer(0)

        self.maze_pen = self.create_pen()
        self.hud_pen = self.create_pen()
        self.message_pen = self.create_pen()
        self.label_pen = self.create_pen()
        self.countdown_pen = self.create_pen()

        self.initialize_game()
        self.bind_controls()

        try:
            self.game_loop()
        except (turtle.Terminator, Exception):
            pass

    def create_pen(self):
        pen = turtle.Turtle()
        pen.hideturtle()
        pen.penup()
        pen.speed(0)
        return pen

    def initialize_game(self):
        self.maze_pen.clear()
        self.hud_pen.clear()
        self.message_pen.clear()
        self.label_pen.clear()
        self.countdown_pen.clear()

        if hasattr(self, 'ghost'):
            self.player.t.hideturtle()
            self.ghost.t.hideturtle()
            self.exit_turtle.hideturtle()

        self.maze = Maze()
        self.player = Player(0, 0)
        self.exit_position = (COLS - 1, ROWS - 1)
        self.ghost = Ghost(COLS - 1, 0)

        self.game_over = False
        self.player_won = False
        self.game_over_time = None          # when finish_game was called
        self.last_countdown_shown = -1      # last integer second we drew
        self.last_collapse_time = time.time()
        self.portal_animation_timer = time.time()
        self.portal_pulse = False

        self.draw_maze()
        self.create_exit_portal()

        self.player.teleport(self.maze)
        self.ghost.teleport(self.maze)
        self.ghost.recalc(self.maze, self.player.pos)

    def draw_maze(self):
        self.maze.draw(self.maze_pen)

    def create_exit_portal(self):
        self.exit_turtle = turtle.Turtle()
        self.exit_turtle.shape("circle")
        self.exit_turtle.penup()
        self.exit_turtle.speed(0)
        self.exit_turtle.color(EXIT_COLOR_A)
        self.exit_turtle.shapesize(1.1)

        x, y = self.maze.cell(*self.exit_position).center()
        self.exit_turtle.goto(x, y)

        self.label_pen.color(EXIT_COLOR_B)
        self.label_pen.goto(x, y + 20)
        self.label_pen.write("EXIT", align="center", font=("Courier", 8, "bold"))

    def bind_controls(self):
        self.screen.listen()

        controls = [
            ("Up", "N"), ("Down", "S"), ("Left", "W"), ("Right", "E"),
            ("w", "N"), ("s", "S"), ("a", "W"), ("d", "E"),
        ]

        for key, direction in controls:
            self.screen.onkeypress(lambda d=direction: self.handle_player_move(d), key)

    def handle_player_move(self, direction):
        if self.game_over:
            return

        moved = self.player.try_move(self.maze, direction)
        if not moved:
            return

        self.ghost.recalc(self.maze, self.player.pos)
        self.ghost.step(self.maze)

        if self.player.pos == self.exit_position:
            self.finish_game(player_won=True)
            return

        if self.ghost.pos == self.player.pos:
            self.finish_game(player_won=False)
            return

    def draw_hud(self, time_left):
        self.hud_pen.clear()

        top = WIN_H / 2

        self.hud_pen.goto(0, top - 22)
        self.hud_pen.color(HUD_COLOR)
        self.hud_pen.write("QUANTUM MAZE RUNNER", align="center", font=("Courier", 15, "bold"))

        self.hud_pen.goto(0, top - 42)
        self.hud_pen.color(TEXT_COLOR)
        self.hud_pen.write(f"Collapse In: {time_left:.1f}s", align="center", font=("Courier", 9, "bold"))

        self.hud_pen.goto(-WIN_W / 2 + 8, top - 42)
        self.hud_pen.color("#55aa77")
        self.hud_pen.write("WASD / ARROWS", align="left", font=("Courier", 8, "normal"))

        right_x = WIN_W / 2 - 8
        self.hud_pen.goto(right_x, top - 35)
        self.hud_pen.color(PLAYER_COLOR)
        self.hud_pen.write("● PLAYER", align="right", font=("Courier", 8, "bold"))

        self.hud_pen.goto(right_x, top - 48)
        self.hud_pen.color(GHOST_COLOR)
        self.hud_pen.write("● GHOST", align="right", font=("Courier", 8, "bold"))

        self.hud_pen.goto(right_x, top - 61)
        self.hud_pen.color(EXIT_COLOR_B)
        self.hud_pen.write("● EXIT", align="right", font=("Courier", 8, "bold"))

    def finish_game(self, player_won):
        """Mark game as over and draw the result box. Countdown runs in game_loop."""
        self.game_over = True
        self.game_over_time = time.time()
        self.last_countdown_shown = -1
        self.message_pen.clear()
        self.countdown_pen.clear()

        if player_won:
            self.end_bg_color    = "#003300"
            self.end_border_color = "#00ff88"
            self.end_text_color  = "#00ff88"
            title    = "YOU ESCAPED!"
            subtitle = "QUANTUM MAZE CONQUERED!"
        else:
            self.end_bg_color    = "#330000"
            self.end_border_color = "#ff2244"
            self.end_text_color  = "#ff2244"
            title    = "THE GHOST CAUGHT YOU!"
            subtitle = "BETTER LUCK NEXT TIME!"

        # Draw solid background box
        self.message_pen.color(self.end_bg_color)
        self.message_pen.fillcolor(self.end_bg_color)
        box_w, box_h = 340, 120
        x0, y0 = -box_w / 2, -box_h / 2
        self.message_pen.goto(x0, y0)
        self.message_pen.begin_fill()
        self.message_pen.pendown()
        for dx, dy in [(box_w, 0), (0, box_h), (-box_w, 0), (0, -box_h)]:
            self.message_pen.goto(self.message_pen.xcor() + dx, self.message_pen.ycor() + dy)
        self.message_pen.end_fill()
        self.message_pen.penup()

        # Draw border
        self.message_pen.color(self.end_border_color)
        self.message_pen.width(3)
        self.message_pen.goto(x0, y0)
        self.message_pen.pendown()
        for dx, dy in [(box_w, 0), (0, box_h), (-box_w, 0), (0, -box_h)]:
            self.message_pen.goto(self.message_pen.xcor() + dx, self.message_pen.ycor() + dy)
        self.message_pen.penup()
        self.message_pen.width(1)

        # Title text
        self.message_pen.goto(0, 28)
        self.message_pen.color(self.end_text_color)
        self.message_pen.write(title, align="center", font=("Courier", 16, "bold"))

        # Subtitle
        self.message_pen.goto(0, 4)
        self.message_pen.color(TEXT_COLOR)
        self.message_pen.write(subtitle, align="center", font=("Courier", 10, "normal"))

    def update_countdown(self):
        """Called every frame while game_over is True. Redraws only when second changes."""
        elapsed = time.time() - self.game_over_time
        remaining = max(0, RESTART_DELAY - int(elapsed))

        if remaining == self.last_countdown_shown:
            return  # nothing changed, skip redraw

        self.last_countdown_shown = remaining

        # Erase previous countdown line by overdrawing with bg colour
        self.countdown_pen.clear()
        self.countdown_pen.color(self.end_bg_color)
        self.countdown_pen.fillcolor(self.end_bg_color)
        self.countdown_pen.goto(-160, -52)
        self.countdown_pen.begin_fill()
        self.countdown_pen.pendown()
        for dx, dy in [(320, 0), (0, 24), (-320, 0), (0, -24)]:
            self.countdown_pen.goto(self.countdown_pen.xcor() + dx,
                                    self.countdown_pen.ycor() + dy)
        self.countdown_pen.end_fill()
        self.countdown_pen.penup()

        # Draw updated number
        self.countdown_pen.goto(0, -46)
        self.countdown_pen.color("#888888")
        label = f"Restarting in {remaining} second{'s' if remaining != 1 else ''}..."
        self.countdown_pen.write(label, align="center", font=("Courier", 9, "normal"))

        if elapsed >= RESTART_DELAY:
            self.initialize_game()

    def animate_portal(self):
        now = time.time()
        if now - self.portal_animation_timer < 0.45:
            return

        self.portal_pulse = not self.portal_pulse

        if self.portal_pulse:
            self.exit_turtle.color(EXIT_COLOR_B)
            self.exit_turtle.shapesize(1.35)
        else:
            self.exit_turtle.color(EXIT_COLOR_A)
            self.exit_turtle.shapesize(1.0)

        self.portal_animation_timer = now

    def handle_quantum_collapse(self):
        current_time = time.time()
        elapsed = current_time - self.last_collapse_time

        if elapsed < COLLAPSE_INTERVAL:
            return elapsed

        changed = self.maze.quantum_collapse(self.player.pos, self.exit_position)

        if changed:
            self.maze.draw_flash(self.maze_pen, changed)
            self.screen.update()
            time.sleep(0.08)

        self.draw_maze()
        self.player.teleport(self.maze)
        self.ghost.teleport(self.maze)
        self.ghost.recalc(self.maze, self.player.pos)

        self.last_collapse_time = current_time
        return 0

    def game_loop(self):
        while True:
            if self.game_over:
                self.update_countdown()
                self.screen.update()
                time.sleep(1 / 30)
                continue

            elapsed = self.handle_quantum_collapse()
            time_left = max(0, COLLAPSE_INTERVAL - elapsed)

            self.animate_portal()
            self.draw_hud(time_left)
            self.screen.update()

            time.sleep(1 / 60)