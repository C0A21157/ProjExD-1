
import sys
import random,time
import pygame as pg
import maze_maker as mm
import tkinter

scene = 0
font1 =("Century",30) #初期画面で使用する文字フォント
font2 =("Century",20)
font3 =("Century",15)

key=""
def key(e):
    global key
    key=e.keysym
""""
WALL_COLOR = (87, 45, 24) #迷路　棒倒し法
FLOOR_COLOR = (181, 152, 132)

# 床1枚の幅と高さ
FLOOR_W = 60
FLOOR_H = 60
# 迷路の幅と高さ（床の枚数）
MAZE_W = 20
MAZE_H = 15
# リストの宣言と初期化
maze = []
for y in range(MAZE_H):
    maze.append([0] * MAZE_W)

# 迷路の設計情報を自動生成する
def make_maze():
    # 柱から伸ばす壁のに利用する値を定義
    # [上, 右, 下, 左]
    XP = [0, 1, 0, -1]
    YP = [-1, 0, 1, 0]

    # 迷路を囲う壁を作る
    for x in range(MAZE_W):
        maze[0][x] = 1
        maze[MAZE_H - 1][x] = 1
    for y in range(1, MAZE_H - 1):
        maze[y][0] = 1
        maze[y][MAZE_W - 1] = 1
    
    # 中を何もない状態にする
    for y in range(1, MAZE_H - 1):
        for x in range(1, MAZE_W - 1):
            maze[y][x] = 0
    
    # 柱を作る
    for y in range(2, MAZE_H - 2, 2):           # range()は第三引数を2を指定し、ステップ機能で1マス飛ばししている
        for x in range(2, MAZE_W - 2, 2):
            maze[y][x] = 1
    
    # 各柱から壁を伸ばす
    for y in range(2, MAZE_H - 2, 2):
        for x in range(2, MAZE_W - 2, 2):
            while True:
                d = random.randint(0, 3)            # 変数dに柱から伸ばす方向を0~3で指定
                if x > 2:                           # 2列目以降なら0~2（左を示す3を含めない）で左に伸ばさない
                    d = random.randint(0, 2)
                
                if maze[y + YP[d]][x + XP[d]] == 1: # dの値が既に壁が作られた場所であればやり直し
                    continue

                # 柱から伸ばす壁を示す値（変数d）を、定数YP、XPの添字に使い壁を伸ばすマス目を指定
                # そのマス目を表すmaze[]に壁有りを示す1を代入
                maze[y + YP[d]][x + XP[d]] = 1
                break

def main():
    pygame.init()
    pygame.display.set_caption("いもむしマン")
    screen = pygame.display.set_mode((FLOOR_W * MAZE_W, FLOOR_H * MAZE_H))
    clock = pygame.time.Clock()

    make_maze()


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    make_maze()
        
        # 自動生成した迷路の設計情報を使い実際に描画する
        for y in range(MAZE_H):
            for x in range(MAZE_W):
                W = FLOOR_W
                H = FLOOR_H
                X = x * W
                Y = y * H
                # 通路を描画
                if maze[y][x] == 0:
                    pygame.draw.rect(screen, FLOOR_COLOR, [X, Y, W, H])
                # 壁を描画
                if maze[y][x] == 1:
                    pygame.draw.rect(screen, WALL_COLOR, [X, Y, W, H])
        
        pygame.display.update()
        clock.tick(2)
"""

class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title) 
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect() 

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 

class Maze:
    def __init__(self,maze_lst,scr:Screen):
        self.sfc=pg.Surface((1200,900)) 
        self.sfc.set_colorkey((0,0,0))
        color=["white", "blue"] #迷路の色
        for y in range(len(maze_lst)): 
            for x in range(len(maze_lst[y])):
                pg.draw.rect(self.sfc,color[maze_lst[y][x]],(x*50,y*50,50,50)) #迷路の一マスの大きさと間隔
        self.rct=self.sfc.get_rect()

    def blit(self,scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)
                
