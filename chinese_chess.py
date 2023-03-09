import sys
import time
import pygame
from constant import *


class Game(object):
    """游戏类"""

    click1 = None
    click2 = None
    red = True
    black = False
    index = 0

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("./musics/start.mp3")
        self.ico1 = pygame.image.load("./images/ico1.png")
        self.ico2 = pygame.image.load("./images/b_j.png")
        self.dot = pygame.image.load("./images/dot.png")
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption(WINDOW_TITLE)
        self.move = pygame.mixer.Sound("musics/move.WAV")
        self.eat = pygame.mixer.Sound("./musics/eat.WAV")
        self.move.set_volume(1)
        self.eat.set_volume(1)
        pygame.mixer.music.set_volume(1)
        pygame.mixer.music.play()

    @staticmethod
    def img_load():
        """加载棋盘和棋子素材"""

        bg1 = pygame.image.load("images/bg1.png")
        bg2 = pygame.image.load("images/bg3.png")
        r_box = pygame.image.load("images/r_box.png")
        b_box = pygame.image.load("images/b_box.png")
        b_z = pygame.image.load("images/b_z.png")
        b_p = pygame.image.load("images/b_p.png")
        b_c = pygame.image.load("images/b_c.png")
        b_m = pygame.image.load("images/b_m.png")
        b_x = pygame.image.load("images/b_x.png")
        b_s = pygame.image.load("images/b_s.png")
        b_j = pygame.image.load("images/b_j.png")
        r_z = pygame.image.load("images/r_z.png")
        r_p = pygame.image.load("images/r_p.png")
        r_c = pygame.image.load("images/r_c.png")
        r_m = pygame.image.load("images/r_m.png")
        r_x = pygame.image.load("images/r_x.png")
        r_s = pygame.image.load("images/r_s.png")
        r_j = pygame.image.load("images/r_j.png")
        return (bg1, bg2, r_box, b_box), (b_z, b_p, b_c, b_m, b_x, b_s, b_j), (r_z, r_p, r_c, r_m, r_x, r_s, r_j)
    
    @staticmethod
    def chess_coord():
        """计算坐标"""

        # 计算所有棋子初始防置坐标
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

    def img_place(self):
        """放置棋盘和棋子"""

        self.chess_coord()
        bg, b_chess, r_chess = self.img_load()

        self.window.blit(bg[1], (0, 0))
        self.window.blit(bg[0], (128, 0))
        self.window.blit(b_chess[2], INIT_COORD[0])
        self.window.blit(b_chess[3], INIT_COORD[1])
        self.window.blit(b_chess[4], INIT_COORD[2])
        self.window.blit(b_chess[5], INIT_COORD[3])
        self.window.blit(b_chess[6], INIT_COORD[4])
        self.window.blit(b_chess[5], INIT_COORD[5])
        self.window.blit(b_chess[4], INIT_COORD[6])
        self.window.blit(b_chess[3], INIT_COORD[7])
        self.window.blit(b_chess[2], INIT_COORD[8])
        self.window.blit(b_chess[1], INIT_COORD[9])
        self.window.blit(b_chess[1], INIT_COORD[10])
        self.window.blit(b_chess[0], INIT_COORD[11])
        self.window.blit(b_chess[0], INIT_COORD[12])
        self.window.blit(b_chess[0], INIT_COORD[13])
        self.window.blit(b_chess[0], INIT_COORD[14])
        self.window.blit(b_chess[0], INIT_COORD[15])
        self.window.blit(r_chess[2], INIT_COORD[16])
        self.window.blit(r_chess[3], INIT_COORD[17])
        self.window.blit(r_chess[4], INIT_COORD[18])
        self.window.blit(r_chess[5], INIT_COORD[19])
        self.window.blit(r_chess[6], INIT_COORD[20])
        self.window.blit(r_chess[5], INIT_COORD[21])
        self.window.blit(r_chess[4], INIT_COORD[22])
        self.window.blit(r_chess[3], INIT_COORD[23])
        self.window.blit(r_chess[2], INIT_COORD[24])
        self.window.blit(r_chess[1], INIT_COORD[25])
        self.window.blit(r_chess[1], INIT_COORD[26])
        self.window.blit(r_chess[0], INIT_COORD[27])
        self.window.blit(r_chess[0], INIT_COORD[28])
        self.window.blit(r_chess[0], INIT_COORD[29])
        self.window.blit(r_chess[0], INIT_COORD[30])
        self.window.blit(r_chess[0], INIT_COORD[31])

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
        if self.red:
            pygame.display.set_icon(self.ico2)
            self.black = True
            self.red = False
        elif self.black:
            pygame.display.set_icon(self.ico1)
            self.black = False
            self.red = True
    
    def show_dot(self, name1, d_coord, all_coord):
        """显示点击棋子可以走的点"""
        
        if "红卒" in name1 and all_coord[1] <= d_coord[1]:
            if d_coord[1] <= 226:
                if (d_coord[0] - CHESS_INTERVAL1 == all_coord[0] and d_coord[1] == all_coord[1]) or (d_coord[0] + CHESS_INTERVAL1 == all_coord[0] and d_coord[1] == all_coord[1]) or (d_coord[0] == all_coord[0] and d_coord[1] - CHESS_INTERVAL1 == all_coord[1]):
                    FEASIBLE_COORD.append(all_coord)
            elif all_coord[0] == d_coord[0] and d_coord[1] - CHESS_INTERVAL1 == all_coord[1]:
                FEASIBLE_COORD.append(all_coord)

        elif "黑卒" in name1 and all_coord[1] >= d_coord[1]:
            if d_coord[1] >= 282:
                if (d_coord[0] - CHESS_INTERVAL1 == all_coord[0] and d_coord[1] == all_coord[1]) or (d_coord[0] + CHESS_INTERVAL1 == all_coord[0] and d_coord[1] == all_coord[1]) or (d_coord[0] == all_coord[0] and d_coord[1] + CHESS_INTERVAL1 == all_coord[1]):
                    FEASIBLE_COORD.append(all_coord)
            elif all_coord[0] == d_coord[0] and d_coord[1] + CHESS_INTERVAL1 == all_coord[1]:
                FEASIBLE_COORD.append(all_coord)

        else:
            pass

    @staticmethod
    def logic(f_coord):
        """棋子走棋逻辑判断"""

        if f_coord in FEASIBLE_COORD:
            return True
        return False

    def operate(self, flag, coord, old_coord, new_coord, un1_coord, un2_coord, eat, name1, name2):
        """棋子操作"""

        def blit1(n):
            """放置棋子"""

            if eat:
                CHESS_NAME.remove(name1)
                INIT_COORD.remove(old_coord)
                INIT_RANGER.remove(new_coord)
                CHESS_NAME.remove(name2)
                INIT_COORD.remove(un1_coord[-1])
                INIT_RANGER.remove(un2_coord[-1])
                CHESS_NAME.insert(0, name1)
                INIT_COORD.insert(0, un1_coord[-1])
                INIT_RANGER.insert(0, un2_coord[-1])
                UNPLACED_COORD.insert(0, old_coord)
                UNPLACED_RANGER.insert(0, new_coord)
                print("事件: {}吃掉了{}".format(name1, name2))
                self.eat.play()

            else:
                CHESS_NAME.remove(name1)
                INIT_COORD.remove(old_coord)
                INIT_RANGER.remove(new_coord)
                UNPLACED_COORD.remove(un1_coord[-1])
                UNPLACED_RANGER.remove(un2_coord[-1])
                CHESS_NAME.insert(0, name1)
                INIT_COORD.insert(0, un1_coord[-1])
                INIT_RANGER.insert(0, un2_coord[-1])
                UNPLACED_COORD.insert(0, old_coord)
                UNPLACED_RANGER.insert(0, new_coord)
                print("事件: {}从{}移动到{}".format(name1, old_coord, coord[0]))
                self.move.play()

            self.window.blit(bg[0], (128, 0))
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
                        for a in chess_name:
                            if a in key:
                                self.window.blit(chess_name[a], value)
                else:
                    if name1 != key:
                        for a in chess_name:
                            if a in key:
                                self.window.blit(chess_name[a], value)
            self.window.blit(n, coord[0])
            self.window.blit(bg[2], (coord[0]))
            self.window.blit(bg[2], old_coord)
            self.update()
            coord.clear()

        if flag and self.logic(un1_coord[-1]):
            bg, b_chess, r_chess = self.img_load()
            chess_name = {"黑卒": b_chess[0], "黑炮": b_chess[1], "黑车": b_chess[2], "黑马": b_chess[3],
                          "黑象": b_chess[4], "黑士": b_chess[5], "黑将": b_chess[6],
                          "红卒": r_chess[0], "红炮": r_chess[1], "红车": r_chess[2], "红马": r_chess[3],
                          "红象": r_chess[4], "红士": r_chess[5], "红将": r_chess[6]}
            for name in chess_name.keys():
                if name in name1:
                    self.no_go()
                    blit1(chess_name[name])
        else:
            return False

    def event(self):
        """事件判断"""

        click_coord = []
        midpoint = []
        name = None 
        bg, b_chess, r_chess = self.img_load()
        while True:
            time.sleep(0.001)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.click1 is None:
                            self.click1 = event.pos
                            if len(click_coord):
                                self.window.blit(bg[3], click_coord[-1])
                            if len(FEASIBLE_COORD):
                                FEASIBLE_COORD.clear()
                            for n, old_coord, new_coord in zip(CHESS_NAME, INIT_COORD, INIT_RANGER):
                                old_x = old_coord[0]
                                old_y = old_coord[1]
                                new_x = new_coord[0]
                                new_y = new_coord[1]
                                click1_x = event.pos[0]
                                click1_y = event.pos[1]
                                if old_x <= click1_x <= new_x and old_y <= click1_y <= new_y:
                                    name = n
                                    click_coord.append(old_coord)
                                    self.window.blit(bg[2], old_coord)
                                    self.update()
                            ALL_COORD = INIT_COORD + UNPLACED_COORD
                            for coord in ALL_COORD:
                                self.show_dot(name, click_coord[-1], coord)
                            """for dot_coord in FEASIBLE_COORD:
                                dot_x = dot_coord[0] + CHESS_INTERVAL1
                                dot_y = dot_coord[1] + CHESS_INTERVAL1
                                point_x = (dot_coord[0] + dot_x) / 2 - 7
                                point_y = (dot_coord[1] + dot_y) / 2 - 7
                                midpoint.append((point_x, point_y))
                            for point in midpoint:
                                init_x = point[0] - 5
                                init_y = point[1] - 5
                                print(init_x, init_y)
                                self.window.blit(self.dot, (init_x, init_y))
                                self.update()"""
                                
                        else:
                            self.click2 = event.pos
                            self.click_1(self.click1, self.click2)
                            print("当前 red:{},black:{}".format(self.red, self.black))
                            self.click1 = None
                            self.click2 = None

            if not pygame.mixer.music.get_busy():
                self.index += 1
                self.play_music()

    @staticmethod
    def update():
        pygame.display.update()

    def play_music(self):
        """播放音频"""

        def play1():
            pygame.mixer.music.load("./musics/bgm1.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()

        def play2():
            pygame.mixer.music.load("./musics/bgm2.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()

        def play3():
            pygame.mixer.music.load("./musics/bgm3.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()

        def play4():
            pygame.mixer.music.load("./musics/bgm4.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()

        def play5():
            pygame.mixer.music.load("./musics/bgm5.flac")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play()

        if self.index == 1:
            play1()
        elif self.index == 2:
            play2()
        elif self.index == 3:
            play3()
        elif self.index == 4:
            play4()
        elif self.index == 5:
            play5()
        else:
            self.index = 0


if __name__ == "__main__":
    game = Game()
    game.img_place()
    game.update()
    game.event()
