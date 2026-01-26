from pygame import *

screen = display.set_mode((0, 0), FULLSCREEN)
info = display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

CENTER_WALLX = WIDTH // 2
CENTER_WALLY = HEIGHT // 2
display.set_caption("Pong Game")
WHITE = (255, 255, 255)
class Player(sprite.Sprite):
    def __init__(self, player_x, player_y, enemy=False):
        super().__init__()
        self.direction = None
        self.width = 10
        self.height = 100
        self.speed = 5
        self.enemy = enemy
        self.rect = Rect(player_x, player_y, self.width, self.height)
    def update(self, ball):
        if not self.enemy:
            keys = key.get_pressed()
            if keys[K_UP] or keys[K_w]: 
                self.rect.y -= 1
            if keys[K_DOWN] or keys[K_s]: 
                self.rect.y += 1 
            if self.rect.y >= 985:
                self.rect.y -= 1
            if self.rect.y < 0:
                self.rect.y = 0
        else:
            if self.rect.y < ball.rect.y:
                self.rect.y += 1
            if self.rect.y > ball.rect.y:
                self.rect.y -= 1
            if self.rect.y >= 985:
                self.rect.y -= 1
            if self.rect.y < 0:
                self.rect.y = 0 
    def draw_player(self, screen):
        draw.rect(screen, WHITE, self.rect)

class Ball(sprite.Sprite):
    def __init__(self, ball_x, ball_y):
        super().__init__()
        self.Vx = 0.5
        self.Vy = 0.5
        self.width = 30
        self.height = 30
        self.rect = Rect(ball_x, ball_y, self.width, self.height)
    def update(self):
        self.rect.x += self.Vx 
        self.rect.y += self.Vy

    def draw(self, screen):
        draw.ellipse(screen, WHITE, self.rect)

class Wall(sprite.Sprite):
    def __init__(self, wall_x, wall_y):
        super().__init__()
        self.width = 10
        self.height = 1100
        self.rect = Rect(wall_x, wall_y, self.width, self.height)
    def draw(self, screen):
        draw.rect(screen, WHITE, self.rect)

Player_paddle = Player(25, 300, False)
Enemy_paddle = Player(1900, 300, True)
Wall_middle = Wall(CENTER_WALLX, 0)
Ball_pong = Ball(CENTER_WALLX, 0)
run = True

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    Player_paddle.draw_player(screen)
    Enemy_paddle.draw_player(screen)
    Wall_middle.draw(screen)
    Ball_pong.draw(screen)

    Ball_pong.update()
    Player_paddle.update(Ball_pong)
    Enemy_paddle.update(Ball_pong)
    if sprite.collide_rect(Player_paddle, Ball_pong) or sprite.collide_rect(Enemy_paddle, Ball_pong):
        pass
    display.update()
    screen.fill((0, 0, 0))
