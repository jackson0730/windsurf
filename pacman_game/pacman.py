import pygame
import random
import sys
import math

# 初始化Pygame
pygame.init()

# 颜色定义
BLACK = (0, 0, 0)
BLUE = (65, 105, 225)  # 更柔和的蓝色
WHITE = (240, 240, 240)  # 稍微柔和的白色
YELLOW = (255, 223, 0)  # 柔和的黄色
RED = (220, 80, 80)  # 柔和的红色
PINK = (255, 182, 193)  # 柔和的粉色
ORANGE = (255, 160, 122)  # 柔和的橙色
CYAN = (100, 220, 220)  # 柔和的青色
SCARED_GHOST = (140, 140, 220)  # 柔和的蓝紫色（幽灵被惊吓时的颜色）
GREEN = (100, 200, 100)  # 柔和的绿色用于提示信息
PURPLE = (147, 112, 219)  # 添加浅紫色用于墙的边框

# 游戏设置
CELL_SIZE = 30
COLS = 19
ROWS = 21
WINDOW_WIDTH = CELL_SIZE * COLS
WINDOW_HEIGHT = CELL_SIZE * ROWS
GAME_SPEED = 10  # 降低游戏速度（原为15）

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Pacman Game')
clock = pygame.time.Clock()

# 设置字体
font = pygame.font.Font(None, 36)

