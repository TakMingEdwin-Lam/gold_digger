import pygame, sys
import random

# Basic setup
pygame.init()
clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Gold Digger')

# Upload images
bg_image = pygame.image.load('images/decorations/background.png').convert_alpha()
sand_image = pygame.image.load('images/decorations/sand.png').convert_alpha()
health_img = pygame.image.load('images/others/health.png').convert_alpha()
game_over_img = pygame.image.load('images/decorations/game_over.png').convert_alpha()

start_btn = pygame.image.load('images/button/start_btn.png').convert_alpha()
restart_btn = pygame.image.load('images/button/restart_btn.png').convert_alpha()
exit_btn = pygame.image.load('images/button/exit_btn.png').convert_alpha()
title_txt = pygame.image.load('images/text/title.png').convert_alpha()
game_txt = pygame.image.load('images/text/game_description.png').convert_alpha()
intro_txt = pygame.image.load('images/text/intro.png').convert_alpha()

intro_cactus = pygame.image.load('images/items/cactus.png').convert_alpha()
intro_bomb = pygame.image.load('images/items/bomb.png').convert_alpha()
stop_img = pygame.image.load('images/others/stop.png').convert_alpha()
warning_img = pygame.image.load('images/text/warning.png').convert_alpha()

game_over_txt = pygame.image.load('images/text/game_over.png').convert_alpha()
troll_txt = pygame.image.load('images/text/troll.png').convert_alpha()


# Music
bg_music = pygame.mixer.Sound('sound/The Shadows - Apache.mp3')
bg_music.play(-1)
button_sound = pygame.mixer.Sound('sound/button.mp3')
button_sound.set_volume(0.15)
hammer_sound = pygame.mixer.Sound('sound/hammer.mp3')
hammer_sound.set_volume(1.2)
money_sound = pygame.mixer.Sound('sound/money.mp3')
money_sound.set_volume(1.1)
gold_sound = pygame.mixer.Sound('sound/gold.mp3')
gold_sound.set_volume(0.8)
ouch_sound = pygame.mixer.Sound('sound/ouch.mp3')
ouch_sound.set_volume(4)
nabbit_dead = pygame.mixer.Sound('sound/nabbit_dead.wav')
nabbit_dead.set_volume(0.75)
nabbit_escape = pygame.mixer.Sound('sound/nabbit_escape.wav')
nabbit_escape.set_volume(0.75)
health_sound = pygame.mixer.Sound('sound/health.wav')
health_sound.set_volume(0.8)
bomb_sound = pygame.mixer.Sound('sound/bomb.mp3')
bomb_sound.set_volume(1.2)


class Hammer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.img = pygame.image.load('images/items/hammer.png').convert_alpha()
        self.clicked = False
        self.score = 0
        self.health = 3
        self.max_health = 5

    def draw(self):
        pos = pygame.mouse.get_pos()
        x = pos[0]
        y = pos[1]        
        self.rect = self.img.get_rect(center = (x, y))        
        screen.blit(self.img, self.rect)
        
        # Check mouseover and click condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                #hammer_sound.play()
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

    def limit(self):
        if self.health >= 5:
            self.health = 5
        if self.score <= 0:
            self.score = 0
        
    def update(self):
        self.draw()
        self.limit()
            

