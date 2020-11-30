import pygame as pg
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
try:
    with open('record.txt', 'x') as f:
        f.write(str(0))
except BaseException:
    pass

SIZE = WIDTH, HEIGHT = 800, 600
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
RED = (128, 0, 0)
BLUE = (0, 0, 128)
WHITE = (200, 200, 200)
COLOR = (255, 125, 0)
COLOUR = (255, 20, 147)
COLORER = (0, 250, 154)
life = 3
time = 0

pg.init()
pg.display.set_caption('Rally')
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()
car_accident = 0
block = False
block2 = False
game_starting = 0
level = 40
rgb = [0, 128, 0]
list_x = []

'''image place'''

canister_image = pg.image.load('Image/canister.png')
fuel_image = pg.image.load('Image/fuel.png')
pound_image = pg.image.load('Image/water.png')
st_button = pg.image.load('Image/start_button.png')
st_button_rect = st_button.get_rect(topleft=(240, 150))
stp_button = pg.image.load('Image/stop_button.png')
stp_button_rect = stp_button.get_rect(topleft=(240, 320))

main_bg = pg.image.load('Image2/Patrick.png')
main_bg_rect = main_bg.get_rect(topleft=(0, 0))

cars = [pg.image.load('Image/car1.png'), pg.image.load('Image/car2.png'), pg.image.load('Image/car3.png')]
sound_car_accident = pg.mixer.Sound('Sound/udar.wav')
canister_sound = pg.mixer.Sound('Sound/canister.wav')
font = pg.font.Font(None, 32)

u1_event = pg.USEREVENT + 1
pg.time.set_timer(u1_event, random.randrange(6000, 26001, 4000))

