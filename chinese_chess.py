import sys
import time
import pygame
import os
import random

WINDOW_SIZE = (756, 560)
WINDOW_TITLE = "中国象棋"
CHESS_X = 128
CHESS_Y = 2
CHESS_INTERVAL1 = 56

CHESS_NAME = []
INIT_COORD = []
UNPLACED_COORD = []
INIT_RANGER = []
UNPLACED_RANGER = []
MIDPOINT = []
MIN_COORD = []
MAX_COORD = []
CHESS_STATE = {}
NAME = []
FEASIBLE_COORD = []
CHESS_INIT = {}


def random_num():
    """获取背景音乐列表并生成随机播放顺序
    
    Returns:
        tuple: (所有背景音乐列表, 随机顺序索引列表, 音乐数量)
    """
    # 获取音乐文件列表
    musics = os.listdir("./musics")
    all_bgm = []
    
    # 筛选背景音乐文件
    for music in musics:
        if "bgm" in music:
            all_bgm.append(music)
    
    # 生成随机播放顺序
    index = len(all_bgm)
    # 使用random.sample更高效地生成不重复的随机数列表
    if index > 0:
        num_list = random.sample(range(index), index)
    else:
        num_list = []
        
    return all_bgm, num_list, index


def count_init_coord():
    """计算初始坐标"""

    # 计算所有棋子初始方置坐标
    initialize_coord = {
        # 黑棋
        "黑车1": (CHESS_X, CHESS_Y),
        "黑马1": (CHESS_INTERVAL1 + CHESS_X, CHESS_Y),
        "黑象1": (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_Y),
        "黑士1": (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_Y),
        "黑将": (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_Y),
        "黑士2": (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_Y),
        "黑象2": (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_Y),
        "黑马2": (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_Y),
        "黑车2": (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_Y),
        "黑炮1": (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        "黑炮2": (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        "黑卒1": (CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        "黑卒2": (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        "黑卒3": (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        "黑卒4": (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        "黑卒5": (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        # 红棋
        "红车1": (CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红马1": (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红象1": (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红士1": (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红将": (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红士2": (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红象2": (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红马2": (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红车2": (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 * 9 + CHESS_Y),
        "红炮1": (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        "红炮2": (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        "红卒1": (CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y),
        "红卒2": (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y),
        "红卒3": (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y),
        "红卒4": (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y),
        "红卒5": (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y)}

    # 计算所有棋子初始未放置坐标
    unplaced_coord = [
        # 第一列
        (CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        (CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        (CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y),
        # 第二列
        (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y),
        (CHESS_INTERVAL1 + CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y),
        # 第三列
        (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        (CHESS_INTERVAL1 * 2 + CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y),
        # 第四列
        (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y),
        (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        (CHESS_INTERVAL1 * 3 + CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y),
        # 第五列
        (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        (CHESS_INTERVAL1 * 4 + CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y),
        # 第六列
        (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y),
        (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        (CHESS_INTERVAL1 * 5 + CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y),
        # 第七列
        (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        (CHESS_INTERVAL1 * 6 + CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y),
        # 第八列
        (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 * 3 + CHESS_Y),
        (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 * 6 + CHESS_Y),
        (CHESS_INTERVAL1 * 7 + CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y),
        # 第九列
        (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 + CHESS_Y),
        (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 * 2 + CHESS_Y),
        (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 * 4 + CHESS_Y),
        (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 * 5 + CHESS_Y),
        (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 * 7 + CHESS_Y),
        (CHESS_INTERVAL1 * 8 + CHESS_X, CHESS_INTERVAL1 * 8 + CHESS_Y)]

    keys = initialize_coord.keys()
    values = initialize_coord.values()
    for chess_name, init_coord in zip(keys, values):
        CHESS_NAME.append(chess_name)
        INIT_COORD.append(init_coord)
    for a in unplaced_coord:
        UNPLACED_COORD.append(a)

    # 计算棋子初始范围坐标
    for coord in INIT_COORD:
        init_x = coord[0] + CHESS_INTERVAL1
        init_y = coord[1] + CHESS_INTERVAL1
        INIT_RANGER.append((init_x, init_y))
    # 计算剩余未放置棋子初始范围坐标
    for a_coord in UNPLACED_COORD:
        un_x = a_coord[0] + CHESS_INTERVAL1
        un_y = a_coord[1] + CHESS_INTERVAL1
        UNPLACED_RANGER.append((un_x, un_y))
    # 计算棋盘上棋子可点击的坐标
    all_x = []
    all_y = []
    chess_x = 149
    chess_y = 23
    for a_x in range(0, 9):
        all_x.append(chess_x)
        chess_x += 57
    for a_y in range(0, 10):
        all_y.append(chess_y)
        chess_y += 57
    for y in all_y:
        for x in all_x:
            MIDPOINT.append((x, y))
    # 计算棋盘上棋子可点击的坐标范围
    for mt_coord in MIDPOINT:
        mt_x = mt_coord[0]
        mt_y = mt_coord[1]
        min_x1 = mt_x - 15
        min_y1 = mt_y - 15
        max_x2 = mt_x + 15
        max_y2 = mt_y + 15
        MIN_COORD.append((min_x1, min_y1))
        MAX_COORD.append((max_x2, max_y2))


class Game(object):
    """游戏类"""

    click1 = None
    click2 = None
    red = True
    black = False
    index = 0
    chess_left_x = []
    chess_right_x = []
    chess_up_y = []
    chess_down_y = []
    chess_left_y = None
    chess_right_y = None
    chess_up_x = None
    chess_down_x = None
    name = None
    start_click_coord = None
    old_click_coord = None
    end_click_coord = None
    go = False
    m_chess_coord = {}
    no_go_coord = {}

    def __init__(self, existing_window=None):
        """初始化游戏环境、资源和状态变量
        
        Args:
            existing_window: 可选的现有pygame窗口，用于避免创建新窗口
        """
        # 设置窗口
        self.window = existing_window if existing_window else pygame.display.set_mode(WINDOW_SIZE)
        self.original_images = {}  # 存储原始图片
        # 初始化pygame和音频系统，但避免重新初始化
        if not pygame.get_init():
            pygame.init()
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        # 初始化音效控制状态
        self.bgm_enabled = True  # 背景音乐开关状态
        self.sfx_enabled = True  # 棋子音效开关状态
        
        # 初始化音效资源
        self.move = pygame.mixer.Sound("musics/move.WAV")  # 移动音效
        self.eat = pygame.mixer.Sound("./musics/eat.WAV")  # 吃子音效
        self.move.set_volume(1)
        self.eat.set_volume(1)
        
        # 加载并播放随机选择的背景音乐，但仅当没有音乐播放时
        if not pygame.mixer.music.get_busy():
            # 使用random_num函数获取随机音乐
            all_music, num_list, index = random_num()
            if index > 0:  # 确保有可用的背景音乐
                # 随机选择一首背景音乐播放
                random_music = all_music[num_list[0]]
                pygame.mixer.music.load(f"./musics/{random_music}")
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play()
        
        # 初始化音量控制按钮
        self.button_width = 150
        self.button_height = 50
        self.button_margin = 5
        
        # 音量控制按钮位置
        self.button_width = 100  # 减小按钮宽度
        self.button_height = 25  # 减小按钮高度
        self.bgm_button_rect = pygame.Rect(
            WINDOW_SIZE[0] - self.button_width - 15,
            10,
            self.button_width,
            self.button_height
        )
        self.sfx_button_rect = pygame.Rect(
            WINDOW_SIZE[0] - self.button_width - 15,
            10 + self.button_height + self.button_margin,
            self.button_width,
            self.button_height
        )
        # 返回按钮位置
        self.back_button_rect = pygame.Rect(
            WINDOW_SIZE[0] - self.button_width - 15,
            10 + (self.button_height + self.button_margin) * 2,
            self.button_width,
            self.button_height
        )
        
        # 音量控制状态
        self.bgm_enabled = True
        self.sfx_enabled = True
        self.bgm_volume = 0.5  # 初始音量
        self.sfx_volume = 1.0  # 初始音量
        
        # 设置字体
        try:
            self.button_font = pygame.font.SysFont('microsoft yahei', 14)  # 减小字体大小
        except:
            self.button_font = pygame.font.Font(None, 14)  # 减小字体大小
        
        # 初始化游戏窗口，如果提供了现有窗口则使用它
        pygame.display.set_caption(WINDOW_TITLE)
        if existing_window:
            self.window = existing_window
        else:
            self.window = pygame.display.set_mode(WINDOW_SIZE)
        
        # 加载并保存原始图片资源
        # 图标和界面元素
        self.original_images['ico1'] = pygame.image.load("./images/ico1.png")  # 红方图标
        self.original_images['ico2'] = pygame.image.load("./images/b_j.png")   # 黑方图标
        self.original_images['r_box'] = pygame.image.load("images/r_box.png")  # 红色选择框
        self.original_images['b_box'] = pygame.image.load("images/b_box.png")  # 黑色选择框
        self.original_images['dot'] = pygame.image.load("./images/dot.png")    # 可移动点
        
        # 背景图片
        self.original_images['bg1'] = pygame.image.load("images/bg1.png")  # 棋盘
        self.original_images['bg2'] = pygame.image.load("images/bg2.png")  # 背景
        
        # 初始化当前使用的图片
        self.ico1 = self.original_images['ico1']
        self.ico2 = self.original_images['ico2']
        self.r_box = self.original_images['r_box']
        self.b_box = self.original_images['b_box']
        self.dot = self.original_images['dot']
        self.bg1 = self.original_images['bg1']
        self.bg2 = self.original_images['bg2']
        
        # 加载并保存原始棋子图片
        # 黑方棋子图片
        self.original_images['b_z'] = pygame.image.load("images/b_z.png")  # 黑卒
        self.original_images['b_p'] = pygame.image.load("images/b_p.png")  # 黑炮
        self.original_images['b_c'] = pygame.image.load("images/b_c.png")  # 黑车
        self.original_images['b_m'] = pygame.image.load("images/b_m.png")  # 黑马
        self.original_images['b_x'] = pygame.image.load("images/b_x.png")  # 黑象
        self.original_images['b_s'] = pygame.image.load("images/b_s.png")  # 黑士
        self.original_images['b_j'] = pygame.image.load("images/b_j.png")  # 黑将
        
        # 红方棋子图片
        self.original_images['r_z'] = pygame.image.load("images/r_z.png")  # 红卒
        self.original_images['r_p'] = pygame.image.load("images/r_p.png")  # 红炮
        self.original_images['r_c'] = pygame.image.load("images/r_c.png")  # 红车
        self.original_images['r_m'] = pygame.image.load("images/r_m.png")  # 红马
        self.original_images['r_x'] = pygame.image.load("images/r_x.png")  # 红象
        self.original_images['r_s'] = pygame.image.load("images/r_s.png")  # 红士
        self.original_images['r_j'] = pygame.image.load("images/r_j.png")  # 红将
        
        # 初始化当前使用的棋子图片
        self.b_z = self.original_images['b_z']
        self.b_p = self.original_images['b_p']
        self.b_c = self.original_images['b_c']
        self.b_m = self.original_images['b_m']
        self.b_x = self.original_images['b_x']
        self.b_s = self.original_images['b_s']
        self.b_j = self.original_images['b_j']
        self.r_z = self.original_images['r_z']
        self.r_p = self.original_images['r_p']
        self.r_c = self.original_images['r_c']
        self.r_m = self.original_images['r_m']
        self.r_x = self.original_images['r_x']
        self.r_s = self.original_images['r_s']
        self.r_j = self.original_images['r_j']
        
        # 组织资源集合
        self.bg = (self.bg1, self.bg2)  # 背景图片元组
        self.b_chess = (self.b_z, self.b_p, self.b_c, self.b_m, self.b_x, self.b_s, self.b_j)  # 黑方棋子元组
        self.r_chess = (self.r_z, self.r_p, self.r_c, self.r_m, self.r_x, self.r_s, self.r_j)  # 红方棋子元组
        
        # 棋子名称到图片的映射字典
        self.chess_name = {
            "黑卒": self.b_chess[0], "黑炮": self.b_chess[1],
            "黑车": self.b_chess[2], "黑马": self.b_chess[3],
            "黑象": self.b_chess[4], "黑士": self.b_chess[5],
            "黑将": self.b_chess[6], "红卒": self.r_chess[0],
            "红炮": self.r_chess[1], "红车": self.r_chess[2],
            "红马": self.r_chess[3], "红象": self.r_chess[4],
            "红士": self.r_chess[5], "红将": self.r_chess[6]
        }

    def draw_sound_buttons(self):
        """绘制音量控制按钮和返回按钮"""
        # 获取鼠标位置以检测悬停状态
        mouse_pos = pygame.mouse.get_pos()
        bgm_hover = self.bgm_button_rect.collidepoint(mouse_pos)
        sfx_hover = self.sfx_button_rect.collidepoint(mouse_pos)
        back_hover = self.back_button_rect.collidepoint(mouse_pos)
        
        # 定义渐变色和阴影效果
        base_color = (245, 222, 179)  # 小麦色基础颜色
        hover_color = (222, 184, 135)  # 棕褐色悬停颜色
        shadow_color = (139, 69, 19, 128)  # 马鞍棕色阴影
        border_color = (139, 69, 19)  # 马鞍棕色边框
        text_color = (61, 43, 31)  # 深棕色文字
        
        # 绘制背景音乐按钮
        # 绘制阴影
        shadow_rect = self.bgm_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, shadow_color, shadow_surface.get_rect(), border_radius=5)
        self.window.blit(shadow_surface, shadow_rect)
        
        # 绘制按钮主体
        color = hover_color if bgm_hover else base_color
        pygame.draw.rect(self.window, color, self.bgm_button_rect, border_radius=5)
        pygame.draw.rect(self.window, border_color, self.bgm_button_rect, 2, border_radius=5)
        
        # 绘制文字
        bgm_text = "关闭音乐" if self.bgm_enabled else "开启音乐"
        text_surface = self.button_font.render(bgm_text, True, text_color)
        text_rect = text_surface.get_rect(center=self.bgm_button_rect.center)
        self.window.blit(text_surface, text_rect)
        
        # 绘制音效按钮
        # 绘制阴影
        shadow_rect = self.sfx_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, shadow_color, shadow_surface.get_rect(), border_radius=5)
        self.window.blit(shadow_surface, shadow_rect)
        
        # 绘制按钮主体
        color = hover_color if sfx_hover else base_color
        pygame.draw.rect(self.window, color, self.sfx_button_rect, border_radius=5)
        pygame.draw.rect(self.window, border_color, self.sfx_button_rect, 2, border_radius=5)
        
        # 绘制文字
        sfx_text = "关闭音效" if self.sfx_enabled else "开启音效"
        text_surface = self.button_font.render(sfx_text, True, text_color)
        text_rect = text_surface.get_rect(center=self.sfx_button_rect.center)
        self.window.blit(text_surface, text_rect)
        
        # 绘制返回按钮
        # 绘制阴影
        shadow_rect = self.back_button_rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        shadow_surface = pygame.Surface((shadow_rect.width, shadow_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surface, shadow_color, shadow_surface.get_rect(), border_radius=5)
        self.window.blit(shadow_surface, shadow_rect)
        
        # 绘制按钮主体
        color = hover_color if back_hover else base_color
        pygame.draw.rect(self.window, color, self.back_button_rect, border_radius=5)
        pygame.draw.rect(self.window, border_color, self.back_button_rect, 2, border_radius=5)
        
        # 绘制文字
        back_text = "返回"
        text_surface = self.button_font.render(back_text, True, text_color)
        text_rect = text_surface.get_rect(center=self.back_button_rect.center)
        self.window.blit(text_surface, text_rect)
    
    def img_place(self):
        """放置棋盘和棋子"""

        count_init_coord()
        # 清空棋子状态字典，确保重新初始化
        global CHESS_STATE
        CHESS_STATE = {}
        
        # 绘制背景和棋盘
        self.window.blit(self.bg[1], (0, 0))
        self.window.blit(self.bg[0], (128, 0))
        
        # 绘制音量控制按钮
        self.draw_sound_buttons()
        
        # 初始化棋子状态字典
        for name, coord in zip(CHESS_NAME, INIT_COORD):
            CHESS_STATE[name] = coord
        
        # 绘制所有棋子
        self.window.blit(self.b_chess[2], INIT_COORD[0])  # 黑车1
        self.window.blit(self.b_chess[3], INIT_COORD[1])  # 黑马1
        self.window.blit(self.b_chess[4], INIT_COORD[2])  # 黑象1
        self.window.blit(self.b_chess[5], INIT_COORD[3])  # 黑士1
        self.window.blit(self.b_chess[6], INIT_COORD[4])  # 黑将
        self.window.blit(self.b_chess[5], INIT_COORD[5])  # 黑士2
        self.window.blit(self.b_chess[4], INIT_COORD[6])  # 黑象2
        self.window.blit(self.b_chess[3], INIT_COORD[7])  # 黑马2
        self.window.blit(self.b_chess[2], INIT_COORD[8])  # 黑车2
        self.window.blit(self.b_chess[1], INIT_COORD[9])  # 黑炮1
        self.window.blit(self.b_chess[1], INIT_COORD[10]) # 黑炮2
        self.window.blit(self.b_chess[0], INIT_COORD[11]) # 黑卒1
        self.window.blit(self.b_chess[0], INIT_COORD[12]) # 黑卒2
        self.window.blit(self.b_chess[0], INIT_COORD[13]) # 黑卒3
        self.window.blit(self.b_chess[0], INIT_COORD[14]) # 黑卒4
        self.window.blit(self.b_chess[0], INIT_COORD[15]) # 黑卒5
        self.window.blit(self.r_chess[2], INIT_COORD[16]) # 红车1
        self.window.blit(self.r_chess[3], INIT_COORD[17]) # 红马1
        self.window.blit(self.r_chess[4], INIT_COORD[18]) # 红象1
        self.window.blit(self.r_chess[5], INIT_COORD[19]) # 红士1
        self.window.blit(self.r_chess[6], INIT_COORD[20]) # 红将
        self.window.blit(self.r_chess[5], INIT_COORD[21]) # 红士2
        self.window.blit(self.r_chess[4], INIT_COORD[22]) # 红象2
        self.window.blit(self.r_chess[3], INIT_COORD[23]) # 红马2
        self.window.blit(self.r_chess[2], INIT_COORD[24]) # 红车2
        self.window.blit(self.r_chess[1], INIT_COORD[25]) # 红炮1
        self.window.blit(self.r_chess[1], INIT_COORD[26]) # 红炮2
        self.window.blit(self.r_chess[0], INIT_COORD[27]) # 红卒1
        self.window.blit(self.r_chess[0], INIT_COORD[28]) # 红卒2
        self.window.blit(self.r_chess[0], INIT_COORD[29]) # 红卒3
        self.window.blit(self.r_chess[0], INIT_COORD[30]) # 红卒4
        self.window.blit(self.r_chess[0], INIT_COORD[31]) # 红卒5

    def click_1(self, click1, click2):
        """第一次点击"""

        for name1, old_coord, new_coord in zip(CHESS_NAME, INIT_COORD, INIT_RANGER):
            old_x = old_coord[0]
            old_y = old_coord[1]
            new_x = new_coord[0]
            new_y = new_coord[1]
            click1_x = click1[0]
            click1_y = click1[1]
            # 判断第一次点击的坐标是不是在棋子初始坐标范围内
            if old_x <= click1_x <= new_x and old_y <= click1_y <= new_y:
                # print("{}被点击了".format(name1))
                # print("第一次点击: 棋子范围:({}~{}, {}~{}), 点击坐标:{}".format(old_x, new_x, old_y, new_y, click1))
                self.click_2(click2, name1, old_coord, new_coord)
                return

    def click_2(self, click2, name1, old_coord, new_coord):
        """第二次点击"""

        def go_on(eat):
            """继续判断"""
            for name2, init_coord, init_ranger in zip(CHESS_NAME, INIT_COORD, INIT_RANGER):
                # 判断两次点击是否都是棋子
                # if init_coord[0] < min_x < init_ranger[0] and init_coord[1] < min_y < init_ranger[1]:
                if init_coord[0] <= click2_x <= init_ranger[0] and init_coord[1] <= click2_y <= init_ranger[1]:
                    # 判断两次点击的棋子是否不一样
                    if "红" in name1 and "黑" in name2 or "黑" in name1 and "红" in name2:
                        if self.logic(init_coord):
                            eat = True
                            NAME.append(name2)
                            coord.append(init_coord)
                            un1_coord.append(init_coord)
                            un2_coord.append(init_ranger)
                            if len(NAME):
                                self.operate(len(coord), coord, old_coord, new_coord, un1_coord, un2_coord, eat, name1,
                                             name2=NAME[-1])
                                eat = False
                else:
                    for un1, un2 in zip(UNPLACED_COORD, UNPLACED_RANGER):
                        un_x1 = un1[0]
                        un_y1 = un1[1]
                        un_x2 = un2[0]
                        un_y2 = un2[1]
                        if un_x1 < min_x < un_x2 and un_y1 < min_y < un_y2:
                            coord.append(un1)
                            un1_coord.append(un1)
                            un2_coord.append(un2)
                    if len(NAME):
                        self.operate(len(coord), coord, old_coord, new_coord, un1_coord, un2_coord, eat, name1,
                                     name2=NAME[-1])
                    else:
                        self.operate(len(coord), coord, old_coord, new_coord, un1_coord, un2_coord, eat, name1,
                                     name2=None)

        for min_coord, max_coord in zip(MIN_COORD, MAX_COORD):
            min_x = min_coord[0]
            min_y = min_coord[1]
            max_x = max_coord[0]
            max_y = max_coord[1]
            click2_x = click2[0]
            click2_y = click2[1]
            # 判断第二次点击的坐标是不是在棋子可落子的坐标范围内
            if min_x <= click2_x <= max_x and min_y <= click2_y <= max_y:
                # print("第二次点击: 中心范围:({}~{}, {}~{}), 点击坐标:{}".format(min_x, max_x, min_y, max_y, click2))
                coord = []
                un1_coord = []
                un2_coord = []
                e = False
                if "红" in name1 and self.red:
                    go_on(e)
                elif "黑" in name1 and self.black:
                    go_on(e)
                else:
                    return

    def no_go(self):
        """切换当前行棋方
        
        在每次有效移动后调用，切换红黑双方的行棋权，
        并更新窗口图标以指示当前行棋方。
        """
        if self.red:  # 如果当前是红方行棋
            pygame.display.set_icon(self.ico2)  # 切换图标为黑方
            self.black = True  # 切换为黑方行棋
            self.red = False
        elif self.black:  # 如果当前是黑方行棋
            pygame.display.set_icon(self.ico1)  # 切换图标为红方
            self.black = False  # 切换为红方行棋
            self.red = True

    @staticmethod
    def logic(f_coord):
        """判断目标坐标是否是合法的走棋位置
        
        Args:
            f_coord: 目标坐标
            
        Returns:
            bool: 如果坐标在可行坐标列表中返回True，否则返回False
        """
        return f_coord in FEASIBLE_COORD

    def operate(self, flag, coord, old_coord, new_coord, un1_coord, un2_coord, eat, name1, name2):
        """棋子操作"""

        def blit(n):
            """放置棋子"""

            if eat:
                if name1 in CHESS_NAME:
                    CHESS_NAME.remove(name1)
                if old_coord in INIT_COORD:
                    INIT_COORD.remove(old_coord)
                if new_coord in INIT_RANGER:
                    INIT_RANGER.remove(new_coord)
                if name2 in CHESS_NAME:
                    CHESS_NAME.remove(name2)
                if un1_coord[-1] in INIT_COORD:
                    INIT_COORD.remove(un1_coord[-1])
                if un2_coord[-1] in INIT_RANGER:
                    INIT_RANGER.remove(un2_coord[-1])
                CHESS_NAME.insert(0, name1)
                INIT_COORD.insert(0, un1_coord[-1])
                INIT_RANGER.insert(0, un2_coord[-1])
                UNPLACED_COORD.insert(0, old_coord)
                UNPLACED_RANGER.insert(0, new_coord)
                # print("事件: {}吃掉了{}".format(name1, name2))
                self.eat.play()

            else:
                if name1 in CHESS_NAME:
                    CHESS_NAME.remove(name1)
                if old_coord in INIT_COORD:
                    INIT_COORD.remove(old_coord)
                if new_coord in INIT_RANGER:
                    INIT_RANGER.remove(new_coord)
                if un1_coord[-1] in UNPLACED_COORD:
                    UNPLACED_COORD.remove(un1_coord[-1])
                if un2_coord[-1] in UNPLACED_RANGER:
                    UNPLACED_RANGER.remove(un2_coord[-1])
                CHESS_NAME.insert(0, name1)
                INIT_COORD.insert(0, un1_coord[-1])
                INIT_RANGER.insert(0, un2_coord[-1])
                UNPLACED_COORD.insert(0, old_coord)
                UNPLACED_RANGER.insert(0, new_coord)
                # print("事件: {}从{}移动到{}".format(name1, old_coord, coord[0]))
                self.move.play()

            self.window.blit(self.bg[0], (128, 0))
            for a_name, init_coord in zip(CHESS_NAME, INIT_COORD):
                CHESS_STATE[a_name] = init_coord
            if name2 is not None and eat:
                for keys, value in zip(list(CHESS_STATE.keys()), list(CHESS_STATE.values())):
                    if name2 == keys:
                        del CHESS_STATE[name2]
            if name2 is not None and not eat:
                for keys, value in zip(list(CHESS_STATE.keys()), list(CHESS_STATE.values())):
                    if name2 == keys:
                        del CHESS_STATE[name2]
            for key, value in zip(CHESS_STATE.keys(), CHESS_STATE.values()):
                if eat:
                    if name2 != key:
                        for a in self.chess_name:
                            if a in key:
                                self.window.blit(self.chess_name[a], value)
                else:
                    if name1 != key:
                        for a in self.chess_name:
                            if a in key:
                                self.window.blit(self.chess_name[a], value)

            self.go = True
            self.old_click_coord = old_coord
            self.end_click_coord = coord[0]
            self.window.blit(n, coord[0])
            self.update()
            coord.clear()

        if flag and self.logic(un1_coord[-1]):

            for name in self.chess_name.keys():
                if name in name1:
                    self.no_go()
                    blit(self.chess_name[name])
        else:
            return False

    def show_dot(self, name1, d_coord, all_coord):
        """计算棋子可以走的点位"""

        def rule():
            if (d_coord[0] == all_coord[0] or d_coord[1] == all_coord[1]) and d_coord != all_coord:
                if all_coord[0] < d_coord[0]:
                    if all_coord in INIT_COORD:
                        self.chess_left_x.append(all_coord[0])
                        self.chess_left_x.sort(reverse=True)
                        self.chess_left_y = all_coord[1]
                    else:
                        if self.chess_left_x and self.chess_left_x[0] < all_coord[0]:
                            FEASIBLE_COORD.append(all_coord)
                        elif not self.chess_left_x and all_coord[0] < d_coord[0]:
                            FEASIBLE_COORD.append(all_coord)

                elif all_coord[0] > d_coord[0]:
                    if all_coord in INIT_COORD:
                        self.chess_right_x.append(all_coord[0])
                        self.chess_right_x.sort()
                        self.chess_right_y = all_coord[1]
                    else:
                        if self.chess_right_x and all_coord[0] < self.chess_right_x[0]:
                            FEASIBLE_COORD.append(all_coord)
                        elif not self.chess_right_x and d_coord[0] < all_coord[0]:
                            FEASIBLE_COORD.append(all_coord)

                elif all_coord[1] < d_coord[1]:
                    if all_coord in INIT_COORD:
                        self.chess_up_x = all_coord[0]
                        self.chess_up_y.append(all_coord[1])
                        self.chess_up_y.sort(reverse=True)
                    else:
                        if self.chess_up_y and self.chess_up_y[0] < all_coord[1]:
                            FEASIBLE_COORD.append(all_coord)
                        elif not self.chess_up_y and all_coord[1] < d_coord[1]:
                            FEASIBLE_COORD.append(all_coord)

                elif all_coord[1] > d_coord[1]:
                    if all_coord in INIT_COORD:
                        self.chess_down_x = all_coord[0]
                        self.chess_down_y.append(all_coord[1])
                        self.chess_down_y.sort()
                    else:
                        if self.chess_down_y and all_coord[1] < self.chess_down_y[0]:
                            FEASIBLE_COORD.append(all_coord)
                        elif not self.chess_down_y and d_coord[1] < all_coord[1]:
                            FEASIBLE_COORD.append(all_coord)

        def rule2():

            if "士" in name1:
                if d_coord[0] == all_coord[0] - CHESS_INTERVAL1 and d_coord[1] == all_coord[1] - CHESS_INTERVAL1:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] == all_coord[0] + CHESS_INTERVAL1 and d_coord[1] == all_coord[1] - CHESS_INTERVAL1:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] == all_coord[0] - CHESS_INTERVAL1 and d_coord[1] == all_coord[1] + CHESS_INTERVAL1:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] == all_coord[0] + CHESS_INTERVAL1 and d_coord[1] == all_coord[1] + CHESS_INTERVAL1:
                    FEASIBLE_COORD.append(all_coord)
            elif "将" in name1:
                if d_coord[0] == all_coord[0] - CHESS_INTERVAL1 and d_coord[1] == all_coord[1]:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] == all_coord[0] + CHESS_INTERVAL1 and d_coord[1] == all_coord[1]:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] == all_coord[0] and d_coord[1] == all_coord[1] - CHESS_INTERVAL1:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] == all_coord[0] and d_coord[1] == all_coord[1] + CHESS_INTERVAL1:
                    FEASIBLE_COORD.append(all_coord)

        if "红卒" in name1 and all_coord[1] <= d_coord[1]:
            if d_coord[1] <= 226:
                if d_coord[0] - CHESS_INTERVAL1 == all_coord[0] and d_coord[1] == all_coord[1]:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] + CHESS_INTERVAL1 == all_coord[0] and d_coord[1] == all_coord[1]:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] == all_coord[0] and d_coord[1] - CHESS_INTERVAL1 == all_coord[1]:
                    FEASIBLE_COORD.append(all_coord)
            elif all_coord[0] == d_coord[0] and d_coord[1] - CHESS_INTERVAL1 == all_coord[1]:
                FEASIBLE_COORD.append(all_coord)

        elif "黑卒" in name1 and all_coord[1] >= d_coord[1]:
            if d_coord[1] >= 282:
                if d_coord[0] - CHESS_INTERVAL1 == all_coord[0] and d_coord[1] == all_coord[1]:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] + CHESS_INTERVAL1 == all_coord[0] and d_coord[1] == all_coord[1]:
                    FEASIBLE_COORD.append(all_coord)
                elif d_coord[0] == all_coord[0] and d_coord[1] + CHESS_INTERVAL1 == all_coord[1]:
                    FEASIBLE_COORD.append(all_coord)
            elif all_coord[0] == d_coord[0] and d_coord[1] + CHESS_INTERVAL1 == all_coord[1]:
                FEASIBLE_COORD.append(all_coord)

        elif "炮" in name1 or "车" in name1:
            rule()
        elif "马" in name1:
            self.m_chess_coord["up_left"] = d_coord[0] - CHESS_INTERVAL1, d_coord[1] - CHESS_INTERVAL1 * 2
            self.m_chess_coord["up_right"] = d_coord[0] + CHESS_INTERVAL1, d_coord[1] - CHESS_INTERVAL1 * 2
            self.m_chess_coord["left_up"] = d_coord[0] - CHESS_INTERVAL1 * 2, d_coord[1] - CHESS_INTERVAL1
            self.m_chess_coord["left_down"] = d_coord[0] - CHESS_INTERVAL1 * 2, d_coord[1] + CHESS_INTERVAL1
            self.m_chess_coord["right_up"] = d_coord[0] + CHESS_INTERVAL1 * 2, d_coord[1] - CHESS_INTERVAL1
            self.m_chess_coord["right_down"] = d_coord[0] + CHESS_INTERVAL1 * 2, d_coord[1] + CHESS_INTERVAL1
            self.m_chess_coord["down_left"] = d_coord[0] - CHESS_INTERVAL1, d_coord[1] + CHESS_INTERVAL1 * 2
            self.m_chess_coord["down_right"] = d_coord[0] + CHESS_INTERVAL1, d_coord[1] + CHESS_INTERVAL1 * 2
            self.m_chess_coord["down_left"] = d_coord[0] - CHESS_INTERVAL1, d_coord[1] + CHESS_INTERVAL1 * 2
            self.m_chess_coord["down_right"] = d_coord[0] + CHESS_INTERVAL1, d_coord[1] + CHESS_INTERVAL1 * 2
            self.no_go_coord["go_left"] = d_coord[0] - CHESS_INTERVAL1, d_coord[1]
            self.no_go_coord["go_right"] = d_coord[0] + CHESS_INTERVAL1, d_coord[1]
            self.no_go_coord["go_up"] = d_coord[0], d_coord[1] - CHESS_INTERVAL1
            self.no_go_coord["go_down"] = d_coord[0], d_coord[1] + CHESS_INTERVAL1
        elif "象" in name1:
            self.m_chess_coord["up_left"] = d_coord[0] - CHESS_INTERVAL1 * 2, d_coord[1] + CHESS_INTERVAL1 * 2
            self.m_chess_coord["up_right"] = d_coord[0] + CHESS_INTERVAL1 * 2, d_coord[1] + CHESS_INTERVAL1 * 2
            self.m_chess_coord["down_left"] = d_coord[0] - CHESS_INTERVAL1 * 2, d_coord[1] - CHESS_INTERVAL1 * 2
            self.m_chess_coord["down_right"] = d_coord[0] + CHESS_INTERVAL1 * 2, d_coord[1] - CHESS_INTERVAL1 * 2
            self.no_go_coord["up_left"] = d_coord[0] - CHESS_INTERVAL1, d_coord[1] + CHESS_INTERVAL1
            self.no_go_coord["up_right"] = d_coord[0] + CHESS_INTERVAL1, d_coord[1] + CHESS_INTERVAL1
            self.no_go_coord["down_left"] = d_coord[0] - CHESS_INTERVAL1, d_coord[1] - CHESS_INTERVAL1
            self.no_go_coord["down_right"] = d_coord[0] + CHESS_INTERVAL1, d_coord[1] - CHESS_INTERVAL1

        elif "士" in name1 or "将" in name1:
            if "红" in name1:
                if CHESS_INTERVAL1 * 3 + CHESS_X <= all_coord[0] <= CHESS_INTERVAL1 * 5 + CHESS_X and CHESS_INTERVAL1 * 7 + CHESS_Y <= all_coord[1] <= CHESS_INTERVAL1 * 9 + CHESS_Y:
                    rule2()
            elif "黑" in name1:
                if CHESS_INTERVAL1 * 3 + CHESS_X <= all_coord[0] <= CHESS_INTERVAL1 * 5 + CHESS_X and CHESS_Y <= all_coord[1] <= CHESS_INTERVAL1 * 2 + CHESS_Y:
                    rule2()

    @staticmethod
    def play_music(music):
        """播放背景音乐
        
        Args:
            music: 音乐文件名
        """
        pygame.mixer.music.load(f"./musics/{music}")  # 使用f-string格式化，更现代的字符串格式化方式
        pygame.mixer.music.set_volume(0.5)  # 设置音量为50%
        pygame.mixer.music.play()  # 播放音乐

    def handle_volume_control(self, event):
        """处理音量控制滑动条的交互"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了滑块
            if self.bgm_knob_rect.collidepoint(event.pos):
                self.bgm_dragging = True
            elif self.sfx_knob_rect.collidepoint(event.pos):
                self.sfx_dragging = True
        
        elif event.type == pygame.MOUSEBUTTONUP:
            # 停止拖动
            self.bgm_dragging = False
            self.sfx_dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            # 处理滑块拖动
            if self.bgm_dragging:
                # 更新背景音乐滑块位置
                new_y = max(self.bgm_slider_rect.top, min(event.pos[1], self.bgm_slider_rect.bottom))
                self.bgm_knob_rect.centery = new_y
                # 计算并设置音量
                self.bgm_volume = 1 - (new_y - self.bgm_slider_rect.top) / self.slider_height
                pygame.mixer.music.set_volume(self.bgm_volume)
            
            elif self.sfx_dragging:
                # 更新音效滑块位置
                new_y = max(self.sfx_slider_rect.top, min(event.pos[1], self.sfx_slider_rect.bottom))
                self.sfx_knob_rect.centery = new_y
                # 计算并设置音量
                self.sfx_volume = 1 - (new_y - self.sfx_slider_rect.top) / self.slider_height
                self.move.set_volume(self.sfx_volume)
                self.eat.set_volume(self.sfx_volume)

    def handle_resize(self, new_size):
        """处理窗口大小变化
        
        Args:
            new_size: 新的窗口大小(width, height)
        """
        global WINDOW_SIZE, SCALE_FACTOR, CHESS_X, CHESS_Y, CHESS_INTERVAL1
        
        # 计算新的缩放因子
        width_scale = new_size[0] / BASE_WINDOW_SIZE[0]
        height_scale = new_size[1] / BASE_WINDOW_SIZE[1]
        SCALE_FACTOR = min(width_scale, height_scale)
        
        # 更新窗口大小和游戏元素尺寸
        WINDOW_SIZE = new_size
        CHESS_X = int(BASE_CHESS_X * SCALE_FACTOR)
        CHESS_Y = int(BASE_CHESS_Y * SCALE_FACTOR)
        CHESS_INTERVAL1 = int(BASE_CHESS_INTERVAL * SCALE_FACTOR)
        
        # 缩放所有图片
        for key, original_image in self.original_images.items():
            new_size = (int(original_image.get_width() * SCALE_FACTOR),
                       int(original_image.get_height() * SCALE_FACTOR))
            scaled_image = pygame.transform.smoothscale(original_image, new_size)
            
            # 更新对应的图片属性
            if key in ['ico1', 'ico2', 'r_box', 'b_box', 'dot', 'bg1', 'bg2']:
                setattr(self, key, scaled_image)
            elif key.startswith('b_') or key.startswith('r_'):
                setattr(self, key, scaled_image)
        
        # 更新棋子组合
        self.b_chess = (self.b_z, self.b_p, self.b_c, self.b_m, self.b_x, self.b_s, self.b_j)
        self.r_chess = (self.r_z, self.r_p, self.r_c, self.r_m, self.r_x, self.r_s, self.r_j)
        self.bg = (self.bg1, self.bg2)
        
        # 更新棋子名称到图片的映射
        self.chess_name = {
            "黑卒": self.b_chess[0], "黑炮": self.b_chess[1],
            "黑车": self.b_chess[2], "黑马": self.b_chess[3],
            "黑象": self.b_chess[4], "黑士": self.b_chess[5],
            "黑将": self.b_chess[6], "红卒": self.r_chess[0],
            "红炮": self.r_chess[1], "红车": self.r_chess[2],
            "红马": self.r_chess[3], "红象": self.r_chess[4],
            "红士": self.r_chess[5], "红将": self.r_chess[6]
        }
        
        # 重新计算所有坐标
        count_init_coord()
        
        # 重新绘制游戏界面
        self.img_place()
    
    def main(self):
        """事件判断"""

        name = None
        # 获取随机排序的背景音乐列表
        all_music, num_list, index = random_num()
        # 只在调试模式下打印音乐信息
        # print(all_music, num_list, index)
        while True:
            time.sleep(0.001)

            # 检查音乐是否播放完毕，如果播放完毕则播放下一首
            if not pygame.mixer.music.get_busy() and self.bgm_enabled:
                # 确保有可用的背景音乐
                if index > 0:
                    # 获取当前索引对应的音乐
                    music = all_music[num_list[self.index]]
                    # 只在调试模式下打印当前播放的音乐
                    # print(f"正在播放: {music}, 索引: {self.index}")
                    # 播放当前音乐
                    self.play_music(music)
                    # 更新索引，指向下一首要播放的音乐
                    self.index += 1
                    # 如果已经播放完所有音乐，重新开始
                    if self.index >= index:
                        self.index = 0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.VIDEORESIZE:
                    # 处理窗口大小变化事件
                    self.handle_resize(event.size)
                
                # 处理音量控制按钮点击
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        if self.bgm_button_rect.collidepoint(event.pos):
                            self.bgm_enabled = not self.bgm_enabled
                            if not self.bgm_enabled:
                                pygame.mixer.music.set_volume(0.0)
                            else:
                                pygame.mixer.music.set_volume(self.bgm_volume)
                            self.draw_sound_buttons()
                            pygame.display.update()  # 立即更新显示
                        elif self.sfx_button_rect.collidepoint(event.pos):
                            self.sfx_enabled = not self.sfx_enabled
                            # 重绘音量控制按钮
                            self.draw_sound_buttons()
                            # 更新显示
                            pygame.display.update()
                            if not self.sfx_enabled:
                                self.move.set_volume(0.0)
                                self.eat.set_volume(0.0)
                            else:
                                self.move.set_volume(self.sfx_volume)
                                self.eat.set_volume(self.sfx_volume)
                            self.draw_sound_buttons()
                        elif self.back_button_rect.collidepoint(event.pos):
                            # 停止当前音乐
                            pygame.mixer.music.stop()
                            # 返回到开始菜单
                            from start_menu import main
                            main()
                        if self.click1 is None:
                            self.click1 = event.pos
                            if len(FEASIBLE_COORD):
                                FEASIBLE_COORD.clear()
                                self.chess_left_x.clear()
                                self.chess_right_x.clear()
                                self.chess_up_y.clear()
                                self.chess_down_y.clear()
                                self.m_chess_coord.clear()
                                self.no_go_coord.clear()
                            for n, old_coord, new_coord in zip(CHESS_NAME, INIT_COORD, INIT_RANGER):
                                old_x = old_coord[0]
                                old_y = old_coord[1]
                                new_x = new_coord[0]
                                new_y = new_coord[1]
                                click1_x = event.pos[0]
                                click1_y = event.pos[1]
                                CHESS_INIT[n] = old_coord
                                if old_x <= click1_x <= new_x and old_y <= click1_y <= new_y:
                                    name = n
                                    self.name = n
                                    self.start_click_coord = old_coord
                                    self.window.blit(self.r_box, old_coord)
                                    self.update()
                            all_coord = INIT_COORD + UNPLACED_COORD
                            if self.start_click_coord is not None:
                                for coord in all_coord:
                                    self.show_dot(name, self.start_click_coord, coord)
                                if "炮" in self.name:
                                    if len(self.chess_left_x) >= 2:
                                        FEASIBLE_COORD.append((self.chess_left_x[1], self.chess_left_y))
                                    if len(self.chess_right_x) >= 2:
                                        FEASIBLE_COORD.append((self.chess_right_x[1], self.chess_right_y))
                                    if len(self.chess_up_y) >= 2:
                                        FEASIBLE_COORD.append((self.chess_up_x, self.chess_up_y[1]))
                                    if len(self.chess_down_y) >= 2:
                                        FEASIBLE_COORD.append((self.chess_down_x, self.chess_down_y[1]))
                                elif "车" in self.name:
                                    print(self.chess_left_x)
                                    if len(self.chess_left_x) >= 1:
                                        FEASIBLE_COORD.append((self.chess_left_x[0], self.chess_left_y))
                                    if len(self.chess_right_x) >= 1:
                                        FEASIBLE_COORD.append((self.chess_right_x[0], self.chess_right_y))
                                    if len(self.chess_up_y) >= 1:
                                        FEASIBLE_COORD.append((self.chess_up_x, self.chess_up_y[0]))
                                    if len(self.chess_down_y) >= 1:
                                        FEASIBLE_COORD.append((self.chess_down_x, self.chess_down_y[0]))
                                elif "马" in self.name:
                                    for key1, value1 in self.no_go_coord.items():
                                        for key2, value2 in self.m_chess_coord.items():
                                            if value1 not in INIT_COORD and value1 in UNPLACED_COORD:
                                                if key1[3:] == key2[:2] or key1[3:] == key2[:4] or key1[3:] == key2[:5]:
                                                    if CHESS_X <= value2[0] <= CHESS_INTERVAL1 * 8 + CHESS_X and CHESS_Y <= value2[1] <= CHESS_INTERVAL1 * 9 + CHESS_Y:
                                                        FEASIBLE_COORD.append(value2)
                                elif "象" in self.name:
                                    for key3, value3 in self.no_go_coord.items():
                                        for key4, value4 in self.m_chess_coord.items():
                                            if value3 not in INIT_COORD and value3 in UNPLACED_COORD:
                                                if key3 == key4:
                                                    if CHESS_X <= value4[0] <= CHESS_INTERVAL1 * 8 + CHESS_X and CHESS_Y <= value4[1] <= CHESS_INTERVAL1 * 9 + CHESS_Y:
                                                        if "红" in self.name and value4[1] >= 282:
                                                            FEASIBLE_COORD.append(value4)
                                                        elif "黑" in self.name and value4[1] <= 226:
                                                            FEASIBLE_COORD.append(value4)
                                if not self.go:
                                    for key, value in CHESS_INIT.items():
                                        if value in FEASIBLE_COORD:
                                            if self.name[0] == key[0]:
                                                FEASIBLE_COORD.remove(value)
                                elif self.go:
                                    for key, value in CHESS_STATE.items():
                                        if value in FEASIBLE_COORD:
                                            if self.name[0] == key[0]:
                                                FEASIBLE_COORD.remove(value)

                                for a_coord in FEASIBLE_COORD:
                                    self.window.blit(self.dot, a_coord)
                                self.update()

                        else:
                            self.click2 = event.pos
                            self.click_1(self.click1, self.click2)
                            print("当前 red:{},black:{}".format(self.red, self.black))
                            self.click1 = None
                            self.click2 = None
                            if not self.go:
                                self.window.blit(self.bg[0], (128, 0))
                                for chess_name in self.chess_name.keys():
                                    for key, value in CHESS_INIT.items():
                                        if chess_name in key:
                                            self.window.blit(self.chess_name[chess_name], value)
                            else:
                                self.window.blit(self.bg[0], (128, 0))
                                for chess_name in self.chess_name.keys():
                                    for key, value in CHESS_STATE.items():
                                        if chess_name in key:
                                            self.window.blit(self.chess_name[chess_name], value)
                                self.window.blit(self.b_box, self.old_click_coord)
                                self.window.blit(self.b_box, self.end_click_coord)
                            self.update()

    @staticmethod
    def update():
        """更新游戏窗口显示
        
        在每次绘制操作后调用，将更改显示到屏幕上
        """
        pygame.display.update()


if __name__ == "__main__":
    # 程序入口点
    game = Game()  # 创建游戏实例
    game.img_place()  # 初始化棋盘和棋子
    game.update()  # 更新显示
    game.main()  # 开始事件循环
