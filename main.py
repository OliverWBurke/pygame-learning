from time import sleep
import random
import logging
import argparse
import pygame


class Game:
    def __init__(self):
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 500
        self.SCORE_HEIGHT = 25
        self.GAME_HEIGHT = 475
        self.BORDER_WIDTH = 10
        self.BACKGROUND_COLOUR = "Black"
        self.FOREGROUND_COLOUR = "White"
        self.status = "playing"
        self.score = 0
        self.screen = self.get_screen()
        self.display_score()
        self.draw_borders()
        self.paddle = Paddle(self)
        self.balls = []
        self.balls.append(Ball(self))

    def get_screen(self):
        return pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

    def add_score(self):
        self.display_score(hide=True)
        self.score += 1
        self.display_score()

    def display_score(self, hide=False):
        if hide:
            text_colour = self.BACKGROUND_COLOUR
        else:
            text_colour = self.FOREGROUND_COLOUR
        font = pygame.font.SysFont(None, 24)

        text = font.render(f"Score: {self.score}", True, pygame.Color(text_colour))
        font_height = text.get_height()

        self.screen.blit(
            text, (10, self.GAME_HEIGHT + (self.SCORE_HEIGHT - font_height) / 2,),
        )
        pygame.display.update()

    def draw_borders(self):
        border_colour = pygame.Color(self.FOREGROUND_COLOUR)
        borders = [
            ((0, 0), (self.SCREEN_WIDTH, self.BORDER_WIDTH)),
            ((0, 0), (self.BORDER_WIDTH, self.GAME_HEIGHT)),
            (
                (0, self.GAME_HEIGHT - self.BORDER_WIDTH),
                (self.SCREEN_WIDTH, self.BORDER_WIDTH),
            ),
        ]

        for border in borders:
            pygame.draw.rect(self.screen, border_colour, pygame.Rect(border))
        pygame.display.flip()

    def update(self):
        for ball in self.balls:
            ball.update()
            self.paddle.update()
            ball.check_paddle(self.paddle)

    def game_over(self):
        self.status = "game over"
        margin = 50
        font = pygame.font.SysFont(None, 24)
        text = font.render("Game Over!", True, pygame.Color("RED"))
        text_height = text.get_height()
        text_width = text.get_width()
        self.screen.blit(
            text,
            (
                (self.SCREEN_WIDTH / 2 - text_width / 2),
                (self.GAME_HEIGHT / 2) - (text_height / 2),
            ),
        )
        box_width = text_width + margin + self.BORDER_WIDTH
        box_height = text_height + margin + self.BORDER_WIDTH
        game_over_rect = pygame.Rect(
            (
                (self.SCREEN_WIDTH / 2 - box_width / 2),
                (self.GAME_HEIGHT / 2) - (box_height / 2),
            ),
            (box_width, box_height),
        )
        pygame.draw.rect(
            self.screen, pygame.Color("White"), game_over_rect, self.BORDER_WIDTH,
        )
        pygame.display.update()


