"""2D Space Shooter
-----------------
Controls:
  Arrow Keys / A,D - Move left/right
  Space - Shoot
  R - Restart after Game Over
  Esc - Quit


"""


import pygame
import random
import sys

# ----------------------------- Setup -----------------------------
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 480, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()
FPS = 60

FONT_SM = pygame.font.SysFont("consolas", 22)
FONT_MD = pygame.font.SysFont("consolas", 36)
FONT_LG = pygame.font.SysFont("consolas", 56)

WHITE = (255, 255, 255)
BLACK = (10, 10, 20)
RED = (220, 60, 60)
GREEN = (80, 220, 120)
YELLOW = (240, 220, 80)
CYAN = (80, 200, 240)
GREY = (150, 150, 150)

# ----------------------------- Starfield -----------------------------
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(1, 4)
        self.size = random.choice([1, 1, 2])

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)

    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), self.size)


# ----------------------------- Player -----------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, CYAN, [(20, 0), (0, 40), (40, 40)])
        pygame.draw.polygon(self.image, WHITE, [(20, 0), (0, 40), (40, 40)], 2)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
        self.speed = 6
        self.health = 100
        self.shoot_delay = 250 # ms
        self.last_shot = 0

    def update(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        self.rect.clamp_ip(screen.get_rect())

    def can_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_delay:
            self.last_shot = now
            return True
        return False


# ----------------------------- Bullet -----------------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 12))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 10

    def update(self, *args):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()


class coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20)), pygame.SRCALPHA  
        pygame.draw.circle(self.image, (255, 215, 0), (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - 20) 
        self.rect.y = random.randint(-100, -40)  
        self.speedy = random.randint(2, 4) 

    def update(self, *args):
                self.rect.y += self.speedy
                if self.rect.top > HEIGHT:
                    self.kill()
           
# ----------------------------- Enemy ---------------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        size = random.randint(24, 40)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.polygon(
            self.image, RED,
            [(size // 2, size), (0, 0), (size, 0)]
        )
        pygame.draw.polygon(
            self.image, WHITE,
            [(size // 2, size), (0, 0), (size, 0)], 2
        )
        self.rect = self.image.get_rect(
            midtop=(random.randint(20, WIDTH - 20), random.randint(-100, -40))
        )
        self.speed = random.uniform(2, 4)
        self.value = max(1, int((5 - self.speed) * 10))

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


# ----------------------------- Explosion -----------------------------
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.radius = 5
        self.max_radius = 28
        self.center = center
        self.image = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=center)
        self.growth = 3

    def update(self, *args):
        self.radius += self.growth
        self.image.fill((0, 0, 0, 0))
        alpha = max(0, 255 - int(self.radius * 8))
        color = (255, min(255, 100 + self.radius * 3), 0, alpha)
        if self.radius < self.max_radius:
            pygame.draw.circle(self.image, color, (self.max_radius, self.max_radius), int(self.radius))
        else:
            self.kill()


# ----------------------------- Game class -----------------------------
class Game:
    def __init__(self):
        self.stars = [Star() for _ in range(80)]
        self.reset()
        self.high_score = 0

    def reset(self):
        self.player = Player()
        self.player_group = pygame.sprite.GroupSingle(self.player)
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.explosions = pygame.sprite.Group()
        self.score = 0
        self.spawn_timer = 0
        self.spawn_interval = 900 # ms, decreases over time
        self.game_over = False
        self.start_ticks = pygame.time.get_ticks()

    def spawn_enemies(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_ticks
        # difficulty ramps up over time
        self.spawn_interval = max(250, 900 - elapsed // 200)
        if now - self.spawn_timer > self.spawn_interval:
            self.spawn_timer = now
            self.enemies.add(Enemy())

    def handle_shooting(self, keys):
        if keys[pygame.K_SPACE] and self.player.can_shoot():
            self.bullets.add(Bullet(self.player.rect.centerx, self.player.rect.top))

    def update(self, keys):
        if self.game_over:
            return

        for star in self.stars:
            star.update()

        self.player_group.update(keys)
        self.handle_shooting(keys)
        self.bullets.update()
        self.enemies.update()
        self.explosions.update()
        self.spawn_enemies()

        # Bullet-enemy collisions
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, True, True)
        for enemy in hits:
            self.score += enemy.value
            self.explosions.add(Explosion(enemy.rect.center))

        # Player-enemy collisions
        collided = pygame.sprite.spritecollide(self.player, self.enemies, True)
        for enemy in collided:
            self.player.health -= 25
            self.explosions.add(Explosion(enemy.rect.center))
            if self.player.health <= 0:
                self.player.health = 0
                self.end_game()

    def end_game(self):
        self.game_over = True
        if self.score > self.high_score:
            self.high_score = self.score

    def draw_hud(self):
        score_surf = FONT_SM.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_surf, (10, 10))

        # Health bar
        bar_w, bar_h = 150, 16
        x, y = WIDTH - bar_w - 10, 10
        pygame.draw.rect(screen, GREY, (x, y, bar_w, bar_h), 2)
        fill_w = int(bar_w * (self.player.health / 100))
        color = GREEN if self.player.health > 40 else RED
        pygame.draw.rect(screen, color, (x, y, fill_w, bar_h))
        hp_label = FONT_SM.render("HP", True, WHITE)
        screen.blit(hp_label, (x - 35, y - 2))

    def draw(self):
        screen.fill(BLACK)
        for star in self.stars:
            star.draw(screen)

        if not self.game_over:
            self.player_group.draw(screen)
        self.bullets.draw(screen)
        self.enemies.draw(screen)
        self.explosions.draw(screen)
        self.draw_hud()

        if self.game_over:
            self.draw_game_over()

    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        title = FONT_LG.render("GAME OVER", True, RED)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 80)))

        score_txt = FONT_MD.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_txt, score_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))

        high_txt = FONT_SM.render(f"High Score: {self.high_score}", True, YELLOW)
        screen.blit(high_txt, high_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20)))

        restart_txt = FONT_SM.render("Press R to Restart or Esc to Quit", True, GREEN)
        screen.blit(restart_txt, restart_txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 70)))


# ----------------------------- Main loop -----------------------------
def main():
    game = Game()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()

        keys = pygame.key.get_pressed()
        game.update(keys)
        game.draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
