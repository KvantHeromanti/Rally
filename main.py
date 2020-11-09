import pygame as pg

SIZE = WIDTH, HEIGHT = 800, 600
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
WHITE = (200, 200, 200)

pg.init()
pg.display.set_caption('Rally')
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()

'''bg_image = pg.image.load('Image/road.jpg')
bg_image_rect = bg_image.get_rect(topleft=(0, 0))
bg_image_2_rect = bg_image.get_rect(topleft=(0, -HEIGHT))'''


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


class Car(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('Image/car1.png')


all_sprite = pg.sprite.Group()
for r in range(2):
    all_sprite.add(Road(0, 0 if r == 0 else -HEIGHT))

car1 = Car()
car1_image = car1.image
car1_w, car1_h = car1.image.get_width(), car1.image.get_height()
car1.x, car1.y = (WIDTH - car1_w) // 2, (HEIGHT - car1_h) // 2

game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
    '''
    car1.y -= 1
    if car1.y < -car1_h:
        car1.y = HEIGHT

    bg_image_rect.y += 1
    if bg_image_rect.y > HEIGHT:
        bg_image_rect.y = 0
    bg_image_2_rect.y += 1
    if bg_image_2_rect.y > 0:
        bg_image_2_rect.y = -HEIGHT

    screen.fill(GREY)
    for i in range(2):
        screen.blit(bg_image, bg_image_rect if i == 0 else bg_image_2_rect)
    screen.blit(car1_image, (car1.x, car1.y))
    '''
    all_sprite.update()
    all_sprite.draw(screen)

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Rally      FPS: {int(clock.get_fps())}')

#pg.image.save(screen, 'road.jpg')
