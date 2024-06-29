import pygame
from pygame.locals import *
# import mydef
import json
from os import path

pygame.init()

clock = pygame.time.Clock()
#difine my frame rate
fps = 60

#coordinates

screen_w = 800
screen_h = 800

screen = pygame.display.set_mode((screen_w,screen_h))
#caption

pygame.display.set_caption('gamebypy')

#my varibles

tile_size = 40
Game_Over  = 0
main_menu = True
level = 0
max_level = 2

#load img

image = pygame.image.load("PNG/spacebk.png")
image = pygame.transform.scale(image,(screen_w,screen_h))
restart_img = pygame.image.load('PNG/restart.png')
start_img = pygame.image.load('PNG/start.png')
exit_img = pygame.image.load('PNG/exit.png')

# def draw_grid():
#     for line in range(0,20):
#         #draws line to the screen to make placing thing easier
#         pygame.draw.line(screen,(255,255,255),(0,line * tile_size),(screen_w,line * tile_size))
#         pygame.draw.line(screen,(255,255,255),(line * tile_size,0),(line * tile_size,screen_h))

def reset_level(level):
    player.reset(100,screen_h - 180)
    blob_group.empty()
    spike_group.empty()
    exit_group.empty()

    if path.exists(f"level{level}_data.json"):
        with open(f"level{level}_data.json", "r") as f:
            world_data = json.load(f)
    world = World(world_data)

    return world


class button():
    def __init__(b, x, y, image):
        b.image = pygame.transform.scale(image,(300,100))
        #lma b3ml kda m4 b7tag 2ny 23ml .load b3mlha lw7dha
        b.rect = b.image.get_rect()
        b.rect.x = x
        b.rect.y = y
        b.clicked = False
        #34an 2dos just once
    def draw(b):
        action = False

        #get mouse position
        pos = pygame.mouse.get_pos()

        #check mouseover and click conditions
        if b.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and b.clicked == False:
                #left click index = 0
                action = True
                b.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            b.clicked = False





        #draw my buttons
        screen.blit(b.image,b.rect)
        #hna 2l coordinates mkan 2l rectangle bta3y 2lh7ddo fo2
        #wa hy3ml blit llsora 2l hd5lha
        return action

