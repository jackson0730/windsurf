import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 100, 100)  # 柔和的红色
GREEN = (100, 180, 100)  # 柔和的绿色
GRAY = (150, 150, 150)  # 用于显示速度的灰色

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
MIN_SPEED = 5
MAX_SPEED = 25
GAME_SPEED = 15  # 默认速度

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

# 设置字体
try:
    # 尝试使用系统默认中文字体
    font = pygame.font.SysFont(None, 36)  # 先创建一个默认字体
    available_fonts = pygame.font.get_fonts()  # 获取所有可用字体
    chinese_fonts = [f for f in available_fonts if any(name in f.lower() for name in ['heiti', 'hei', 'songti', 'song', 'arial unicode ms', 'microsoft yahei'])]
    
    if chinese_fonts:
        font = pygame.font.SysFont(chinese_fonts[0], 30)
    else:
        print("未找到中文字体，使用默认字体")
except Exception as e:
    print(f"字体加载错误: {e}")
    font = pygame.font.Font(None, 36)

# 创建简单的英文显示文本
SCORE_TEXT = "Score: "
SPEED_TEXT = "Speed: "

class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN
        self.score = 0
        self.speed = GAME_SPEED  # 添加速度属性

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = self.direction
        new = ((cur[0] + (x*BLOCK_SIZE)) % WINDOW_WIDTH, (cur[1] + (y*BLOCK_SIZE)) % WINDOW_HEIGHT)
        if new in self.positions[3:]:
            return False
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return True

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0
        # 保持当前速度不变

    def render(self):
        for p in self.positions:
            pygame.draw.rect(screen, self.color, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
                        random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE)

    def render(self):
        pygame.draw.rect(screen, self.color, (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))

# 定义方向
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                                 pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]:
                    speed_level = int(event.unicode)
                    snake.speed = MIN_SPEED + ((MAX_SPEED - MIN_SPEED) * (speed_level - 1) // 8)

        if not snake.update():
            snake.reset()
            food.randomize_position()

        if snake.get_head_position() == food.position:
            snake.length += 1
            snake.score += 1
            food.randomize_position()

        # 绘制游戏界面
        screen.fill(BLACK)
        snake.render()
        food.render()
        
        # 使用英文显示分数和速度
        score_text = font.render(f'{SCORE_TEXT}{snake.score}', True, WHITE)
        speed_text = font.render(f'{SPEED_TEXT}{snake.speed}', True, GRAY)
        
        # 调整文本位置
        screen.blit(score_text, (20, 20))
        screen.blit(speed_text, (20, 60))

        pygame.display.update()
        clock.tick(snake.speed)

if __name__ == '__main__':
    main()
