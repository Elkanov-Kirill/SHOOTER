from pygame import *
from random import randint
window = display.set_mode((700, 500))
background = transform.scale(image.load("galaxy.jpg"), (700, 500))


class GameSprite(sprite.Sprite):
    def __init__(self, img , x, y, speed, w, h):
        super().__init__() #активирую супер класс
        self.image = transform.scale(image.load(img), (w ,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

bullets = sprite.Group()
patrons = 7
class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= 600:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.x + 42, self.rect.y, 3, 15, 30)
        bullets.add(bullet) 
        global patrons
        patrons -= 1
        if patrons <= -1:
            patrons = 0 


        

lost = 0 #количество пропущенных пришельцов

class NLO(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost    
        if self.rect.y >= 400:
            x = randint(0, 600)
            self.rect.x = x
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()



aliens = sprite.Group()

font.init()
font_1 = font.SysFont('Arial', 16)
font_2 = font.SysFont('Arial', 60)



for i in range(6):
    x = randint(0, 600)
    nlo = NLO("ufo.png" , x, 0, 2, 80, 60)
    aliens.add(nlo)


clock = time.Clock()
FPS = 60

player = Player("rocket.png", 200, 400 , 5, 100, 100)               

#музыка
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play() 
fire = mixer.Sound("fire.ogg")



run = True
score = 0
finish = False
while run:
    clock.tick(FPS)
    for e in event.get():
        
        if e.type == QUIT:
            run = False
            finish = True

        if e.type == KEYDOWN:                                      
            if e.key == K_SPACE and patrons != 0:
                fire.play()
                player.fire()
            
            elif e.key == K_f:
                patrons = 7
    sprite_list = sprite.groupcollide(bullets, aliens, True, True)

    

        
        


    

    for i in sprite_list:
        score += 1
        x = randint(0, 600)
        nlo = NLO("ufo.png" , x, 0, 2, 80, 60)
        aliens.add(nlo)
    if finish != True:
        window.blit(background,(0, 0))
        bullets.draw(window)
        bullets.update()
        player.reset()
        player.move()
        aliens.draw(window)
        aliens.update()
        kills = font_1.render("Убито:" + str(score), True, (255, 255, 255))
        window.blit(kills, (4, 10))
        losts = font_1.render("Пропущенно:" + str(lost), True, (255, 255, 255))
        window.blit(losts, (4, 30))
        patron = font_1.render("Пуль:" + str(patrons) +"/7", True, (255, 255, 255))
        window.blit(patron, (620, 480))
        if score >= 10:
                win = font_2.render("YOU WIN!", True, (255, 215, 0))
                window.blit(win, (200, 200))
                finish = True
        if lost >= 5:
                losee = font_2.render("YOU LOSE!", True, (92, 0, 0))
                window.blit(losee, (200, 200))
                finish = True
            
    
    display.update()
