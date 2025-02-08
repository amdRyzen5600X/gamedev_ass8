import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


LEVELS = {
    1: [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W..........................................................................W",
        "W..C...................................................................C...W",
        "W..........................................................................W",
        "W...............WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W...............W..........................................................W",
        "W...............W..............................C...........................W",
        "W...............W................................................C.........W",
        "W.E.............W..........................................................W",
        "W...............W..........................................................W",
        "W...............W..........................................................W",
        "W...............W..............................C...........................W",
        "W...............W................................................C.........W",
        "W.E.............W..........................................................W",
        "W...............W..........................................................W",
        "W...............WWWWWWWWWWWWWWWWWWWWWWWWWWWW...............................W",
        "W..........................................................................W",
        "W.E........................................................................W",
        "W..........................................................................W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW...............................W",
        "W..........................................................................W",
        "W.E........................................................................W",
        "W.........................................E................................W",
        "W..........................................................................W",
        "W..........................................................................W",
        "W...................C......................................................W",
        "W.............WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W...................C.......................WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W...........................................WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W...........................................WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ],
    2: [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W.........W.........................................W......................W",
        "W..C......W...........................E.............W..................C...W",
        "W.........W................................................................W",
        "W.........W......E.........................................................W",
        "W.........W................................................................W",
        "W.........W....................................C...........................W",
        "W.........W....................................C...........................W",
        "W.........W..............E.......................................C.........W",
        "W.........W....................................C...........................W",
        "W.........W..............E.......................................C.........W",
        "W.E.......W................................................................W",
        "W.........W.........................................W......................W",
        "W.........W.........................................W.......E..............W",
        "W.........W......E..................................W......................W",
        "W.E.......W.........................................W......................W",
        "W.........W.........................................W......................W",
        "W.........WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW.......E..............W",
        "W.........W......E..................................W......................W",
        "W.........W..............E..........................W............C.........W",
        "W.E.......W........................W................W......................W",
        "W.........W........................W................W......................W",
        "W.........W........................W................W.......E..............W",
        "W.........W......E.................W................W......................W",
        "W.E................................W................W......................W",
        "W..................................W......E.........W......................W",
        "W..................................W.......................................W",
        "W...................C..............W.......................................W",
        "W..................................W..E....................................W",
        "W..................................W.......................................W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]
}

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.x + SCREEN_WIDTH // 2
        y = -target.rect.y + SCREEN_HEIGHT // 2
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/player_idle.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5
        self.health = 100
        self.score = 0

    def move(self, dx, dy, walls):
        self.rect.x += dx
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x -= dx
        self.rect.y += dy
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.y -= dy
                # if dx > 0:
                #     self.rect.right = wall.rect.left
                # elif dx < 0:
                #     self.rect.left = wall.rect.right
                # if dy > 0:
                #     self.rect.bottom = wall.rect.top
                # elif dy < 0:
                #     self.rect.top = wall.rect.bottom

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        self.image = pygame.image.load("assets/enemy.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self, player, walls):
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = (dx**2 + dy**2)**0.5
        if distance != 0:
            self.rect.x += self.speed * dx / distance
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.x -= self.speed * dx / distance
            self.rect.y += self.speed * dy / distance
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    self.rect.y -= self.speed * dy / distance

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/coin.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/wall.png").convert()
        self.rect = self.image.get_rect(topleft=(x, y))

def load_level(level_num):
    walls = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    layout = LEVELS[level_num]
    for y, row in enumerate(layout):
        for x, cell in enumerate(row):
            if cell == "W":
                walls.add(Wall(x * TILE_SIZE, y * TILE_SIZE))
            elif cell == "C":
                coins.add(Coin(x * TILE_SIZE, y * TILE_SIZE))
            elif cell == "E":
                speed = 1 if level_num == 1 else 2
                enemies.add(Enemy(x * TILE_SIZE, y * TILE_SIZE, speed))

    return walls, coins, enemies

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("2D Adventure")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    pygame.mixer.music.load("assets/background_music.mp3")
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.02)
    coin_sound = pygame.mixer.Sound("assets/coin_sound.wav")
    hit_sound = pygame.mixer.Sound("assets/hit_sound.wav")

    current_level = 1
    walls, coins, enemies = load_level(current_level)
    player = Player(TILE_SIZE * 2, TILE_SIZE * 2)
    camera = Camera(len(LEVELS[1][0]) * TILE_SIZE, len(LEVELS[1]) * TILE_SIZE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]: dx -= player.speed
        if keys[pygame.K_d]: dx += player.speed
        if keys[pygame.K_w]: dy -= player.speed
        if keys[pygame.K_s]: dy += player.speed
        player.move(dx, dy, walls)

        camera.update(player)

        for enemy in enemies:
            enemy.update(player, walls)
            if enemy.rect.colliderect(player.rect):
                player.health -= 10
                hit_sound.play()
                if player.health <= 0:
                    running = False

        for coin in coins:
            if player.rect.colliderect(coin.rect):
                player.score += 10
                coin_sound.play()
                coins.remove(coin)

        if len(coins) == 0:
            if current_level == 1:
                current_level = 2
                walls, coins, enemies = load_level(current_level)
                player.rect.topleft = (TILE_SIZE * 2, TILE_SIZE * 2)
            else:
                running = False

        screen.fill(BLACK)
        for wall in walls:
            screen.blit(wall.image, camera.apply(wall))
        for coin in coins:
            screen.blit(coin.image, camera.apply(coin))
        for enemy in enemies:
            screen.blit(enemy.image, camera.apply(enemy))
        screen.blit(player.image, camera.apply(player))

        score_text = font.render(f"Score: {player.score}", True, WHITE)
        health_text = font.render(f"Health: {player.health}", True, RED)
        screen.blit(score_text, (10, 10))
        screen.blit(health_text, (10, 50))

        pygame.display.flip()
        clock.tick(FPS)

    screen.fill(BLACK)
    if player.health <= 0:
        text = font.render("Game Over!", True, RED)
    else:
        text = font.render("Level Complete!", True, YELLOW)
    screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 20))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
