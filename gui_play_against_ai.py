import sys
import time
import pygame
import os
import random
import numpy as np

from XQlightPy.position import Position
from XQlightPy.search import Search
from XQlightPy.cchess import move2Iccs, Iccs2move
import chinese_chess

WINDOW_SIZE = (756, 560)
WINDOW_TITLE = "中国象棋 - AI对弈"
CHESS_X = 128
CHESS_Y = 2
CHESS_INTERVAL1 = 56

SEARCH_TIME_MS = 1000

class AIGame(chinese_chess.Game):
    """AI对弈游戏类，继承自基本游戏类"""
    
    def __init__(self, existing_window=None, player_side=0):
        """初始化AI对弈游戏
        
        Args:
            existing_window: 可选的现有pygame窗口
            player_side: 玩家方，0为红方（先手），1为黑方（后手）
        """
        # 确保棋盘坐标已经被计算
        if not chinese_chess.MIDPOINT:
            chinese_chess.count_init_coord()
            
        # 添加AI最后一步的起始和目标位置记录
        self.ai_last_src = None
        self.ai_last_dst = None
            
        # 调用父类初始化
        super().__init__(existing_window)
        
        # 初始化AI引擎
        self.pos = Position()
        self.pos.fromFen("rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1")
        self.search = Search(self.pos, 16)
        
        # 设置玩家方和AI方
        self.player_side = player_side  # 0为红方（先手），1为黑方（后手）
        self.ai_side = 1 - player_side  # AI方与玩家方相反
        
        # 游戏状态
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.selected_piece = None
        self.valid_moves = []  # 当前选中棋子的有效移动
        
        # 添加悔棋和重新开始按钮
        self.button_width = 100
        self.button_height = 25
        # 将按钮放置在窗口右侧中间位置
        button_y_start = WINDOW_SIZE[1] // 2 - 100  # 从中间位置稍微往上
        self.undo_button_rect = pygame.Rect(
            WINDOW_SIZE[0] - self.button_width - 15, 
            button_y_start, 
            self.button_width, 
            self.button_height
        )
        self.restart_button_rect = pygame.Rect(
            WINDOW_SIZE[0] - self.button_width - 15, 
            button_y_start + self.button_height + 10,
            self.button_width,
            self.button_height
        )
        
        # 添加状态显示区域（放在按钮下方）
        self.status_rect = pygame.Rect(
            WINDOW_SIZE[0] - self.button_width - 15,  # 与按钮x坐标对齐
            button_y_start + (self.button_height + 10) * 2,
            self.button_width, 80  # 增加高度以显示完整信息
        )
        
        # 初始化字体
        try:
            self.status_font = pygame.font.SysFont('microsoft yahei', 14)
            self.button_font = pygame.font.SysFont('microsoft yahei', 18)
            self.message_font = pygame.font.SysFont('microsoft yahei', 36)
        except:
            self.status_font = pygame.font.Font(None, 16)
            self.button_font = pygame.font.Font(None, 18)
            self.message_font = pygame.font.Font(None, 36)
        
        # 初始化按钮颜色
        self.button_color = (245, 222, 179)  # 小麦色
        self.button_hover_color = (222, 184, 135)  # 棕褐色
        self.button_border_color = (139, 69, 19)  # 马鞍棕色
        self.button_text_color = (61, 43, 31)  # 深棕色
        
        # 初始化消息显示
        self.message = ""
        self.message_time = 0
        self.message_duration = 2000  # 消息显示持续时间（毫秒）
        
        # 如果玩家是黑方（后手），AI先行
        if self.player_side == 1:
            self.ai_move()
    
    def draw_button(self, rect, text, hover=False):
        """绘制按钮"""
        # 创建圆角矩形
        radius = 10
        
        # 绘制按钮背景
        if hover:
            pygame.draw.rect(self.window, self.button_hover_color, rect, border_radius=radius)
        else:
            pygame.draw.rect(self.window, self.button_color, rect, border_radius=radius)
        
        # 绘制按钮边框
        pygame.draw.rect(self.window, self.button_border_color, rect, 2, border_radius=radius)
        
        # 绘制按钮文本
        text_obj = self.button_font.render(text, True, self.button_text_color)
        text_rect = text_obj.get_rect(center=rect.center)
        self.window.blit(text_obj, text_rect)
    
    def draw_status(self):
        """绘制游戏状态信息"""
        # 绘制状态背景
        pygame.draw.rect(self.window, (245, 245, 220), self.status_rect, border_radius=10)
        pygame.draw.rect(self.window, (139, 69, 19), self.status_rect, 2, border_radius=10)
        
        # 绘制当前回合和玩家方信息
        turn_text = "轮到: " + ("红方" if self.pos.sdPlayer == 0 else "黑方")
        turn_color = (255, 0, 0) if self.pos.sdPlayer == 0 else (0, 0, 0)
        turn_obj = self.status_font.render(turn_text, True, turn_color)
        self.window.blit(turn_obj, (self.status_rect.x + 5, self.status_rect.y + 5))
        
        player_text = "执棋: " + ("红方" if self.player_side == 0 else "黑方")
        player_color = (255, 0, 0) if self.pos.sdPlayer == self.player_side else (0, 0, 0)
        player_obj = self.status_font.render(player_text, True, player_color)
        self.window.blit(player_obj, (self.status_rect.x + 5, self.status_rect.y + 25))
        
        # 如果有上一步移动，显示它
        if self.last_move:
            move_text = "着法: " + move2Iccs(self.last_move).replace("-", "").lower()
            move_obj = self.status_font.render(move_text, True, (0, 0, 0))
            self.window.blit(move_obj, (self.status_rect.x + 5, self.status_rect.y + 45))
    
    def show_message(self, message, duration=2000):
        """显示临时消息"""
        self.message = message
        self.message_time = pygame.time.get_ticks()
        self.message_duration = duration
    
    def draw_message(self):
        """绘制临时消息"""
        if self.message and pygame.time.get_ticks() - self.message_time < self.message_duration:
            # 创建半透明背景
            overlay = pygame.Surface((WINDOW_SIZE[0], 60))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.window.blit(overlay, (0, WINDOW_SIZE[1] // 2 - 30))
            
            # 绘制消息文本
            text_obj = self.message_font.render(self.message, True, (255, 255, 255))
            text_rect = text_obj.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
            self.window.blit(text_obj, text_rect)
    
    def board_coord_to_pos(self, x, y):
        """将棋盘坐标转换为Position中的坐标"""
        # 计算在90个点中的索引
        index = -1
        for i, (min_coord, max_coord) in enumerate(zip(chinese_chess.MIN_COORD, chinese_chess.MAX_COORD)):
            if min_coord[0] <= x <= max_coord[0] and min_coord[1] <= y <= max_coord[1]:
                index = i
                break
        
        if index == -1:
            return None
        
        # 计算行和列（从0开始）
        col = index % 9
        row = index // 9
        
        # 转换为XQlightPy坐标系统（从3开始）
        file = col + 3
        rank = row + 3
        
        # 返回XQlightPy坐标
        return (rank << 4) + file
    
    def pos_coord_to_board(self, pos_coord):
        """将Position中的坐标转换为棋盘坐标"""
        # 提取行和列（XQlightPy坐标系统）
        file = pos_coord & 15
        rank = pos_coord >> 4
        
        # 检查坐标是否在棋盘范围内
        if file < 3 or file > 11 or rank < 3 or rank > 12:
            return None
        
        # 转换为游戏坐标系统
        col = file - 3
        row = rank - 3
        
        # 计算在90个点中的索引
        index = row * 9 + col
        
        # 确保索引在有效范围内
        if 0 <= index < len(chinese_chess.MIDPOINT):
            # 返回中心点坐标
            return chinese_chess.MIDPOINT[index]
        
        return None
    
    def get_piece_at_pos(self, pos_coord):
        """获取指定位置的棋子"""
        return self.pos.squares[pos_coord]
    
    def is_player_piece(self, piece):
        """检查棋子是否属于玩家"""
        if piece == 0:
            return False
        
        piece_side = 1 if piece >= 16 else 0
        return piece_side == self.player_side
    
    def get_valid_moves(self, src_coord):
        """获取指定位置棋子的所有合法移动"""
        valid_moves = []
        
        # 遍历所有可能的目标位置
        for dst_rank in range(3, 13):
            for dst_file in range(3, 12):
                dst_coord = (dst_rank << 4) + dst_file
                move = (dst_coord << 8) + src_coord
                
                # 检查移动是否合法
                if self.pos.legalMove(move):
                    valid_moves.append(move)
        
        return valid_moves
    
    def highlight_selected_piece(self, coord):
        """高亮显示选中的棋子"""
        if coord is None:
            return
        
        # 获取棋盘坐标
        board_coord = self.pos_coord_to_board(coord)
        if board_coord is None:
            return
        
        # 根据当前玩家选择合适的选择框
        box = self.r_box if self.player_side == 0 else self.b_box
        
        # 绘制选择框
        self.window.blit(box, (board_coord[0] - 25, board_coord[1] - 25))
    
    def highlight_valid_moves(self, moves):
        """高亮显示有效移动"""
        for move in moves:
            dst_coord = move >> 8
            board_coord = self.pos_coord_to_board(dst_coord)
            if board_coord is not None:
                self.window.blit(self.dot, (board_coord[0] - 25, board_coord[1] - 25))
    
    def ai_move(self):
        """AI走棋"""
        # 检查游戏是否结束
        if self.game_over:
            return
        
        # 检查是否轮到AI
        if self.pos.sdPlayer != self.ai_side:
            return
        
        # 显示AI思考中消息
        self.show_message("AI思考中...", 10000)
        self.draw()
        pygame.display.update()
        
        # AI搜索最佳移动
        move = self.search.searchMain(64, SEARCH_TIME_MS)
        
        # 获取起始和目标位置坐标
        src_coord = move & 255
        dst_coord = move >> 8
        src_board_coord = self.pos_coord_to_board(src_coord)
        dst_board_coord = self.pos_coord_to_board(dst_coord)
        
        # 检查是否吃子
        dst_piece = self.get_piece_at_pos(dst_coord)
        
        # 执行移动
        self.pos.makeMove(move)
        self.last_move = move
        
        # 记录AI最后一步的起始和目标位置
        self.ai_last_src = src_coord
        self.ai_last_dst = dst_coord
        
        # 播放音效
        if dst_piece != 0:
            self.eat.play()
        else:
            self.move.play()
        
        # 清除消息
        self.message = ""
        
        # 重新绘制棋盘和所有棋子
        self.draw()
        
        # 更新显示
        pygame.display.update()
        
        # 检查游戏是否结束
        self.check_game_over()
    
    def player_move(self, src_coord, dst_coord):
        """玩家走棋"""
        # 创建移动
        move = (dst_coord << 8) + src_coord
        
        # 检查移动是否合法
        if not self.pos.legalMove(move):
            self.show_message("不合法的移动！")
            return False
        
        # 检查是否吃子
        dst_piece = self.get_piece_at_pos(dst_coord)
        
        # 执行移动
        self.pos.makeMove(move)
        self.last_move = move
        
        # 播放音效
        if dst_piece != 0:
            self.eat.play()
        else:
            self.move.play()
        
        # 获取棋盘坐标并显示走棋提示框
        src_board_coord = self.pos_coord_to_board(src_coord)
        dst_board_coord = self.pos_coord_to_board(dst_coord)
        if src_board_coord and dst_board_coord:
            box = self.r_box if self.player_side == 0 else self.b_box
            self.window.blit(box, (src_board_coord[0] - 25, src_board_coord[1] - 25))
            self.window.blit(box, (dst_board_coord[0] - 25, dst_board_coord[1] - 25))
            pygame.display.update()
        
        # 检查游戏是否结束
        if not self.check_game_over():
            # 如果游戏未结束，AI走棋
            self.ai_move()
        
        return True
    
    def undo_move(self):
        """悔棋"""
        # 如果游戏已结束，不允许悔棋
        if self.game_over:
            self.show_message("游戏已结束，无法悔棋！")
            return
        
        # 撤销玩家和AI的移动
        self.pos.undoMakeMove()  # 撤销AI的移动
        self.pos.undoMakeMove()  # 撤销玩家的移动
        
        # 重置状态
        self.last_move = None
        self.selected_piece = None
        self.valid_moves = []
        
        self.show_message("已悔棋")
    
    def restart_game(self):
        """重新开始游戏"""
        # 重置棋盘位置
        self.pos = Position()
        self.pos.fromFen("rnbakabnr/9/1c5c1/p1p1p1p1p/9/9/P1P1P1P1P/1C5C1/9/RNBAKABNR w - - 0 1")
        self.search = Search(self.pos, 16)
        
        # 重置游戏状态
        self.game_over = False
        self.winner = None
        self.last_move = None
        self.selected_piece = None
        self.valid_moves = []
        self.ai_last_src = None
        self.ai_last_dst = None
        
        # 如果玩家是黑方（后手），AI先行
        if self.player_side == 1:
            self.ai_move()
        
        self.show_message("游戏已重新开始")
    
    def check_game_over(self):
        """检查游戏是否结束"""
        winner = self.pos.winner()
        if winner is not None:
            self.game_over = True
            self.winner = winner
            
            if winner == 0:
                self.show_message("红方胜利！", 10000)
            elif winner == 1:
                self.show_message("黑方胜利！", 10000)
            elif winner == 2:
                self.show_message("和棋！", 10000)
            
            return True
        
        return False
    
    def draw(self):
        """绘制游戏界面"""
        # 绘制背景和棋盘
        self.window.blit(self.bg[1], (0, 0))
        self.window.blit(self.bg[0], (CHESS_X, CHESS_Y))
        
        # 绘制棋子
        for i in range(256):
            piece = self.pos.squares[i]
            if piece != 0:
                # 获取棋子类型和颜色
                piece_type = piece & 7
                piece_side = 1 if piece >= 16 else 0
                
                # 获取棋子图片
                # 棋子类型映射：0=帅/将，1=仕/士，2=相/象，3=马，4=车，5=炮，6=兵/卒
                # 而r_chess和b_chess的索引是：0=兵/卒，1=炮，2=车，3=马，4=相/象，5=仕/士，6=帅/将
                # 需要进行映射转换
                chess_type_map = {0: 6, 1: 5, 2: 4, 3: 3, 4: 2, 5: 1, 6: 0}
                mapped_type = chess_type_map.get(piece_type, 0)
                
                if piece_side == 0:  # 红方
                    img = self.r_chess[mapped_type]
                else:  # 黑方
                    img = self.b_chess[mapped_type]
                
                # 获取棋盘坐标并绘制
                board_coord = self.pos_coord_to_board(i)
                if board_coord is not None:
                    # 调整棋子位置，使其居中显示在棋盘交叉点上
                    self.window.blit(img, (board_coord[0] - 25, board_coord[1] - 25))
        
        # 高亮显示选中的棋子和有效移动
        if self.selected_piece is not None:
            self.highlight_selected_piece(self.selected_piece)
            self.highlight_valid_moves(self.valid_moves)
        
        # 绘制按钮
        mouse_pos = pygame.mouse.get_pos()
        undo_hover = self.undo_button_rect.collidepoint(mouse_pos)
        restart_hover = self.restart_button_rect.collidepoint(mouse_pos)
        
        self.draw_button(self.undo_button_rect, "悔棋", undo_hover)
        self.draw_button(self.restart_button_rect, "重新开始", restart_hover)
        
        # 绘制状态信息
        self.draw_status()
        
        # 绘制AI最后一步的走子路径
        if self.ai_last_src is not None and self.ai_last_dst is not None:
            src_board_coord = self.pos_coord_to_board(self.ai_last_src)
            dst_board_coord = self.pos_coord_to_board(self.ai_last_dst)
            if src_board_coord and dst_board_coord:
                self.window.blit(self.b_box, (src_board_coord[0] - 25, src_board_coord[1] - 25))
                self.window.blit(self.b_box, (dst_board_coord[0] - 25, dst_board_coord[1] - 25))
        
        # 绘制临时消息
        self.draw_message()
        
        # 绘制音量控制按钮和返回按钮
        self.draw_sound_buttons()
    
    def handle_click(self, pos):
        """处理鼠标点击"""
        # 检查是否点击了按钮
        if self.undo_button_rect.collidepoint(pos):
            self.undo_move()
            return
        
        if self.restart_button_rect.collidepoint(pos):
            self.restart_game()
            return
        
        # 检查音量控制按钮
        if self.bgm_button_rect.collidepoint(pos):
            self.bgm_enabled = not self.bgm_enabled
            if self.bgm_enabled:
                pygame.mixer.music.set_volume(self.bgm_volume)
            else:
                pygame.mixer.music.set_volume(0)
            return
        
        if self.sfx_button_rect.collidepoint(pos):
            self.sfx_enabled = not self.sfx_enabled
            if self.sfx_enabled:
                self.move.set_volume(self.sfx_volume)
                self.eat.set_volume(self.sfx_volume)
            else:
                self.move.set_volume(0)
                self.eat.set_volume(0)
            return
        
        # 检查返回按钮
        if self.back_button_rect.collidepoint(pos):
            # 停止当前音乐
            pygame.mixer.music.stop()
            # 返回到开始菜单
            from start_menu import main
            main()
            return
        
        # 如果游戏已结束或不是玩家回合，忽略点击
        if self.game_over or self.pos.sdPlayer != self.player_side:
            return
        
        # 将点击位置转换为棋盘坐标
        board_coord = self.board_coord_to_pos(pos[0], pos[1])
        if board_coord is None:
            return
        
        # 获取点击位置的棋子
        piece = self.get_piece_at_pos(board_coord)
        
        # 如果已经选中了棋子
        if self.selected_piece is not None:
            # 如果点击了同一个棋子，取消选择
            if board_coord == self.selected_piece:
                self.selected_piece = None
                self.valid_moves = []
                return
            
            # 如果点击了另一个己方棋子，选择新棋子
            if piece != 0 and self.is_player_piece(piece):
                self.selected_piece = board_coord
                self.valid_moves = self.get_valid_moves(board_coord)
                return
            
            # 尝试移动到目标位置
            if self.player_move(self.selected_piece, board_coord):
                # 移动成功，清除选择
                self.selected_piece = None
                self.valid_moves = []
        else:
            # 如果点击了己方棋子，选择它
            if piece != 0 and self.is_player_piece(piece):
                self.selected_piece = board_coord
                self.valid_moves = self.get_valid_moves(board_coord)
    
    def main(self):
        """游戏主循环"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        self.handle_click(event.pos)
            
            # 绘制游戏界面
            self.draw()
            
            # 更新显示
            pygame.display.update()
            
            # 控制帧率
            clock.tick(30)


def choose_side():
    """选择玩家方"""
    # 初始化pygame
    pygame.init()
    pygame.mixer.init()
    
    # 设置窗口
    window = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption(WINDOW_TITLE)
    
    # 加载背景图片
    bg = pygame.image.load("./images/bg2.png")
    
    # 设置字体
    try:
        title_font = pygame.font.SysFont('microsoft yahei', 48)
        button_font = pygame.font.SysFont('microsoft yahei', 36)
    except:
        title_font = pygame.font.Font(None, 48)
        button_font = pygame.font.Font(None, 36)
    
    # 设置按钮
    button_width = 200
    button_height = 60
    button_margin = 30
    
    # 红方按钮
    red_button_rect = pygame.Rect(
        WINDOW_SIZE[0] // 2 - button_width // 2,
        WINDOW_SIZE[1] // 2 - button_height - button_margin // 2,
        button_width,
        button_height
    )
    
    # 黑方按钮
    black_button_rect = pygame.Rect(
        WINDOW_SIZE[0] // 2 - button_width // 2,
        WINDOW_SIZE[1] // 2 + button_margin // 2,
        button_width,
        button_height
    )
    
    # 按钮颜色
    button_color = (245, 222, 179)  # 小麦色
    button_hover_color = (222, 184, 135)  # 棕褐色
    button_border_color = (139, 69, 19)  # 马鞍棕色
    button_text_color = (61, 43, 31)  # 深棕色
    
    # 主循环
    running = True
    choice = None
    
    while running and choice is None:
        # 填充背景
        window.blit(bg, (0, 0))
        
        # 绘制标题
        title_text = title_font.render("请选择执棋方", True, (255, 0, 0))
        title_rect = title_text.get_rect(center=(WINDOW_SIZE[0] // 2, 100))
        window.blit(title_text, title_rect)
        
        # 获取鼠标位置
        mx, my = pygame.mouse.get_pos()
        
        # 检查鼠标是否悬停在按钮上
        red_hover = red_button_rect.collidepoint(mx, my)
        black_hover = black_button_rect.collidepoint(mx, my)
        
        # 绘制红方按钮
        pygame.draw.rect(
            window,
            button_hover_color if red_hover else button_color,
            red_button_rect,
            border_radius=15
        )
        pygame.draw.rect(
            window,
            button_border_color,
            red_button_rect,
            2,
            border_radius=15
        )
        red_text = button_font.render("执红先行", True, (255, 0, 0))
        red_text_rect = red_text.get_rect(center=red_button_rect.center)
        window.blit(red_text, red_text_rect)
        
        # 绘制黑方按钮
        pygame.draw.rect(
            window,
            button_hover_color if black_hover else button_color,
            black_button_rect,
            border_radius=15
        )
        pygame.draw.rect(
            window,
            button_border_color,
            black_button_rect,
            2,
            border_radius=15
        )
        black_text = button_font.render("执黑后行", True, (0, 0, 0))
        black_text_rect = black_text.get_rect(center=black_button_rect.center)
        window.blit(black_text, black_text_rect)
        
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    if red_button_rect.collidepoint(mx, my):
                        choice = 0  # 红方
                    elif black_button_rect.collidepoint(mx, my):
                        choice = 1  # 黑方
        
        # 更新屏幕
        pygame.display.update()
    
    return choice, window


def main():
    """AI对弈主函数"""
    # 选择玩家方
    player_side, window = choose_side()
    
    # 如果用户关闭了窗口
    if player_side is None:
        pygame.quit()
        return
    
    # 创建游戏实例
    game = AIGame(existing_window=window, player_side=player_side)
    
    # 运行游戏
    game.main()
    
    # 退出pygame
    pygame.quit()


if __name__ == "__main__":
    main()