
"""
GameEngine: owns the helicopter and all obstacles.
Handles collision detection and game-over state.
"""

import random
import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0
        self.shield_active = False
        self.shield_used = False
        self.shield_grace_frames = 0
        self.shielded_obstacle = None

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(
            margin + GAP_HEIGHT // 2,
            HEIGHT - margin - GAP_HEIGHT // 2,
        )
        self.obstacles.append(
            Obstacle(
                x=WIDTH,
                gap_y=gap_y,
                gap_height=GAP_HEIGHT,
                wall_width=WALL_WIDTH,
                screen_height=HEIGHT,
                speed=SCROLL_SPEED,
            )
        )

    def handle_input(self, keys_pressed):
        if not self.game_over:
            self.helicopter.handle_input(keys_pressed)

    
    def handle_keydown(self, key):
        if (
            key == pygame.K_SPACE
            and not self.shield_used
            and not self.game_over
        ):
            self.shield_active = True
            self.shield_used = True


    
    
    def _check_collisions(self):
        helicopter_rect = self.helicopter.get_rect()

        for obstacle in self.obstacles:
            # Ignore the obstacle absorbed by the shield
            if obstacle is self.shielded_obstacle:
                if obstacle.x + obstacle.wall_width < helicopter_rect.left:
                    self.shielded_obstacle = None
                else:
                    continue

            top_rect = obstacle.get_top_rect()
            bottom_rect = obstacle.get_bottom_rect()

            collided = (
                helicopter_rect.colliderect(top_rect)
                or helicopter_rect.colliderect(bottom_rect)
            )

            if collided:
                if self.shield_active:
                    self.shield_active = False
                    self.shielded_obstacle = obstacle
                    return

                self.game_over = True
                return



    def update(self):
        if self.game_over:
            return

        if self.shield_grace_frames > 0:
            self.shield_grace_frames -= 1

        self.helicopter.update(HEIGHT)
        self.distance += 1
        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()

        self.obstacles = [
            obstacle for obstacle in self.obstacles
            if not obstacle.is_off_screen()
        ]

        self._check_collisions()

    
    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface, self.helicopter, self.obstacles
        )

        if self.shield_active:
            pygame.draw.ellipse(
                surface,
                (0, 150, 255),
                self.helicopter.get_rect().inflate(20, 20),
                3,
            )

        renderer.draw_text(
            surface,
            font,
            f"Distance: {self.distance}",
            (10, 10),
        )

        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER")
