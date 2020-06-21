from time import sleep
import logging
import argparse
import pygame


class Ball:
    def __init__(
        self,
        screen,
        x_position=None,
        y_position=None,
        x_velocity=10,
        y_velocity=10,
        radius=10,
        colour="white",
    ):
        self.screen = screen
        if x_position and y_position:
            self.x_position = x_position
            self.y_position = y_position
        else:
            logging.debug(
                "Position parameters provided, putting ball in default position"
            )
            self.x_position = (
                screen.get_width() - radius - 20
            )  # todo fix hack, this 20 is just to make sure it misses the border
            self.y_position = int(screen.get_height() / 2)
        self.x_velocity = -x_velocity
        self.y_velocity = -y_velocity
        self.radius = radius
        self.colour = pygame.Color(colour)
        self.bg_colour = pygame.Color("black")

    def get_coordinates(self):
        return self.x_position, self.y_position

    def touching_border(self):
        border_width = 10  # todo: not hardcode this
        width_and_radius = border_width + self.radius
        if (
            self.x_position <= width_and_radius
        ):  # or self.x_position >= self.screen.get_width()-width_and_radius:
            self.x_velocity = self.x_velocity * -1
        if (
            self.y_position <= width_and_radius
            or self.y_position >= self.screen.get_height() - width_and_radius
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
        sleep(0.1)
        self.hide()
        self.x_position = self.x_position + self.x_velocity
        self.y_position = self.y_position + self.y_velocity
        self.touching_border()
        self.show()

    def check_paddle(self, paddle):
        border_width = 10  # todo: not hardcode this
        width_and_radius = border_width + self.radius
        if self.x_position >= self.screen.get_width() - width_and_radius:
            paddle_top, paddle_bottom = paddle.get_position()
            if self.y_position >= paddle_top and self.y_position <= paddle_bottom:
                self.x_velocity = self.x_velocity * -1


class Paddle:
    def __init__(self, screen):
        self.screen = screen
        self.width = 10  # todo fix, should be border width
        self.height = self.screen.get_height() / 10
        self.x_position = screen.get_width() - self.width
        self.y_position = (self.screen.get_height() / 2) - (self.height / 2)
        self.colour = pygame.Color("white")
        self.bg_colour = pygame.Color("black")

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


def draw_borders(screen, SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_WIDTH):
    border_colour = pygame.Color("white")
    borders = [
        ((0, 0), (SCREEN_WIDTH, BORDER_WIDTH)),
        ((0, 0), (BORDER_WIDTH, SCREEN_HEIGHT)),
        ((0, SCREEN_HEIGHT - BORDER_WIDTH), (SCREEN_WIDTH, BORDER_WIDTH)),
    ]

    for border in borders:
        pygame.draw.rect(screen, border_colour, pygame.Rect(border))
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
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    BORDER_WIDTH = 10

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    draw_borders(screen, SCREEN_WIDTH, SCREEN_HEIGHT, BORDER_WIDTH)
    ball = Ball(screen)
    ball.show()
    paddle = Paddle(screen)
    paddle.show()

    while True:
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break
        ball.update()
        paddle.update()
        ball.check_paddle(paddle)


if __name__ == "__main__":
    main()
