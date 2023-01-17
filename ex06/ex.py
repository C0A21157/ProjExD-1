
import sys
import random,time,math
import pygame as pg
import maze_maker as mm


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

def check_bound(obj_rct, scr_rct):
    # 第1引数；敵rect
    # 第2引数：スクリーンrect
    # 範囲内：+1/範囲外：-1
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

def main2():
    clock = pg.time.Clock()
    scr = Screen("食べろにょろにょろ", (1600,900), "fig/pg_bg.jpg")

    make_lst=mm.make_maze(18,18) #マスの数
    print (make_lst)
    maze=Maze(make_lst,scr)

    color_red = pg.Color(255, 0, 0)
    color_green = pg.Color(0, 255, 0)
    color_yello = pg.Color(255, 212, 0)
    screen = pg.display.set_mode((900, 1000)) #スクリーンの大きさ
    pg.display.set_caption("蛇")
    arr = [([0] * 91) for i in range(101)]  
    x = 10  # 蛇の初期x座標
    y = 10  # 蛇の初期y座標
    foodx = random.randint(1, 90)  # 食べ物のx座標
    foody = random.randint(1, 100)  # 食べ物のy座標
    arr[foodx][foody] = -1
    snake_lon = 3  # 蛇の長さ
    way = 1  # 蛇の運動方向

    tekix = random.randint(1, 90)  # 敵のx座標
    tekiy = random.randint(1, 100)  # 敵のy座標
    arr[tekix][tekiy] = -2

    teki_sfc = pg.Surface((10, 10)) # 正方形の空のSurface
    pg.draw.rect(teki_sfc, color_yello, (0, 0, 10, 10))
    teki_rct = teki_sfc.get_rect()
    teki_rct.centerx = tekix*10
    teki_rct.centery = tekiy*10

    xy = [+3,-3, 0]        #敵の移動と方向    
    vx = random.choice(xy)
    vy = random.choice(xy)

    font = pg.font.Font(None, 30) #スコアの文字列
    scor = 0 #スコアの初期値

    st = time.time()

    spd = 1 # 蛇の移動速度(筒井)
    t = 0.1 # 蛇の移動速度変更用の変数(筒井)

    while True:
        scr.blit()
        maze.blit(scr)

        text = font.render(f"Score {scor}", True, (0,0,0))   # 描画する文字列の設定
        scr.sfc.blit(text, [20, 1])# 文字列の表示位置
        ed = time.time()
        gt = ed-st
        
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
            x += spd # 1をspdに変更(筒井)
        if way == 2:
            x -= spd
        if way == 3:
            y -= spd
        if way == 4:
            y += spd
        if (x > 90) or (y > 100) or (x < 1) or (y < 1) or (arr[x][y] > 0):  # 死亡(壁、自分の体をぶつかったら)
            font1 = pg.font.Font(None, 100) 
            text1 = font1.render("Game Over!", True, color_red)
            text2 = font1.render(f"Score {scor}", True, color_red)   # 描画する文字列の設定
            scr.sfc.blit(text1, [100, 100])# 文字列の表示位置
            scr.sfc.blit(text2, [150, 200])
            return
        arr[x][y] = snake_lon
        for a, b in enumerate(arr, 1):
            for c, d in enumerate(b, 1):
                # 食べ物は-1，空地は0，蛇の位置は正数
                if (d > 0):
                    # print(a,c) #蛇の座標を表示
                    arr[a - 1][c - 1] = arr[a - 1][c - 1] - 1
                    pg.draw.rect(screen, color_green, ((a - 1) * 10, (c - 1) * 10, 10, 10))
                if (d == -1):
                    pg.draw.rect(scr.sfc, color_red, ((a - 1) * 10, (c - 1) * 10, 10, 10))
                if (d == -2):
                    teki_rct.move_ip(vx, vy)
                    
                    yoko,tate = check_bound(teki_rct, scr.rct)
                    vx *= yoko
                    vy *= tate
                    scr.sfc.blit(teki_sfc, teki_rct)
                    xf,xi = math.modf(teki_rct.centerx/10)
                    yf,yi = math.modf(teki_rct.centery/10)

        if (x == xi) and (y == yi): #敵をぶつかったら、ゲームオーバー
            teki_rct.move_ip(vx, vy)
                
            yoko,tate = check_bound(teki_rct, scr.rct)
            vx = 0
            vy = 0
            scr.sfc.blit(teki_sfc, teki_rct)
            font1 = pg.font.Font(None, 100) 
            text1 = font1.render("Game Over!", True, color_red)
            text2 = font1.render(f"Score {scor}", True, color_red)   # 描画する文字列の設定
            scr.sfc.blit(text1, [100, 100])# 文字列の表示位置
            scr.sfc.blit(text2, [150, 200])
            return

        else:
            if (x == foodx) and (y == foody):   #蛇が食べ物を食べったら
                snake_lon += 1    #長さ+1
                t -= t/4 # 蛇が現在の速度の1/4加速(筒井)
                while (arr[foodx][foody] != 0):    #新しい食べ物を表示
                    foodx = random.randint(1, 90)
                    foody = random.randint(1, 100)
                arr[foodx][foody] = -1
                scor += 1 #スコアが+1
            if round(gt%5) == 0: #五秒ごと経つと敵動く方向が変わる
                vx = random.choice(xy)
                vy = random.choice(xy)
                teki_rct.move_ip(vx, vy)
                scr.sfc.blit(teki_sfc, teki_rct)   
                if (d < 0):
                    pg.draw.rect(screen, color_red, ((a - 1) * 10, (c - 1) * 10, 10, 10))  
    

        pg.display.update()
        clock.tick(1000)

if __name__ == '__main__':
    pg.init()
    main2()
    pg.quit()
    sys.exit()   