class Ball:
    def __init__(
        self,
        game_setup,
        x_position=None,
        y_position=None,
        random_pos=False,
        x_velocity=10,
        y_velocity=10,
        radius=10,
    ):
        self.game_setup = game_setup
        self.screen = game_setup.screen
        self.radius = radius
        self.set_position(x_position, y_position, random_pos)
        self.x_velocity = -x_velocity
        self.y_velocity = -y_velocity
        self.colour = pygame.Color(game_setup.FOREGROUND_COLOUR)
        self.bg_colour = pygame.Color(game_setup.BACKGROUND_COLOUR)
        self.border_and_ball_width = self.game_setup.BORDER_WIDTH + self.radius
        self.show()

    def set_position(self, x_position, y_position, random_pos=False):

        if x_position and y_position:
            self.x_position = x_position
            self.y_position = y_position
        elif random_pos:
            self.x_position = (
                random.randrange(self.game_setup.SCREEN_WIDTH)
                - self.radius
                - self.game_setup.BORDER_WIDTH
            )
            self.y_position = random.randrange(
                self.game_setup.BORDER_WIDTH + self.radius,
                self.game_setup.SCREEN_HEIGHT - self.game_setup.BORDER_WIDTH,
            )
        else:
            logging.debug(
                "Position parameters not provided, putting ball in default position"
            )
            self.x_position = (
                self.game_setup.SCREEN_WIDTH
                - self.radius
                - self.game_setup.BORDER_WIDTH
            )
            self.y_position = int(self.game_setup.GAME_HEIGHT / 2) + 5

    def get_coordinates(self):
        return self.x_position, self.y_position

    def touching_border(self):
        touching = False
        if self.x_position <= self.border_and_ball_width:
            self.x_velocity = self.x_velocity * -1
            touching = True
        if (
            self.y_position <= self.border_and_ball_width
            or self.y_position
            >= self.game_setup.GAME_HEIGHT - self.border_and_ball_width
        ):
            self.y_velocity = self.y_velocity * -1
            touching = True
        if touching:
            self.game_setup.draw_borders()

    def show(self):
        pygame.draw.circle(
            self.screen, self.colour, self.get_coordinates(), self.radius
        )
        pygame.display.flip()

    def hide(self):
        pygame.draw.circle(
            self.screen, self.bg_colour, self.get_coordinates(), self.radius
        )
        pygame.display.flip()

    def update(self):
        self.hide()
        self.touching_border()
        self.x_position = self.x_position + self.x_velocity
        self.y_position = self.y_position + self.y_velocity
        self.show()

    def check_paddle(self, paddle):
        if self.x_position < self.screen.get_width() - self.border_and_ball_width:
            logging.debug("ball in play")
        else:
            logging.info("Ball at end")
            paddle_top, paddle_bottom = paddle.get_position()
            if self.y_position in range(
                paddle_top - self.radius, paddle_bottom + self.radius
            ):
                self.x_velocity = self.x_velocity * -1
                logging.info("Hit - Add Score")
                self.game_setup.add_score()
                if self.game_setup.score % 3 == 0:
                    self.x_velocity += 2 * int(self.x_velocity / abs(self.x_velocity))
                    self.y_velocity += 2 * int(self.y_velocity / abs(self.y_velocity))
            else:
                logging.info("Missed - Game Over")
                self.game_setup.game_over()


class Paddle:
    def __init__(self, game_setup):
        self.game_setup = game_setup
        self.screen = game_setup.screen
        self.width = game_setup.BORDER_WIDTH
        self.height = int(self.game_setup.GAME_HEIGHT / 10)
        self.x_position = self.game_setup.SCREEN_WIDTH - self.width
        self.y_position = (self.game_setup.GAME_HEIGHT / 2) - (self.height / 2)
        self.colour = pygame.Color(self.game_setup.FOREGROUND_COLOUR)
        self.bg_colour = pygame.Color(self.game_setup.BACKGROUND_COLOUR)
        self.show()

    def get_position(self):
        top = self.y_position
        bottom = self.y_position + self.height
        return top, bottom

    def hide(self):
        rect = pygame.Rect(self.x_position, self.y_position, self.width, self.height)
        pygame.draw.rect(self.screen, self.bg_colour, rect)
        pygame.display.flip()

    def show(self):
        rect = pygame.Rect(self.x_position, self.y_position, self.width, self.height)
        pygame.draw.rect(self.screen, self.colour, rect)
        pygame.display.flip()

    def update(self):
        self.hide()
        self.y_position = pygame.mouse.get_pos()[1]
        if self.y_position < self.width:
            self.y_position = self.width
        if self.y_position > self.game_setup.GAME_HEIGHT - self.height - self.width:
            self.y_position = self.game_setup.GAME_HEIGHT - self.height - self.width
        self.show()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug_mode",
        "-db",
        action="store_true",
        help="If flag is set, will print debug level logs",
    )
    parsed_args = parser.parse_args()
    return parsed_args


def main():
    args = parse_args()
    if args.debug_mode:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    pygame.init()

    game_setup = Game()

    while game_setup.status == "playing":
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        sleep(0.05)
        game_setup.update()
        logging.info(f"Score is {game_setup.score}")

    while game_setup.status == "game over":
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        if e.type == pygame.KEYDOWN:
            break


if __name__ == "__main__":
    main()
