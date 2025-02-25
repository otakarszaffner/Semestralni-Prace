import pygame
import math
import buttons
from sys import exit
from game_setup import *   # * vsechny promene a funkce
import random

pygame.init()

# herni okno
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space_Marines")
clock = pygame.time.Clock()

paused = False
menu_state = "main"

# promenne
global kill_count
kill_count = 0

enemy_spawn_timer = 0
item_spawn_timer = 0


# fonty
font = pygame.font.SysFont("arialblack", 40)
font2 = pygame.font.SysFont("Futura", 40)
font3 = pygame.font.SysFont("Futura", 100)

# muzika
volume = VOLUME
pygame.mixer.init()
pygame.mixer.music.set_volume(volume / 100)

#nacteni obrazku tlacitek
resume_img = pygame.image.load("semestralni_prace/images/menu/button_resume.png").convert_alpha()
quit_img = pygame.image.load("semestralni_prace/images/menu/button_quit.png").convert_alpha()
video_img = pygame.image.load("semestralni_prace/images/menu/button_video.png").convert_alpha()
sound_img = pygame.image.load("semestralni_prace/images/menu/button_audio.png").convert_alpha()
back_img = pygame.image.load("semestralni_prace/images/menu/button_back.png").convert_alpha()
options_img = pygame.image.load("semestralni_prace/images/menu/button_options.png").convert_alpha()
play_again_img = pygame.image.load("semestralni_prace/images/menu/button_play_again.png").convert_alpha()

#vytvoreni instanci tlacitek
resume_button = buttons.Button(304, 125, resume_img, 1)
options_button = buttons.Button(297, 250, options_img, 1)
quit_button = buttons.Button(336, 375, quit_img, 1)
video_button = buttons.Button(226, 75, video_img, 1)
audio_button = buttons.Button(225, 200, sound_img, 1)
back_button = buttons.Button(332, 450, back_img, 1)

# nacteni obrazku rozliseni a typy rozliseni
resolution_options = ["800x600", "1024x768", "1280x720", "1920x1080"]
resolution_images = [   
    pygame.image.load(f"semestralni_prace/images/menu/button_resolution{i+1}.png").convert_alpha()
    for i in range(4)
]

resolution_buttons = [buttons.Button(300, 200 + i * 50, resolution_images[i], 1) for i in range(4)]

# slider - zvuk
slider_rect = pygame.Rect(300, 350, 200, 10)
slider_knob = pygame.Rect(300 + int((volume / 100) * slider_rect.width), 345, 10, 20)

# obrazky pickapu
health_box = pygame.image.load("semestralni_prace/images/items/health.png").convert_alpha()
ammo_box = pygame.image.load("semestralni_prace/images/items/ammo.png").convert_alpha()

# knihovna itemu
items = {
    'health' : health_box,
    'ammo' : ammo_box
}

# funkce pro zobrazeni textu
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# nacteni obrazku pozadi
background = pygame.transform.rotozoom(pygame.image.load("semestralni_prace/images/background/background.png").convert_alpha(), 0, BACKGROUND_SCALE)

