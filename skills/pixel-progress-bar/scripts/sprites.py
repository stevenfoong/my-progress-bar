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
