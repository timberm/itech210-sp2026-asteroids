import pygame
import random
import math

WIDTH = 800
HEIGHT = 450
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ITECH 210 ASTEROIDS")
clock = pygame.time.Clock()
debug = False

#background music
pygame.mixer.music.load("notathing2.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)

#bullet sound effect
bullet_sound = pygame.mixer.Sound('alienshoot2.ogg')

#colors
BLUE = (31, 81, 255)
WHITE =(255,255,255)

#fonts
score_font = pygame.font.SysFont("showcard gothic", 30)
go_font = pygame.font.SysFont("showcard gothic", 60)

#load images
space_ship = pygame.image.load("images/playerShip1_orange.png").convert_alpha()
space_ship = pygame.transform.rotate(space_ship, -90)
space_bg = pygame.image.load("images/bg.jpg")
asteroid_1 = pygame.image.load("images/meteorBrown_big1.png")


#background
bg = pygame.transform.scale(space_bg, (WIDTH, HEIGHT))

#player
# player_angle = -90
# player_size = (50,50)
# player_pos = [WIDTH//2, HEIGHT//2]
# player_hit_radius = 18
# player_speed = 20
# player_lives = 3
player = {
    'angle': -90,
    'size': (50,50),
    'pos':[WIDTH//2, HEIGHT//2],
    'speed': 20,
    'lives':3,
    'radius': 19,
    'invincible_timer': 2000,
    'last_hit': 0
}

#bullets
bullets = []
bullet_fire_rate = 200
bullet_last_fire = 0
bullet_speed = 30

#asteroids
asteroids = []
asteroid_spawn_rate = 1000
asteroid_last_spawn = 0
asteroid_spawn_locations = [[WIDTH//2, -200],[WIDTH+200, 0],[WIDTH+200, HEIGHT],[WIDTH//2, HEIGHT+200],[-200, HEIGHT], [-200, 0]]

#Game Properties
game_over = False
score = 0
running = True

#functions
def update_player(dt):
    global player_angle
    angle = 1
    
    #get input and update position
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT ]:
        player['angle'] -= angle * player['speed'] * dt
    if keys[pygame.K_RIGHT ]:
        player['angle'] += angle * player['speed'] * dt
    
def update_bullet_position(dt, bullet):
    rad = math.radians(bullet['angle'])
    dx = math.cos(rad) * bullet['speed'] * dt
    dy = math.sin(rad) * bullet['speed'] * dt
    bullet['pos'][0] += dx
    bullet['pos'][1] += dy

def check_offscreen(item):
    if item['pos'][0] < 0 or item['pos'][0] > WIDTH:
        return True
    if item['pos'][1] < 0 or item['pos'][1] > HEIGHT:
        return True
    return False

def update_asteroid_position(dt, asteroid):
    rad = math.radians(asteroid['angle'])
    dx = math.cos(rad) * asteroid['speed'] * dt
    dy = math.sin(rad) * asteroid['speed'] * dt
    asteroid['pos'][0] += dx
    asteroid['pos'][1] += dy

def draw_player(screen):
    player_sprite = pygame.transform.scale(space_ship, player['size'])
    player_sprite = pygame.transform.rotate(player_sprite, player['angle']*-1)
    player_rect = player_sprite.get_rect(center=player['pos'])
    screen.blit(player_sprite, player_rect)

def draw_bullet(screen, bullet):
    pygame.draw.circle(screen, BLUE, bullet['pos'], bullet['radius'])

def draw_asteroid(screen, asteroid):
    asteroid_sprite = pygame.transform.rotate(asteroid_1, asteroid['angle'])
    asteroid_rect = asteroid_sprite.get_rect(center=asteroid['pos'])
    screen.blit(asteroid_sprite, asteroid_rect)

#main loop
while running:
    dt = clock.tick(60) / 100  #60 frames per second
    tick = pygame.time.get_ticks()

    #check for pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    if game_over:
        continue   

    #========== 
    #  UPDATE 
    #==========
    player_input = pygame.key.get_pressed() 
    
    #update player position
    if player_input[pygame.K_LEFT ]:
        player['angle'] -= player['speed'] * dt
    if player_input[pygame.K_RIGHT ]:
        player['angle'] += player['speed'] * dt
    
    #spawn bullets
    if player_input[pygame.K_SPACE] and tick > bullet_last_fire + bullet_fire_rate:
        bullets.append({
            'pos': player['pos'].copy(),
            'angle': player['angle'],
            'speed': bullet_speed,
            'radius': 4
        })
        bullet_last_fire = tick
        bullet_sound.play()

    #update bullet position
    for i in range(len(bullets)):
        if check_offscreen(bullets[i]) == False:
            update_bullet_position(dt, bullets[i])

    
    #check for bullets off screen



    #spawn asteroids
    if tick > asteroid_last_spawn + asteroid_spawn_rate:
        pos = random.choice(asteroid_spawn_locations).copy()
        target_x = player['pos'][0] + (random.random()*(WIDTH//2))-(WIDTH//4)
        target_y = player['pos'][1] + (random.random()*(HEIGHT//2))-(HEIGHT//4)
        asteroids.append({
            'pos': pos,
            'angle': math.degrees(math.atan2(player['pos'][1]-pos[1], target_x-pos[0])), 
            'speed': 4,
            'radius': 45
        })
        asteroid_last_spawn = tick

    #update asteroid position
    # update_asteroid_position(dt, bullets)
    for i in range(len(asteroids)):
        update_asteroid_position(dt, asteroids[i])



    
    #check for asteroids off screen
    #if check_offscreen(asteroid) == True:




    #check for collisions with asteroids
    for asteroid in asteroids:
        if math.dist(asteroid['pos'], player['pos']) < asteroid['radius'] + player['radius']:
            asteroids.remove(asteroid)
            if tick > player['last_hit'] + player['invincible_timer']:
                player['lives'] -= 1
                player['last_hit'] = tick

                if player['lives'] <= 0:
                    game_over = True
        
        for bullet in bullets:
            if math.dist(asteroid['pos'], bullet['pos']) < asteroid['radius'] + bullet['radius']:
                asteroids.remove(asteroid)
                bullets.remove(bullet)
                score += 10

    
    
    #========== 
    #  DRAW
    #==========
    #draw background
    screen.blit(bg, (0,0))

    #draw bullets
    for i in range(len(bullets)):
        draw_bullet(screen, bullets[i])


    #draw asteroids
    for i in range(len(asteroids)):
        draw_asteroid(screen, asteroids[i])



    #draw player
    #if the player is in invincible state flicker the sprit
    #else draw normally
    if tick > player['last_hit'] and tick < player['last_hit'] + player['invincible_timer']: 
        if tick % 200 < 100:
            pass
        else: 
            draw_player(screen)
    else:
        draw_player(screen) 
    
    #draw player lives
    icon_width = 25
    for i in range(player['lives']):
        icon_sprite = pygame.transform.scale(space_ship, (icon_width, icon_width))
        icon_sprite = pygame.transform.rotate(icon_sprite, 90)
        icon_rect = icon_sprite.get_rect(bottomleft=(i*icon_width+(10*(i+1)), HEIGHT-10))
        screen.blit(icon_sprite, icon_rect)
    
    #draw score
    score_text = score_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(bottomright=(WIDTH-10,HEIGHT-10))
    screen.blit(score_text, score_rect)
    
    #draw Game Over
    if game_over:
        go_text = go_font.render("GAME OVER", True, WHITE)
        go_rect = go_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(go_text, go_rect)
    
    pygame.display.flip()
    

pygame.quit()

