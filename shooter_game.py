import pygame as pg
from random import randint, choice

pg.font.init()
pg.mixer.init()

WIDTH = 800
HEIGHT = 640

points = 0
fud = 300

window = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

class ImageSprite(pg.sprite.Sprite):
    def __init__(self, filename, size, position, speed):
        super().__init__()
        self.image = pg.image.load(filename)
        self.image = pg.transform.scale(self.image, size)
        self.rect = pg.Rect(position, size)
        self.speed = pg.Vector2(speed)
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        
class Player(ImageSprite):
    def __init__(self, filename, size, position, speed):
        super().__init__(filename, size, position, speed)
        self.initial_position = position
    def update(self):
        global fud
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.rect.x -= self.speed.x
            fud = 300
        if keys[pg.K_d]:
            self.rect.x += self.speed.x
            fud = 300
        if keys[pg.K_RIGHT]:
            self.rect.x += self.speed.x
            fud = 300
        if keys[pg.K_LEFT]:
            self.rect.x -= self.speed.x
            fud = 300
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    def reset(self):
        self.rect.topleft = self.initial_position
    def shoot(self):
        b = Bullet('li.png', (30,30), self.rect.midtop, (0,-15))
        bullets.add(b)
    def shoot2(self):
        cooldown = 2 * 60
        b2 = Bullet('li.png', (30,30), self.rect.midtop, (0,-15))
        bullets.add

class Enemy(ImageSprite):
    def update(self):
        if self.rect.top > HEIGHT:
            random_position = (randint(0,WIDTH-self.rect.width), -self.rect.height)
            self.rect.topleft = random_position
        self.rect.topleft += self.speed

class Enemy2(ImageSprite):
    def update(self):
        if self.rect.top > HEIGHT:
            random_position = (randint(0,WIDTH-self.rect.width), -self.rect.height)
            self.rect.topleft = random_position
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.speed.x*= -1
        self.rect.topleft += self.speed
        
class Enemy3(ImageSprite):
    def update(self):
        self.rect.topleft += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
        

class Bullet(ImageSprite):
    def update(self):
        if self.rect.bottom < 0:
            self.kill()
        self.rect.topleft += self.speed

class TextSprite(pg.sprite.Sprite):
    def __init__(self, text, font_size, position, color, bg_color = None):
        super().__init__()
        self.font = pg.font.Font(None, font_size)
        self.position = position
        self.color = color
        self.bg_color = bg_color
        self.update_text(text)    
    def update_text(self, new_text):
        self.image = self.font.render(new_text, True, self.color, self.bg_color)
    def draw(self, surface):
        surface.blit(self.image, self.position)

die = TextSprite(text='NICE TRY!', font_size=100, position=(WIDTH/3.2, HEIGHT/2.3), color='white')
m2 = TextSprite(text='Press M to go back to the menu', font_size=60, position = (WIDTH/6.8, 450), color='white')
retry = TextSprite(text='Press ENTER/RETURN to retry', font_size=70, position=(WIDTH/13, 500), color='White')

points_counter = TextSprite(text='Points: '+str(points), font_size=30, position = (WIDTH-150,HEIGHT-600), color='white')

bg = ImageSprite(filename='aosd.jpeg',size=(WIDTH,HEIGHT),position=(0,0),speed=(0,0))
p = Player(filename='as.png',size=(50,50),position=(WIDTH/2,560),speed=(5,0))
kill_sound = pg.mixer.Sound('rumble.flac')
shoot1_sound = pg.mixer.Sound('laser1.wav')
shoot2_sound = pg.mixer.Sound('laser3.wav')
shoot3_sound = pg.mixer.Sound('laser4.wav')
shoot4_sound = pg.mixer.Sound('laser5.wav')
shoot5_sound = pg.mixer.Sound('laser11.wav')
shooting_sounds = [shoot1_sound, shoot2_sound, shoot3_sound, shoot4_sound, shoot5_sound]

state='menu'
intro = TextSprite(text='Buggy Intruder', font_size=100, position=(WIDTH/6.3, 100), color='Aquamarine')
rule = TextSprite(text='Press R for rules & controls', font_size=60, position=(WIDTH/6.7, 200), color='Aquamarine')
r1 = TextSprite(text='Rules', font_size=100, position=(WIDTH/2.5, 100), color='Aquamarine')
r2 = TextSprite(text='One life, one type of bullet and buncha enemies!', font_size=40, position=(WIDTH/10, 200), color='Aquamarine')
c1 = TextSprite(text='D/-> to go right', font_size=40, position=(WIDTH/2.5, 300), color='Aquamarine')
c2 = TextSprite(text='A/<- to go left', font_size=40, position=(WIDTH/2.5, 400), color='Aquamarine')
c3 = TextSprite(text='Space/K to shoot', font_size=40, position=(WIDTH/2.5, 500), color='Aquamarine')
m1 = TextSprite(text='Press M to go back to the menu', font_size=60, position = (WIDTH/6.8, 550), color='Aquamarine')
begin = TextSprite(text='Press ENTER/RETURN to start', font_size=70, position=(WIDTH/13, 300), color='Aquamarine')


