"""Pixel-art sprites for the journey progress bar.

Every sprite is drawn in code at its native (tiny) size so it stays crisp when
scaled up with nearest-neighbour. `build_all()` returns {name: RGBA Image}.
Run `python3 sprites.py OUTDIR [--scale N ...]` to export PNG files.
"""
from PIL import Image, ImageDraw
import os, sys

OUT = (28, 18, 40, 255)
C = {
 'K': OUT,
 'S': (246, 200, 158, 255), 's': (206, 144, 108, 255),
 'H': (128, 74, 38, 255), 'h': (170, 108, 56, 255),
 'T': (64, 118, 196, 255), 't': (40, 78, 140, 255),      # tunic
 'B': (96, 58, 32, 255), 'G': (250, 200, 80, 255), 'g': (190, 130, 40, 255),
 'N': (62, 56, 84, 255), 'n': (44, 40, 62, 255),         # pants
 'O': (120, 74, 42, 255), 'o': (84, 50, 28, 255),        # boots
 'P': (128, 66, 192, 255), 'p': (84, 40, 136, 255), 'L': (170, 112, 232, 255),
 'W': (236, 242, 250, 255), 'w': (150, 162, 186, 255),
}

def canvas(w, h): return Image.new('RGBA', (w, h), (0, 0, 0, 0))

def grid(img, x0, y0, rows):
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch in C: img.putpixel((x0 + x, y0 + y), C[ch])

def outline(img, col=OUT):
    w, h = img.size; px = img.load(); src = img.copy().load()
    for y in range(h):
        for x in range(w):
            if src[x, y][3] == 0:
                for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
                    nx, ny = x+dx, y+dy
                    if 0 <= nx < w and 0 <= ny < h and src[nx, ny][3] and src[nx, ny] != col:
                        px[x, y] = col; break
    return img

# ---------------- adventurer ----------------
HEAD = [
 "...hhhH.....",
 ".hHHHHHHH...",
 "hHHHHHHHHH..",
 "HHHHHHHHHHH.",
 "HHHHHHHSSSS.",
 "HHHHHSSSSSS.",
 "HHHsHSSSKSS.",
 "HHHssSSSKSSS",
 ".HHsSSSSSSS.",
 "..HSSSSSSs..",
 "...ssSSSs...",
]
TORSO = [
 "..GTTTTt.",
 ".TTTTTTTt",
 ".TTTTTTTt",
 ".TTTTTTTt",
 ".tTTTTTTt",
 ".BBBBGBBB",
 ".tTTTTTTt",
]


# ---------------- house ----------------
def house():
    W, H = 34, 30; img = canvas(W, H); d = ImageDraw.Draw(img)
    R, r, Rl = (196,72,56,255),(140,46,40,255),(230,110,80,255)
    wall, walls = (240,214,160,255),(204,170,118,255)
    wood = (120,74,42,255); stone=(150,146,160,255); glow=(255,214,110,255)
    grass, grassd = (96,176,76,255),(62,128,58,255)
    # chimney + smoke
    d.rectangle([22,3,24,9], fill=stone); d.rectangle([21,2,25,3], fill=(120,116,132,255))
    # walls
    d.rectangle([7,14,26,26], fill=wall); d.rectangle([7,14,8,26], fill=walls)
    for x in (7,16,26): d.line([(x,14),(x,26)], fill=wood)
    d.line([(7,20),(26,20)], fill=wood)
    # roof
    d.polygon([(4,15),(16,4),(17,4),(29,15)], fill=R)
    for y in range(7,15,3): d.line([(16-(y-4),y),(17+(y-4),y)], fill=r)
    d.line([(16,4),(5,15)], fill=Rl)
    d.line([(4,15),(29,15)], fill=r)
    # door
    d.rectangle([12,19,15,26], fill=wood); d.rectangle([12,19,15,19], fill=(84,50,28,255))
    img.putpixel((14,23), (250,200,80,255))
    # window warm light
    d.rectangle([19,17,23,21], fill=(84,50,28,255)); d.rectangle([20,18,22,20], fill=glow)
    img.putpixel((21,19),(255,240,170,255))
    # base
    d.rectangle([3,27,30,28], fill=grass); d.line([(3,28),(30,28)], fill=grassd)
    for x,c in ((4,(250,120,170,255)),(9,(255,230,90,255)),(28,(250,120,170,255)),(25,(255,255,255,255))):
        img.putpixel((x,26),c); img.putpixel((x,27),grassd)
    d.rectangle([13,27,14,28], fill=stone)
    img = outline(img)
    return img

