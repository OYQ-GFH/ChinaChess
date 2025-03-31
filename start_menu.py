import sys
import pygame
import os

import chinese_chess
import play_against_ai

WINDOW_SIZE = (756, 560)
WINDOW_TITLE = "中国象棋"

class StartMenu:
    """开始菜单类"""
    
    def __init__(self):
        """初始化开始菜单"""
        # 初始化pygame，只初始化必要的模块
        pygame.display.init()
        pygame.font.init()
        
        # 初始化音频系统
        try:
            pygame.mixer.init()
            self.sound_initialized = True
            self.is_muted = False
        except Exception as e:
            print(f"音频初始化失败: {e}")
            self.sound_initialized = False
            self.is_muted = True
        
        # 设置窗口
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)
        
        # 延迟加载资源
        self.original_images = {}
        self.load_original_images()
        
        # 初始化背景音乐
        self.initialize_sound()
        
        # 加载原始图片
    def load_original_images(self):
        # 加载图标
        icon = pygame.image.load("./images/ico1.png")
        pygame.display.set_icon(icon)
        
        # 加载音量控制图标，使用convert_alpha优化性能
        self.original_images['sound_on'] = pygame.image.load("./images/sound_on.svg").convert_alpha()
        self.original_images['sound_off'] = pygame.image.load("./images/sound_off.svg").convert_alpha()
        self.sound_icon_size = (32, 32)
        self.sound_on_icon = pygame.transform.scale(self.original_images['sound_on'], self.sound_icon_size)
        self.sound_off_icon = pygame.transform.scale(self.original_images['sound_off'], self.sound_icon_size)
        
        # 音量控制按钮位置
        self.sound_button_rect = pygame.Rect(WINDOW_SIZE[0] - 50, 20, 32, 32)
        self.is_muted = False
        
        # 加载背景图片和装饰图案，使用convert优化性能
        self.bg = pygame.image.load("./images/bg2.png").convert()
        self.bg_pattern = pygame.image.load("./images/bg_pattern.svg").convert_alpha()
        self.bg_pattern = pygame.transform.scale(self.bg_pattern, WINDOW_SIZE)
        
        # 设置字体 - 使用支持中文的字体
        try:
            # 尝试使用微软雅黑字体
            self.title_font = pygame.font.SysFont('microsoft yahei', 80)
            self.button_font = pygame.font.SysFont('microsoft yahei', 50)
        except:
            # 如果微软雅黑不可用，尝试使用其他常见中文字体
            try:
                self.title_font = pygame.font.SysFont('simsun', 80)  # 宋体
                self.button_font = pygame.font.SysFont('simsun', 50)
            except:
                # 如果都不可用，使用系统默认字体并打印警告
                print("警告：无法加载中文字体，可能导致中文显示异常")
                self.title_font = pygame.font.Font(None, 80)
                self.button_font = pygame.font.Font(None, 50)
        
        # 设置颜色
        self.white = (245, 222, 179)  # 小麦色作为按钮背景
        self.black = (61, 43, 31)  # 深棕色作为文字
        self.red = (255, 0, 0)
        self.gold = (205, 133, 63)  # 秘鲁色作为悬停边框
        self.hover_color = (222, 184, 135)  # 棕褐色作为悬停背景
        self.button_border_color = (139, 69, 19)  # 马鞍棕色作为按钮边框
        self.shadow_color = (101, 67, 33, 128)  # 棕色阴影
        
        # 设置按钮
        self.button_width = 300
        self.button_height = 60
        self.button_margin = 30
        
        # 按钮位置
        self.center_x = WINDOW_SIZE[0] // 2
        self.center_y = WINDOW_SIZE[1] // 2
        
        # 双人对战按钮
        self.two_player_rect = pygame.Rect(
            self.center_x - self.button_width // 2,
            self.center_y - self.button_height - self.button_margin // 2,
            self.button_width,
            self.button_height
        )
        
        # AI对弈按钮
        self.ai_player_rect = pygame.Rect(
            self.center_x - self.button_width // 2,
            self.center_y + self.button_margin // 2,
            self.button_width,
            self.button_height
        )
        
        # 退出按钮
        self.exit_rect = pygame.Rect(
            self.center_x - self.button_width // 2,
            self.center_y + self.button_height + self.button_margin,
            self.button_width,
            self.button_height
        )
    
    def draw_text(self, text, font, color, surface, x, y, center=True, shadow=False):
        """绘制文本"""
        if shadow:
            # 创建渐变色文本
            gradient_colors = [(255, 0, 0), (255, 215, 0)]
            text_surfaces = []
            for c in gradient_colors:
                text_surface = font.render(text, True, c)
                text_surfaces.append(text_surface)
            
            # 创建阴影
            shadow_surface = font.render(text, True, (0, 0, 0))
            shadow_rect = shadow_surface.get_rect()
            if center:
                shadow_rect.center = (x + 4, y + 4)
            else:
                shadow_rect.topleft = (x + 4, y + 4)
            shadow_surface.set_alpha(128)
            surface.blit(shadow_surface, shadow_rect)
            
            # 混合渐变色文本
            text_rect = text_surfaces[0].get_rect()
            if center:
                text_rect.center = (x, y)
            else:
                text_rect.topleft = (x, y)
            
            # 创建渐变效果
            for i, text_surface in enumerate(text_surfaces):
                text_surface.set_alpha(255 - i * 128)
                surface.blit(text_surface, text_rect)
        else:
            text_obj = font.render(text, True, color)
            text_rect = text_obj.get_rect()
            if center:
                text_rect.center = (x, y)
            else:
                text_rect.topleft = (x, y)
            surface.blit(text_obj, text_rect)
    
    def draw_button(self, rect, text, hover=False):
        """绘制按钮"""
        # 创建圆角矩形
        radius = 15
        
        # 使用缓存的矩形对象
        if not hasattr(self, '_shadow_rect'):
            self._shadow_rect = pygame.Rect(0, 0, rect.width, rect.height)
            self._glow_rect = pygame.Rect(0, 0, rect.width + 4, rect.height + 4)
        
        # 更新矩形位置
        self._shadow_rect.x = rect.x + 4
        self._shadow_rect.y = rect.y + 4
        pygame.draw.rect(self.window, self.shadow_color, self._shadow_rect, border_radius=radius)
        
        # 绘制按钮背景
        if hover:
            # 创建发光效果
            self._glow_rect.center = rect.center
            pygame.draw.rect(self.window, self.gold, self._glow_rect, border_radius=radius)
            pygame.draw.rect(self.window, self.hover_color, rect, border_radius=radius)
        else:
            pygame.draw.rect(self.window, self.white, rect, border_radius=radius)
        
        # 绘制按钮边框
        pygame.draw.rect(self.window, self.button_border_color, rect, 2, border_radius=radius)
        
        # 绘制按钮文本
        self.draw_text(text, self.button_font, self.black, self.window, rect.centerx, rect.centery)
        
        # 绘制华丽的正方形装饰边框
        # 创建一个比按钮略大的正方形
        decoration_rect = rect.copy()
        decoration_rect.inflate_ip(20, 20)  # 扩大边框尺寸
        
        # 绘制正方形边框 - 使用金色
        pygame.draw.rect(self.window, (218, 165, 32), decoration_rect, 2, border_radius=radius+5)  # 外层金色边框
        
        # 添加角落装饰
        corner_size = 15
        # 左上角
        pygame.draw.line(self.window, (255, 215, 0), 
                        (decoration_rect.left, decoration_rect.top + corner_size),
                        (decoration_rect.left, decoration_rect.top), 3)
        pygame.draw.line(self.window, (255, 215, 0), 
                        (decoration_rect.left, decoration_rect.top),
                        (decoration_rect.left + corner_size, decoration_rect.top), 3)
        
        # 右上角
        pygame.draw.line(self.window, (255, 215, 0), 
                        (decoration_rect.right, decoration_rect.top + corner_size),
                        (decoration_rect.right, decoration_rect.top), 3)
        pygame.draw.line(self.window, (255, 215, 0), 
                        (decoration_rect.right, decoration_rect.top),
                        (decoration_rect.right - corner_size, decoration_rect.top), 3)
        
        # 左下角
        pygame.draw.line(self.window, (255, 215, 0), 
                        (decoration_rect.left, decoration_rect.bottom - corner_size),
                        (decoration_rect.left, decoration_rect.bottom), 3)
        pygame.draw.line(self.window, (255, 215, 0), 
                        (decoration_rect.left, decoration_rect.bottom),
                        (decoration_rect.left + corner_size, decoration_rect.bottom), 3)
        
        # 右下角
        pygame.draw.line(self.window, (255, 215, 0), 
                        (decoration_rect.right, decoration_rect.bottom - corner_size),
                        (decoration_rect.right, decoration_rect.bottom), 3)
        pygame.draw.line(self.window, (255, 215, 0), 
                        (decoration_rect.right, decoration_rect.bottom),
                        (decoration_rect.right - corner_size, decoration_rect.bottom), 3)
        
        # 如果是悬停状态，添加额外的装饰效果
        if hover:
            inner_rect = decoration_rect.copy()
            inner_rect.inflate_ip(-8, -8)  # 内层边框稍小
            pygame.draw.rect(self.window, (255, 140, 0), inner_rect, 2, border_radius=radius+2)  # 内层橙色边框
    

    def initialize_sound(self):
        """初始化背景音乐"""
        if self.sound_initialized and not self.is_muted:
            try:
                pygame.mixer.music.load("./musics/start.mp3")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)  # 循环播放
            except Exception as e:
                print(f"背景音乐加载失败: {e}")
                self.is_muted = True

    def run(self):
        """运行开始菜单"""
        running = True
        
        while running:
            # 填充背景和装饰图案
            self.window.blit(self.bg, (0, 0))
            self.window.blit(self.bg_pattern, (0, 0))
            
            # 绘制标题
            self.draw_text("中国象棋", self.title_font, self.red, self.window, self.center_x, 100, shadow=True)
            
            # 获取鼠标位置
            mx, my = pygame.mouse.get_pos()
            
            # 检查鼠标是否悬停在按钮上
            two_player_hover = self.two_player_rect.collidepoint(mx, my)
            ai_player_hover = self.ai_player_rect.collidepoint(mx, my)
            exit_hover = self.exit_rect.collidepoint(mx, my)
            
            # 绘制按钮
            self.draw_button(self.two_player_rect, "双人对战", two_player_hover)
            self.draw_button(self.ai_player_rect, "AI对弈", ai_player_hover)
            self.draw_button(self.exit_rect, "退出游戏", exit_hover)
            
            # 绘制音量控制按钮
            current_icon = self.sound_off_icon if self.is_muted else self.sound_on_icon
            self.window.blit(current_icon, self.sound_button_rect)
            
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    # 处理窗口大小变化事件
                    self.handle_resize(event.size)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        if self.two_player_rect.collidepoint(mx, my):
                            # 启动双人对战模式
                            if self.sound_initialized:
                                pygame.mixer.music.stop()
                            return "two_player"
                        
                        if self.ai_player_rect.collidepoint(mx, my):
                            # 启动AI对弈模式
                            if self.sound_initialized:
                                pygame.mixer.music.stop()
                            return "ai_player"
                        
                        if self.exit_rect.collidepoint(mx, my):
                            # 退出游戏
                            pygame.quit()
                            sys.exit()
                        
                        if self.sound_button_rect.collidepoint(mx, my):
                            # 初始化音频系统(如果尚未初始化)
                            if not self.sound_initialized and not self.is_muted:
                                self.initialize_sound()
                            # 切换音量状态
                            self.is_muted = not self.is_muted
                            if self.is_muted:
                                pygame.mixer.music.set_volume(0.0)
                            else:
                                pygame.mixer.music.set_volume(0.5)
            
            # 更新屏幕
            pygame.display.update()


