from pygame import *

font.init()
font = font.Font(None, 50)

win_font = font.render("You win", True, (255, 255, 255))
lose_font = font.render("You lose", True, (255, 255, 255))
q_to_quit = font.render("q to quit", True, (255, 255, 255))


screen = display.set_mode((0, 0), FULLSCREEN)
info = display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

CENTER_WALLX = WIDTH // 2
CENTER_WALLY = HEIGHT // 2
display.set_caption("Pong Game")
WHITE = (255, 255, 255)

class Button(sprite.Sprite):
    def __init__(self, color, x, y, width, height, text, text_color=(255, 255, 255)):
        super().__init__()
        self.color = color
        self.rect = Rect(x, y, width, height)
        self.text_surf = font.render(text, True, text_color)
        self.text_rect = self.text_surf.get_rect()
        self.text_rect.center = self.rect.center
    def draw(self, screen):
        draw.rect(screen, self.color, self.rect)

        screen.blit(self.text_surf, self.text_rect)
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Player(sprite.Sprite):
    def __init__(self, player_x, player_y, enemy=False):
        super().__init__()
        self.direction = None
        self.width = 10
        self.height = 100
        self.speed = 7
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
        self.player_score = 0
        self.enemy_score = 0
        self.Vx = 0.6
        self.radius = 10
        self.Vy = 0.6
        self.width = 30
        self.height = 30
        self.rect = Rect(ball_x, ball_y, self.width, self.height)
    def update(self):
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.Vy *= -1
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
Ball_pong = Ball(CENTER_WALLX, 20)

run = True
finish = False
game_state = 'menu'

def reset_game():
    global player_score, enemy_score, game_state
    player_score = 0
    enemy_score = 0
    game_state = 'playing'
    Ball_pong.rect.center = (CENTER_WALLX, CENTER_WALLY)
    Ball_pong.Vx = 0.6
    Ball_pong.Vy = 0.6
    Player_paddle.rect.y = 300
    Enemy_paddle.rect.y = 300
clock = time.Clock()
player_score = 0
enemy_score = 0


btn_restart = Button((0, 0, 0), 250, 300, 200, 80, "RESTART") 
btn_play = Button((0, 0, 0), 250, 300, 200, 80, "Play") 
btn_PlayerVsBot = Button((0, 0, 0), 250, 300, 200, 80, "Player vs robot") 
btn_PlayerVsPlayer = Button((0, 0, 0), 250, 300, 200, 80, "Player Vs Player") 


while run:
    screen.fill((0, 0, 0))
    for e in event.get():
        keys = key.get_pressed()
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            if game_state == 'game_over' and btn_restart.is_clicked(e.pos):
                reset_game()
            if game_state == 'menu' and btn_play.is_clicked(e.pos):
                reset_game()
        if keys[K_q]:
            run = False
        if keys[K_ESCAPE]:
            run = False
    if game_state == 'menu':
        btn_play.draw(screen)
        
    elif game_state == 'playing':
        Player_paddle.draw_player(screen)
        Enemy_paddle.draw_player(screen)
        Wall_middle.draw(screen)
        Ball_pong.draw(screen)

        Ball_pong.update()
        Player_paddle.update(Ball_pong)
        Enemy_paddle.update(Ball_pong)

        if sprite.collide_rect(Player_paddle, Ball_pong):
            Ball_pong.Vx = abs(Ball_pong.Vx)
            Ball_pong.rect.left = Player_paddle.rect.right
            Ball_pong.Vx *= 1.1
            Ball_pong.Vy *= 1.1
        if sprite.collide_rect(Enemy_paddle, Ball_pong):
            Ball_pong.Vx = -abs(Ball_pong.Vx)
            Ball_pong.rect.right = Enemy_paddle.rect.left
            Ball_pong.Vx *= 1.1
            Ball_pong.Vy *= 1.1   

        if Ball_pong.rect.right >= WIDTH:
            player_score += 1
            Ball_pong.rect.center = (CENTER_WALLX, CENTER_WALLY) 
            Ball_pong.Vx *= -1
        if Ball_pong.rect.left <= 0:
            enemy_score += 1
            Ball_pong.rect.center = (CENTER_WALLX, CENTER_WALLY) 
            Ball_pong.Vx *= -1

        if player_score == 3 or enemy_score == 3:
            game_state = 'game_over'

        player_score_font = font.render(f"{player_score}", True, (255, 255, 255))
        enemy_score_font = font.render(f"{enemy_score}", True, (255, 255, 255))
        screen.blit(player_score_font, (910, 20))
        screen.blit(enemy_score_font, (1000, 20))
        screen.blit(q_to_quit, (300, 20))
    elif game_state == 'game_over':
        if player_score == 3:
            screen.blit(win_font, (WIDTH // 2 - 100, HEIGHT // 3))
        else:
            screen.blit(lose_font, (WIDTH // 2 - 100, HEIGHT // 3))

        btn_restart.draw(screen)
    display.update()
    clock.tick()
