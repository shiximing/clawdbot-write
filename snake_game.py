import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
CELL_SIZE = 20
CELL_NUMBER_X = WINDOW_WIDTH // CELL_SIZE
CELL_NUMBER_Y = WINDOW_HEIGHT // CELL_SIZE

# 颜色定义
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

class Snake:
    def __init__(self):
        self.body = [(CELL_NUMBER_X // 2, CELL_NUMBER_Y // 2)]
        self.direction = (1, 0)  # 初始方向向右
        self.grow = False
        
    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = ((head_x + dir_x) % CELL_NUMBER_X, (head_y + dir_y) % CELL_NUMBER_Y)
        
        if new_head in self.body:
            return False  # 游戏结束，撞到自己
            
        self.body.insert(0, new_head)
        
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
            
        return True
        
    def change_direction(self, new_dir):
        # 防止反向移动
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
            
    def grow_snake(self):
        self.grow = True
        
    def draw(self, surface):
        for i, segment in enumerate(self.body):
            rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if i == 0:  # 蛇头
                pygame.draw.rect(surface, DARK_GREEN, rect)
            else:  # 蛇身
                pygame.draw.rect(surface, GREEN, rect)

class Food:
    def __init__(self):
        self.position = self.generate_position()
        
    def generate_position(self):
        return (random.randint(0, CELL_NUMBER_X - 1), random.randint(0, CELL_NUMBER_Y - 1))
        
    def respawn(self, snake_body):
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break
                
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, RED, rect)

def draw_grid(surface):
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, (40, 40, 40), rect, 1)

def draw_score(surface, score):
    font = pygame.font.SysFont('arial', 20)
    text = font.render(f'Score: {score}', True, WHITE)
    surface.blit(text, (10, 10))

def main():
    # 创建游戏窗口
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake Game')
    clock = pygame.time.Clock()
    
    # 创建游戏对象
    snake = Snake()
    food = Food()
    food.respawn(snake.body)
    
    score = 0
    
    # 游戏主循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction((0, -1))
                elif event.key == pygame.K_DOWN:
                    snake.change_direction((0, 1))
                elif event.key == pygame.K_LEFT:
                    snake.change_direction((-1, 0))
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction((1, 0))
        
        # 移动蛇
        if not snake.move():
            running = False  # 游戏结束
        
        # 检查是否吃到食物
        if snake.body[0] == food.position:
            snake.grow_snake()
            food.respawn(snake.body)
            score += 10
        
        # 绘制游戏画面
        screen.fill(BLACK)
        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)
        draw_score(screen, score)
        
        pygame.display.flip()
        clock.tick(10)  # 控制游戏速度
    
    # 游戏结束后显示最终得分
    font = pygame.font.SysFont('arial', 30)
    text = font.render(f'Game Over! Final Score: {score}', True, WHITE)
    text_rect = text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    
    # 等待几秒后退出
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()