def main():
    """主函数"""
    # 创建开始菜单
    menu = StartMenu()
    
    # 运行菜单并获取选择
    choice = menu.run()
    
    # 根据选择启动相应模式
    if choice == "two_player":
        # 保持当前窗口，避免黑屏闪烁
        window = menu.window
        # 保存当前屏幕状态
        current_screen = window.copy()
        
        # 创建淡出效果
        for alpha in range(0, 255, 25):  # 逐渐增加透明度
            window.blit(current_screen, (0, 0))
            fade = pygame.Surface(WINDOW_SIZE)
            fade.fill((0, 0, 0))
            fade.set_alpha(alpha)
            window.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(30)  # 短暂延迟
        
        # 不要停止音乐，而是淡出
        pygame.mixer.music.fadeout(500)
        
        # 显示加载界面，让用户知道游戏正在加载中
        loading_font = pygame.font.SysFont('microsoft yahei', 36)
        loading_text = loading_font.render("游戏加载中，请稍候...", True, (255, 255, 255))
        loading_rect = loading_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
        
        # 创建进度条背景
        progress_bg_rect = pygame.Rect(WINDOW_SIZE[0]//2 - 150, WINDOW_SIZE[1]//2 + 40, 300, 20)
        progress_rect = pygame.Rect(WINDOW_SIZE[0]//2 - 150, WINDOW_SIZE[1]//2 + 40, 0, 20)
        
        # 显示初始加载界面
        window.fill((0, 0, 0))
        window.blit(loading_text, loading_rect)
        pygame.draw.rect(window, (100, 100, 100), progress_bg_rect)
        pygame.display.update()
        
        # 创建游戏实例并传递现有窗口
        game = chinese_chess.Game(existing_window=window)
        
        # 更新进度条 - 25%
        progress_rect.width = 75
        pygame.draw.rect(window, (255, 0, 0), progress_rect)
        pygame.display.update()
        pygame.time.delay(100)  # 短暂延迟
        
        # 预加载游戏资源
        count_init_coord = chinese_chess.count_init_coord()
        
        # 更新进度条 - 50%
        progress_rect.width = 150
        pygame.draw.rect(window, (255, 0, 0), progress_rect)
        pygame.display.update()
        pygame.time.delay(100)  # 短暂延迟
        
        # 预加载游戏棋盘和棋子
        game.img_place()
        
        # 更新进度条 - 100%
        progress_rect.width = 300
        pygame.draw.rect(window, (255, 0, 0), progress_rect)
        pygame.display.update()
        pygame.time.delay(300)  # 短暂延迟
        
        # 清除进度条，重新绘制游戏界面以避免红线问题
        window.fill((0, 0, 0))  # 完全清除屏幕
        pygame.display.update()
        pygame.time.delay(100)  # 短暂延迟
        
        # 重新初始化全局变量，避免棋子位置错误
        chinese_chess.CHESS_NAME = []
        chinese_chess.INIT_COORD = []
        chinese_chess.UNPLACED_COORD = []
        chinese_chess.INIT_RANGER = []
        chinese_chess.UNPLACED_RANGER = []
        chinese_chess.MIDPOINT = []
        chinese_chess.MIN_COORD = []
        chinese_chess.MAX_COORD = []
        chinese_chess.CHESS_STATE = {}
        chinese_chess.NAME = []
        chinese_chess.FEASIBLE_COORD = []
        chinese_chess.CHESS_INIT = {}
        
        # 重新计算坐标并绘制棋盘和棋子
        # 注意：img_place方法会调用count_init_coord()，所以这里不需要单独调用
        game.img_place()  # 重新绘制棋盘和棋子
        game.update()  # 更新显示
        
        # 启动游戏主循环
        game.main()
    elif choice == "ai_player":
        # 保持当前窗口，避免黑屏闪烁
        window = menu.window
        # 保存当前屏幕状态
        current_screen = window.copy()
        
        # 创建淡出效果
        for alpha in range(0, 255, 25):  # 逐渐增加透明度
            window.blit(current_screen, (0, 0))
            fade = pygame.Surface(WINDOW_SIZE)
            fade.fill((0, 0, 0))
            fade.set_alpha(alpha)
            window.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(30)  # 短暂延迟
        
        # 不要停止音乐，而是淡出
        pygame.mixer.music.fadeout(500)
        
        # 显示加载界面，让用户知道AI模式正在加载中
        loading_font = pygame.font.SysFont('microsoft yahei', 36)
        loading_text = loading_font.render("AI对弈模式加载中，请稍候...", True, (255, 255, 255))
        loading_rect = loading_text.get_rect(center=(WINDOW_SIZE[0]//2, WINDOW_SIZE[1]//2))
        
        # 创建进度条背景
        progress_bg_rect = pygame.Rect(WINDOW_SIZE[0]//2 - 150, WINDOW_SIZE[1]//2 + 40, 300, 20)
        progress_rect = pygame.Rect(WINDOW_SIZE[0]//2 - 150, WINDOW_SIZE[1]//2 + 40, 0, 20)
        
        # 显示初始加载界面
        window.fill((0, 0, 0))
        window.blit(loading_text, loading_rect)
        pygame.draw.rect(window, (100, 100, 100), progress_bg_rect)
        pygame.display.update()
        
        # 更新进度条 - 50%
        progress_rect.width = 150
        pygame.draw.rect(window, (255, 0, 0), progress_rect)
        pygame.display.update()
        pygame.time.delay(300)  # 短暂延迟
        
        # 更新进度条 - 100%
        progress_rect.width = 300
        pygame.draw.rect(window, (255, 0, 0), progress_rect)
        pygame.display.update()
        pygame.time.delay(300)  # 短暂延迟
        
        # 清除进度条，避免红线问题
        window.fill((0, 0, 0))
        pygame.display.update()
        pygame.time.delay(100)  # 短暂延迟
        
        # 重新初始化全局变量，避免棋子位置错误
        chinese_chess.CHESS_NAME = []
        chinese_chess.INIT_COORD = []
        chinese_chess.UNPLACED_COORD = []
        chinese_chess.INIT_RANGER = []
        chinese_chess.UNPLACED_RANGER = []
        chinese_chess.MIDPOINT = []
        chinese_chess.MIN_COORD = []
        chinese_chess.MAX_COORD = []
        chinese_chess.CHESS_STATE = {}
        chinese_chess.NAME = []
        chinese_chess.FEASIBLE_COORD = []
        chinese_chess.CHESS_INIT = {}
        
        # 启动AI对弈模式
        # 导入AI对弈模块
        import gui_play_against_ai
        
        # 启动AI对弈主函数，传递现有窗口
        gui_play_against_ai.main()


if __name__ == "__main__":
    main()