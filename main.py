from time import sleep
import logging
import argparse
import pygame


class Ball:
    def __init__(
        self,
        game_setup,
        x_position=None,
        y_position=None,
        x_velocity=10,
        y_velocity=10,
        radius=10,
    ):
        self.game_setup = game_setup
        self.screen = game_setup["screen"]
        if x_position and y_position:
            self.x_position = x_position
            self.y_position = y_position
        else:
            logging.debug(
                "Position parameters provided, putting ball in default position"
            )
            self.x_position = (
                game_setup["SCREEN_WIDTH"] - radius - game_setup["BORDER_WIDTH"]
            )
            self.y_position = int(game_setup["SCREEN_HEIGHT"] / 2)
        self.x_velocity = -x_velocity
        self.y_velocity = -y_velocity
        self.radius = radius
        self.colour = pygame.Color(game_setup["FOREGROUND_COLOUR"])
        self.bg_colour = pygame.Color(game_setup["BACKGROUND_COLOUR"])
        self.border_and_ball_width = self.game_setup["BORDER_WIDTH"] + self.radius

    def get_coordinates(self):
        return self.x_position, self.y_position

    def touching_border(self):

        if self.x_position <= self.border_and_ball_width:
            self.x_velocity = self.x_velocity * -1
        if (
            self.y_position <= self.border_and_ball_width
            or self.y_position
            >= self.game_setup["SCREEN_HEIGHT"] - self.border_and_ball_width
        ):
            self.y_velocity = self.y_velocity * -1

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
        self.x_position = self.x_position + self.x_velocity
        self.y_position = self.y_position + self.y_velocity
        self.touching_border()
        self.show()

    def check_paddle(self, paddle):
        if self.x_position < self.screen.get_width() - self.border_and_ball_width:
            logging.debug("ball in play")
            return 0
        else:
            logging.info("Ball at end")
            paddle_top, paddle_bottom = paddle.get_position()
            if self.y_position in range(
                paddle_top - self.radius, paddle_bottom + self.radius
            ):
                self.x_velocity = self.x_velocity * -1
                logging.info("Hit - Add Score")
                return 1
            else:
                logging.info("Missed - Game Over")
                self.game_setup["status"] = "game over"
                return 0


class Paddle:
    def __init__(self, game_setup):
        self.screen = game_setup["screen"]
        self.width = game_setup["BORDER_WIDTH"]
        self.height = int(self.screen.get_height() / 10)
        self.x_position = self.screen.get_width() - self.width
        self.y_position = (self.screen.get_height() / 2) - (self.height / 2)
        self.colour = pygame.Color(game_setup["FOREGROUND_COLOUR"])
        self.bg_colour = pygame.Color(game_setup["BACKGROUND_COLOUR"])

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
        if self.y_position > self.screen.get_height() - self.height - self.width:
            self.y_position = self.screen.get_height() - self.height - self.width
        self.show()


def game_over(game_setup, text_string="Game Over!"):

    margin = 50
    font = pygame.font.SysFont(None, 24)
    text = font.render(text_string, True, pygame.Color("RED"))
    text_height = text.get_height()
    text_width = text.get_width()
    game_setup["screen"].blit(
        text,
        (
            (game_setup["SCREEN_WIDTH"] / 2 - text_width / 2),
            (game_setup["SCREEN_HEIGHT"] / 2) - (text_height / 2),
        ),
    )
    box_width = text_width + margin + game_setup["BORDER_WIDTH"]
    box_height = text_height + margin + game_setup["BORDER_WIDTH"]
    game_over_rect = pygame.Rect(
        (
            (game_setup["SCREEN_WIDTH"] / 2 - box_width / 2),
            (game_setup["SCREEN_HEIGHT"] / 2) - (box_height / 2),
        ),
        (box_width, box_height),
    )
    pygame.draw.rect(
        game_setup["screen"],
        pygame.Color("White"),
        game_over_rect,
        game_setup["BORDER_WIDTH"],
    )
    pygame.display.update()


def draw_borders(game_setup):
    border_colour = pygame.Color(game_setup["FOREGROUND_COLOUR"])
    borders = [
        ((0, 0), (game_setup["SCREEN_WIDTH"], game_setup["BORDER_WIDTH"])),
        ((0, 0), (game_setup["BORDER_WIDTH"], game_setup["SCREEN_HEIGHT"])),
        (
            (0, game_setup["SCREEN_HEIGHT"] - game_setup["BORDER_WIDTH"]),
            (game_setup["SCREEN_WIDTH"], game_setup["BORDER_WIDTH"]),
        ),
    ]

    for border in borders:
        pygame.draw.rect(game_setup["screen"], border_colour, pygame.Rect(border))
    pygame.display.flip()


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

    game_setup = {
        "score": 0,
        "SCREEN_WIDTH": 800,
        "SCREEN_HEIGHT": 500,
        "BORDER_WIDTH": 10,
        "BACKGROUND_COLOUR": "Black",
        "FOREGROUND_COLOUR": "White",
        "status": "playing",
    }
    game_setup["screen"] = pygame.display.set_mode(
        (game_setup["SCREEN_WIDTH"], game_setup["SCREEN_HEIGHT"])
    )
    draw_borders(game_setup)
    ball = Ball(game_setup)
    ball.show()
    paddle = Paddle(game_setup)
    paddle.show()

    while game_setup["status"] == "playing":
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        sleep(0.05)
        ball.update()
        paddle.update()
        score_update = ball.check_paddle(paddle)
        game_setup["score"] += score_update
        logging.info(f"Score is {game_setup['score']}")
        if game_setup["status"] == "game over":
            game_over(game_setup)

    while game_setup["status"] == "game over":
        e = pygame.event.poll()
        if e.type == pygame.KEYDOWN:
            break


if __name__ == "__main__":
    main()