bullets = pg.sprite.Group()
enemies = pg.sprite.Group()
unkillable_enemies = pg.sprite.Group()

def create_enemy():
    random_speed = (0,randint(1,7))
    e = Enemy('pa2.png', (50,50), (0,0), random_speed)
    random_position = (randint(0,WIDTH-e.rect.width), -e.rect.height)
    e.rect.topleft = random_position
    enemies.add(e)

def create_diagonal_enemy():
    random_speed = (randint(1,7),randint(1,7))
    e2 = Enemy2('pa2.png', (50,50), (0,0), random_speed)
    random_position = (randint(0,WIDTH-e2.rect.width), -e2.rect.height)
    e2.rect.topleft = random_position
    enemies.add(e2)

def create_unkillable_enemy():
    e3 = Enemy3('G.O.D.png',(125,125), (0, 0), (0,10))
    e3.rect.centerx = p.rect.centerx
    unkillable_enemies.add(e3)

def spawn_enemies(how_many):
    enemies.empty()
    for i in range(how_many):
        create_enemy()

create_enemy()
while True:
    if pg.event.peek(pg.QUIT):
        break
    for e in pg.event.get():
        if e.type == pg.KEYDOWN and (e.key == pg.K_SPACE or e.key == pg.K_k) and state == 'start':
            p.shoot()
            choice(shooting_sounds).play()
        if e.type == pg.KEYDOWN and e.key == pg.K_RETURN and (state == 'menu' or state == 'gg'):
            state = 'start'
            points = 0
        if e.type == pg.KEYDOWN and e.key == pg.K_r and state == 'menu':
            state = 'rule'
        if e.type == pg.KEYDOWN and e.key == pg.K_m and (state == 'rule' or state == 'gg'):
            state = 'menu'
            points = 0
            enemies.empty()
            create_enemy()
            points_counter.update_text('Points: '+str(points))
            
    if state == 'menu':
        window.fill((51, 66, 255))
        intro.draw(window)
        rule.draw(window)
        begin.draw(window) 

    elif state == 'rule':
        window.fill((51, 66, 255))
        r1.draw(window)
        r2.draw(window)
        c1.draw(window)
        c2.draw(window)
        c3.draw(window)
        m1.draw(window)

    elif state == 'start':
        fud -= 1
        bg.draw(window)
        p.draw(window)
        enemies.draw(window)
        bullets.draw(window)
        points_counter.draw(window)
        unkillable_enemies.draw(window)
        enemy_hits = pg.sprite.groupcollide(bullets, enemies, True, True)
        for hit in enemy_hits:
            points = points + 1
            points_counter.update_text('Points: '+str(points))
            create_enemy()
            kill_sound.play()
            if points <= 25:
                if points % 5 == 0:
                    create_enemy()
            elif points <= 40 and points >= 25:
                if points % 10 == 0:
                    create_diagonal_enemy()
                    create_diagonal_enemy()
            elif points <= 50 and points >= 40:
                    create_enemy()
                    create_enemy()
                    
        points_counter = TextSprite(text='Points: '+str(points), font_size=30, position = (WIDTH-150,HEIGHT-600), color='white')

        player_hits = pg.sprite.spritecollide(p, enemies, True)
        for hit in player_hits:
            state = 'gg'

        unkillable_enemies_hits = pg.sprite.spritecollide(p, unkillable_enemies, True)
        for hit in unkillable_enemies_hits:
            state = 'gg'

        if fud <= 0:
            create_unkillable_enemy()
            fud = 300

        p.update()
        enemies.update()
        unkillable_enemies.update()
        bullets.update()

    elif state == 'gg':
        window.fill('red')
        die.draw(window)
        m2.draw(window)
        retry.draw(window)
        points_counter = TextSprite(text='Points: '+str(points), font_size=70, position = (WIDTH/2.5,HEIGHT/4), color='white')
        points_counter.draw(window)
    pg.display.update()
    clock.tick(60)