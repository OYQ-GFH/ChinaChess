import os
import random


WINDOW_SIZE = (756, 560)
WINDOW_TITLE = "中国象棋"
CHESS_NAME = []
INIT_COORD = []
UNPLACED_COORD = []
INIT_RANGER = []
UNPLACED_RANGER = []
MIDPOINT = []
MIN_COORD = []
MAX_COORD = []
CHESS_X = 128
CHESS_Y = 2
CHESS_INTERVAL1 = 56
CHESS_STATE = {}
NAME = []
FEASIBLE_COORD = []
CHESS_INIT = {}


def random_num():
    """计算7个随机数"""

    musics = os.listdir("./musics")
    all_bgm = []
    num_list = []

    for music in musics:
        if "bgm" in music:
            all_bgm.append(music)

    index = len(all_bgm)
    for i in range(1, 10000):
        num = random.randint(0, index - 1)
        if num not in num_list:
            num_list.append(num)
        if len(num_list) == index:
            return all_bgm, num_list, index
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


if __name__ == "__main__":
    pass
