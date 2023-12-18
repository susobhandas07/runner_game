from random import choice
import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 468))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
is_alive = False


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.src = './player/player_stand.png'
        self.image = pygame.image.load(self.src).convert_alpha()
        self.rect = self.image.get_rect(midtop=(80, 0))
        self.gravity = 0

    def apply_gravity(self) -> None:
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.gravity > -4:
                self.gravity = -17

    def update(self) -> None:
        self.handle_input()
        self.apply_gravity()


speed = 5


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type='snail'):
        super().__init__()
        self.src = './enemies/snail/snail1.png'
        self.bottom = 300
        if type == 'fly':
            self.src = './enemies/fly/fly1.png'
            self.bottom = 170
        self.image = pygame.image.load(self.src).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(800, self.bottom))

    def move(self) -> None:
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

    def update(self) -> None:
        self.move()


font = pygame.font.Font('./Pixeltype.ttf', 100)
text = 'Start Game'
score_board_text = 'Score: '
score_board_position = (5, 5)

score = 0
start_time = 0

sky_surface = pygame.image.load('./Sky.png').convert()
ground_surface = pygame.image.load('./ground.png').convert()

player = pygame.sprite.GroupSingle()
player.add(Player())

obstacles = pygame.sprite.Group()
obstacles.add(Obstacle())
obstacle_timer = pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer, 1500)

speed_timer = pygame.USEREVENT+2
pygame.time.set_timer(speed_timer, 10000)


def handle_collision() -> bool:
    if pygame.sprite.spritecollide(player.sprite, obstacles, False):
        obstacles.empty()
        return False
    return True


def calculate_score() -> int:
    _temp = pygame.time.get_ticks()//200-start_time
    score_board = font.render(f"{score_board_text}{score}", False, (0, 0, 0))
    score_board_rect = score_board.get_rect(topleft=score_board_position)
    screen.blit(score_board, score_board_rect)
    return _temp


while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == obstacle_timer:
            obstacles.add(Obstacle(type=choice(['snail', 'fly'])))
        elif event.type == speed_timer:
            speed += 1
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not is_alive:
            is_alive = True
            text = 'Your Score: '
            font = pygame.font.Font('./Pixeltype.ttf', 50)
            start_time = pygame.time.get_ticks()//1000
            speed = 6

    pygame.display.flip()
    if is_alive:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()
        is_alive = handle_collision()
        score = calculate_score()
    else:
        screen.fill((94, 129, 162))
        message = font.render(
            f"{text}{score if score else ""}", False, (111, 196, 169))
        message_rect = message.get_rect(center=(400, 234))
        screen.blit(message, message_rect)