def main2():
    global scene, jid

    if scene == 0:#初期画面
            canvas.create_text(300,100,text="食べろにょろにょろ",fill="black",font=font1,tag="スタート画面")#タイトル
            canvas.create_text(300,200,text="[操作説明]",fill="black",font=font2,tag="スタート画面")#操作説明
            canvas.create_text(300,250,text="・十字キーで操作してね",fill="black",font=font3,tag="スタート画面")
            canvas.create_text(300,270,text="・アイテムのリンゴを食べたら加速するよ",fill="black",font=font3,tag="スタート画面")
            canvas.create_text(300,290,text="・黄色い■は敵！あたったらライフが減るよ",fill="black",font=font3,tag="スタート画面")
            canvas.create_text(300,310,text="・リンゴを５個あつめたらclear！",fill="black",font=font3,tag="スタート画面")    
            canvas.create_text(300,380,text="スペースキーでスタート",fill="lime",font=font2,tag="スタート画面")
            
            if key == "space": #スペースがおされたらゲーム開始
                #print(0)
                root.after_cancel(jid)#スタート画面削除
                scene = 1
                root.destroy()
            else:
                jid = root.after(100,main2)
        
    if scene ==1:
        scr = Screen("食べろにょろにょろ", (1600,900), "fig/pg_bg.jpg")

        make_lst=mm.make_maze(18,18) #マスの数
        print (make_lst)
        maze=Maze(make_lst,scr)

        color_red = pg.Color(255, 0, 0)
        color_green = pg.Color(0, 255, 0)
        screen = pg.display.set_mode((900, 1000)) #スクリーンの大きさ
        pg.display.set_caption("蛇")
        arr = [([0] * 41) for i in range(61)]  
        x = 10  # 蛇の初期x座標
        y = 10  # 蛇の初期y座標
        foodx = random.randint(1, 60)  # 食べ物のx座標
        foody = random.randint(1, 40)  # 食べ物のy座標
        arr[foodx][foody] = -1
        snake_lon = 3  # 蛇の長さ
        way = 1  # 蛇の運動方向

        while True:
            scr.blit()
            maze.blit(scr)
            
            #screen.fill(color_white)
            time.sleep(0.1)
            for event in pg.event.get():  # 监听器
                if event.type == pg.QUIT:
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if (event.key == pg.K_RIGHT) and (way != 2):  # 右
                        way = 1
                    if (event.key == pg.K_LEFT) and (way != 1):  # 左
                        way = 2
                    if (event.key == pg.K_UP) and (way != 4):  # 上
                        way = 3
                    if (event.key == pg.K_DOWN) and (way != 3):  # 下に移動
                        way = 4
            if way == 1:
                x += 1
            if way == 2:
                x -= 1
            if way == 3:
                y -= 1
            if way == 4:
                y += 1
            if (x > 60) or (y > 40) or (x < 1) or (y < 1) or (arr[x][y] > 0):  # 死亡(壁、自分の体をぶつかったら)
                sys.exit()
            arr[x][y] = snake_lon
            for a, b in enumerate(arr, 1):
                for c, d in enumerate(b, 1):
                    # 食べ物は-1，空地は0，蛇の位置は正数
                    if (d > 0):
                        # print(a,c) #蛇の座標を表示
                        arr[a - 1][c - 1] = arr[a - 1][c - 1] - 1
                        pg.draw.rect(screen, color_green, ((a - 1) * 10, (c - 1) * 10, 10, 10))
                    if (d < 0):
                        pg.draw.rect(screen, color_red, ((a - 1) * 10, (c - 1) * 10, 10, 10))
            if (x == foodx) and (y == foody):   #蛇が食べ物を食べったら
                snake_lon += 1    #長さ+1
                while (arr[foodx][foody] != 0):    #新しい食べ物を表示
                    foodx = random.randint(1, 60)
                    foody = random.randint(1, 40)
                arr[foodx][foody] = -1

            pg.display.update()


if __name__ == '__main__':
    pg.init()
    root = tkinter.Tk()
    root.title("スタート") #初期画面タイトル
    root.bind("<KeyPress>", key)
    canvas = tkinter.Canvas(width=600, height=400, bg="white") #初期画面の画面サイズ設定
    canvas.pack()
    main2()
    root.mainloop()
    pg.quit()
    sys.exit()
    