from pgzero.actor import Actor
import pgzrun
from pygame import Rect

tela_atual = 'menu'
music.play('music_b')

WIDTH = 800
HEIGHT = 600

bg = Actor('background')

entrar = Rect((200, 50), (400, 100))
volume = Rect((200, 250), (400, 100))
sair = Rect((200, 450), (400, 100))

volume_on = True

TILE_SIZE = 64
platforms = []

block1 = Actor("terrain_stone_cloud_left", (32, 568))
rect1 = Rect(block1.x - TILE_SIZE // 2, block1.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
platforms.append((block1, rect1))

block9 = Actor("terrain_stone_horizontal_overhang_right", (448, 100))

width2 = int(TILE_SIZE * 1)
height2 = int(TILE_SIZE * 0.1)
rect9 = Rect(block9.x - width2 // 2, block9.y - TILE_SIZE // 2, width2, height2)
platforms.append((block9, rect9))

block2 = Actor("terrain_stone_cloud_right", (768, 568))
rect2 = Rect(block2.x - TILE_SIZE // 2, block2.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
platforms.append((block2, rect2))

for x in range(96, 750, 64):
    middle = Actor("terrain_stone_cloud_middle", (x, 568))
    rect = Rect(middle.x - TILE_SIZE // 2, middle.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
    platforms.append((middle, rect))

block5 = Actor("terrain_stone_cloud", (224, 443))
rect5 = Rect(block5.x - width2 // 2, block5.y - TILE_SIZE // 2, width2, height2)
platforms.append((block5, rect5))

block6 = Actor("terrain_stone_cloud", (352, 347))
rect6 = Rect(block6.x - width2 // 2, block6.y - TILE_SIZE // 2, width2, height2)
platforms.append((block6, rect6))

block7 = Actor("terrain_stone_cloud", (480, 283))
rect7 = Rect(block7.x - width2 // 2, block7.y - TILE_SIZE // 2, width2, height2)
platforms.append((block7, rect7))

block8 = Actor("terrain_stone_cloud", (608, 219))
rect8 = Rect(block8.x - width2 // 2, block8.y - TILE_SIZE // 2, width2, height2)
platforms.append((block8, rect8))

block10 = Actor("terrain_stone_horizontal_overhang_left", (32, 100))
rect10 = Rect(block10.x - TILE_SIZE // 2, block10.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)
platforms.append((block10, rect10))

for x in range(96, 450, 64):
    middle = Actor("terrain_stone_horizontal_middle", (x, 100))
    width1 = int(TILE_SIZE * 1)
    height1 = int(TILE_SIZE * 0.1)
    rect = Rect(middle.x - width1 // 2, middle.y - TILE_SIZE // 2, width1, height1)
    platforms.append((middle, rect))

door = Actor("door", (32, 36))
door_rect = Rect(door.x - TILE_SIZE // 2, door.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)

key = Actor("key", (768, 504))
key_rect = Rect(key.x - TILE_SIZE // 2, key.y - TILE_SIZE // 2, TILE_SIZE, TILE_SIZE)

class Inimigo:
    def __init__(self, images, pos, speed, x_limits, rect_offset):
        self.frames = images
        self.index = 0
        self.timer = 0
        self.interval = 10
        self.direction = 1
        self.speed = speed
        self.actor = Actor(images[0], pos)
        self.rect_offset = rect_offset
        self.x_limits = x_limits

    def get_rect(self):
        width, height, off_x, off_y = self.rect_offset
        return Rect(self.actor.x - width // 2, self.actor.y + off_y, width, height)

    def update(self):
        self.actor.x += self.direction * self.speed
        if self.actor.x < self.x_limits[0] or self.actor.x > self.x_limits[1]:
            self.direction *= -1

        self.timer += 1
        if self.timer >= self.interval:
            self.timer = 0
            self.index = (self.index + 1) % len(self.frames)
            self.actor.image = self.frames[self.index]

    def draw(self):
        self.actor.draw()

worm = Inimigo(
    ["worm_ring_move_a", "worm_ring_move_b"],
    (96, 36),
    1.5,
    (96, 450),
    (TILE_SIZE, int(TILE_SIZE * 0.53), TILE_SIZE // -2, TILE_SIZE // 2 - int(TILE_SIZE * 0.53))
)

slime = Inimigo(
    ["slime_1", "slime_2"],
    (704, 504),
    1,
    (32, 768),
    (TILE_SIZE, int(TILE_SIZE * 0.8), TILE_SIZE // -2, TILE_SIZE // 2 - int(TILE_SIZE * 0.8))
)

class Heroi:
    def __init__(self, pos, rect_size, animations):
        self.actor = Actor(animations['parado'][0], pos)
        self.width, self.height, self.off_x, self.off_y = rect_size
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_force = -11
        self.on_ground = False
        self.animations = animations
        self.index = 0
        self.timer = 0
        self.interval = 20

    def get_rect(self):
        return Rect(self.actor.x - self.width // 2, self.actor.y + self.off_y, self.width, self.height)

    def update(self):
        self.velocity_y += self.gravity
        self.actor.y += self.velocity_y
        self.on_ground = False

        hero_rect = self.get_rect()

        for _, plat_rect in platforms:
            if hero_rect.colliderect(plat_rect) and self.velocity_y >= 0:
                self.actor.y = plat_rect.top - (TILE_SIZE // 2) + 1
                self.velocity_y = 0
                self.on_ground = True
                break

        if keyboard.up and self.on_ground:
            self.velocity_y = self.jump_force
            sounds.jump.play()

        if keyboard.left:
            self.actor.x -= 5
        if keyboard.right:
            self.actor.x += 5

        self.actor.x = max(20, min(780, self.actor.x))

        self.timer += 1
        if self.timer >= self.interval:
            self.timer = 0
            if self.velocity_y < 0 or not self.on_ground:
                self.actor.image = self.animations['pulando'][0]
            elif keyboard.left or keyboard.right:
                self.index = (self.index + 1) % len(self.animations['andando'])
                self.actor.image = self.animations['andando'][self.index]
            else:
                self.index = (self.index + 1) % len(self.animations['parado'])
                self.actor.image = self.animations['parado'][self.index]

    def draw(self):
        self.actor.draw()

alien = Heroi(
    (32, 350),
    (int(TILE_SIZE * 0.4), int(TILE_SIZE * 0.1), TILE_SIZE // -2, TILE_SIZE // 2 - int(TILE_SIZE * 0.1)),
    {
        'parado': ["character_pink_front", "character_pink_duck"],
        'andando': ["character_pink_walk_a", "character_pink_walk_b"],
        'pulando': ["character_pink_jump"]
    }
)

vida = 3
chave = False
win = False
game_over = False

invulneravel = False
frames_invulneravel = 0

def reiniciar_jogo():
    global tela_atual, game_over, win, vida, chave
    tela_atual = 'menu'
    game_over = False
    win = False
    vida = 3
    chave = False
    alien.actor.x, alien.actor.y = 32, 350
    worm.actor.x = 96
    slime.actor.x = 704

def on_mouse_down(pos):
    global volume_on, tela_atual

    if entrar.collidepoint(pos):
        tela_atual = 'jogo'

    if volume.collidepoint(pos):
        if volume_on:
            volume_on = False
            music.pause()
        else:
            volume_on = True
            music.unpause()

    if sair.collidepoint(pos):
        exit()

def update():
    global vida, chave, win, game_over, tela_atual, invulneravel, frames_invulneravel

    if tela_atual != 'jogo':
        return

    alien.update()
    worm.update()
    slime.update()

    alien_rect = alien.get_rect()
    worm_rect = worm.get_rect()
    slime_rect = slime.get_rect()

    if alien_rect.colliderect(worm_rect) and not invulneravel:
        vida -= 1
        sounds.hurt.play()
        invulneravel = True
        frames_invulneravel = 0

    if alien_rect.colliderect(slime_rect) and not invulneravel:
        vida -= 1
        sounds.hurt.play()
        invulneravel = True
        frames_invulneravel = 0

    if invulneravel:
        frames_invulneravel += 1
        if frames_invulneravel >= 60:
            invulneravel = False

    if alien_rect.colliderect(key_rect):
        chave = True

    if chave and alien_rect.colliderect(door_rect) and not game_over:
        win = True
        game_over = True
        sounds.collect.play()
        clock.schedule_unique(reiniciar_jogo, 3)

    if vida <= 0 and not game_over:
        game_over = True
        win = False
        clock.schedule_unique(reiniciar_jogo, 3)

def draw():
    if tela_atual == 'menu':
        bg.draw()
        screen.draw.filled_rect(entrar, "blue")
        screen.draw.text("INICIAR", center=entrar.center, fontname='pixel', fontsize=30, color="white")
        screen.draw.filled_rect(volume, "blue")
        screen.draw.text("MUSICA", center=volume.center, fontname='pixel', fontsize=30, color="white")
        screen.draw.filled_rect(sair, "blue")
        screen.draw.text("SAIR", center=sair.center, fontname='pixel', fontsize=30, color="white")

    elif tela_atual == 'jogo':
        bg.draw()
        for bloco, rect in platforms:
            bloco.draw()
        door.draw()
        if not chave:
            key.draw()
        worm.draw()
        slime.draw()
        if invulneravel:
            if (frames_invulneravel // 5) % 2 == 0:
                alien.draw()
        else:
            alien.draw()
        screen.draw.text(f"Vida: {vida}", (700, 10), fontsize=30, color="red")
        if game_over:
            if win:
                screen.draw.text("Vitoria", center=(WIDTH // 2, HEIGHT // 2), fontname='pixel', fontsize=80, color="green")
            else:
                screen.draw.text("Derrota", center=(WIDTH // 2, HEIGHT // 2), fontname='pixel', fontsize=80, color="red")

