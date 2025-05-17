import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 设置游戏窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('贪吃蛇大作战')

# 游戏状态
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2 # 暂未使用，但可以扩展

# 字体
# 尝试使用 'SimHei' (黑体) 或 'Microsoft YaHei' (微软雅黑) 来支持中文显示
# 如果这些字体在您的系统上不可用，Pygame 可能会回退到默认字体，或者您可能需要指定一个 .ttf 字体文件的路径
FONT_STYLE = 'SimHei' # 或者 'Microsoft YaHei', 'msyh.ttc' 等

# 更多颜色
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (144, 238, 144)
DARK_GREEN = (0, 100, 0)
GREY = (128, 128, 128)

class Snake:
    def __init__(self, color=GREEN):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.color = color # 允许自定义蛇的颜色
        self.score = 0

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        x, y = cur

        if self.direction == "UP":
            y -= BLOCK_SIZE
        elif self.direction == "DOWN":
            y += BLOCK_SIZE
        elif self.direction == "LEFT":
            x -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            x += BLOCK_SIZE

        # 墙壁穿越逻辑
        x %= WINDOW_WIDTH
        y %= WINDOW_HEIGHT

        self.positions.insert(0, (x, y))

        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(WINDOW_WIDTH//2, WINDOW_HEIGHT//2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.score = 0

    def draw(self, surface):
        # 绘制蛇头
        head_x, head_y = self.positions[0]
        pygame.draw.rect(surface, DARK_GREEN, (head_x, head_y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(surface, self.color, (head_x+2, head_y+2, BLOCK_SIZE-4, BLOCK_SIZE-4))

        # 绘制蛇身
        for i, p in enumerate(self.positions[1:]):
            # 交替颜色，增加视觉效果
            body_color = LIGHT_GREEN if i % 2 == 0 else self.color
            pygame.draw.rect(surface, DARK_GREEN, (p[0], p[1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(surface, body_color, (p[0]+2, p[1]+2, BLOCK_SIZE-4, BLOCK_SIZE-4))

class Food:
    def __init__(self, color=RED):
        self.position = (0, 0)
        self.color = color # 允许自定义食物颜色
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, (WINDOW_WIDTH-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE,
            random.randint(0, (WINDOW_HEIGHT-BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        )

    def draw(self, surface):
        # 绘制食物，增加一点细节
        pygame.draw.ellipse(surface, self.color, 
                            (self.position[0], self.position[1], BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.ellipse(surface, tuple(max(0, c-50) for c in self.color), 
                            (self.position[0]+2, self.position[1]+2, BLOCK_SIZE-4, BLOCK_SIZE-4))

def draw_text(surface, text, size, x, y, color=WHITE, font_name=FONT_STYLE, center=False):
    font = pygame.font.SysFont(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_button(surface, text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, active_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(surface, inactive_color, (x, y, width, height))

    draw_text(surface, text, 20, x + width / 2, y + height / 2, BLACK, center=True)

def game_menu(clock):
    speeds = {"极慢": 5, "慢": 7, "中": 10, "快": 15, "极快": 20} # 调整了速度档位
    speed_names = list(speeds.keys())
    current_speed_index = speed_names.index("中") # 默认选中 "中" 速
    
    menu_running = True
    start_game_flag = False

    def decrease_speed():
        nonlocal current_speed_index
        current_speed_index = (current_speed_index - 1 + len(speeds)) % len(speeds)

    def increase_speed():
        nonlocal current_speed_index
        current_speed_index = (current_speed_index + 1) % len(speeds)

    def trigger_start_game():
        nonlocal start_game_flag
        nonlocal menu_running
        start_game_flag = True
        menu_running = False

    def trigger_quit_game():
        pygame.quit()
        sys.exit()

    while menu_running:
        window.fill(BLACK)
        draw_text(window, "贪吃蛇大作战", 64, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4, GREEN, center=True)

        selected_speed_value = speeds[speed_names[current_speed_index]]
        draw_text(window, f"速度: {speed_names[current_speed_index]} ({selected_speed_value})", 30, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50, WHITE, center=True)
        
        draw_button(window, "<", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 15, 40, 30, GREY, LIGHT_GREEN, decrease_speed)
        draw_button(window, ">", WINDOW_WIDTH // 2 + 60, WINDOW_HEIGHT // 2 - 15, 40, 30, GREY, LIGHT_GREEN, increase_speed)
        
        draw_button(window, "开始游戏", WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT * 3 // 4 - 30, 150, 50, GREEN, LIGHT_GREEN, trigger_start_game)
        draw_button(window, "退出", WINDOW_WIDTH // 2 - 75, WINDOW_HEIGHT * 3 // 4 + 30, 150, 50, RED, tuple(max(0,c-50) for c in RED), trigger_quit_game)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # 按回车开始游戏
                    trigger_start_game()
                elif event.key == pygame.K_LEFT:
                    decrease_speed()
                elif event.key == pygame.K_RIGHT:
                    increase_speed()
        
        pygame.display.flip()
        clock.tick(30) # 提高菜单帧率，改善按钮响应

    if start_game_flag:
        return speeds[speed_names[current_speed_index]]
    else: # 如果通过关闭窗口等方式退出菜单，也视为退出游戏
        pygame.quit()
        sys.exit()

def main():
    clock = pygame.time.Clock()
    game_state = GAME_STATE_MENU
    # game_speed_setting stores the snake's updates per second (e.g., 5, 7, 10)
    game_speed_setting = 10 # Default snake updates per second

    TARGET_RENDER_FPS = 30  # Fixed FPS for rendering and input polling
    snake_update_timer = 0.0
    # time_per_snake_update will be 1.0 / game_speed_setting

    snake = Snake(color=GREEN)
    food = Food(color=RED)
    
    # 美化背景
    background_image = pygame.Surface(window.get_size())
    background_image = background_image.convert()
    for y in range(0, WINDOW_HEIGHT, BLOCK_SIZE):
        for x in range(0, WINDOW_WIDTH, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            color = (30, 30, 30) if (x // BLOCK_SIZE + y // BLOCK_SIZE) % 2 == 0 else (40, 40, 40)
            pygame.draw.rect(background_image, color, rect)

    while True:
        dt = clock.get_time() / 1000.0 # Delta time in seconds

        if game_state == GAME_STATE_MENU:
            game_speed_setting = game_menu(clock) # This returns snake updates per second
            snake.reset() # 重置蛇的状态以便新游戏
            food.randomize_position() # 重置食物位置
            game_state = GAME_STATE_PLAYING
            snake_update_timer = 0.0 # Reset timer for snake updates

        elif game_state == GAME_STATE_PLAYING:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.direction != "DOWN":
                        snake.direction = "UP"
                    elif event.key == pygame.K_DOWN and snake.direction != "UP":
                        snake.direction = "DOWN"
                    elif event.key == pygame.K_LEFT and snake.direction != "RIGHT":
                        snake.direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and snake.direction != "LEFT":
                        snake.direction = "RIGHT"
                    elif event.key == pygame.K_ESCAPE: # 按 ESC 返回菜单
                        game_state = GAME_STATE_MENU
            
            if game_state != GAME_STATE_PLAYING: # If ESC was pressed, skip rest of loop
                continue

            # Update snake based on game_speed_setting (snake updates per second)
            snake_update_timer += dt
            time_per_snake_update = 1.0 / game_speed_setting if game_speed_setting > 0 else 0

            if time_per_snake_update == 0 or snake_update_timer >= time_per_snake_update:
                snake.update()
                snake_update_timer = 0 # Reset timer after update

                # 检查是否吃到食物
                if snake.get_head_position() == food.position:
                    snake.length += 1
                    snake.score += 1
                    food.randomize_position()

                # 检查自身碰撞
                head = snake.get_head_position()
                if head in snake.positions[1:]:
                    draw_text(window, "游戏结束!", 60, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50, RED, center=True)
                    draw_text(window, f"最终得分: {snake.score}", 40, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20, YELLOW, center=True)
                    draw_text(window, "按 ESC 返回菜单", 30, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 70, WHITE, center=True)
                    pygame.display.flip()
                    waiting_for_input = True
                    while waiting_for_input:
                        for event_game_over in pygame.event.get(): # Use a different event variable name
                            if event_game_over.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event_game_over.type == pygame.KEYDOWN and event_game_over.key == pygame.K_ESCAPE:
                                game_state = GAME_STATE_MENU
                                waiting_for_input = False
                        clock.tick(15) # Keep game over screen responsive
                    if game_state == GAME_STATE_MENU:
                        continue

            # 绘制游戏界面
            window.blit(background_image, (0,0)) # 绘制背景
            snake.draw(window)
            food.draw(window)

            # 显示分数
            draw_text(window, f'分数: {snake.score}', 36, 10, 10, WHITE)
            # Display the selected speed setting (e.g., 5, 7, 10)
            draw_text(window, f'速度: {game_speed_setting}', 24, WINDOW_WIDTH - 100, 10, WHITE)

            pygame.display.update()
            clock.tick(TARGET_RENDER_FPS) # Run game loop at fixed FPS for rendering/input

if __name__ == "__main__":
    main()