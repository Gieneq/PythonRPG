import pygame

from core.debug import Debugger
from entity.entity import Entity


class Player(Entity):
    def __init__(self, starting_pos, world, visible=True):
        super().__init__(world=world)
        self.image = pygame.image.load('./data/graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=starting_pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.add(self.world.entities)
        self.set_visible(visible)

        self.direction = pygame.math.Vector2()
        self.speed = 6
        self.cooldown = 0
        self.cooldown_start_time = 0

    def input(self):
        keys = pygame.key.get_pressed()

        # movement
        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
            self.world.on_player_move()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal', self.direction)
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical', self.direction)

        self.rect.center = self.hitbox.center

    def update(self, *args, **kwargs):
        Debugger.print(f"Player_center: {self.rect.center}")
        self.input()
        self.move(self.speed)