# 迷宫地图 (0:路径, 1:墙, 2:豆子, 3:能量豆)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,3,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,3,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,2,1,1,1,1,1,2,1,2,1,1,2,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,1,1,1,2,1,1,1,0,1,0,1,1,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,0,1,1,0,1,2,1,1,1,1],
    [0,0,0,0,2,0,0,1,0,0,0,1,0,0,2,0,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [0,0,0,1,2,1,0,0,0,0,0,0,0,1,2,1,0,0,0],
    [1,1,1,1,2,1,0,1,1,1,1,1,0,1,2,1,1,1,1],
    [1,2,2,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,1],
    [1,2,1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,2,1],
    [1,3,2,1,2,2,2,2,2,2,2,2,2,2,2,1,2,3,1],
    [1,1,2,1,2,1,2,1,1,1,1,1,2,1,2,1,2,1,1],
    [1,2,2,2,2,1,2,2,2,1,2,2,2,1,2,2,2,2,1],
    [1,2,1,1,1,1,1,1,2,1,2,1,1,1,1,1,1,2,1],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# 创建原始迷宫的副本
ORIGINAL_MAZE = [row[:] for row in MAZE]

class Pacman:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.row = 15
        self.col = 9
        self.direction = [0, 0]  # [dx, dy]
        self.next_direction = [0, 0]
        self.score = 0
        self.power_up = False
        self.power_timer = 0
        self.mouth_angle = 45  # 初始张嘴角度
        self.mouth_opening = True  # 控制嘴巴开合方向
        
    def update(self):
        self.move()
        if self.power_up:
            self.power_timer -= 1
            if self.power_timer <= 0:
                self.power_up = False
        
        # 更新嘴巴动画
        if self.mouth_opening:
            self.mouth_angle += 3
            if self.mouth_angle >= 45:
                self.mouth_opening = False
        else:
            self.mouth_angle -= 3
            if self.mouth_angle <= 5:
                self.mouth_opening = True
    
    def render(self):
        x = self.col * CELL_SIZE + CELL_SIZE // 2
        y = self.row * CELL_SIZE + CELL_SIZE // 2
        
        # 确定吃豆人的朝向角度
        start_angle = 0
        if self.direction[0] == 1:  # 向右
            start_angle = 0
        elif self.direction[0] == -1:  # 向左
            start_angle = 180
        elif self.direction[1] == -1:  # 向上
            start_angle = 90
        elif self.direction[1] == 1:  # 向下
            start_angle = 270
        
        # 绘制吃豆人
        pygame.draw.circle(screen, YELLOW, (x, y), CELL_SIZE // 2 - 2)
        
        # 只有在移动时才显示嘴巴
        if self.direction != [0, 0]:
            # 绘制嘴巴（用黑色三角形遮盖部分圆形）
            mouth_points = [
                (x, y),
                (x + (CELL_SIZE // 2) * math.cos(math.radians(start_angle - self.mouth_angle)),
                 y - (CELL_SIZE // 2) * math.sin(math.radians(start_angle - self.mouth_angle))),
                (x + (CELL_SIZE // 2) * math.cos(math.radians(start_angle + self.mouth_angle)),
                 y - (CELL_SIZE // 2) * math.sin(math.radians(start_angle + self.mouth_angle)))
            ]
            pygame.draw.polygon(screen, BLACK, mouth_points)
    
    def move(self):
        # 检查下一个方向是否可行
        next_row = self.row + self.next_direction[1]
        next_col = self.col + self.next_direction[0]
        
        # 处理左右通道互穿
        if next_col < 0:
            next_col = COLS - 1
        elif next_col >= COLS:
            next_col = 0
            
        if 0 <= next_row < ROWS and MAZE[next_row][next_col] != 1:
            self.direction = self.next_direction
        
        # 按当前方向移动
        new_row = self.row + self.direction[1]
        new_col = self.col + self.direction[0]
        
        # 处理左右通道互穿
        if new_col < 0:
            new_col = COLS - 1
        elif new_col >= COLS:
            new_col = 0
            
        if 0 <= new_row < ROWS and MAZE[new_row][new_col] != 1:
            self.row = new_row
            self.col = new_col
            
            # 收集豆子
            if MAZE[self.row][self.col] == 2:
                MAZE[self.row][self.col] = 0
                self.score += 10
            elif MAZE[self.row][self.col] == 3:
                MAZE[self.row][self.col] = 0
                self.score += 50
                self.power_up = True
                self.power_timer = 300  # 5秒

class Ghost:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.direction = [0, 0]
        self.scared = False
        self.move_counter = 0
        self.move_delay = 2
        
    def move(self, pacman):
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        self.move_counter = 0
        
        possible_moves = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_row = self.row + dy
            new_col = self.col + dx
            
            # 处理左右通道互穿
            if new_col < 0:
                new_col = COLS - 1
            elif new_col >= COLS:
                new_col = 0
                
            if 0 <= new_row < ROWS and MAZE[new_row][new_col] != 1:
                possible_moves.append((dx, dy))
        
        if possible_moves:
            if random.random() < 0.5:
                best_move = min(possible_moves, 
                              key=lambda m: abs(self.row + m[1] - pacman.row) + 
                                          abs(self.col + m[0] - pacman.col))
                self.direction = best_move
            else:
                self.direction = random.choice(possible_moves)
            
            self.row += self.direction[1]
            self.col += self.direction[0]
            
            # 处理左右通道互穿
            if self.col < 0:
                self.col = COLS - 1
            elif self.col >= COLS:
                self.col = 0
    
    def render(self):
        x = self.col * CELL_SIZE + CELL_SIZE // 2
        y = self.row * CELL_SIZE + CELL_SIZE // 2
        color = SCARED_GHOST if self.scared else self.color
        
        # 绘制幽灵身体
        pygame.draw.circle(screen, color, (x, y), CELL_SIZE // 2 - 2)
        
        # 绘制幽灵下部
        points = [
            (x - CELL_SIZE // 2 + 2, y),
            (x - CELL_SIZE // 2 + 2, y + CELL_SIZE // 2 - 2),
            (x - CELL_SIZE // 4, y + CELL_SIZE // 4 - 2),
            (x, y + CELL_SIZE // 2 - 2),
            (x + CELL_SIZE // 4, y + CELL_SIZE // 4 - 2),
            (x + CELL_SIZE // 2 - 2, y + CELL_SIZE // 2 - 2),
            (x + CELL_SIZE // 2 - 2, y)
        ]
        pygame.draw.polygon(screen, color, points)
        
        # 绘制眼睛
        eye_color = WHITE if not self.scared else BLUE
        pygame.draw.circle(screen, eye_color, (x - 5, y - 2), 4)
        pygame.draw.circle(screen, eye_color, (x + 5, y - 2), 4)
        
        # 绘制瞳孔
        pupil_color = BLACK if not self.scared else WHITE
        pygame.draw.circle(screen, pupil_color, (x - 5 + self.direction[0] * 2, y - 2 + self.direction[1] * 2), 2)
        pygame.draw.circle(screen, pupil_color, (x + 5 + self.direction[0] * 2, y - 2 + self.direction[1] * 2), 2)

def draw_maze():
    # 首先检查相邻的墙
    def has_adjacent_wall(row, col):
        adjacent = []
        # 检查上下左右是否有墙
        if row > 0:  # 上
            adjacent.append(MAZE[row-1][col] == 1)
        else:
            adjacent.append(False)
        if row < ROWS-1:  # 下
            adjacent.append(MAZE[row+1][col] == 1)
        else:
            adjacent.append(False)
        if col > 0:  # 左
            adjacent.append(MAZE[row][col-1] == 1)
        else:
            adjacent.append(False)
        if col < COLS-1:  # 右
            adjacent.append(MAZE[row][col+1] == 1)
        else:
            adjacent.append(False)
        return adjacent  # 返回[上,下,左,右]是否有墙

    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            cell = MAZE[row][col]
            if cell == 1:  # 墙
                # 先画黑色背景
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))
                
                # 检查相邻的墙
                adjacent = has_adjacent_wall(row, col)
                
                # 画四条边，如果相应方向没有相邻的墙才画
                if not adjacent[0]:  # 上边
                    pygame.draw.line(screen, PURPLE, (x, y), (x + CELL_SIZE, y))
                if not adjacent[1]:  # 下边
                    pygame.draw.line(screen, PURPLE, (x, y + CELL_SIZE), (x + CELL_SIZE, y + CELL_SIZE))
                if not adjacent[2]:  # 左边
                    pygame.draw.line(screen, PURPLE, (x, y), (x, y + CELL_SIZE))
                if not adjacent[3]:  # 右边
                    pygame.draw.line(screen, PURPLE, (x + CELL_SIZE, y), (x + CELL_SIZE, y + CELL_SIZE))
                
            elif cell == 2:  # 普通豆子
                pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 2)
            elif cell == 3:  # 能量豆
                # 添加能量豆闪烁效果
                if pygame.time.get_ticks() % 1000 < 500:  # 每秒闪烁一次
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 8)
                else:
                    pygame.draw.circle(screen, WHITE, (x + CELL_SIZE // 2, y + CELL_SIZE // 2), 6)

def reset_game():
    # 重置迷宫
    global MAZE
    MAZE = [row[:] for row in ORIGINAL_MAZE]
    
    # 重置吃豆人
    pacman = Pacman()
    
    # 重置幽灵
    ghosts = [
        Ghost(10, 9, RED),
        Ghost(10, 8, PINK),
        Ghost(10, 10, ORANGE),
        Ghost(10, 11, CYAN)
    ]
    
    return pacman, ghosts

def check_win():
    # 检查是否还有普通豆子
    for row in MAZE:
        if 2 in row:  # 如果还有普通豆子
            return False
    return True

def show_game_over(score, is_win):
    screen.fill(BLACK)
    
    # 显示胜利或失败信息
    if is_win:
        title_text = font.render('YOU WIN!', True, GREEN)
    else:
        title_text = font.render('GAME OVER', True, RED)
    screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, WINDOW_HEIGHT // 3))
    
    # 显示分数
    score_text = font.render(f'Final Score: {score}', True, WHITE)
    screen.blit(score_text, (WINDOW_WIDTH // 2 - score_text.get_width() // 2, WINDOW_HEIGHT // 2))
    
    # 显示操作说明
    restart_text = font.render('Press SPACE to restart', True, GREEN)
    quit_text = font.render('Press Q to quit', True, GREEN)
    screen.blit(restart_text, (WINDOW_WIDTH // 2 - restart_text.get_width() // 2, WINDOW_HEIGHT * 2 // 3))
    screen.blit(quit_text, (WINDOW_WIDTH // 2 - quit_text.get_width() // 2, WINDOW_HEIGHT * 2 // 3 + 40))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        clock.tick(30)

def show_ready_screen():
    ready_timer = 60  # 约2秒的准备时间
    while ready_timer > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)
        draw_maze()
        
        # 显示准备信息
        ready_text = font.render('Get Ready!', True, YELLOW)
        text_rect = ready_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(ready_text, text_rect)
        
        pygame.display.flip()
        clock.tick(30)
        ready_timer -= 1

def main():
    pacman, ghosts = reset_game()
    show_ready_screen()
    
    running = True
    while running:
        current_time = pygame.time.get_ticks()  # 获取当前时间用于动画
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.next_direction = [-1, 0]
                elif event.key == pygame.K_RIGHT:
                    pacman.next_direction = [1, 0]
                elif event.key == pygame.K_UP:
                    pacman.next_direction = [0, -1]
                elif event.key == pygame.K_DOWN:
                    pacman.next_direction = [0, 1]
                elif event.key == pygame.K_q:
                    running = False
        
        # 更新游戏状态
        pacman.update()
        
        # 检查是否获胜
        if check_win():
            show_game_over(pacman.score, True)
            pacman, ghosts = reset_game()
            show_ready_screen()
            continue
        
        # 更新幽灵状态
        for ghost in ghosts:
            ghost.scared = pacman.power_up  # 确保幽灵状态与吃豆人能量状态同步
            ghost.move(pacman)
            
            # 检查与幽灵的碰撞
            if ghost.row == pacman.row and ghost.col == pacman.col:
                if ghost.scared:
                    ghost.row = 9
                    ghost.col = 9
                    ghost.scared = False
                    pacman.score += 200
                else:
                    show_game_over(pacman.score, False)
                    pacman, ghosts = reset_game()
                    show_ready_screen()
                    break
        
        # 绘制游戏画面
        screen.fill(BLACK)
        draw_maze()
        pacman.render()
        for ghost in ghosts:
            ghost.render()
            
        # 显示分数
        score_text = font.render(f'Score: {pacman.score}', True, WHITE)
        screen.blit(score_text, (10, WINDOW_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(GAME_SPEED)
    
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