class player():
    def __init__(p,x,y):
        p.reset(x,y)


    def update(p,Game_Over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        if Game_Over == 0:
        #keypress
            key = pygame.key.get_pressed()
            if key[pygame.K_UP] and p.jumped == False and p.in_air == False:
                p.vel_y = -15
                p.jumped = True
            if key[pygame.K_UP] == False:
                p.jumped = False

            if key[pygame.K_LEFT]:
                dx -= 5
                p.counter += 1
                p.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                p.counter += 1
                p.direction = 1
            if key[pygame.K_LEFT] == False and key[pygame.K_RIGHT] == False:
                p.counter = 0
                p.index = 0
                p.image = p.images_right[p.index]


            #handle animation
            if p.counter > walk_cooldown:
                p.counter = 0
                p.index += 1
                if p.index >= len(p.images_right):
                    p.index = 0
                if p.direction == 1:
                    p.image = p.images_right[p.index]
                if p.direction == -1:
                    p.image = p.images_left[p.index]




            #add gravity
            p.vel_y += 1
            if p.vel_y > 10 :
                p.vel_y = 10

            dy += p.vel_y
    #hncalculate collision bm3na lw 2lmkan da fy 7aga wa
    #hy7sl collision m4 hy3dy
            #collision
            p.in_air = True

            for tile in world.tile_list:
                #check for collision in x direction
                if tile[1].colliderect(p.rect.x + dx, p.rect.y, p.width, p.height):
                    dx = 0
                #check for collision in y direction
                if tile[1].colliderect(p.rect.x, p.rect.y + dy, p.width, p.height):
                    #check if below the ground i.e. jumping
                    if p.vel_y < 0:
                        dy = tile[1].bottom - p.rect.top
                        p.vel_y = 0
                    #check if above the ground i.e. falling
                    elif p.vel_y >= 0:
                        dy = tile[1].top - p.rect.bottom
                        p.vel_y = 0
                        p.in_air = False
            #check for collision with enemy or danger
            #2l25tlaf 3n dy wa 2l rect() 2n 2na hna bt check between two charectors m4
            #bt check collision between rectangles
                if pygame.sprite.spritecollide(p,blob_group,False):
                    #lw 3mlt True lw 5bto fy b3d hy5tfo
                    Game_Over = -1
                if pygame.sprite.spritecollide(p,spike_group,False):
                    Game_Over = -1
                if pygame.sprite.spritecollide(p,exit_group,False):
                    Game_Over = 1


            #update player coordinates
            p.rect.x += dx
            p.rect.y += dy
            #dt kant 2bl collision 34an my234
            # if self.rect.bottom > screen_h :
            #     self.rect.bottom = screen_h
            #     dy = 0
            #draw player into the screen
        elif Game_Over == -1:
            p.image = p.dead_image
            p.rect.y -= 5
        screen.blit(p.image,p.rect)
        pygame.draw.rect(screen,(255,255,255),p.rect, -1)
        return Game_Over

    def reset(set, x, y):
        set.images_right = []
        set.images_left = []
        set.index = 0
        set.counter = 0
        for num in range(1,9):
            img_right = pygame.image.load(f"PNG/p1_walk0{num}.png")
            img_right = pygame.transform.scale(img_right,(40,60))
            img_left = pygame.transform.flip(img_right, True, False)
            #flip bta5d true and false fy 25r 7gtyn as true indicates yes flip
            #false do not flip true in the sec flip horizontaly
            set.images_right.append(img_right)
            set.images_left.append(img_left)
        set.dead_image = pygame.image.load('PNG/spirit.png')
        set.image = set.images_right[set.index]
        set.rect = set.image.get_rect()
        set.rect.x = x
        set.rect.y = y
        set.width = set.image.get_width()
        set.height = set.image.get_height()
        set.vel_y = 0
        set.jumped = False
        set.direction = 0
        set.in_air = True
        #check if he is jumping


class World():
    def __init__(wd,data):
        #2llist 2lh7t fyha 2lmrb3at 2lgdyda
        wd.tile_list = []
        #h3rf 2lswr 2lbst3mlha
        ground = pygame.image.load("PNG/img.png")
        down_grouond = pygame.image.load("PNG/spaceground.png")
        spike = pygame.image.load("PNG/spikes.png")
        #hloop 3la 2l 2llista bta3t 2l2rkam blraw and coulmn
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 2:
                    img = pygame.transform.scale(ground,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    wd.tile_list.append(tile)
                if tile == 1:
                        img = pygame.transform.scale(down_grouond,(tile_size,tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count * tile_size
                        img_rect.y = row_count * tile_size
                        tile = (img, img_rect)
                        wd.tile_list.append(tile)
                if tile == 3:
                    blob = enemy(col_count * tile_size, row_count * tile_size + 6)
                    #2l plus fy y axis 34an 25lyh y2f 3la the tile i created wa m4 y float
                    blob_group.add(blob)
                if tile == 6:
                    spikes = ground_danger(col_count * tile_size -35, row_count * tile_size -30)
                    spike_group.add(spikes)
                if tile == 8:
                    exitt = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exitt)

#34an 25lyh yt7rk llnext row wa coulmn
                col_count += 1
            row_count += 1

    def draw(wd):
       #34an 2l7aga ttb3 kl 4waya
        for tile in wd.tile_list:
           #hloop 3la 2l2info 2l2na tl3tha mn index zero
           #hna b loop 34an 2tb3 b blit which bttb3 3la mrb3at
           #fhna bloop 3la my tiles wtb3 2lfl for loop
           screen.blit(tile[0] ,tile[1])
           pygame.draw.rect(screen, (255,255,255), tile[1], -1)
#100 pixel on x and for y screen hight - (50 pixel for tile and 80 for player so 130)



class enemy(pygame.sprite.Sprite):
    #.sprite.sprite to control the movement and stuff and make it act as a sprite
    def __init__(enmy, x, y):
        pygame.sprite.Sprite.__init__(enmy)
        #i want the enemy class to be a child of sprite class  and inherit  somethings
        enmy.image = pygame.image.load('slimeBlue.png')
        enmy.rect = enmy.image.get_rect()
        enmy.rect.x = x
        #position rectangle in x input
        enmy.rect.y = y
        #position rect in y input
        enmy.move_direction = 1
        #dlw2ty 2na 3yza 27rkhm fa to do that ill move there blockes
        enmy.move_counter = 0
        #to know how many pixels it moved
    def update(enmy):
        enmy.rect.x += enmy.move_direction #move right
        enmy.move_counter += 1
        # if reached the limit flip
        if abs(enmy.move_counter) > 60:
            enmy.move_direction *= -1
            enmy.move_counter *= -1
            #msfrt4 2lcounter 34an 3yzah ym4y ymyn 2lcounter b3dha
            #4malo m4 yrg3 llcenter wa yro7 ymyn wa yrg3 llcenter wyro7 ymyn



class ground_danger(pygame.sprite.Sprite):
    def __init__(danger, x, y):
        pygame.sprite.Sprite.__init__(danger)
        danger.image = pygame.image.load('PNG/spikes.png')
        danger.rect = pygame.transform.scale(image,(tile_size,tile_size/2))
        #2lns 34an tb2a mn t7t mn ns 2lblock mtb2a4 block kmla
        danger.rect = danger.image.get_rect()
        danger.rect.x = x
        danger.rect.y = y
        danger.move_direction = 1
        danger.move_counter = 0

class Exit(pygame.sprite.Sprite):
    def __init__(EX, x, y):
        pygame.sprite.Sprite.__init__(EX)
        img = pygame.image.load("flagBlue.png")
        EX.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        EX.rect = EX.image.get_rect()
        EX.rect.x = x
        EX.rect.y = y



# world_data =[
# [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2],
# [2, 2, 0, 0, 0, 2, 0, 0, 3, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 7, 0, 0, 7, 2, 0, 0, 0, 1],
# [1, 0, 2, 0, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 2, 2, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 1, 1, 1],
# [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1, 1],
# [1, 0, 0, 0, 0, 0, 2, 2, 2, 0, 6, 6, 6, 6, 1, 1, 1, 1, 1, 1],
# [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
# [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# ]
player = player(100,screen_h - 180)

blob_group = pygame.sprite.Group()
#group so i can use my enemy class
spike_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

if path.exists(f"level{level}_data.json"):
    with open(f"level{level}_data.json", "r") as f:
        world_data = json.load(f)
world = World(world_data)

#create bottons
restart_botton = button(screen_w // 2-160,screen_h // 2-130,restart_img)
#34an tb2a in the middle of the screen
start_botton = button(screen_w // 2-160,screen_h // 2-130,start_img)
exit_botton = button(screen_w // 2-160,screen_h // 2,exit_img)



run = True
while run:
    clock.tick(fps)

    screen.blit(image,(0,0))
    if main_menu == True:
        if exit_botton.draw():
            run = False
        if start_botton.draw():
            main_menu = False

    else:
        world.draw()
        if Game_Over == 0:

        #m4 m7taga fl enemy 2nady kl 7aga fl update ill just 2nady the whole group
            blob_group.update()

        #i haven`t defined a draw in enemy but the reason it is working is because
        #of the .spirit.spirit they automaticly draw what is in self.image
        blob_group.draw(screen)
        # draw_grid()
        spike_group.draw(screen)
        exit_group.draw(screen)

        Game_Over = player.update(Game_Over)
        #34an gameover value argument tt8yr

        if Game_Over == -1:
            if restart_botton.draw():
                # player.reset(100,screen_h - 180)
                world_data = []
                world = reset_level(level)
                Game_Over = 0
        if Game_Over == 1:
            level += 1
            if level <= max_level:
                world_data = []
                world = reset_level(level)
                Game_Over = 0
            else:
                if restart_botton.draw():
                    level = 0
                    world_data = []
                    world = reset_level(level)
                    Game_Over = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
pygame.quit()
