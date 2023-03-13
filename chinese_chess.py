# 
#           _.._        ,------------.
#        ,'      `.    ( We want you! )
#       /  __) __` \    `-,----------'
#      (  (`-`(-')  ) _.-'
#      /)  \  = /  (
#     /'    |--' .  \
#    (  ,---|  `-.)__`
#     )(  `-.,--'   _`-.
#    '/,'          (  Uu",
#      (_       ,    `/,-' )
#       `.__,  : `-'/  /`--'
#        |     `--'  |
#        `   `-._   /
#         \        (
#         /\ .      \.
#        / |` \     ,-\
#       /  \| .)   /   \
#      ( ,'|\    ,'     :
#      | \,`.`--"/      }
#      `,'    \  |,'    /
#     / "-._   `-/      |
#     "-.   "-.,'|     ;
#    /        _/["---'""]
#   :        /  |"-     '
#   '           |      /
#               `      |
#
# author: OYQ
# write_date: 2023.2.28
#

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

    def __init__(self):
        """初始化"""

        pygame.init()
        pygame.mixer.init()
        # 初始化音效
        self.move = pygame.mixer.Sound("musics/move.WAV")
        self.eat = pygame.mixer.Sound("./musics/eat.WAV")
        self.move.set_volume(1)
        self.eat.set_volume(1)
        pygame.mixer.music.load("./musics/start.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()
        # 初始化窗口
        pygame.display.set_caption(WINDOW_TITLE)
        self.window = pygame.display.set_mode(WINDOW_SIZE)
        # 初始化图片素材
        self.ico1 = pygame.image.load("./images/ico1.png")
        self.ico2 = pygame.image.load("./images/b_j.png")
        self.r_box = pygame.image.load("images/r_box.png")
        self.b_box = pygame.image.load("images/b_box.png")
        self.dot = pygame.image.load("./images/dot.png")
        self.bg1 = pygame.image.load("images/bg1.png")
        self.bg2 = pygame.image.load("images/bg3.png")
        self.b_z = pygame.image.load("images/b_z.png")
        self.b_p = pygame.image.load("images/b_p.png")
        self.b_c = pygame.image.load("images/b_c.png")
        self.b_m = pygame.image.load("images/b_m.png")
        self.b_x = pygame.image.load("images/b_x.png")
        self.b_s = pygame.image.load("images/b_s.png")
        self.b_j = pygame.image.load("images/b_j.png")
        self.r_z = pygame.image.load("images/r_z.png")
        self.r_p = pygame.image.load("images/r_p.png")
        self.r_c = pygame.image.load("images/r_c.png")
        self.r_m = pygame.image.load("images/r_m.png")
        self.r_x = pygame.image.load("images/r_x.png")
        self.r_s = pygame.image.load("images/r_s.png")
        self.r_j = pygame.image.load("images/r_j.png")
        self.bg = self.bg1, self.bg2
        self.b_chess = self.b_z, self.b_p, self.b_c, self.b_m, self.b_x, self.b_s, self.b_j
        self.r_chess = self.r_z, self.r_p, self.r_c, self.r_m, self.r_x, self.r_s, self.r_j
        self.chess_name = {
            "黑卒": self.b_chess[0], "黑炮": self.b_chess[1],
            "黑车": self.b_chess[2], "黑马": self.b_chess[3],
            "黑象": self.b_chess[4], "黑士": self.b_chess[5],
            "黑将": self.b_chess[6], "红卒": self.r_chess[0],
            "红炮": self.r_chess[1], "红车": self.r_chess[2],
            "红马": self.r_chess[3], "红象": self.r_chess[4],
            "红士": self.r_chess[5], "红将": self.r_chess[6]}

    def img_place(self):
        """放置棋盘和棋子"""

        count_init_coord()
        self.window.blit(self.bg[1], (0, 0))
        self.window.blit(self.bg[0], (128, 0))
        self.window.blit(self.b_chess[2], INIT_COORD[0])
        self.window.blit(self.b_chess[3], INIT_COORD[1])
        self.window.blit(self.b_chess[4], INIT_COORD[2])
        self.window.blit(self.b_chess[5], INIT_COORD[3])
        self.window.blit(self.b_chess[6], INIT_COORD[4])
        self.window.blit(self.b_chess[5], INIT_COORD[5])
        self.window.blit(self.b_chess[4], INIT_COORD[6])
        self.window.blit(self.b_chess[3], INIT_COORD[7])
        self.window.blit(self.b_chess[2], INIT_COORD[8])
        self.window.blit(self.b_chess[1], INIT_COORD[9])
        self.window.blit(self.b_chess[1], INIT_COORD[10])
        self.window.blit(self.b_chess[0], INIT_COORD[11])
        self.window.blit(self.b_chess[0], INIT_COORD[12])
        self.window.blit(self.b_chess[0], INIT_COORD[13])
        self.window.blit(self.b_chess[0], INIT_COORD[14])
        self.window.blit(self.b_chess[0], INIT_COORD[15])
        self.window.blit(self.r_chess[2], INIT_COORD[16])
        self.window.blit(self.r_chess[3], INIT_COORD[17])
        self.window.blit(self.r_chess[4], INIT_COORD[18])
        self.window.blit(self.r_chess[5], INIT_COORD[19])
        self.window.blit(self.r_chess[6], INIT_COORD[20])
        self.window.blit(self.r_chess[5], INIT_COORD[21])
        self.window.blit(self.r_chess[4], INIT_COORD[22])
        self.window.blit(self.r_chess[3], INIT_COORD[23])
        self.window.blit(self.r_chess[2], INIT_COORD[24])
        self.window.blit(self.r_chess[1], INIT_COORD[25])
        self.window.blit(self.r_chess[1], INIT_COORD[26])
        self.window.blit(self.r_chess[0], INIT_COORD[27])
        self.window.blit(self.r_chess[0], INIT_COORD[28])
        self.window.blit(self.r_chess[0], INIT_COORD[29])
        self.window.blit(self.r_chess[0], INIT_COORD[30])
        self.window.blit(self.r_chess[0], INIT_COORD[31])

    def no_go(self):
        if self.red:
            pygame.display.set_icon(self.ico2)
            self.black = True
            self.red = False
        elif self.black:
            pygame.display.set_icon(self.ico1)
            self.black = False
            self.red = True

    @staticmethod
    def logic(f_coord):
        """棋子走棋逻辑判断"""
        if f_coord in FEASIBLE_COORD:
            return True
        return False

    @staticmethod
    def play_music(music):
        """播放音频"""
        pygame.mixer.music.load("./musics/{}".format(music))
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play()

    @staticmethod
    def update():
        pygame.display.update()

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

    def operate(self, flag, coord, old_coord, new_coord, un1_coord, un2_coord, eat, name1, name2):
        """棋子操作"""

        def blit(n):
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
                # print("事件: {}吃掉了{}".format(name1, name2))
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
        def boss():
            if "士"in name1:
                    if d_coord[0] == all_coord[0] - CHESS_INTERVAL1 and d_coord[1] == all_coord[1] - CHESS_INTERVAL1:
                         FEASIBLE_COORD.append(all_coord)
                    elif d_coord[0] == all_coord[0] + CHESS_INTERVAL1 and d_coord[1] == all_coord[1] - CHESS_INTERVAL1:
                        FEASIBLE_COORD.append(all_coord)
                    elif d_coord[0] == all_coord[0]  - CHESS_INTERVAL1 and d_coord[1] == all_coord[1] + CHESS_INTERVAL1:
                        FEASIBLE_COORD.append(all_coord)
                    elif d_coord[0] == all_coord[0]  + CHESS_INTERVAL1 and d_coord[1] == all_coord[1] + CHESS_INTERVAL1:
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
                        
        if "卒" in name1 and all_coord[1] <= d_coord[1]:
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
            self.no_go_coord["up_right"]= d_coord[0] + CHESS_INTERVAL1, d_coord[1] + CHESS_INTERVAL1
            self.no_go_coord["down_left"] = d_coord[0] - CHESS_INTERVAL1, d_coord[1] - CHESS_INTERVAL1
            self.no_go_coord["down_right"] = d_coord[0] + CHESS_INTERVAL1 , d_coord[1] - CHESS_INTERVAL1

        elif "士" in name1 or "将"in name1:
            if "红" in name1:
                if CHESS_INTERVAL1 * 3 + CHESS_X <= all_coord[0] <= CHESS_INTERVAL1 * 5 + CHESS_X and CHESS_INTERVAL1 * 7 + CHESS_Y <= all_coord[1] <= CHESS_INTERVAL1 * 9 + CHESS_Y:
                    boss()
            elif "黑" in name1:
                if CHESS_INTERVAL1 * 3 + CHESS_X <= all_coord[0] <= CHESS_INTERVAL1 * 5 + CHESS_X and CHESS_Y <= all_coord[1] <= CHESS_INTERVAL1 * 2 + CHESS_Y:
                    boss()
 
    def event(self):
        """事件判断"""

        name = None
        while True:
            time.sleep(0.001)

            if not pygame.mixer.music.get_busy():
                all_music, num_list, index = random_num()
                music = all_music[num_list[self.index]]
                if self.index <= index:
                    self.play_music(music)
                else:
                    self.index = 0
                    self.play_music(music)
                self.index += 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        sys.exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
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
                                                    FEASIBLE_COORD.append(value2)
                                elif "象" in self.name:
                                    for key3, value3 in self.no_go_coord.items():
                                        for key4, value4 in self.m_chess_coord.items():
                                            if value3 not in INIT_COORD and value3 in UNPLACED_COORD:
                                                if key3 == key4:
                                                     FEASIBLE_COORD.append(value4)
                                if not self.go:
                                    for key, value in CHESS_INIT.items():
                                        if value in FEASIBLE_COORD:
                                            if self.name[0] == key[0]:
                                                print(self.name)
                                                FEASIBLE_COORD.remove(value)
                                elif self.go:
                                    for key, value in CHESS_STATE.items():
                                        if value in FEASIBLE_COORD:
                                            if self.name[0] == key[0]:
                                                print(self.name)
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


if __name__ == "__main__":
    game = Game()
    game.img_place()
    game.update()
    game.event()