class Item(pygame.sprite.Sprite):
    def __init__(self, char_type, show_time):
        super().__init__()
        self.char_type = char_type
        self.img = pygame.image.load(f'images/items/{self.char_type}.png').convert_alpha()
        self.item_list = [(150, 150), (150, 300), (150, 450), (300, 150), (300, 300), (300, 450),
                           (450, 150), (450, 300), (450, 450)]
        self.rect = self.img.get_rect(center = random.choice(self.item_list))
        self.activate_effect = False
        self.show_time = show_time

    def draw(self):
        screen.blit(self.img, self.rect)

    def check_collision(self):
        if hammer.clicked and pygame.sprite.spritecollide(self, hammer_single, False):                
                self.activate_effect = True
                if self.char_type == 'money':
                    self.kill()
                    money_sound.play()
                    hammer.score += 100
                    pow_effect = SpecialEffects('images/special_effects/pow.png', self.rect.x, self.rect.y)
                    special_group.add(pow_effect)
                                       
                elif self.char_type == 'gold':
                    self.kill()
                    gold_sound.play()
                    hammer.score += 300
                    pow_alt = SpecialEffects('images/special_effects/pow_alt.png', self.rect.x, self.rect.y)
                    special_group.add(pow_alt)
                        
                elif self.char_type == 'cactus':
                    self.kill()
                    ouch_sound.play()
                    hammer.health -= 1
                    ouch = SpecialEffects('images/special_effects/ouch.png', self.rect.x, self.rect.y)
                    special_group.add(ouch)
                    
                elif self.char_type == 'nabbit':
                    self.kill()
                    nabbit_dead.play()
                    kapow = SpecialEffects('images/special_effects/kapow.png', self.rect.x, self.rect.y)
                    special_group.add(kapow)
                    
                elif self.char_type == '1-up-mushroom':
                    self.kill()
                    health_sound.play()
                    hammer.health += 1
                    health_effect = SpecialEffects('images/special_effects/1up.png', self.rect.x, self.rect.y)
                    special_group.add(health_effect)

                elif self.char_type == 'bomb':
                    self.kill()
                    bomb_sound.play()
                    hammer.health = 0
                    hammer.score = 0

    def check_disappear(self):
        self.show_time -= 1
        if self.show_time <= 0:
            self.kill()
            if self.char_type == 'nabbit':
                hammer.score -= 200
                nabbit_escape.play()
            
    def update(self):
        self.draw()
        self.check_collision()
        self.check_disappear()


class SpecialEffects(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(self.name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.disappear_countdown = 50
        
    def draw(self):
        screen.blit(self.image, self.rect)

    def check_activate(self):
        self.disappear_countdown -= 1
        if self.disappear_countdown <= 0:
            self.kill()

    def update(self):
        self.draw()
        self.check_activate()

        
class Burrows():
    def __init__(self):
        self.burrow_x = 80
        self.burrow_y = 110
        self.img = pygame.image.load('images/decorations/burrow.png').convert_alpha()
        self.rect = self.img.get_rect(center = (self.burrow_x, self.burrow_y))
        
    def draw_burrows(self):
        for j in range(3):
            for i in range(3):
                screen.blit(self.img, (self.burrow_x + 150 * i, self.burrow_y + 150 * j))

                                          
class Button():
	def __init__(self,x, y, image, scale):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.center = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action


# instances for buttons
start_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, start_btn, 0.75)
restart_button = Button(110, SCREEN_HEIGHT - 60, restart_btn, 1.5)
exit_button = Button(SCREEN_WIDTH // 2, 430, exit_btn, 0.7)
game_start_button = Button(500, 550, start_btn, 0.6)

# create sprite groups
hammer_single = pygame.sprite.GroupSingle()
item_group = pygame.sprite.Group()
special_group = pygame.sprite.Group()

# Draw text
font = pygame.font.Font('font/joystix.ttf', 30)
score_font = pygame.font.Font('font/joystix.ttf', 60)
def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))
    
# Instances for sprites
hammer = Hammer()
burrow = Burrows()

hammer_single.add(hammer)

# Time for items/ objects to spawn
level_1 = pygame.USEREVENT + 1
pygame.time.set_timer(level_1, 1400)

level_2 = pygame.USEREVENT + 2
pygame.time.set_timer(level_2, 1050)

level_3 = pygame.USEREVENT + 3
pygame.time.set_timer(level_3, 800)

level_4 = pygame.USEREVENT + 4
pygame.time.set_timer(level_4, 700)

level_5 = pygame.USEREVENT + 5
pygame.time.set_timer(level_5, 600)

# Timer for countdown
countdown = 91
last_count = pygame.time.get_ticks()

# Main Game Loop
run = True

# Game state
game_start = False
instruction = False
game_over = False

