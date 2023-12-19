from random import choice
import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 468))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
is_alive = False
game_sound = pygame.mixer.Sound('./sound/music.wav')
game_sound.set_volume(0.3)
crash_sound = pygame.mixer.Sound('./sound/collision.mp3')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.srcs = {'stand': ('./player/player_stand.png'), 'walk': (
            './player/player_walk1.png', './player/player_walk2.png'), 'jump': ('./player/player_jump.png')}
        self.mode = 'walk'
        self.indx = 0
        self.frame_duration = 0.2
        self.image = pygame.image.load(
            self.srcs[self.mode][self.indx]).convert_alpha()
        self.rect = self.image.get_rect(midtop=(80, 0))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('./sound/jump.mp3')

    def apply_gravity(self) -> None:
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.gravity = 0
            self.mode = 'walk'

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.gravity > -4:
                self.gravity = -17
                self.mode = 'jump'
                self.jump_sound.play()

    def walk(self):
        self.indx = (self.indx+self.frame_duration) % 2
        self.image = pygame.image.load(self.srcs[self.mode][int(self.indx)])

    def jump(self):
        self.image = pygame.image.load(self.srcs[self.mode])

    def update(self) -> None:
        self.handle_input()
        if self.mode == 'jump':
            self.jump()
        else:
            self.walk()
        self.apply_gravity()


speed = 5


class Obstacle(pygame.sprite.Sprite):

    def __init__(self, type='snail'):
        super().__init__()
        self.srcs = ['./enemies/snail/snail1.png',
                     './enemies/snail/snail2.png']
        self.indx = 0
        self.frame_duration = 0.1
        self.bottom = 300
        if type == 'fly':
            self.srcs = ['./enemies/fly/fly1.png', './enemies/fly/fly2.png']
            self.bottom = 170
            self.frame_duration = 0.2
        self.image = pygame.image.load(self.srcs[self.indx]).convert_alpha()
        self.rect = self.image.get_rect(bottomleft=(800, self.bottom))

    def move(self) -> None:
        self.rect.x -= speed
        if self.rect.right < 0:
            self.kill()

    def update(self) -> None:
        self.indx = (self.indx+self.frame_duration) % 2
        self.image = pygame.image.load(
            self.srcs[int(self.indx)]).convert_alpha()
        self.move()


font = pygame.font.Font('./Pixeltype.ttf', 100)
text = 'Start Game'
score_board_text = 'Score: '
score_board_position = (5, 5)


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
        crash_sound.play()
        return False
    return True


def calculate_score(start_time) -> int:
    _temp = pygame.time.get_ticks()//200-start_time
    score_board = font.render(f"{score_board_text}{_temp}", False, (0, 0, 0))
    score_board_rect = score_board.get_rect(topleft=score_board_position)
    screen.blit(score_board, score_board_rect)
    return _temp


score = 0
start_time = 0

while True:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if is_alive:
            if event.type == obstacle_timer:
                obstacles.add(Obstacle(type=choice(['snail', 'fly'])))
            if event.type == speed_timer:
                speed += 2
                player.sprite.frame_duration += 0.02
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            is_alive = True
            text = 'Your Score: '
            font = pygame.font.Font('./Pixeltype.ttf', 50)
            start_time = pygame.time.get_ticks()//200
            speed = 6
            game_sound.play(loops=-1)

    pygame.display.flip()

    if is_alive:
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        player.draw(screen)
        player.update()
        obstacles.draw(screen)
        obstacles.update()
        is_alive = handle_collision()
        score = calculate_score(start_time)
    else:
        game_sound.stop()
        screen.fill((94, 129, 162))
        message = font.render(
            f"{text}{score if score else ""}", False, (111, 196, 169))
        message_rect = message.get_rect(center=(400, 234))
        screen.blit(message, message_rect)
