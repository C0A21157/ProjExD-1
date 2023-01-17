import sys
import random,time,math
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
        self.sfc=pg.Surface((1600,900)) 
        self.sfc.set_colorkey((0,0,0))
        color=["white", "blue"] #迷路の色
        for y in range(len(maze_lst)): 
            for x in range(len(maze_lst[y])):
                pg.draw.rect(self.sfc,color[maze_lst[y][x]],(x*50,y*50,50,50)) #迷路の一マスの大きさと間隔
        self.rct=self.sfc.get_rect()

    def blit(self,scr:Screen):
        scr.sfc.blit(self.sfc,self.rct)

def check_bound(obj_rct, scr_rct): # 敵の運動方向の変化(楊)
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

        clock = pg.time.Clock()
        scr = Screen("食べろにょろにょろ", (1600,900), "fig/pg_bg.jpg")

        maze_lst=mm.make_maze(18,18) #マスの数
        print (maze_lst)
        maze=Maze(maze_lst,scr)

        

        color_red = pg.Color(255, 0, 0)
        color_green = pg.Color(0, 255, 0)
        color_yello = pg.Color(255, 212, 0)
        screen = pg.display.set_mode((900, 900)) #スクリーンの大きさ
        pg.display.set_caption("蛇")
        arr = [([0] * 91) for i in range(91)]  
        x = 5  # 蛇の初期x座標
        y = 5 # 蛇の初期y座標
        mx, my = 50/x, 50/y
        foodx = random.randint(1, 90)  # 食べ物のx座標
        foody = random.randint(1, 90)  # 食べ物のy座標
        arr[foodx][foody] = -1
        snake_lon = 3  # 蛇の長さ
        way = 1  # 蛇の運動方向

        life = 3 # ライフの数
        pg.mixer.music.load("優雅なお猫様.mp3")  # BGMのロード
        pg.mixer.music.play(100)  # BGMを100回再生
        get = pg.mixer.Sound("レトロアクション.mp3")  # 餌ゲット時のSEのロード
        end = pg.mixer.Sound("しょげる.mp3")  # 終了時のSEのロード
        fonto = pg.font.Font(None,80)
        fonto2 = pg.font.Font(None,30)
        appnum = 3 #りんごゲットのノルマ(坂本)
        app = fonto2.render((f"APPLE:{appnum}"),True,(0,0,0)) #残りのりんごの獲得ノルマ表示(坂本)
        clear = fonto.render("Game Clear",True,(0,250,0))#ゲームクリアの表示(坂本)
        gover = fonto.render("Game Over",True,(255,0,0))#ゲームオーバーの表示(坂本)
        game = True #ゲームが続いているかのフラグ(坂本)

        # 敵の座標設定(楊)
        tekix = random.randint(1, 90) 
        tekiy = random.randint(1, 90)  
        arr[tekix][tekiy] = -2 

        # (楊)敵を描く
        teki_sfc = pg.Surface((10, 10)) # 正方形の空のSurface
        pg.draw.rect(teki_sfc, color_yello, (0, 0, 10, 10))
        teki_rct = teki_sfc.get_rect()
        teki_rct.centerx = tekix*10
        teki_rct.centery = tekiy*10

        xy = [+3,-3, 0]        #(楊)敵の移動と方向    
        vx = random.choice(xy)
        vy = random.choice(xy)


        st = time.time()

        spd = 1 # 蛇の移動速度(筒井)
        t = 0.1 # 蛇の移動速度変更用の変数(筒井)

        while True:
            if game:
                scr.blit()
                maze.blit(scr)

                ed = time.time()
                gt = ed-st

                screen.blit(app,(50,50))#スクリーンに表示(坂本)
                #screen.fill(color_white)
                time.sleep(0.1)
                for i in range(life):  #life表示
                    H_sfc = pg.image.load("Hart.png")
                    H_sfc = pg.transform.rotozoom(H_sfc, 0, 0.15)
                    H_rct = H_sfc.get_rect()
                    H_rct.center = i*50+30, 30

                    # scrn_sfcにtori_rctに従って，tori_sfcを貼り付ける
                    screen.blit(H_sfc, H_rct)
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
                if (x > 90) or (y > 90) or (x < 1) or (y < 1) or (arr[x][y] > 0):  # 死亡(壁、自分の体をぶつかったら)
                    end.play()  # 終了時のSE
                    time.sleep(1)  # 1秒停止
                    screen.blit(gover,(300,400))#ゲームオーバーの表示(坂本)
                    pg.display.update()
                    game= False   #ゲームオーバーのフラグ(坂本)
                arr[x][y] = snake_lon
                for a, b in enumerate(arr, 1):
                    for c, d in enumerate(b, 1):
                        # 食べ物は-1，空地は0，蛇の位置は正数
                        if (d > 0):
                            # print(a,c) #蛇の座標を表示
                            arr[a - 1][c - 1] = arr[a - 1][c - 1] - 1
                            pg.draw.rect(screen, color_green, ((a - 1) * 10, (c - 1) * 10, 10, 10))
                        if (d == -1):
                            pg.draw.rect(screen, color_red, ((a - 1) * 10, (c - 1) * 10, 10, 10))
                        if (d == -2): #(楊)敵の移動
                            teki_rct.move_ip(vx, vy)

                            yoko,tate = check_bound(teki_rct, scr.rct)
                            vx *= yoko
                            vy *= tate
                            scr.sfc.blit(teki_sfc, teki_rct)
                            xf,xi = math.modf(teki_rct.centerx/10)
                            yf,yi = math.modf(teki_rct.centery/10)
                            if (x == xi) and (y == yi):  
                                life -= 1
                            


                    

                if (x == foodx) and (y == foody):   #蛇が食べ物を食べったら
                    get.play()  # 餌ゲット時のSE 
                    snake_lon += 1    #長さ+1
                    appnum -= 1
                    app = fonto2.render((f"APPLE:{appnum}"),True,(0,0,0))
                    
                    while (arr[foodx][foody] != 0):    #新しい食べ物を表示
                        foodx = random.randint(1, 90)
                        foody = random.randint(1, 90)
                    arr[foodx][foody] = -1

                    
                    pg.display.update()
                    if appnum < 1:                   #りんごのノルマを達成していたら(坂本)
                        screen.blit(clear,(300,400)) #クリア表示(坂本)
                        pg.display.update()
                        game = False #ゲームオーバーのフラグ(坂本) 
                if life == 0:
                    end.play()  # 終了時のSE
                    time.sleep(1)  # 1秒停止
                    screen.blit(gover,(300,400))#ゲームオーバーの表示(坂本)
                    pg.display.update()
                    game= False   #ゲームオーバーのフラグ(坂本)
                if round(gt%5) == 0: #五秒ごと経つと敵動く方向が変わる
                    vx = random.choice(xy)
                    vy = random.choice(xy)
                    teki_rct.move_ip(vx, vy)
                    scr.sfc.blit(teki_sfc, teki_rct)   
            else:
                for event in pg.event.get():  
                    if event.type == pg.QUIT:
                        sys.exit()

            pg.display.update()
            clock.tick(1000)

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