#Создай собственный Шутер!

from pygame import *
from random import randint

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_widht - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

score = 0
lost = 0
max_lost = 3
goal = 10

win_widht = 700
win_height = 500
window = display.set_mode((win_widht, win_height))
display.set_caption('pygame window')
background = transform.scale(image.load('galaxy.jpg'), (win_widht, win_height))
screen = display.set_mode((0,0), FULLSCREEN)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_height - 80)
            self.rect.y = 0
            lost = lost + 1

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(80, win_widht - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

font.init()
font2 = font.Font(None,36)

ship = Player('rocket.png', 5, win_height - 100, 80, 100, 10)

game = True
clock = time.Clock()
FPS = 60

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN', True, (255, 255, 255))
lose = font1.render('YOU LOSE', True, (180, 0, 0))
font2 = font.Font(None, 36)



finish = False   
run = True 

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                ship.fire()
                fire_sound.play()
    if not finish:
        window.blit(background,(0,0))
        text = font2.render('Счет:'+ str(score), 1, (255, 255, 255))
        window.blit(text,(10,20))

        text_lose = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose,(10,50))
        
        ship.update()
        ship.reset()
        clock.tick(FPS)
        bullets.update()
        bullets.draw(window)
        monsters.update()
        monsters.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy('ufo.png', randint(80, win_widht - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win,(200,200))   
        display.update()
        time.delay(40)



