from pygame import *

screen = display.set_mode((0, 0), FULLSCREEN)
display.set_caption("Pong Game")
WHITE = (255, 255, 255)
class Player(sprite.Sprite):
    def __init__(self, player_x, player_y, enemy=False):
        self.width = 10
        self.height = 100
        self.speed = 5
        self.enemy = enemy
        self.rect = Rect(player_x, player_y, self.width, self.height)
    def update(self):
        if not self.enemy:
            keys = key.get_pressed()
            if keys[K_UP] or keys[K_w]: self.rect.y -= 5
            if keys[K_DOWN] or keys[K_s]: self.rect.y += 5
    def draw_player(self, screen):
        draw.rect(screen, WHITE, self.rect)

Player_paddle = Player(25, 300, False)
Enemy_paddle = Player(1900, 300, True)
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    Player_paddle.draw_player(screen)
    Enemy_paddle.draw_player(screen)
    Player_paddle.update()
    Enemy_paddle.update()

    display.update()
    screen.fill((0, 0, 0))