while run:            
    # Opening screen
    if not game_start:
        screen.blit(bg_image, (0, 0))        
        if not instruction:
            screen.blit(title_txt, (15, 30))
            screen.blit(game_txt, (-5, 150))
            if start_button.draw(screen):
                instruction = True
                button_sound.play()                
            if exit_button.draw(screen):
                pygame.quit()
                sys.exit()
        else:
            screen.blit(intro_txt, (10, 10))
            screen.blit(intro_cactus, (40, 470))
            screen.blit(intro_bomb, (250, 470))
            screen.blit(stop_img, (20, 480))
            screen.blit(stop_img, (230, 470))
            screen.blit(warning_img, (125, 470))
            # Show background and instruction
            if game_start_button.draw(screen):
                game_start = True
                instruction = False
                button_sound.play()
            
    # Main Game    
    else:
        if not game_over:
            #Hide the mouse cursor
            pygame.mouse.set_visible(0)
            screen.blit(sand_image, (0, 0))
            draw_text('Time:' + str(countdown), font, (36, 36, 36), 10, 10)
            draw_text('Money:' + str(hammer.score), font, (36, 36, 36), 325, 10)
            draw_text('Health:', font, (36, 36, 36), 10, 50)

            for i in range(hammer.health):
                screen.blit(health_img, (180 + (i * 40), 50))
            
            # Player death
            for hammer in hammer_single:
                if hammer.health <= 0:
                    hammer.health = 0
                    hammer.score = 0
                    game_over = True
                    
            # update sprites                    
            burrow.draw_burrows()
            special_group.update()
            item_group.update()    
            hammer_single.update()
            
            # Timer
            if countdown > 0:
                count_timer = pygame.time.get_ticks()
                if count_timer - last_count >= 1000: # 1 second
                    countdown -= 1
                    last_count = count_timer                   
            else:
                game_over = True

            # Level types; increased difficulty when time proceeds                
            for event in pygame.event.get():
                if event.type == level_1:
                    if countdown > 75:
                        item = Item('money', 70)
                        item_group.add(item)
                    elif 60 < countdown < 75:
                        item = Item(random.choice(['money', 'money', 'money', 'gold']), 65)
                        item_group.add(item)                        
                    else:
                        event.type == level_2
                if event.type == level_2:
                    if 45 < countdown < 60:
                        item = Item(random.choice(['money', 'money', 'gold', 'cactus', 'cactus']), 58)
                        item_group.add(item)
                    else:
                        event.type == level_3
                if event.type == level_3:
                    if 30 < countdown < 45:
                        item = Item(random.choice(['gold', 'cactus', 'cactus', 'money', 'money',
                                                   'cactus', '1-up-mushroom']), 48)
                        item_group.add(item)
                    else:
                        event.type == level_4
                if event.type == level_4:
                    if 15 < countdown < 30:
                        item = Item(random.choice(['gold', 'cactus', 'money', 'money', 'cactus', 'nabbit',
                                                           'nabbit', '1-up-mushroom']), 38)
                        item_group.add(item)
                    else:
                        event.type == level_5
                if event.type == level_5:
                    if 0 < countdown < 15:
                        item = Item(random.choice(['gold', 'money', 'money', 'money', 'cactus',
                                                           'nabbit', 'cactus', 'bomb', 'bomb']), 30)
                        item_group.add(item)
                        
                # Exit Screen                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()            
        else:
            # Game over screen transition
            screen.blit(game_over_img, (0, 0))
            screen.blit(game_over_txt, (15, 30))
            screen.blit(troll_txt, (15, 250))
            draw_text('Money:' + str(hammer.score), score_font, (36, 36, 36), 20, SCREEN_HEIGHT // 2 + 120)
            pygame.mouse.set_visible(255)
            # restart screen
            if restart_button.draw(screen):
                special_group.empty()
                item_group.empty()    
                countdown = 91
                game_start = False
                game_over = False
                hammer.score = 0
                hammer.health = 3
                button_sound.play()
                
    for event in pygame.event.get():    
        # Exit Screen                
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.flip()
    clock.tick(FPS)                
        
pygame.quit()
