import pygame
import sys
from random import randint, uniform


class Score:
    def __init__(self):
        self.font = pygame.font.Font("fonts/subatomic.ttf", 50)

    def display_score(self):
        surface = self.font.render(f"Score {pygame.time.get_ticks() // 1000}", True, "White")
        rect = surface.get_rect(midbottom=(window_width / 2, window_height - 80))
        display_surface.blit(surface, rect)
        pygame.draw.rect(display_surface, "White", rect.inflate(30,30), width=8, border_radius=6)

class Laser(pygame.sprite.Sprite):
    def __init__(self, groups, start_position):
        super().__init__(groups)
        self.image = pygame.image.load("images/laser.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(midbottom=start_position)
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(0,-1)
        self.speed = 200
        self.collision_sound = pygame.mixer.Sound("sounds/explosion.wav")

    def update(self):
        self.position += self.direction * self.speed * dt
        self.rect.topleft = (round(self.position.x), round(self.position.y))
        self._meteor_collision()
        self._clean()

    def _meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, True, pygame.sprite.collide_mask):
            self.collision_sound.play()
            self.kill()

    def _clean(self):
        if self.rect.bottom < 0:
            self.kill()

class Ship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load("images/ship.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(640,364))
        self.can_shoot = False
        self.last_shoot_time = 0
        self.shoot_sound = pygame.mixer.Sound("sounds/laser.ogg")

    def update(self):
        self._move()
        self._laser_timer()
        self._laser_shoot()
        self._meteor_collision()

    def _move(self):
        self.rect.center = pygame.mouse.get_pos()

    def _laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if (current_time - self.last_shoot_time) > 300:
                self.can_shoot = True

    def _laser_shoot(self):
        if pygame.mouse.get_pressed()[0] and self.can_shoot:
            Laser(laser_group, ship.rect.midtop)
            self.shoot_sound.play()
            self.last_shoot_time = pygame.time.get_ticks()
            self.can_shoot = False

    def _meteor_collision(self):
        if pygame.sprite.spritecollide(self, meteor_group, False, pygame.sprite.collide_mask):
            pygame.quit()
            sys.exit()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.surface = pygame.image.load("images/meteor.png").convert_alpha()
        scale = pygame.math.Vector2(self.surface.get_size()) * uniform(0.5, 1.8)
        self.image = pygame.transform.scale(self.surface, scale)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(randint(-100, window_width+100), randint(-200, -100)))
        self.position = pygame.math.Vector2(self.rect.topleft)
        self.direction = pygame.math.Vector2(uniform(-0.5, 0.5), 1)
        self.speed = 300
        self.rotation = 0
        self.rotation_speed = randint(20,50)

    def update(self):
        self._move()
        self._rotate()
        self._clean()

    def _move(self):
        self.position += self.direction * self.speed * dt
        self.rect.topleft = (round(self.position.x), round(self.position.y))

    def _rotate(self):
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.surface, self.rotation, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def _clean(self):
        if self.rect.top > window_height:
            self.kill()

# init
pygame.init()

# property
window_width = 1280
window_height = 720

clock = pygame.time.Clock()

display_surface = pygame.display.set_mode((window_width, window_height))
background_surface = pygame.image.load("images/background.png").convert()

pygame.display.set_caption("Asteroid")
pygame.mixer.Sound("sounds/music.wav").play(loops=-1)


pop_meteor_event = pygame.event.custom_type()
pygame.time.set_timer(pop_meteor_event, 800)

ship_group = pygame.sprite.GroupSingle()
laser_group = pygame.sprite.Group()
meteor_group = pygame.sprite.Group()

ship = Ship(ship_group)
score = Score()

# game loop
while True:
    # delta time
    dt = clock.tick(120) / 1000

    # event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pop_meteor_event:
            Meteor(meteor_group)

    # update
    ship_group.update()
    laser_group.update()
    meteor_group.update()

    # draw
    display_surface.blit(background_surface, (0,0))
    score.display_score()
    ship_group.draw(display_surface)
    laser_group.draw(display_surface)
    meteor_group.draw(display_surface)

    # display
    pygame.display.update()