u2_event = pg.USEREVENT + 2
pg.time.set_timer(u2_event, random.randrange(4000, 18001, 3000))


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('Image/car4.png')
        self.orig_image = self.image
        self.angle = 0
        self.speed = 2
        self.acceleration = 0.02
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.rect = self.image.get_rect()
        self.position = pg.math.Vector2(self.x, self.y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.velocity
        self.rect.center = self.position

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
            self.angle -= 1
            if self.angle < -25:
                self.angle = -25
        elif keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
            self.angle += 1
            if self.angle > 25:
                self.angle = 25
        else:
            self.velocity.x = 0
            if self.angle < 0:
                self.angle += 1
            elif self.angle > 0:
                self.angle -= 1
        if keys[pg.K_UP]:
            self.velocity.y -= self.acceleration
            if self.velocity.y < -self.speed:
                self.velocity.y = -self.speed
        elif keys[pg.K_DOWN]:
            self.velocity.y += self.acceleration
            if self.velocity.y > self.speed:
                self.velocity.y = self.speed
        else:
            if self.velocity.y < 0:
                self.velocity.y += self.acceleration
                if self.velocity.y > 0:
                    self.velocity.y = 0
            elif self.velocity.y < 0:
                self.velocity.y -= self.acceleration
                if self.velocity.y < 0:
                    self.velocity.y = 0
        if self.rect.left < 38:
            self.rect.left = 40
            self.angle -= .1
            if self.angle >= 0:
                self.angle = 0


class Road(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(screen.get_size())
        self.image.fill(GREY)
        pg.draw.line(self.image, GREEN, (20, 0), (20, 600), 40)
        pg.draw.line(self.image, GREEN, (780, 0), (780, 600), 40)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(
                    self.image, WHITE,
                    (40 + xx * 80, 0 if xx == 0 or xx == 9 else 10 + yy * 60),
                    (40 + xx * 80, 600 if xx == 0 or xx == 9 else 50 + yy * 60), 5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, img):
        pg.sprite.Sprite.__init__(self)

        if img == fuel_image:
            self.image = img
            self.speed = 0
        elif img == canister_image or img == pound_image:
            self.image = img
            self.speed = 1
        else:
            self.image = pg.transform.flip(img, False, True)
            self.speed = random.randint(2, 3)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            if self == canister or self == pound:
                self.kill()
            else:
                list_x.remove(self.rect.centerx)
                while True:
                    self.rect.centerx = random.randrange(80, WIDTH, 80)
                    if self.rect.centerx in list_x:
                        continue
                    else:
                        list_x.append(self.rect.centerx)
                        self.speed = random.randint(2, 3)
                        self.rect.bottom = 0
                        break


all_sprite = pg.sprite.Group()
cars_group = pg.sprite.Group()
canister_group = pg.sprite.Group()
pound_group = pg.sprite.Group()
for r in range(2):
    all_sprite.add(Road(0, 0 if r == 0 else -HEIGHT))

fuel = Car(720, 45, fuel_image)
canister = Car(0, 0, canister_image)
pound = Car(0, 0, pound_image)

player = Player()
all_sprite.add(player, fuel)


def screen1():
    sc = pg.Surface(screen.get_size())
    sc.fill(pg.Color('navy'))
    sc.blit(main_bg, main_bg_rect)
    sc.blit(st_button, (st_button_rect))
    sc.blit(stp_button, (stp_button_rect))
    screen.blit(sc, (0, 0))


def my_record():
    with open('record.txt', 'r+') as d:
        record = d.read()
        if time < int(record):
            record = str(time)
        d.seek(0)
        d.truncate()
        d.write(record)
    return


game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game_starting = 0
            for s in cars_group:
                s.kill()
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if st_button_rect.collidepoint(e.pos):
                    game_starting = 1
                    list_x.clear()
                    n = 0
                    while n < 6:
                        x = random.randrange(80, WIDTH, 80)
                        if x in list_x:
                            continue
                        else:
                            list_x.append(x)
                            cars_group.add(Car(x, -cars[0].get_height(), cars[n] if n < len(cars) else random.choice(cars)))
                            n += 1
                    all_sprite.add(cars_group)
                elif stp_button_rect.collidepoint(e.pos):
                    game = False
        elif e.type == u1_event:
            pound_group.add(pound)
            all_sprite.add(pound)
            pound.rect.center = \
                random.randrange(80, WIDTH, 80), - pound.rect.h
            pg.time.set_timer(u1_event, random.randrange(6000, 26001, 4000))
        elif e.type == u2_event:
            canister_group.add(canister)
            all_sprite.add(canister)
            canister.rect.center = \
                random.randrange(80, WIDTH, 80), - canister.rect.h
            pg.time.set_timer(u2_event, random.randrange(4000, 18001, 3000))

    if pg.sprite.spritecollideany(player, cars_group):
        if block is False:
            car_accident += 1
            player.position[0] += 50 * random.randrange(-1, 2, 2)
            player.angle = 50 * random.randrange(-1, 2, 2)
            sound_car_accident.play()
            life -= 1
            block = True
            if life <= 0:
                game_starting = 0
                life = 3
                for s in cars_group:
                    s.kill()
    else:
        block = False

    if pg.sprite.spritecollide(player, canister_group, True):
        level += 15
        canister_sound.play()

    if pg.sprite.spritecollideany(player, pound_group):
        if not block2:
            player.angle = random.randint(60, 90) * random.randrange(-1, 2, 2)
            block = True
    else:
        block2 = False

    time += 0.01

    if game_starting == 0:
        level = 40
        screen1()
        time = 0
        screen.blit(font.render(f'Управление стрелками!', True, COLOR), (45, 10))
    else:
        level -= 0.01
        if level <= 0:
            game_starting = 0
            for s in cars_group:
                s.kill
        elif level <= 10:
            rgb[:2] = 250, 0
        elif level <= 20:
            rgb[0] = 250
        else:
            rgb[:2] = 0, 250

        all_sprite.update()
        all_sprite.draw(screen)
        pg.draw.rect(
            screen, rgb,
            (fuel.rect.left + 10, fuel.rect.bottom - level - 8, 21, level))
        screen.blit(font.render(f'твой рекорд', True, COLORER), (45, 11))
        screen.blit(font.render(f'Количество жизней = {life}', True, COLOUR), (50, 550))
        screen.blit(font.render(str(int(time)), True, COLORER), (200, 9))

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Rally      FPS: {int(clock.get_fps())}')