# zatim jen ukonci hru
def game_over():
    global paused, menu_state
    paused = True
    menu_state = "game_over"

    play_again_button = buttons.Button(SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2, play_again_img, 1)
    quit_button = buttons.Button(SCREEN_WIDTH // 2 + 30, SCREEN_HEIGHT // 2, quit_img, 1)

    while paused:
        screen.fill((52, 78, 91))
        draw_text("Game Over", font3, RED, SCREEN_WIDTH // 2 - 170, SCREEN_HEIGHT // 2 - 150)
        draw_text(f"Kills: {kill_count}", font2, TEXT_COL, SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 50)

        if play_again_button.draw(screen):
            reset_game()
        if quit_button.draw(screen):
            pygame.quit()
            exit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        pygame.display.update()
        clock.tick(FPS)

# funkce reset hry
def reset_game():
    global player, enemy, all_sprites_group, bullets_group, enemy_group, items_group, paused, menu_state
    player = Player()
    enemy = Enemy((ENEMY_X, ENEMY_Y))
    all_sprites_group = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    items_group = pygame.sprite.Group()

    item_box = Item('health', 900, 900)
    items_group.add(item_box)
    item_box = Item('ammo', 1000, 1000)
    items_group.add(item_box)

    all_sprites_group.add(player)
    all_sprites_group.add(items_group)
    paused = False
    menu_state = "main"

# funkce spawni enemy
def spawn_enemy():
    enemy_position = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    enemy = Enemy(enemy_position)
    enemy_group.add(enemy)
    all_sprites_group.add(enemy)

# funkce spawni item
def spawn_item():
    item_type = random.choice(['health', 'ammo'])
    item_position = (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))
    item = Item(item_type, item_position[0], item_position[1])
    items_group.add(item)
    all_sprites_group.add(item)

# clasa hrac
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("semestralni_prace/images/player/player_1.png").convert_alpha(), 0, PLAYER_SCALE)
        self.position = pygame.math.Vector2(PLAYER_S_X, PLAYER_S_Y) # pocatecni pozice
        self.base_image = self.image
        self.player_hitbox = self.base_image.get_rect(center = self.position)
        self.rect = self.player_hitbox.copy()
        self.speed = PLAYER_SPEED
        self.shooting = False
        self.shoot_cooldown = 0
        self.barrel_offset = pygame.math.Vector2(GUN_OFFSET_X, GUN_OFFSET_Y) # misto odku budou vystrelovat kulky
        self.health = PLAYER_HEALTH
        self.ammo = PLAYER_AMMO
        self.angle = 0  # az hru spustim znovu po play again, musim to inicializovat znovu
 
            
    def input(self):
        self.position_x = 0
        self.position_y = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.position_y -= self.speed
        if keys[pygame.K_s]:
            self.position_y = self.speed
        if keys[pygame.K_a]:
            self.position_x -= self.speed
        if keys[pygame.K_d]:
            self.position_x = self.speed
        
        if self.position_x != 0 and self.position_y != 0: #pohyb diagonalne
            self.position_x *= math.sqrt(0.5)
            self.position_y *= math.sqrt(0.5)

        if pygame.mouse.get_pressed() == (1, 0, 0) or keys[pygame.K_SPACE]: # (1,0,0) = (L,M,R) = (
            if self.ammo > 0:
                self.shooting = True
                self.shoot()
            else:
                self.shooting = False
        else:
            self.shooting = False
    
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = COOLDOWN
            spawn_bullet_position = self.position + self.barrel_offset.rotate(self.angle)
            self.bullet = Bullet(spawn_bullet_position[0], spawn_bullet_position[1], self.angle) # nova kulka
            bullets_group.add(self.bullet) # pridani do skupin
            all_sprites_group.add(self.bullet)
            self.ammo -= 1
            if self.ammo <= 0:
                self.ammo = 0

    
    def rotation(self):
        self.mouse_pos = pygame.mouse.get_pos()
        # rozdil mezi stredem obrazovky a pozici myse
        self.x_chanhe_mouse_player = (self.mouse_pos[0] - SCREEN_WIDTH // 2)
        self.y_chanhe_mouse_player = (self.mouse_pos[1] - SCREEN_HEIGHT // 2)
        # math.atan2 - vraci uhel v radianech / math.degrees - prevede radiany na stupne
        self.angle = math.degrees(math.atan2(self.y_chanhe_mouse_player, self.x_chanhe_mouse_player)) # uhel mezi hracem a mysi 
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center = self.rect.center) # otoci hrace podle uhlu

    def movement(self):
        self.position += pygame.math.Vector2(self.position_x, self.position_y) # aktualizace pozice hrace + vstup z klavesnice
        # aktualizace hitboxu a ohraniceni
        self.player_hitbox.center = self.position
        self.rect.center = self.player_hitbox.center
    
    def update(self):
        self.input()
        self.movement()
        self.rotation()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

# classa strely
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.image.load("semestralni_prace/images/player/bullet.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, BULLET_SCALE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y) # stred kulky nastavit na x,y
        self.x = x
        self.y = y
        self.speed = BULLET_SPEED
        self.angle = angle
        self.x_velocity = math.cos(self.angle * (2 * math.pi / 360)) * self.speed
        self.y_velocity = math.sin(self.angle * (2 * math.pi / 360)) * self.speed
        self.lifetime = LIFETIME # pro lepsi vykon / omezeny dostrel
        self.spawn_time = pygame.time.get_ticks() # da mi presny cas, kdy jsem kulku vytvoril
    
    def movement(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.rect.x = int(self.x)
        self.rect.y = int(self.y) # rect musi byt cele cislo

        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.kill()  # Smaže kulku, pokud ji vyprší životnost

    def check_collision(self):
        for enemy in enemy_group:
            if pygame.sprite.collide_rect(self, enemy):
                enemy.health -= 10
                self.kill()  # Remove bullet after collision

    def update(self):
        self.movement()
        self.check_collision()

# clasa enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__(enemy_group, all_sprites_group)
        self.animation = []
        self.animation_atack = []
        self.index = 0
        self.update_time = pygame.time.get_ticks()
        for i in range(5):
            image = pygame.image.load(f'semestralni_prace/images/enemy/run/{i}.png').convert_alpha()
            image = pygame.transform.rotozoom(image, 0, PLAYER_SCALE)
            self.animation.append(image)
        for i in range(5):
            image = pygame.image.load(f'semestralni_prace/images/enemy/atack/{i}.png').convert_alpha()
            image = pygame.transform.rotozoom(image, 0, PLAYER_SCALE)
            self.animation_atack.append(image)
        self.image = self.animation[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = position

        self.speed = ENEMY_SPEED
        self.direction = pygame.math.Vector2()
        self.velocity = pygame.math.Vector2()
        self.health = ENEMY_HEALTH
        self.position = pygame.math.Vector2(position)

    def update_animation(self):
        self.image = self.animation[self.index]
        if pygame.time.get_ticks() - self.update_time > ANIMAT_CULDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1
        # resetuje mi ciklus
        if self.index >= len(self.animation):
            self.index = 0
        if pygame.sprite.collide_rect(self, player):
            self.image = self.animation_atack[self.index]
            if pygame.time.get_ticks() - self.update_time > ANIMAT_CULDOWN:
                self.update_time = pygame.time.get_ticks()
                self.index += 1
            # resetuje mi ciklus
            if self.index >= len(self.animation):
                self.index = 0

    def follow(self):
        player_vector = pygame.math.Vector2(player.player_hitbox.center)
        enemy_vector = pygame.math.Vector2(self.rect.center)
        distance = self.get_vector_distance(player_vector, enemy_vector)

        if distance > 0:
            self.direction = (player_vector - enemy_vector).normalize()
        else:
            self.direction = pygame.math.Vector2()

        self.velocity = self.direction * self.speed
        self.position += self.velocity

        self.rect.centerx = self.position.x
        self.rect.centery = self.position.y

    def get_vector_distance(self, vector1, vector2):
        return (vector2 - vector1).magnitude()
    
    def update(self):
        global kill_count
        self.follow()
        self.update_animation()

        if pygame.sprite.collide_rect(self, player):
            player.health -= 1
            if player.health <= 0:
                player.health = 0
                game_over()

        if self.health <= 0:
            kill_count += 1
            self.kill()
# clasa itemy
class Item(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        super().__init__(items_group, all_sprites_group)
        self.type = type
        self.image = items[self.type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 40 // 2, y + (40 - self.image.get_height()))
    
    def update(self):
        if pygame.sprite.collide_rect(self, player):
            if self.type == 'health':
                player.health += 10
                if player.health > 100:
                    player.health = 100
            elif self.type == 'ammo':
                player.ammo += 10
                if player.ammo > 100:
                    player.ammo = 100
            self.kill()

# clasa camera
class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = pygame.math.Vector2()
        self.floor_rect = background.get_rect(topleft = (0, 0))

    def custom_draw(self):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH // 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT // 2

        # draw the floor
        floor_offset_pos = self.floor_rect.topleft - self.offset
        screen.blit(background, floor_offset_pos)

        for sprite in all_sprites_group:
            offset_pos = sprite.rect.topleft - self.offset
            screen.blit(sprite.image, offset_pos)
        
        draw_text(f'AMMO: {player.ammo}', font2, TEXT_COL, 20, 20)
        draw_text(f'HEALTH: {player.health}', font2, TEXT_COL, 20, 60)
        draw_text(f'ENEMY HEALTH: {enemy.health}', font2, RED, 950, 25)
        draw_text(f'ENEMY KILLS: {kill_count}', font2, TEXT_COL, 950, 60)

# obrazky/sprity
all_sprites_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()

# knihovna itemu
item_box = Item('health', 900, 900)
items_group.add(item_box)
item_box = Item('ammo', 1000, 1000)
items_group.add(item_box)

camera = Camera()
player = Player()

enemy = Enemy((ENEMY_X, ENEMY_Y))

all_sprites_group.add(player)
all_sprites_group.add(items_group)

running = True
adjusting_volume = False

# hlavni herni cyklus
while running:
    keys = pygame.key.get_pressed()

    global current_resolution

    if paused == False:
        # aktualizace vsech objektu
        all_sprites_group.update()

        screen.fill(BLACK)
        camera.custom_draw()

        # kazdou sekundu pridavam +1, kdyz se naplni timer spawnu Enem/Item a resetuju timer
        enemy_spawn_timer += 1
        item_spawn_timer += 1

        if enemy_spawn_timer >= 240:
            spawn_enemy()
            enemy_spawn_timer = 0

        if item_spawn_timer >= 60:
            spawn_item()
            item_spawn_timer = 0

    # je hra pauznuta?
    if paused == True:
        screen.fill((52, 78, 91))
    # stavy menu / 'main', 'options', 'video_options', 'audio_options'

        # je menu state main? 
        if menu_state == "main":
            if resume_button.draw(screen):
                screen.fill(BLACK)
                paused = False
            if options_button.draw(screen):
                menu_state = "options"
            if quit_button.draw(screen):
                running = False
        
        # je menu state options?
        if menu_state == "options":
            if video_button.draw(screen):
                menu_state = "video_options"
            if audio_button.draw(screen):
                menu_state = "audio_options"
            if back_button.draw(screen):
                menu_state = "main"

        # je menu state video_options?
        if menu_state == "video_options":
            draw_text("Select Resolution", font, TEXT_COL, 300, 150)
            for i, button in enumerate(resolution_buttons):
                if button.draw(screen):
                    current_resolution = tuple(map(int, resolution_options[i].split("x")))
                    screen = pygame.display.set_mode(current_resolution)  # aktualizace screen
                    print(f"Resolution set to: {resolution_options[i]}")

            if back_button.draw(screen):
                menu_state = "main"
        
        # je menu state audio_options?
        if menu_state == "audio_options":
            # vykresleni slideru
            draw_text("Adjust Volume", font, TEXT_COL, 300, 150)
            pygame.draw.rect(screen, (180, 180, 180), slider_rect)
            pygame.draw.rect(screen, (255, 0, 0), slider_knob)

            # posun a logika slideru
            mouse_x, _ = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0]:
                if slider_knob.collidepoint(mouse_x, slider_knob.y) or adjusting_volume:
                    adjusting_volume = True
                    slider_knob.x = max(slider_rect.x, min(mouse_x, slider_rect.x + slider_rect.width))
                    volume = int(((slider_knob.x - slider_rect.x) / slider_rect.width) * 100)
                    pygame.mixer.music.set_volume(volume / 100)
                    print(f"Volume set to: {volume}")
            else:
                adjusting_volume = False

            if back_button.draw(screen):
                menu_state = "main"

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = True
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit()