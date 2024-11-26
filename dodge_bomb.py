import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数で与えられたRectが画面の中か外かを判定する
    引数：こうかとんRect or 爆弾Rect
    戻り値：真理値タプル（横，縦）／画面内：True，画面外：False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def create_koukaton_images(base_img):
    """
    方向に応じたこうかとんの画像辞書を作成する。
    引数:
        base_img: こうかとんの元画像
    戻り値:
        辞書: {移動量タプル: Surface}
    """
    directions = {
        (0, -5): pg.transform.rotozoom(base_img, 0, 1.0),   # 上
        (0, +5): pg.transform.rotozoom(base_img, 180, 1.0), # 下
        (-5, 0): pg.transform.rotozoom(base_img, 90, 1.0),  # 左
        (+5, 0): pg.transform.rotozoom(base_img, -90, 1.0), # 右
        (-5, -5): pg.transform.rotozoom(base_img, 45, 1.0), # 左上
        (-5, +5): pg.transform.rotozoom(base_img, 135, 1.0),# 左下
        (+5, -5): pg.transform.rotozoom(base_img, -45, 1.0),# 右上
        (+5, +5): pg.transform.rotozoom(base_img, -135, 1.0)# 右下
    }
    return directions


def create_bombs():
    """
    爆弾の加速リストとサイズリストを作成し、タプルで返す専用の関数。
    """
    accs = [kasoku for kasoku in range(1, 11)]  # 加速リスト
    print(accs)
    bb_imgs = []  # サイズリスト
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r), pg.SRCALPHA)  # Surfaceの透明化
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 爆弾円を描く
        bb_imgs.append(bb_img)
    return accs, bb_imgs



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    #関数に読み込むため、書き方を修正コメントアウト
    # kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    # kk_rct = kk_img.get_rect()
    # kk_rct.center = 300, 200
    kk_img = pg.image.load("fig/3.png")
    # 爆弾リスト生成
    accs, bb_imgs = create_bombs()
    bb_rct = bb_imgs[0].get_rect()
    # 方向画像辞書
    koukaton_imgs = create_koukaton_images(kk_img)
    # 初期位置の設定（デフォルト設定）
    kk_img = koukaton_imgs[(0, -5)]  # 初期は上向き
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    #もともとのやり方(関数で利用してコメントアウト)
    # bb_img = pg.Surface((20, 20))  # 爆弾用の空Surface
    # pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 爆弾円を描く
    # bb_img.set_colorkey((0, 0, 0))  # 四隅の黒を透過させる
    # bb_rct = bb_img.get_rect()  # 爆弾Rectの抽出
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5, +5  # 爆弾速度ベクトル
    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")

            # 背景を暗くする
            gameover_background = pg.Surface((WIDTH, HEIGHT))
            gameover_background.set_alpha(128)  # 半透明
            gameover_background.fill((0, 0, 0))  # 黒色
            screen.blit(gameover_background, (0, 0))

            # ゲームオーバー時の画像描画
            kk_gameover_img_left = pg.image.load("fig/8.png")
            kk_gameover_rct_lft = kk_gameover_img_left.get_rect(center=(WIDTH // 2 -200 , HEIGHT // 2 -50))  # 中央に配置
            screen.blit(kk_gameover_img_left, kk_gameover_rct_lft.topleft)

            # "Game Over" テキストの描画
            fonto = pg.font.Font(None, 80)
            txt = fonto.render("Game Over", True, (255, 255, 255))
            text_rect = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))  # テキストを中央に配置
            screen.blit(txt, text_rect.topleft)

            # ゲームオーバー時の画像描画
            kk_gameover_img = pg.image.load("fig/8.png")
            kk_gameover_rct = kk_gameover_img.get_rect(center=(WIDTH // 2 +200 , HEIGHT // 2-50 ))  # 中央に配置
            screen.blit(kk_gameover_img, kk_gameover_rct.topleft)

            pg.display.update()
            time.sleep(5)  # 5秒間表示
            return  # ゲームオーバー終了
        screen.blit(bg_img, [0, 0]) 
        
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key] == True:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]

        if sum_mv != [0, 0]:  # こうかとんが動いている場合のみ向きを変更
            kk_img = koukaton_imgs.get(tuple(sum_mv), kk_img)  # 移動量に対応する画像を取得
        kk_rct.move_ip(sum_mv)
        # こうかとんが画面外なら，元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        # ここで爆弾の設定
        # 爆弾の拡大・加速
        # avx = vx * accs[min(tmr // 500, 9)]tmrの値に応じて，リストから適切な要素を選択
        idx = min(tmr // 500, 9)  # 最大値はリストの長さ - 1
        bb_img = bb_imgs[idx]
        avx = vx * accs[idx]
        avy = vy * accs[idx]
        #speed changed check
        # print(avx,avy)
        # 爆弾移動
        bb_rct.move_ip(avx, avy)

        # bb_rct.move_ip(vx, vy)  # 爆弾動く
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 横にはみ出てる
            vx *= -1
        if not tate:  # 縦にはみ出てる
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()