# ---------------- evil castle ----------------
def castle():
    W, H = 44, 44; img = canvas(W, H); d = ImageDraw.Draw(img)
    st, std, stl = (92,78,128,255),(64,52,96,255),(124,108,164,255)
    roof, roofd = (150,70,190,255),(104,44,140,255)
    win = (255,70,90,255); winc = (255,170,120,255)
    # back wall
    d.rectangle([8,22,35,41], fill=st)
    # battlements
    for x in range(8,36,4): d.rectangle([x,20,x+1,21], fill=st)
    # side towers
    for x0 in (3,32):
        d.rectangle([x0,16,x0+8,41], fill=st); d.rectangle([x0,16,x0+1,41], fill=stl)
        d.polygon([(x0-1,16),(x0+4,5),(x0+9,16)], fill=roof)
        d.line([(x0+4,5),(x0+8,15)], fill=roofd)
        d.rectangle([x0+3,22,x0+5,25], fill=win); img.putpixel((x0+4,23), winc)
    # keep
    d.rectangle([15,10,28,41], fill=st); d.rectangle([15,10,16,41], fill=stl)
    d.polygon([(13,11),(21,0),(22,0),(30,11)], fill=roof)
    d.line([(22,0),(29,10)], fill=roofd)
    d.rectangle([20,14,23,18], fill=win); d.rectangle([21,15,22,17], fill=winc)
    # flag
    d.line([(21,0),(21,-4)], fill=std)
    # stone texture
    for y in range(24,41,4):
        for x in range(10+ (y//4%2)*2, 34, 5):
            if not (18<=x<=25 and y>=30): img.putpixel((x,y), std)
    # gate
    d.rectangle([18,30,25,41], fill=(30,16,40,255)); d.polygon([(18,30),(21,27),(22,27),(25,30)], fill=(30,16,40,255))
    for x in (19,21,23): d.line([(x,30),(x,41)], fill=(90,70,80,255))
    # base rocks
    d.rectangle([1,41,42,42], fill=(56,48,72,255))
    big = canvas(44, 49); big.alpha_composite(img, (0, 6)); img = big; d = ImageDraw.Draw(img)
    d.line([(21,0),(21,6)], fill=(200,200,215,255))
    d.polygon([(22,0),(27,1),(22,3)], fill=(220,40,60,255))
    img = outline(img)
    return img


C.update({
 'Q': (196, 196, 212, 255),
 'M': (44, 150, 132, 255), 'm': (26, 98, 92, 255),
 'R': (214, 58, 58, 255), 'r': (150, 36, 40, 255),
 'J': (124, 184, 66, 255), 'j': (76, 126, 46, 255),
 'Y': (255, 224, 80, 255), 'X': (255, 255, 255, 255),
})
Y = 6  # extra headroom for hats / plumes

MAGE_HEAD = [
 "..mM.........",
 "...MMM.......",
 "....MMMM.....",
 "....MMMMM....",
 "...MMMMMMm...",
 "...MGGGGGGm..",
 "..MMMMMMMMMm.",
 "MMMMMMMMMMMMM",
 "..QSSSSSSS...",
 "..QSSSSKSSS..",
 "..QsSSSKSSSS.",
 "..XXSSSSSSX..",
 "...XXXXXXXX..",
 "....XXXXXX...",
 ".....XXXX....",
]
MAGE_TORSO = [
 "..MMMMMm..",
 ".MMMMMMMm.",
 ".MMMMMMMm.",
 ".MMMMMMMm.",
 ".gggggGgg.",
 ".MMMMMMMm.",
 ".MMMMMMMm.",
 "MMMMMMMMMm",
 "MMMMMMMMMm",
 "MMMMMMMMMm",
]
KNIGHT_HEAD = [
 "..RRR.......",
 ".RRwWWWw....",
 ".wWWWWWWWw..",
 ".wWWWWWWWWw.",
 ".wWWWWWWWWw.",
 ".wWWWKKKKKKw",
 ".wWWWWWWWWWw",
 ".wWWWWWwWWWw",
 "..wWWWWWWWw.",
 "...wwwwwww..",
]
KNIGHT_TORSO = [
 "..wWWWWw.",
 ".WWWWWWWw",
 ".RRRRRRRw",
 ".RRRGRRRw",
 ".RRRRRRRw",
 ".BBBBGBBB",
 ".RRRRRRRw",
]
# 8-frame walk: (foot dx, lift) for one leg; the other leg runs 4 frames out of phase
STEP = [(4,0),(2,0),(0,0),(-2,0),(-4,0),(-2,2),(0,3),(2,2)]
BOB = [0, 0, -1, -1, 0, 0, -1, -1]

def leg(d, hip, foot, pc, bc):
    hx, hy = hip; fx, fy = foot
    d.line([(hx, hy), (fx, fy - 2)], fill=pc, width=3)
    d.rectangle([fx - 1, fy - 2, fx + 1, fy], fill=bc)
    d.rectangle([fx + 2, fy - 1, fx + 2, fy], fill=bc)

def character(kind, f, idle=False):
    img = canvas(32, 36); d = ImageDraw.Draw(img)
    gy = 27 + Y
    if idle:
        b = [0, -1][f % 2]; ff, fb = (1, 0), (-2, 0); sw = 0
    else:
        b = BOB[f]; ff = STEP[f]; fb = STEP[(f + 4) % 8]; sw = -ff[0] // 2
    yb = Y + b
    if kind == 'hero':
        wv = [0,1,2,1,0,1,2,1][f % 8]; wv2 = [2,1,0,1,2,1,0,1][f % 8]
        if idle: wv, wv2 = f % 2, 1 - f % 2
        cape = [(13,13+yb),(11,13+yb),(8,15+yb),(5,18+yb),(3,22+Y+wv),(2,24+Y+wv),(6,23+Y+wv2),(9,24+Y+wv),(13,22+yb)]
        d.polygon(cape, fill=C['P'])
        d.line([(10,14+yb),(6,19+yb),(4,23+Y+wv)], fill=C['p'])
        d.line([(12,15+yb),(9,20+yb),(8,23+Y+wv)], fill=C['L'])
        pcs = ((C['n'], C['o']), (C['N'], C['O'])); arm = (C['t'], C['T'])
    elif kind == 'mage':
        pcs = ((C['n'], C['o']), (C['N'], C['O'])); arm = (C['m'], C['M'])
    else:
        pcs = (((110,118,140,255), C['n']), (C['w'], (70,70,92,255))); arm = ((110,118,140,255), C['W'])
    leg(d, (13, 20+yb), (13+fb[0], gy-fb[1]), *pcs[0])
    d.line([(14,14+yb),(13-sw,18+yb)], fill=arm[0], width=2)
    leg(d, (14, 20+yb), (14+ff[0], gy-ff[1]), *pcs[1])
    hx, hy = 17 - sw // 2, 18 + yb
    if kind == 'hero':
        grid(img, 10, 13+yb, TORSO); grid(img, 9, 2+yb, HEAD)
        d.line([(15,14+yb),(hx,hy)], fill=C['T'], width=2)
        d.line([(hx+1,hy-1),(hx+6,hy-6)], fill=C['W']); d.line([(hx+2,hy-1),(hx+6,hy-5)], fill=C['w'])
        d.line([(hx,hy-2),(hx+2,hy)], fill=C['G'])
        img.putpixel((hx,hy), C['S']); img.putpixel((hx,hy+1), C['g'])
        img.putpixel((12,13+yb), C['G'])
    elif kind == 'mage':
        grid(img, 10, 13+yb, MAGE_TORSO); grid(img, 8, -2+yb, MAGE_HEAD)
        d.line([(hx+2,hy-11),(hx+2,hy+7)], fill=C['O'])
        d.line([(15,14+yb),(hx,hy)], fill=C['M'], width=2)
        img.putpixel((hx+1,hy), C['S']); img.putpixel((hx+2,hy), C['S'])
        d.rectangle([hx+1,hy-14,hx+3,hy-12], fill=(120,232,255,255)); img.putpixel((hx+1,hy-14), C['X'])
    else:
        grid(img, 10, 13+yb, KNIGHT_TORSO); grid(img, 9, 2+yb, KNIGHT_HEAD)
        d.line([(15,14+yb),(hx,hy)], fill=C['W'], width=2)
        d.ellipse([hx-2,hy-7,hx+4,hy+2], fill=C['R'], outline=C['G'])
        d.line([(hx+1,hy-5),(hx+1,hy)], fill=C['Y']); d.line([(hx-1,hy-3),(hx+3,hy-3)], fill=C['Y'])
    img = outline(img)
    if idle: img = img.transpose(Image.FLIP_LEFT_RIGHT)  # wait facing the hero
    return img

GOB = [
 "......jjjj......",
 ".....JJJJJJ.....",
 "j...JJJJJJJJ...j",
 "jJ.JJJJJJJJJJ.Jj",
 ".jJJJYKJJKYJJJj.",
 "..jJJJJJJJJJJj..",
 "...JJXKXKXKJJ...",
 "....jJJJJJJj....",
 "....OOOOOOOO....",
 "..JJOOOOOOOOJJ..",
 "..J.OoOOOOoO.J..",
 "....BBBBBBBB....",
 "....OoO..OoO....",
 "....jj....jj....",
 "...jjj....jjj...",
]
def goblin(f):
    img = canvas(22, 22); d = ImageDraw.Draw(img); b = [0, 1][f]
    top = 5 + b
    grid(img, 1, top, GOB[:12]); grid(img, 1, 17, GOB[12:])
    d.line([(14,top+10),(18-f,top+1)], fill=C['O'], width=2)
    d.rectangle([17-f,top-2,19-f,top+2], fill=C['o'])
    return outline(img)

def slime(f):
    img = canvas(18, 18); d = ImageDraw.Draw(img)
    w, h, yo = [(12,9,0),(14,7,0),(11,10,-2),(10,11,-4),(11,10,-2),(13,8,0)][f]
    cx, by = 9, 15 + yo
    d.ellipse([cx-w//2, by-h, cx+w//2, by], fill=(84,176,244,255))
    d.ellipse([cx-w//2+1, by-h//2, cx+w//2-1, by], fill=(56,128,210,255))
    d.ellipse([cx-w//2+1, by-h+1, cx+w//2-1, by-2], fill=(84,176,244,255))
    img.putpixel((cx-w//2+2, by-h+2), C['X']); img.putpixel((cx-w//2+3, by-h+2), C['X'])
    ey = by - h//2
    for ex in (cx-3, cx):
        d.rectangle([ex, ey, ex, ey+1], fill=OUT)
    return outline(img)

def signpost():
    img = canvas(22, 26); d = ImageDraw.Draw(img); wood = C['O']; dk = C['o']
    d.rectangle([10,4,11,23], fill=dk)
    d.polygon([(3,5),(16,5),(19,7),(16,9),(3,9)], fill=(196,140,80,255))
    d.line([(5,7),(14,7)], fill=(150,100,56,255))
    d.polygon([(18,11),(6,11),(3,13),(6,15),(18,15)], fill=wood)
    d.line([(8,13),(16,13)], fill=dk)
    d.rectangle([6,24,16,24], fill=C['J']); img.putpixel((7,23),C['J']); img.putpixel((14,23),C['J'])
    img.putpixel((12,23),(250,120,170,255))
    return outline(img)

def warning():
    img = canvas(26, 26); d = ImageDraw.Draw(img); dk = (80,48,30,255)
    d.rectangle([6,10,7,24], fill=dk); d.rectangle([18,9,19,24], fill=dk)
    d.polygon([(2,5),(23,2),(24,14),(3,16)], fill=(118,74,44,255))
    d.line([(4,13),(22,11)], fill=(92,56,32,255))
    d.line([(20,3),(18,8),(21,10)], fill=(70,40,24,255))
    sk = [".XXXX.","XXXXXX","XKXXKX","XXXXXX",".XKKX.",".X.X.."]
    grid(img, 10, 5, sk)
    d.line([(5,6),(5,10)], fill=C['R']); img.putpixel((5,12), C['R'])
    d.line([(21,4),(21,8)], fill=C['R']); img.putpixel((21,10), C['R'])
    d.line([(9,24),(14,23)], fill=(230,230,220,255)); d.line([(11,22),(12,24)], fill=(230,230,220,255))
    d.rectangle([1,25,24,25], fill=(70,62,84,255))
    return outline(img)

def camp(f):
    img = canvas(38, 26); d = ImageDraw.Draw(img)
    d.polygon([(2,23),(12,5),(13,5),(23,23)], fill=(150,96,190,255))
    d.polygon([(13,5),(23,23),(17,23)], fill=(110,64,150,255))
    d.polygon([(10,23),(13,12),(16,23)], fill=(40,24,50,255))
    d.line([(12,5),(12,2)], fill=C['O']); d.polygon([(13,2),(16,3),(13,4)], fill=C['Y'])
    # fire
    for p in [(26,22),(33,24)]: pass
    d.line([(26,24),(34,21)], fill=C['O'], width=2); d.line([(26,21),(34,24)], fill=C['o'], width=2)
    flames = [[(27,21),(29,14),(30,17),(31,12),(33,21)],
              [(27,21),(28,15),(30,13),(32,16),(33,21)],
              [(27,21),(29,12),(31,16),(32,14),(33,21)],
              [(27,21),(28,16),(30,14),(32,13),(33,21)]][f]
    d.polygon(flames, fill=(255,120,40,255))
    d.polygon([(28,21),(30,15+f%2),(32,21)], fill=(255,210,80,255))
    d.rectangle([24,24,36,24], fill=(120,116,132,255))
    img = outline(img)
    sp = [(30,9),(28,7),(32,6),(29,4)][f]
    img.putpixel(sp, (255,200,90,255))
    return img

def dragon(f):
    img = canvas(46, 38); d = ImageDraw.Draw(img)
    D, dd, mem, bel = (196,48,64,255), (128,26,46,255), (236,104,96,255), (246,198,122,255)
    gy = 35
    wings = [[(26,19),(31,1),(40,4),(43,12),(33,18)],
             [(26,19),(35,6),(44,10),(42,18),(32,20)],
             [(26,19),(36,16),(45,24),(37,25),(30,22)],
             [(26,19),(35,6),(44,10),(42,18),(32,20)]][f]
    d.polygon(wings, fill=mem)
    d.line([wings[0], wings[1]], fill=dd); d.line([wings[0], wings[2]], fill=dd); d.line([wings[0], wings[3]], fill=dd)
    d.polygon([(32,26),(40,28),(44,24),(45,27),(41,32),(32,31)], fill=D)
    d.polygon([(43,23),(46,22),(45,26)], fill=dd)
    d.rectangle([19,30,22,gy], fill=dd); d.rectangle([30,30,33,gy], fill=dd)
    d.ellipse([16,17,36,33], fill=D)
    d.ellipse([18,23,29,33], fill=bel)
    d.polygon([(19,22),(24,19),(16,9),(11,11)], fill=D)
    d.polygon([(2,11),(9,7),(16,8),(17,13),(11,16),(3,15)], fill=D)
    d.line([(3,15),(11,16)], fill=bel)
    d.line([(14,8),(18,2)], fill=(240,220,190,255)); d.line([(16,9),(21,5)], fill=(240,220,190,255))
    d.rectangle([11,10,12,10], fill=C['Y']); img.putpixel((12,10), OUT)
    img.putpixel((4,12), OUT)
    for x in range(20, 30, 3): img.putpixel((x, 18), dd)
    for x in (18, 21, 30, 33): img.putpixel((x, gy), (240,220,190,255))
    img = outline(img)
    if f == 2:
        d2 = ImageDraw.Draw(img)
        img.putpixel((1,10),(150,150,160,200)); img.putpixel((0,9),(150,150,160,140))
    return img

def puff(f):
    img = canvas(24, 24); d = ImageDraw.Draw(img)
    r = [3,6,8,9,9][f]; a = [255,255,230,170,90][f]
    for cx, cy, k in ((12,14,1.0),(7,16,0.7),(17,16,0.7),(10,10,0.6),(15,10,0.6)):
        rr = max(1, int(r*k)); d.ellipse([cx-rr, cy-rr, cx+rr, cy+rr], fill=(235,235,245,a))
    if f >= 1:
        for (x, y) in [(2,6),(21,5),(3,21),(22,20)][:f+1]:
            d.line([(x-1,y),(x+1,y)], fill=(255,224,80,a)); d.line([(x,y-1),(x,y+1)], fill=(255,224,80,a))
    return img

def coin(f):
    img = canvas(12, 12); d = ImageDraw.Draw(img)
    d.ellipse([3,5,8,10], fill=C['G']); d.line([(5,6),(5,9)], fill=C['g'])
    img = outline(img)
    if f == 1:
        d = ImageDraw.Draw(img); d.line([(9,1),(9,5)], fill=C['X']); d.line([(7,3),(11,3)], fill=C['X'])
    return img


# =============================================================== library v2
import math

C.update({
 'V': (234, 228, 206, 255), 'v': (170, 164, 140, 255),   # bone
 'F': (214, 124, 52, 255), 'f': (150, 80, 34, 255),      # archer leather
})
STONE, STONE_D, STONE_L = (150, 146, 160, 255), (108, 104, 122, 255), (188, 184, 198, 255)
WOOD, WOOD_D = C['O'], C['o']
GRASS = (96, 176, 76, 255)
RED_ROOF, RED_ROOF_D, RED_ROOF_L = (176, 72, 52, 255), (130, 46, 40, 255), (214, 104, 76, 255)

ARCHER_HEAD = [
 "...HHHH.....",
 ".HHHHHHHH...",
 "HHHHHHHHHH..",
 "HHRRRRRRRRR.",
 "HHHHHHHSSSS.",
 "HHHHHSSSSSS.",
 "HHHsHSSSKSS.",
 "HHHssSSSKSSS",
 "HHHsSSSSSSS.",
 "HH.SSSSSSs..",
 "H...sSSSs...",
]
ARCHER_TORSO = [
 "..FFFFFf.",
 ".FFFFFFFf",
 ".FFFFFFFf",
 ".FFFFFFFf",
 ".fFFFFFFf",
 ".BBBBGBBB",
 ".fFFFFFFf",
]


def archer(f, idle=False):
    """Archer partner: auburn ponytail, red headband, leather tunic, bow + quiver."""
    img = canvas(32, 36); d = ImageDraw.Draw(img)
    gy = 27 + Y
    if idle:
        b = [0, -1][f % 2]; ff, fb = (1, 0), (-2, 0); sw = 0
    else:
        b = BOB[f]; ff = STEP[f]; fb = STEP[(f + 4) % 8]; sw = -ff[0] // 2
    yb = Y + b
    d.rectangle([9, 12 + yb, 11, 19 + yb], fill=C['o'])                 # quiver
    for x, c in ((9, C['W']), (10, C['R']), (11, C['W'])): img.putpixel((x, 11 + yb), c)
    leg(d, (13, 20 + yb), (13 + fb[0], gy - fb[1]), C['n'], C['o'])
    d.line([(14, 14 + yb), (13 - sw, 18 + yb)], fill=C['f'], width=2)
    leg(d, (14, 20 + yb), (14 + ff[0], gy - ff[1]), C['N'], C['O'])
    grid(img, 10, 13 + yb, ARCHER_TORSO); grid(img, 9, 2 + yb, ARCHER_HEAD)
    hx, hy = 17 - sw // 2, 18 + yb
    d.line([(15, 14 + yb), (hx + 1, hy - 1)], fill=C['F'], width=2)
    d.line([(hx + 3, hy - 6), (hx + 3, hy + 6)], fill=(230, 230, 220, 255))           # string
    d.arc([hx, hy - 7, hx + 7, hy + 7], start=-80, end=80, fill=(150, 96, 46, 255), width=2)  # bow
    img.putpixel((hx + 2, hy - 1), C['S']); img.putpixel((hx + 3, hy - 1), C['S'])
    img = outline(img)
    if idle: img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


def quadruped(kind, f, idle=False):
    """Cat / dog partner on the 32x36 character canvas (feet on row 33)."""
    img = canvas(32, 36); d = ImageDraw.Draw(img); gy = 33
    ph = (f % 8) / 8 * 2 * math.pi
    b = 0 if idle else (-1 if f % 4 in (1, 2) else 0)
    def legx(x, p): return x + (0 if idle else round(1.5 * math.sin(ph + p)))
    def lift(p): return 0 if idle else (1 if math.sin(ph + p + math.pi / 2) > 0.7 else 0)
    if kind == 'cat':
        fur, fur_d, light = (240, 160, 70, 255), (190, 110, 40, 255), (252, 224, 184, 255)
        legs = [(10, math.pi, fur_d), (18, 0, fur_d), (12, 0, fur), (20, math.pi, fur)]
        for x, p, c in legs: d.rectangle([legx(x, p), 28 + b, legx(x, p) + 1, gy - lift(p)], fill=c)
        tw = (f % 2) if idle else round(math.sin(ph))
        d.line([(9, 26 + b), (6, 22 + b), (5 + tw, 17 + b)], fill=fur, width=2)
        d.ellipse([8, 23 + b, 22, 30 + b], fill=fur)
        d.ellipse([12, 27 + b, 20, 30 + b], fill=light)
        for x in (11, 14, 17): d.line([(x, 24 + b), (x, 26 + b)], fill=fur_d)
        d.ellipse([18, 17 + b, 27, 25 + b], fill=fur)
        d.polygon([(19, 19 + b), (20, 14 + b), (22, 18 + b)], fill=fur)
        d.polygon([(23, 18 + b), (25, 14 + b), (26, 19 + b)], fill=fur)
        img.putpixel((20, 17 + b), (250, 150, 160, 255)); img.putpixel((25, 17 + b), (250, 150, 160, 255))
        d.rectangle([24, 22 + b, 27, 24 + b], fill=light)
        img.putpixel((24, 20 + b), OUT); img.putpixel((24, 21 + b), OUT)
        img.putpixel((27, 22 + b), (240, 110, 130, 255))
        d.line([(20, 19 + b), (22, 19 + b)], fill=fur_d)
    else:
        fur, fur_d, light = (176, 112, 58, 255), (120, 72, 36, 255), (248, 240, 226, 255)
        legs = [(8, math.pi, fur_d), (17, 0, fur_d), (10, 0, fur), (19, math.pi, light)]
        for x, p, c in legs: d.rectangle([legx(x, p), 27 + b, legx(x, p) + 1, gy - lift(p)], fill=c)
        wag = (f % 2) * 2 if idle else (f % 2) * 2
        d.line([(7, 24 + b), (4, 20 + b), (2 + wag, 17 + b)], fill=fur, width=2)
        d.ellipse([5, 21 + b, 22, 29 + b], fill=fur)
        d.ellipse([16, 22 + b, 22, 29 + b], fill=light)
        d.ellipse([17, 14 + b, 26, 23 + b], fill=fur)
        d.rectangle([24, 18 + b, 29, 22 + b], fill=light)
        d.rectangle([28, 18 + b, 29, 19 + b], fill=OUT)
        d.line([(25, 22 + b), (28, 22 + b)], fill=fur_d)
        d.polygon([(18, 15 + b), (21, 14 + b), (21, 22 + b), (18, 21 + b)], fill=fur_d)
        img.putpixel((23, 17 + b), OUT); img.putpixel((23, 18 + b), OUT)
        d.line([(19, 23 + b), (23, 21 + b)], fill=C['R'])
        img.putpixel((21, 23 + b), C['G'])
    img = outline(img)
    if idle: img = img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


# ---------------- places
def well():
    img = canvas(24, 29); d = ImageDraw.Draw(img)
    d.rectangle([6, 8, 7, 18], fill=WOOD_D); d.rectangle([16, 8, 17, 18], fill=WOOD_D)
    d.line([(7, 11), (16, 11)], fill=WOOD_D)
    d.line([(12, 11), (12, 14)], fill=(210, 200, 180, 255))
    d.rectangle([11, 14, 13, 16], fill=WOOD)
    d.polygon([(3, 10), (12, 2), (20, 10)], fill=RED_ROOF)
    d.line([(12, 2), (4, 10)], fill=RED_ROOF_L); d.line([(3, 10), (20, 10)], fill=RED_ROOF_D)
    d.rectangle([4, 18, 19, 26], fill=STONE); d.rectangle([4, 18, 19, 18], fill=STONE_L)
    for x, y in ((6, 21), (11, 20), (16, 21), (8, 23), (14, 23), (17, 25), (5, 25)):
        d.line([(x, y), (x + 2, y)], fill=STONE_D)
    d.rectangle([2, 27, 21, 27], fill=GRASS)
    img.putpixel((3, 26), GRASS); img.putpixel((20, 26), (250, 120, 170, 255))
    return outline(img)


def windmill(f):
    img = canvas(36, 40); d = ImageDraw.Draw(img)
    wall, wall_d = (236, 218, 176, 255), (196, 170, 124, 255)
    d.polygon([(13, 16), (23, 16), (25, 36), (11, 36)], fill=wall)
    d.polygon([(19, 16), (23, 16), (25, 36), (20, 36)], fill=wall_d)
    d.rectangle([16, 30, 19, 36], fill=WOOD_D); d.rectangle([17, 22, 18, 24], fill=(60, 40, 30, 255))
    d.polygon([(11, 17), (18, 8), (25, 17)], fill=RED_ROOF); d.line([(18, 8), (24, 16)], fill=RED_ROOF_D)
    cx, cy, r = 18, 15, 12
    for k in range(4):
        a = math.radians(k * 90 + f * 22.5); ux, uy = math.cos(a), math.sin(a); px_, py_ = -uy, ux
        sail = [(cx + ux * 5, cy + uy * 5), (cx + ux * r, cy + uy * r),
                (cx + ux * r + px_ * 3, cy + uy * r + py_ * 3), (cx + ux * 5 + px_ * 3, cy + uy * 5 + py_ * 3)]
        d.polygon([(round(x), round(y)) for x, y in sail], fill=(242, 238, 228, 255))
        d.line([(cx, cy), (round(cx + ux * r), round(cy + uy * r))], fill=WOOD_D)
    d.rectangle([cx - 1, cy - 1, cx + 1, cy + 1], fill=WOOD_D)
    d.rectangle([8, 37, 28, 37], fill=GRASS)
    return outline(img)


def bridge():
    img = canvas(44, 20); d = ImageDraw.Draw(img)
    d.rectangle([1, 15, 42, 18], fill=(70, 130, 210, 255))
    d.line([(4, 17), (8, 17)], fill=(170, 210, 250, 255)); d.line([(33, 16), (38, 16)], fill=(170, 210, 250, 255))
    d.polygon([(3, 18), (3, 9), (9, 6), (34, 6), (40, 9), (40, 18), (31, 18), (29, 13), (25, 10),
               (18, 10), (14, 13), (12, 18)], fill=STONE)
    d.line([(3, 9), (9, 6), (34, 6), (40, 9)], fill=STONE_L)
    for x in range(6, 38, 4): img.putpixel((x, 8), STONE_D)
    for x, y in ((5, 12), (8, 15), (35, 12), (37, 15), (20, 8)): d.line([(x, y), (x + 1, y)], fill=STONE_D)
    for x in (5, 13, 21, 29, 37): d.rectangle([x, 3, x + 1, 6], fill=STONE_D)
    d.line([(5, 3), (38, 3)], fill=STONE_D)
    return outline(img)


def chest(f):
    img = canvas(20, 19); d = ImageDraw.Draw(img)
    body, body_d, lid = (150, 92, 46, 255), (108, 62, 30, 255), (178, 114, 60, 255)
    if f == 0:
        d.rectangle([3, 10, 16, 17], fill=body); d.rectangle([3, 6, 16, 10], fill=lid)
        d.rectangle([3, 6, 16, 6], fill=(200, 138, 78, 255)); d.line([(3, 10), (16, 10)], fill=body_d)
        for x in (5, 14): d.line([(x, 6), (x, 17)], fill=C['g'])
        d.rectangle([9, 9, 10, 12], fill=C['G'])
    else:
        d.rectangle([3, 1, 16, 5], fill=lid); d.rectangle([4, 5, 15, 7], fill=(60, 34, 20, 255))
        d.rectangle([3, 10, 16, 17], fill=body)
        d.ellipse([4, 6, 15, 12], fill=C['G']); d.rectangle([4, 9, 15, 10], fill=C['G'])
        for x, y in ((6, 8), (9, 7), (12, 8), (8, 9)): img.putpixel((x, y), C['Y'])
        for x in (5, 14): d.line([(x, 10), (x, 17)], fill=C['g'])
        d.rectangle([9, 11, 10, 13], fill=C['G'])
    img = outline(img)
    if f == 1:
        for x, y in ((1, 4), (18, 2), (17, 8)): img.putpixel((x, y), C['X'])
    return img


def cart():
    img = canvas(36, 28); d = ImageDraw.Draw(img)
    d.line([(27, 18), (34, 21)], fill=WOOD_D, width=2)
    d.line([(6, 15), (6, 6)], fill=WOOD_D); d.line([(26, 15), (26, 6)], fill=WOOD_D)
    d.ellipse([7, 10, 11, 14], fill=C['R']); d.ellipse([11, 11, 14, 14], fill=C['J'])
    d.rectangle([19, 9, 24, 14], fill=(178, 114, 60, 255)); d.line([(19, 11), (24, 11)], fill=WOOD_D)
    d.rectangle([4, 14, 28, 20], fill=WOOD); d.line([(4, 17), (28, 17)], fill=WOOD_D)
    for x in range(4, 29):
        c = C['R'] if (x // 3) % 2 else (242, 238, 228, 255)
        d.line([(x, 3), (x, 6)], fill=c)
        if x % 3 == 1: img.putpixel((x, 7), c)
    for wx in (10, 23):
        d.ellipse([wx - 4, 17, wx + 4, 25], fill=WOOD_D); d.ellipse([wx - 2, 19, wx + 2, 23], fill=WOOD)
        img.putpixel((wx, 21), WOOD_D)
    return outline(img)


def haunted_tree(f):
    img = canvas(30, 35); d = ImageDraw.Draw(img)
    bark, bark_d = (98, 80, 110, 255), (66, 52, 80, 255)
    d.line([(13, 14), (6, 8), (3, 9)], fill=bark, width=2); d.line([(6, 8), (5, 4)], fill=bark)
    d.line([(16, 12), (23, 6), (27, 7)], fill=bark, width=2); d.line([(23, 6), (24, 2)], fill=bark)
    d.line([(14, 8), (12, 3)], fill=bark)
    d.polygon([(11, 33), (13, 18), (12, 10), (15, 6), (17, 10), (17, 18), (20, 33)], fill=bark)
    d.line([(11, 33), (7, 33)], fill=bark, width=2); d.line([(20, 33), (24, 33)], fill=bark, width=2)
    d.line([(16, 12), (18, 31)], fill=bark_d)
    d.ellipse([12, 19, 18, 26], fill=(30, 18, 40, 255))
    glow = (255, 220, 80, 255)
    if f == 0:
        img.putpixel((14, 21), glow); img.putpixel((16, 21), glow)
        d.line([(14, 24), (16, 24)], fill=glow)
    return outline(img)


# ---------------- enemies
def bat(f):
    img = canvas(24, 22); d = ImageDraw.Draw(img); o = 5
    b, bd = (110, 76, 140, 255), (70, 46, 96, 255)
    wy = (-4, -1, 3, -1)[f]
    d.polygon([(11, 7 + o), (3, 4 + o + wy), (1, 8 + o + wy // 2), (4, 8 + o), (6, 10 + o), (11, 10 + o)], fill=b)
    d.polygon([(12, 7 + o), (20, 4 + o + wy), (22, 8 + o + wy // 2), (19, 8 + o), (17, 10 + o), (12, 10 + o)], fill=b)
    d.ellipse([9, 5 + o, 14, 12 + o], fill=bd)
    d.polygon([(9, 6 + o), (9, 3 + o), (11, 5 + o)], fill=bd); d.polygon([(14, 6 + o), (14, 3 + o), (12, 5 + o)], fill=bd)
    img.putpixel((10, 8 + o), (255, 70, 90, 255)); img.putpixel((13, 8 + o), (255, 70, 90, 255))
    img.putpixel((11, 10 + o), C['X']); img.putpixel((12, 10 + o), C['X'])
    return outline(img)


SKEL = [
 "..VVVVV....",
 ".VVVVVVV...",
 ".VKKVKKV...",
 ".VKKVKKV...",
 ".VVVKVVV...",
 "..VKVKV....",
 "....V......",
 ".VVVVVVV...",
 "V..vVv..V..",
 "V..VvV..V..",
 "V..vVv..V..",
 "....V......",
 "...vVv.....",
 "...V.V.....",
 "...V.V.....",
 "...V.V.....",
 "..VV.VV....",
]


def skeleton(f):
    img = canvas(18, 24); d = ImageDraw.Draw(img)
    grid(img, 5, 2 + (f % 2), SKEL[:7]); grid(img, 5, 9, SKEL[7:])
    d.line([(5, 12), (2, 4 + f)], fill=(176, 176, 192, 255)); d.line([(3, 11), (6, 12)], fill=C['g'])
    return outline(img)


def wolf(f):
    img = canvas(30, 21); d = ImageDraw.Draw(img)
    g, gd, gl = (136, 138, 160, 255), (92, 94, 116, 255), (200, 202, 218, 255)
    by = f % 2
    d.polygon([(22, 9 + by), (27, 4), (28, 6), (24, 12)], fill=g)
    d.rectangle([9, 13, 10, 19], fill=gd); d.rectangle([20, 13, 21, 19], fill=gd)
    d.ellipse([6, 7 + by, 24, 15], fill=g)
    d.rectangle([7, 13, 8, 19], fill=g); d.rectangle([18, 13, 19, 19], fill=g)
    d.ellipse([9, 11 + by, 19, 15], fill=gl)
    d.polygon([(2, 10), (5, 6), (8, 4), (10, 6), (11, 11), (7, 13), (3, 12)], fill=g)
    d.polygon([(7, 5), (8, 1), (10, 5)], fill=gd)
    d.rectangle([2, 10, 5, 11], fill=gl)
    img.putpixel((6, 8), (255, 220, 80, 255)); img.putpixel((2, 10), OUT)
    img.putpixel((3, 12), C['X']); img.putpixel((5, 12), C['X'])
    return outline(img)


def mushroom(f):
    img = canvas(21, 21); d = ImageDraw.Draw(img); s = f % 2
    d.rectangle([6, 17, 8, 18], fill=WOOD_D); d.rectangle([12, 17, 14, 18], fill=WOOD_D)
    d.rectangle([6, 9, 14, 16], fill=(240, 226, 196, 255))
    d.pieslice([1, 2 + s, 19, 17 + s], 180, 360, fill=(214, 58, 58, 255))
    d.line([(2, 9 + s), (18, 9 + s)], fill=(160, 36, 40, 255))
    for x, y in ((5, 5), (11, 4), (15, 7), (8, 7)): d.rectangle([x, y + s, x + 1, y + s + 1], fill=(250, 246, 236, 255))
    img.putpixel((8, 12), OUT); img.putpixel((12, 12), OUT)
    d.line([(7, 11), (8, 11)], fill=OUT); d.line([(12, 11), (13, 11)], fill=OUT)
    d.line([(9, 14), (11, 14)], fill=OUT)
    return outline(img)


def ghost(f):
    img = canvas(20, 26); d = ImageDraw.Draw(img); o = (0, 1, 2, 1)[f]
    gc, gd = (214, 226, 255, 255), (160, 176, 226, 255)
    d.polygon([(4, 10 + o), (1, 14 + o), (4, 13 + o)], fill=gc)
    d.ellipse([4, 2 + o, 15, 13 + o], fill=gc); d.rectangle([4, 8 + o, 15, 16 + o], fill=gc)
    for i, x in enumerate(range(4, 16, 3)):
        d.polygon([(x, 16 + o), (x + 3, 16 + o), (x + 1, 18 + o + ((i + f) % 2) * 2)], fill=gc)
    d.rectangle([4, 12 + o, 5, 16 + o], fill=gd)
    d.ellipse([6, 6 + o, 8, 9 + o], fill=OUT); d.ellipse([11, 6 + o, 13, 9 + o], fill=OUT)
    d.ellipse([8, 10 + o, 10, 13 + o], fill=(60, 40, 90, 255))
    return outline(img)


def build_all():
    s = {}
    for k in ('hero', 'mage', 'knight'):
        for f in range(8): s[f'{k}_walk_{f}'] = character(k, f)
        for f in range(2): s[f'{k}_idle_{f}'] = character(k, f, idle=True)
    for f in range(2): s[f'goblin_{f}'] = goblin(f)
    for f in range(6): s[f'slime_{f}'] = slime(f)
    for f in range(4): s[f'camp_{f}'] = camp(f)
    for f in range(4): s[f'dragon_{f}'] = dragon(f)
    for f in range(5): s[f'puff_{f}'] = puff(f)
    for f in range(2): s[f'coin_{f}'] = coin(f)
    s['signpost'] = signpost(); s['warning_sign'] = warning()
    s['house'] = house(); s['castle'] = castle()
    # library v2
    for f in range(8): s[f'archer_walk_{f}'] = archer(f)
    for f in range(2): s[f'archer_idle_{f}'] = archer(f, idle=True)
    for k in ('cat', 'dog'):
        for f in range(8): s[f'{k}_walk_{f}'] = quadruped(k, f)
        for f in range(2): s[f'{k}_idle_{f}'] = quadruped(k, f, idle=True)
    s['well'] = well(); s['bridge'] = bridge(); s['cart'] = cart()
    for f in range(4): s[f'windmill_{f}'] = windmill(f)
    for f in range(2): s[f'chest_{f}'] = chest(f)
    for f in range(2): s[f'haunted_tree_{f}'] = haunted_tree(f)
    for f in range(4): s[f'bat_{f}'] = bat(f)
    for f in range(2): s[f'skeleton_{f}'] = skeleton(f)
    for f in range(2): s[f'wolf_{f}'] = wolf(f)
    for f in range(2): s[f'mushroom_{f}'] = mushroom(f)
    for f in range(4): s[f'ghost_{f}'] = ghost(f)
    return s


if __name__ == '__main__':
    import argparse, re
    from collections import defaultdict
    ap = argparse.ArgumentParser(description='Export sprites as transparent PNGs (+ GIF loops).')
    ap.add_argument('outdir'); ap.add_argument('--scale', type=int, nargs='+', default=[1, 3])
    a = ap.parse_args()
    sprites = build_all()
    for sc in a.scale:
        d = os.path.join(a.outdir, f'x{sc}'); os.makedirs(d, exist_ok=True)
        groups = defaultdict(list)
        for n, im in sprites.items():
            big = im.resize((im.width * sc, im.height * sc), Image.NEAREST); big.save(f'{d}/{n}.png')
            m = re.match(r'(.*)_(\d+)$', n)
            if m: groups[m.group(1)].append((int(m.group(2)), big))
        for g, fr in groups.items():
            fr = [f for _, f in sorted(fr, key=lambda x: x[0])]
            if len(fr) > 1:
                fr[0].save(f'{d}/{g}.gif', save_all=True, append_images=fr[1:], duration=120, loop=0, disposal=2, transparency=0)
    print(f'exported {len(sprites)} sprites to {a.outdir}')
