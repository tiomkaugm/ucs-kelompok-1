import pygame
import heapq
import sys
import math
from collections import defaultdict

# ============================================================
# 1. INISIALISASI PYGAME
# ============================================================

pygame.init()
WIDTH, HEIGHT = 1500, 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UCS - Pencarian Rute Tercepat Kampus")

# Warna
WHITE = (255,255,255)
BLACK = (10,10,10)
DARK = (30,30,30)
GREEN = (46,204,113)
DARK_GREEN = (39,174,96)
RED = (231,76,60)
DARK_RED = (192,57,43)
BLUE = (52,152,219)
DARK_BLUE = (41,128,185)
YELLOW = (241,196,15)
ORANGE = (243,156,18)
PURPLE = (155,89,182)
TEAL = (26,188,156)
PINK = (233,88,152)
GRAY = (200,200,200)
DARK_GRAY = (100,100,100)
LIGHT_GRAY = (240,240,240)
SKY = (235,245,255)
GRASS = (46,204,113)
PATH_COLOR = (220,210,190)
BROWN = (139,69,19)
GOLD = (241,196,15)
NAVY = (44,62,80)
CREAM = (255,248,220)
SOFT_GREEN = (220,255,220)
SOFT_BLUE = (235,245,255)

# Font
font_big = pygame.font.Font(None, 38)
font_med = pygame.font.Font(None, 28)
font_small = pygame.font.Font(None, 22)
font_tiny = pygame.font.Font(None, 18)
font_xsmall = pygame.font.Font(None, 14)
font_math = pygame.font.Font(None, 22)
font_formula = pygame.font.Font(None, 24)

# ============================================================
# 2. GRAF KAMPUS - DATA BENAR
# ============================================================

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)
        self.nodes = set()
    
    def add(self, a, b, w):
        self.edges[a].append((b, w))
        self.edges[b].append((a, w))
        self.nodes.add(a)
        self.nodes.add(b)
    
    def get(self, n):
        return self.edges.get(n, [])
    
    def get_all_nodes(self):
        return sorted(self.nodes)

g = Graph()

# ============================================================
# DATA JALUR (dalam MENIT) - SUDAH BENAR
# ============================================================

g.add('G', 'P', 5)   # Gerbang → Perpustakaan = 5 menit
g.add('G', 'K', 4)   # Gerbang → Kantin = 4 menit
g.add('G', 'O', 7)   # Gerbang → Gedung Olahraga = 7 menit
g.add('G', 'A', 6)   # Gerbang → Auditorium = 6 menit
g.add('G', 'L', 8)   # Gerbang → Laboratorium = 8 menit

g.add('P', 'K', 6)   # Perpustakaan → Kantin = 6 menit
g.add('P', 'O', 8)   # Perpustakaan → Gedung Olahraga = 8 menit
g.add('P', 'A', 4)   # Perpustakaan → Auditorium = 4 menit
g.add('P', 'L', 7)   # Perpustakaan → Laboratorium = 7 menit

g.add('K', 'O', 3)   # Kantin → Gedung Olahraga = 3 menit
g.add('K', 'A', 5)   # Kantin → Auditorium = 5 menit
g.add('K', 'L', 6)   # Kantin → Laboratorium = 6 menit
g.add('K', 'M', 4)   # Kantin → Masjid = 4 menit

g.add('O', 'A', 6)   # Gedung Olahraga → Auditorium = 6 menit
g.add('O', 'L', 5)   # Gedung Olahraga → Laboratorium = 5 menit
g.add('O', 'M', 7)   # Gedung Olahraga → Masjid = 7 menit

g.add('A', 'L', 3)   # Auditorium → Laboratorium = 3 menit
g.add('A', 'M', 5)   # Auditorium → Masjid = 5 menit
g.add('A', 'R', 6)   # Auditorium → Ruang Dosen = 6 menit

g.add('L', 'M', 4)   # Laboratorium → Masjid = 4 menit
g.add('L', 'R', 5)   # Laboratorium → Ruang Dosen = 5 menit

g.add('M', 'R', 4)   # Masjid → Ruang Dosen = 4 menit
g.add('M', 'G', 7)   # Masjid → Gerbang = 7 menit

g.add('R', 'G', 9)   # Ruang Dosen → Gerbang = 9 menit

# ============================================================
# NAMA LOKASI
# ============================================================

NAMA = {
    'G': 'Gerbang Utama', 
    'P': 'Perpustakaan', 
    'K': 'Kantin',
    'O': 'Gedung Olahraga', 
    'A': 'Auditorium', 
    'L': 'Laboratorium',
    'M': 'Masjid Kampus', 
    'R': 'Ruang Dosen'
}

SINGKAT = {'G':'G','P':'P','K':'K','O':'O','A':'A','L':'L','M':'M','R':'R'}
IKON = {'G':'🏛️','P':'📚','K':'🍽️','O':'🏋️','A':'🎭','L':'🔬','M':'🕌','R':'👨‍🏫'}
WARNA = {'G':BLUE,'P':GREEN,'K':YELLOW,'O':ORANGE,'A':PURPLE,'L':TEAL,'M':GOLD,'R':PINK}

# ============================================================
# POSISI DAN UKURAN BANGUNAN
# ============================================================

POSISI = {
    'G': (130, 580), 'P': (130, 180), 'K': (380, 580),
    'O': (630, 580), 'A': (380, 180), 'L': (630, 180),
    'M': (380, 380), 'R': (630, 380),
}

UKURAN = {
    'G': (100, 70), 'P': (110, 75), 'K': (100, 70), 'O': (120, 75),
    'A': (110, 75), 'L': (100, 70), 'M': (100, 70), 'R': (110, 70)
}

# ============================================================
# 3. DROPDOWN CLASS
# ============================================================

class Dropdown:
    def __init__(self, x, y, w, h, options, default=None, label=""):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options
        self.selected = default if default in options else options[0] if options else None
        self.is_open = False
        self.label = label
        self.font = font_small
        self.bg_color = WHITE
        self.hover_color = LIGHT_GRAY
        self.hover_index = -1
        self.opt_rects = []
        
    def draw(self, screen):
        if self.label:
            label_text = self.font.render(self.label, True, DARK)
            screen.blit(label_text, (self.rect.x, self.rect.y - 25))
        
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=8)
        pygame.draw.rect(screen, DARK_GRAY, self.rect, 2, border_radius=8)
        
        text = self.font.render(self.selected if self.selected else "Pilih", True, DARK)
        screen.blit(text, (self.rect.x + 12, self.rect.y + self.rect.height//2 - text.get_height()//2))
        
        arrow = "▼" if not self.is_open else "▲"
        arrow_text = self.font.render(arrow, True, DARK_GRAY)
        screen.blit(arrow_text, (self.rect.x + self.rect.width - 28, self.rect.y + self.rect.height//2 - arrow_text.get_height()//2))
        
        if self.is_open:
            self.opt_rects = []
            for i, option in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + self.rect.height + i * 30, self.rect.width, 30)
                self.opt_rects.append(opt_rect)
                color = self.hover_color if i == self.hover_index else WHITE
                pygame.draw.rect(screen, color, opt_rect, border_radius=4)
                pygame.draw.rect(screen, DARK_GRAY, opt_rect, 1, border_radius=4)
                opt_text = self.font.render(option + " - " + NAMA[option], True, DARK)
                screen.blit(opt_text, (opt_rect.x + 12, opt_rect.y + 5))
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_open = not self.is_open
                return True
            if self.is_open:
                for i, opt_rect in enumerate(self.opt_rects):
                    if opt_rect and opt_rect.collidepoint(event.pos):
                        self.selected = self.options[i]
                        self.is_open = False
                        return True
                self.is_open = False
        if event.type == pygame.MOUSEMOTION and self.is_open:
            self.hover_index = -1
            for i, opt_rect in enumerate(self.opt_rects):
                if opt_rect and opt_rect.collidepoint(event.pos):
                    self.hover_index = i
                    break
        return False

# ============================================================
# 4. MENGGAMBAR PETA
# ============================================================

def draw_campus_map(game):
    # LANGIT
    pygame.draw.rect(screen, SKY, (0, 0, 780, 180))
    pygame.draw.circle(screen, YELLOW, (710, 60), 40)
    pygame.draw.circle(screen, (255,255,200), (710, 60), 30)
    
    for cloud in [(80,40), (280,25), (500,50)]:
        pygame.draw.ellipse(screen, WHITE, (cloud[0], cloud[1], 70, 25))
        pygame.draw.ellipse(screen, WHITE, (cloud[0]+25, cloud[1]-12, 50, 30))
        pygame.draw.ellipse(screen, WHITE, (cloud[0]+50, cloud[1]+5, 40, 20))
    
    # RUMPUT
    pygame.draw.rect(screen, GRASS, (0, 180, 780, 600))
    
    # JALAN
    pygame.draw.rect(screen, PATH_COLOR, (0, 530, 780, 35))
    pygame.draw.rect(screen, PATH_COLOR, (0, 340, 780, 30))
    pygame.draw.rect(screen, PATH_COLOR, (115, 180, 30, 390))
    pygame.draw.rect(screen, PATH_COLOR, (365, 180, 30, 390))
    pygame.draw.rect(screen, PATH_COLOR, (615, 180, 30, 390))
    
    pygame.draw.line(screen, PATH_COLOR, (170, 580), (170, 230), 25)
    pygame.draw.line(screen, PATH_COLOR, (170, 580), (365, 580), 25)
    pygame.draw.line(screen, PATH_COLOR, (395, 580), (615, 580), 25)
    pygame.draw.line(screen, PATH_COLOR, (170, 230), (365, 230), 25)
    pygame.draw.line(screen, PATH_COLOR, (395, 230), (615, 230), 25)
    pygame.draw.line(screen, PATH_COLOR, (395, 560), (395, 400), 22)
    pygame.draw.line(screen, PATH_COLOR, (630, 560), (630, 400), 22)
    pygame.draw.line(screen, PATH_COLOR, (395, 400), (615, 400), 22)
    pygame.draw.line(screen, PATH_COLOR, (200, 230), (395, 560), 22)
    pygame.draw.line(screen, PATH_COLOR, (395, 230), (630, 560), 22)
    pygame.draw.line(screen, PATH_COLOR, (170, 600), (630, 600), 22)
    
    # POHON
    trees = [(40,300),(40,470),(40,630),(280,300),(280,470),(280,630),
             (480,300),(480,470),(480,630),(680,300),(680,470),(680,630)]
    for tx, ty in trees:
        pygame.draw.rect(screen, BROWN, (tx-3, ty, 6, 18))
        pygame.draw.circle(screen, (0,150,0), (tx, ty-10), 18)
        pygame.draw.circle(screen, (0,180,0), (tx-8, ty-5), 13)
        pygame.draw.circle(screen, (0,180,0), (tx+8, ty-5), 13)
    
    # ============================================================
    # GAMBAR EDGE (JALUR) DENGAN BOBOT
    # ============================================================
    
    for node1, neighbors in g.edges.items():
        for node2, weight in neighbors:
            if node1 > node2:
                continue
            
            pos1 = POSISI[node1]
            pos2 = POSISI[node2]
            
            color = DARK_GRAY
            width = 3
            
            # JALUR OPTIMAL (UCS)
            if game.path and node1 in game.path and node2 in game.path:
                idx1 = game.path.index(node1) if node1 in game.path else -1
                idx2 = game.path.index(node2) if node2 in game.path else -1
                if abs(idx1 - idx2) == 1:
                    color = GREEN
                    width = 10
                    pygame.draw.line(screen, (255,215,0), pos1, pos2, width+6)
                    pygame.draw.line(screen, (255,255,100), pos1, pos2, width+4)
            
            # JALUR YANG DILALUI PLAYER
            if game.player_path and game.player_index < len(game.player_path)-1:
                curr = game.player_path[game.player_index]
                nxt = game.player_path[game.player_index+1]
                if (node1 == curr and node2 == nxt) or (node1 == nxt and node2 == curr):
                    color = RED
                    width = 12
                    for i in range(3):
                        trail_color = (255, 255-i*30, 255-i*30)
                        pygame.draw.line(screen, trail_color, pos1, pos2, width+12-i*4)
            
            pygame.draw.line(screen, color, pos1, pos2, width)
            
            # BOBOT DI TENGAH JALUR
            mid = ((pos1[0]+pos2[0])//2, (pos1[1]+pos2[1])//2)
            bg_rect = pygame.Rect(mid[0]-18, mid[1]-10, 36, 20)
            pygame.draw.rect(screen, WHITE, bg_rect, border_radius=4)
            pygame.draw.rect(screen, DARK_GRAY, bg_rect, 1, border_radius=4)
            text = font_xsmall.render(str(weight), True, DARK)
            screen.blit(text, (mid[0]-text.get_width()//2, mid[1]-text.get_height()//2))
    
    # ============================================================
    # GAMBAR NODE (BANGUNAN)
    # ============================================================
    
    for node, pos in POSISI.items():
        w, h = UKURAN[node]
        x, y = pos[0] - w//2, pos[1] - h//2
        
        # BORDER STATUS
        if node in game.wajib:
            pygame.draw.rect(screen, YELLOW, (x-6, y-6, w+12, h+12), 4, border_radius=10)
        if node == game.start:
            pygame.draw.rect(screen, BLUE, (x-6, y-6, w+12, h+12), 4, border_radius=10)
        if node == game.expanding:
            for r in range(5, 0, -1):
                glow_color = (255, 255-r*20, 255-r*20)
                pygame.draw.rect(screen, glow_color, (x-r*5, y-r*5, w+r*10, h+r*10), 3, border_radius=10)
        
        # WARNA BANGUNAN
        color = WARNA[node]
        if node in game.explored and node not in [game.start]:
            color = (100,200,100)
        
        # GAMBAR BANGUNAN
        pygame.draw.rect(screen, color, (x, y, w, h), border_radius=10)
        pygame.draw.rect(screen, DARK, (x, y, w, h), 2, border_radius=10)
        
        # ATAP
        if node in ['P', 'A', 'R']:
            pygame.draw.polygon(screen, (180,80,50), [(x-2, y), (pos[0], y-20), (x+w+2, y)])
            pygame.draw.polygon(screen, DARK, [(x-2, y), (pos[0], y-20), (x+w+2, y)], 1)
        elif node in ['O', 'L']:
            pygame.draw.arc(screen, (180,80,50), (x-2, y-18, w+4, 22), math.pi, 0, 4)
            pygame.draw.arc(screen, DARK, (x-2, y-18, w+4, 22), math.pi, 0, 2)
        
        # NAMA BANGUNAN (BESAR DI DALAM)
        name = NAMA[node]
        if len(name) > 14:
            words = name.split()
            if len(words) >= 2:
                mid_point = len(words)//2
                line1 = " ".join(words[:mid_point])
                line2 = " ".join(words[mid_point:])
                text1 = font_med.render(line1, True, DARK)
                text2 = font_med.render(line2, True, DARK)
                screen.blit(text1, (pos[0]-text1.get_width()//2, pos[1]-18))
                screen.blit(text2, (pos[0]-text2.get_width()//2, pos[1]+6))
            else:
                text = font_med.render(name, True, DARK)
                screen.blit(text, (pos[0]-text.get_width()//2, pos[1]-8))
        else:
            text = font_med.render(name, True, DARK)
            screen.blit(text, (pos[0]-text.get_width()//2, pos[1]-8))
        
        # KODE SINGKAT
        code = font_xsmall.render(SINGKAT[node], True, DARK_GRAY)
        screen.blit(code, (pos[0]-code.get_width()//2, pos[1]+h//2-5))
        
        # IKON
        icon_text = font_med.render(IKON[node], True, DARK)
        screen.blit(icon_text, (pos[0]-icon_text.get_width()//2, pos[1]-h//2-22))
        
        # NILAI g(n) JIKA SUDAH DIEKSPLORASI
        if node in game.explored and node != game.start:
            for i, n in enumerate(game.path):
                if n == node:
                    cost_val = 0
                    for j in range(1, i+1):
                        cost_val += game.get_edge_cost(game.path[j-1], game.path[j])
                    g_text = font_xsmall.render(f"g={cost_val}", True, DARK_BLUE)
                    screen.blit(g_text, (pos[0]-g_text.get_width()//2, pos[1]+h//2+18))
                    break
    
    # ============================================================
    # GAMBAR PLAYER (ORANG BERJALAN)
    # ============================================================
    
    px, py = int(game.player_pos[0]), int(game.player_pos[1])
    
    pygame.draw.ellipse(screen, (0,0,0,80), (px-18, py+20, 36, 8))
    body_color = RED if not game.done else GREEN
    pygame.draw.circle(screen, body_color, (px, py-16), 14)
    
    leg_offset = int(8 * abs(game.player_leg_angle % 0.4 - 0.2) * 5) if game.player_moving else 0
    pygame.draw.line(screen, DARK_RED, (px-7, py-2), (px-12-leg_offset, py+20), 4)
    pygame.draw.line(screen, DARK_RED, (px+7, py-2), (px+12+leg_offset, py+20), 4)
    
    arm_offset = int(5 * abs(game.player_leg_angle % 0.4 - 0.2) * 5) if game.player_moving else 0
    pygame.draw.line(screen, DARK_RED, (px-12, py-7), (px-18-arm_offset, py+6), 3)
    pygame.draw.line(screen, DARK_RED, (px+12, py-7), (px+18+arm_offset, py+6), 3)
    
    pygame.draw.circle(screen, (255,220,200), (px, py-16), 14)
    pygame.draw.circle(screen, body_color, (px, py-16), 14, 2)
    pygame.draw.circle(screen, DARK, (px-5, py-18), 2)
    pygame.draw.circle(screen, DARK, (px+5, py-18), 2)

def draw_title():
    title = "🎓 UCS - Pencarian Rute Tercepat Kampus"
    text = font_big.render(title, True, NAVY)
    screen.blit(text, (390 - text.get_width()//2, 5))
    subtitle = "8 Lokasi | 25 Jalur | Pilih START & GOAL lalu klik GO"
    text = font_small.render(subtitle, True, DARK_GRAY)
    screen.blit(text, (390 - text.get_width()//2, 40))

# ============================================================
# 5. PANEL PERHITUNGAN - TANPA KOTAK + PERHITUNGAN BENAR
# ============================================================

def draw_math_panel(game, start_dropdown, goal_dropdown):
    x = 790
    y = 60
    width = 690
    height = 780
    
    # BACKGROUND
    s = pygame.Surface((width, height))
    s.set_alpha(250)
    s.fill((248,248,252))
    screen.blit(s, (x, y))
    pygame.draw.rect(screen, DARK_GRAY, (x, y, width, height), 1, border_radius=12)
    
    yy = y + 10
    line_x1 = x + 15
    line_x2 = x + width - 15
    
    # JUDUL
    title = font_big.render("📊 PERHITUNGAN UCS", True, NAVY)
    screen.blit(title, (x + width//2 - title.get_width()//2, yy))
    yy += 40
    
    # DROPDOWN + GO
    start_dropdown.rect.x = x + 20
    start_dropdown.rect.y = yy
    start_dropdown.rect.width = 200
    start_dropdown.rect.height = 35
    start_dropdown.draw(screen)
    
    goal_dropdown.rect.x = x + 250
    goal_dropdown.rect.y = yy
    goal_dropdown.rect.width = 200
    goal_dropdown.rect.height = 35
    goal_dropdown.draw(screen)
    
    go_rect = pygame.Rect(x + 480, yy, 80, 35)
    pygame.draw.rect(screen, GREEN, go_rect, border_radius=8)
    pygame.draw.rect(screen, DARK, go_rect, 2, border_radius=8)
    go_text = font_small.render("▶ GO", True, WHITE)
    screen.blit(go_text, (go_rect.x + 28, go_rect.y + 9))
    
    yy += 55
    pygame.draw.line(screen, DARK_GRAY, (line_x1, yy), (line_x2, yy), 1)
    yy += 12
    
    # INFORMASI START & GOAL
    start_label = font_small.render(f"START : {start_dropdown.selected}  ({NAMA[start_dropdown.selected]})", True, BLUE)
    screen.blit(start_label, (x + 20, yy))
    yy += 25
    
    goal_label = font_small.render(f"GOAL  : {goal_dropdown.selected}  ({NAMA[goal_dropdown.selected]})", True, ORANGE)
    screen.blit(goal_label, (x + 20, yy))
    yy += 30
    
    pygame.draw.line(screen, DARK_GRAY, (line_x1, yy), (line_x2, yy), 1)
    yy += 12
    
    # ============================================================
    # RUMUS UCS
    # ============================================================
    
    rumus_bg = pygame.Rect(x+15, yy, width-30, 85)
    pygame.draw.rect(screen, CREAM, rumus_bg, border_radius=8)
    pygame.draw.rect(screen, DARK_GRAY, rumus_bg, 1, border_radius=8)
    
    rumus_title = font_med.render("🧮 RUMUS UCS", True, DARK_RED)
    screen.blit(rumus_title, (x + 30, yy + 8))
    
    rumus1 = font_formula.render("g(n)  =  g(parent)  +  cost(parent, n)", True, DARK_BLUE)
    screen.blit(rumus1, (x + 30, yy + 38))
    
    rumus2 = font_math.render("Pilih node dengan g(n) TERKECIL dari Priority Queue", True, DARK)
    screen.blit(rumus2, (x + 30, yy + 62))
    
    yy += 100
    pygame.draw.line(screen, DARK_GRAY, (line_x1, yy), (line_x2, yy), 1)
    yy += 12
    
    # ============================================================
    # PERHITUNGAN STEP-BY-STEP
    # ============================================================
    
    step_title = font_med.render("📝 PERHITUNGAN STEP-BY-STEP", True, NAVY)
    screen.blit(step_title, (x + 20, yy))
    yy += 30
    
    if game.step > 0:
        # STEP SEKARANG
        step_text = font_small.render(f"STEP {game.step} :", True, DARK_BLUE)
        screen.blit(step_text, (x + 20, yy))
        yy += 24
        
        if game.expanding:
            # HITUNG COST NODE YANG DIEKSPANSI
            exp_cost = 0
            for i, n in enumerate(game.path):
                if n == game.expanding:
                    for j in range(1, i+1):
                        exp_cost += game.get_edge_cost(game.path[j-1], game.path[j])
                    break
            
            # EKSPANSI
            exp_text = font_math.render(f"Ekspansi : {game.expanding}     |     g({game.expanding}) = {exp_cost} menit", True, RED)
            screen.blit(exp_text, (x + 30, yy))
            yy += 24
            
            # PATH - pakai panah → BUKAN KOTAK
            path_str = " → ".join(game.path)
            path_text = font_math.render(f"Path     : {path_str}", True, DARK_BLUE)
            screen.blit(path_text, (x + 30, yy))
            yy += 24
            
            # BIAYA
            cost_text = font_math.render(f"Biaya    : {game.cost} menit", True, DARK_GREEN)
            screen.blit(cost_text, (x + 30, yy))
            yy += 28
        
        # ============================================================
        # PRIORITY QUEUE - TANPA KOTAK, PAKAI ∅
        # ============================================================
        
        pq_state = game.get_pq_state()
        if pq_state:
            pq_title = font_math.render("Priority Queue :", True, PURPLE)
            screen.blit(pq_title, (x + 20, yy))
            yy += 22
            
            for i, (c, n, v) in enumerate(pq_state[:5]):
                # PAKAI ∅ (himpunan kosong) BUKAN KOTAK
                v_str = ",".join(sorted(v)) if v else "∅"
                arrow = "▶" if i == 0 else " "
                color = DARK_GREEN if i == 0 else DARK
                pq_text = font_xsmall.render(f"{arrow}  {i+1}.  {n}    g({n}) = {c} m    [visited: {v_str}]", True, color)
                screen.blit(pq_text, (x + 30, yy))
                yy += 18
            
            if len(pq_state) > 5:
                more_text = font_xsmall.render(f"... +{len(pq_state)-5} lainnya", True, DARK_GRAY)
                screen.blit(more_text, (x + 30, yy))
                yy += 20
            
            if pq_state:
                next_text = font_math.render(f"Selanjutnya : {pq_state[0][1]}     (g = {pq_state[0][0]} m)", True, DARK_GREEN)
                screen.blit(next_text, (x + 20, yy))
                yy += 28
        
        # ============================================================
        # EXPLORED - pakai panah →
        # ============================================================
        
        if game.explored:
            expl_str = " → ".join(game.explored)
            expl_text = font_xsmall.render(f"Explored : {expl_str}", True, DARK_GRAY)
            screen.blit(expl_text, (x + 20, yy))
            yy += 24
        
        # ============================================================
        # PERHITUNGAN g(n) - PERHITUNGAN BENAR
        # ============================================================
        
        yy += 5
        formula_title = font_math.render("🔢 PERHITUNGAN g(n) :", True, NAVY)
        screen.blit(formula_title, (x + 20, yy))
        yy += 25
        
        if game.path and len(game.path) > 1:
            total = 0
            for i in range(len(game.path)-1):
                f_node = game.path[i]
                t_node = game.path[i+1]
                edge_cost = game.get_edge_cost(f_node, t_node)
                total += edge_cost
                
                if i == 0:
                    calc_text = font_xsmall.render(f"g({t_node}) = 0 + {edge_cost}  =  {total} menit", True, DARK)
                else:
                    prev_cost = total - edge_cost
                    calc_text = font_xsmall.render(f"g({t_node}) = {prev_cost} + {edge_cost}  =  {total} menit", True, DARK)
                screen.blit(calc_text, (x + 30, yy))
                yy += 20
            
            # TOTAL dengan background hijau
            total_bg = pygame.Rect(x+20, yy-2, 220, 28)
            pygame.draw.rect(screen, SOFT_GREEN, total_bg, border_radius=6)
            pygame.draw.rect(screen, DARK_GREEN, total_bg, 1, border_radius=6)
            total_text = font_math.render(f"✅ Total = {total} menit", True, DARK_GREEN)
            screen.blit(total_text, (x + 30, yy))
            yy += 40
    
    else:
        wait_text = font_med.render("⏳ Klik GO untuk mulai pencarian", True, DARK_GRAY)
        screen.blit(wait_text, (x + 20, yy))
        yy += 30
    
    # ============================================================
    # HASIL AKHIR
    # ============================================================
    
    yy += 5
    if game.done and game.found:
        result_bg = pygame.Rect(x+20, yy, width-40, 55)
        pygame.draw.rect(screen, DARK_GREEN, result_bg, border_radius=8)
        status = font_med.render("✅ RUTE OPTIMAL DITEMUKAN!", True, WHITE)
        screen.blit(status, (x + width//2 - status.get_width()//2, yy + 8))
        total_text = font_small.render(f"Total : {game.cost} menit     Rute : {' → '.join(game.path)}", True, WHITE)
        screen.blit(total_text, (x + width//2 - total_text.get_width()//2, yy + 33))
        
        yy += 70
        analisis_title = font_med.render("📊 ANALISIS OPTIMALITAS", True, NAVY)
        screen.blit(analisis_title, (x + 20, yy))
        yy += 28
        
        analisis1 = font_xsmall.render("✓ Semua edge cost ≥ 0  →  UCS menjamin optimal", True, DARK_GREEN)
        screen.blit(analisis1, (x + 30, yy))
        yy += 20
        
        analisis2 = font_xsmall.render(f"✓ Total biaya minimum = {game.cost} menit", True, DARK_GREEN)
        screen.blit(analisis2, (x + 30, yy))
        yy += 20
        
        analisis3 = font_xsmall.render(f"✓ Rute : {' → '.join(game.path)}", True, DARK_GREEN)
        screen.blit(analisis3, (x + 30, yy))
    
    return go_rect

def draw_buttons(game):
    buttons = [
        ("AUTO", (790, 750), 100, 40, GREEN),
        ("PAUSE", (900, 750), 100, 40, ORANGE),
        ("RESET", (1010, 750), 100, 40, RED),
        ("SPEED", (1120, 750), 100, 40, PURPLE),
    ]
    
    for label, pos, w, h, color in buttons:
        rect = pygame.Rect(pos[0], pos[1], w, h)
        pygame.draw.rect(screen, color, rect, border_radius=8)
        pygame.draw.rect(screen, DARK, rect, 2, border_radius=8)
        text = font_small.render(label, True, WHITE)
        screen.blit(text, (rect.x + rect.width//2 - text.get_width()//2, rect.y + rect.height//2 - text.get_height()//2))
        
        if label == "AUTO":
            game.btn_auto = rect
        elif label == "PAUSE":
            game.btn_pause = rect
        elif label == "RESET":
            game.btn_reset = rect
        elif label == "SPEED":
            game.btn_speed = rect

def draw_message(game):
    if game.message and pygame.time.get_ticks() - game.message_timer < 4000:
        banner = pygame.Surface((500, 35))
        banner.set_alpha(220)
        banner.fill(DARK_GREEN)
        screen.blit(banner, (140, 70))
        pygame.draw.rect(screen, DARK, (140, 70, 500, 35), 2, border_radius=6)
        text = font_small.render(game.message, True, WHITE)
        screen.blit(text, (160, 77))

# ============================================================
# 6. UCS GAME CLASS
# ============================================================

class UCSGame:
    def __init__(self):
        self.graph = g
        self.reset()
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.auto_mode = True
        self.auto_timer = 0
        self.auto_delay = 1000
        self.paused = False
        self.speed = 1
        self.speed_text = "1x"
        self.message = ""
        self.message_timer = 0
        self.goal_target = 'P'
    
    def reset(self):
        self.start = 'G'
        self.wajib = {'P'}
        self.end = 'P'
        
        self.pq = [(0, 'G', frozenset(), ['G'])]
        self.visited = {}
        self.explored = []
        self.path = []
        self.cost = 0
        self.step = 0
        self.done = False
        self.found = False
        self.expanding = None
        
        self.player_pos = POSISI['G']
        self.player_target = None
        self.player_moving = False
        self.player_path = []
        self.player_index = 0
        self.player_leg_angle = 0
        
        self.message = "🔄 Pilih START & GOAL lalu klik GO"
        self.message_timer = pygame.time.get_ticks()
    
    def set_start(self, node):
        self.start = node
        self.reset()
        self.start = node
        self.wajib = {self.goal_target}
        self.end = self.goal_target
        self.pq = [(0, node, frozenset(), [node])]
        self.player_pos = POSISI[node]
    
    def set_goal(self, node):
        self.goal_target = node
        self.wajib = {node}
        self.end = node
        self.reset()
        self.wajib = {node}
        self.end = node
        self.pq = [(0, self.start, frozenset(), [self.start])]
    
    def get_edge_cost(self, a, b):
        """Mengambil biaya edge dari graf - PASTIKAN BENAR"""
        for nxt, w in self.graph.get(a):
            if nxt == b:
                return w
        return 0
    
    def step_ucs(self):
        if not self.pq or self.done:
            return
        
        # Ambil node dengan biaya terkecil dari Priority Queue
        cost, node, v_set, path = heapq.heappop(self.pq)
        
        if node not in self.explored:
            self.explored.append(node)
        
        self.step += 1
        self.cost = cost
        self.path = path
        self.expanding = node
        
        self.message = f"📍 Step {self.step}: Ekspansi {node} (g(n)={cost}m)"
        self.message_timer = pygame.time.get_ticks()
        
        # Cek GOAL
        if self.wajib.issubset(v_set) and node == self.end:
            self.done = True
            self.found = True
            self.path = path
            self.cost = cost
            self.player_path = path
            self.player_index = 0
            self.message = f"🎉 RUTE OPTIMAL! Total: {cost} MENIT"
            self.message_timer = pygame.time.get_ticks()
            return
        
        # Ekspansi tetangga
        for nxt, w in self.graph.get(node):
            new_cost = cost + w
            new_set = set(v_set)
            if nxt in self.wajib:
                new_set.add(nxt)
            new_set = frozenset(new_set)
            
            state = (nxt, new_set)
            if state not in self.visited or new_cost < self.visited[state]:
                self.visited[state] = new_cost
                heapq.heappush(self.pq, (new_cost, nxt, new_set, path + [nxt]))
    
    def auto_play(self):
        if self.paused:
            return
        
        if not self.done and self.pq:
            now = pygame.time.get_ticks()
            if now - self.auto_timer > self.auto_delay:
                self.step_ucs()
                self.auto_timer = now
        elif self.done and self.player_index < len(self.player_path) - 1:
            self.move_player()
    
    def move_player(self):
        if self.player_index < len(self.player_path) - 1:
            next_node = self.player_path[self.player_index + 1]
            self.player_target = POSISI[next_node]
            self.player_moving = True
    
    def update_player(self):
        if self.player_moving and self.player_target:
            dx = self.player_target[0] - self.player_pos[0]
            dy = self.player_target[1] - self.player_pos[1]
            dist = (dx**2 + dy**2)**0.5
            
            self.player_leg_angle += 0.2
            
            if dist < 3:
                self.player_pos = self.player_target
                self.player_moving = False
                self.player_index += 1
                if self.player_index < len(self.player_path):
                    self.message = f"🚶 Tiba di {self.player_path[self.player_index]}"
                    self.message_timer = pygame.time.get_ticks()
            else:
                speed = 4 * self.speed
                self.player_pos = (
                    self.player_pos[0] + (dx / dist) * speed,
                    self.player_pos[1] + (dy / dist) * speed
                )
    
    def get_pq_state(self):
        return [(c, n, sorted(v)) for c, n, v, p in self.pq[:8]]

# ============================================================
# 7. MAIN
# ============================================================

def main():
    game = UCSGame()
    clock = pygame.time.Clock()
    
    all_nodes = g.get_all_nodes()
    start_dropdown = Dropdown(0, 0, 200, 35, all_nodes, 'G', "START")
    goal_dropdown = Dropdown(0, 0, 200, 35, all_nodes, 'P', "GOAL")
    
    game.btn_auto = pygame.Rect(790, 750, 100, 40)
    game.btn_pause = pygame.Rect(900, 750, 100, 40)
    game.btn_reset = pygame.Rect(1010, 750, 100, 40)
    game.btn_speed = pygame.Rect(1120, 750, 100, 40)
    
    game.auto_timer = pygame.time.get_ticks()
    go_rect = None
    
    while game.running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            
            start_dropdown.handle_event(event)
            goal_dropdown.handle_event(event)
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                
                if go_rect and go_rect.collidepoint(pos):
                    game.set_start(start_dropdown.selected)
                    game.set_goal(goal_dropdown.selected)
                    game.paused = False
                    game.auto_timer = pygame.time.get_ticks()
                    game.message = f"▶ Mencari rute dari {game.start} ke {game.goal_target}"
                    game.message_timer = pygame.time.get_ticks()
                
                if game.btn_auto.collidepoint(pos):
                    game.auto_mode = not game.auto_mode
                    if game.auto_mode:
                        game.paused = False
                        game.auto_timer = pygame.time.get_ticks()
                        game.message = "▶ Auto Play Aktif"
                    else:
                        game.message = "⏹ Auto Play Berhenti"
                    game.message_timer = pygame.time.get_ticks()
                
                elif game.btn_pause.collidepoint(pos):
                    game.paused = not game.paused
                    game.message = "⏸ PAUSE" if game.paused else "▶ Lanjut..."
                    game.message_timer = pygame.time.get_ticks()
                    if not game.paused:
                        game.auto_timer = pygame.time.get_ticks()
                
                elif game.btn_reset.collidepoint(pos):
                    game.set_start(start_dropdown.selected)
                    game.set_goal(goal_dropdown.selected)
                    game.paused = False
                    game.auto_timer = pygame.time.get_ticks()
                    game.message = "🔄 Reset! Mencari rute optimal..."
                    game.message_timer = pygame.time.get_ticks()
                
                elif game.btn_speed.collidepoint(pos):
                    speeds = [1, 2, 3, 5]
                    speed_labels = ["1x", "2x", "3x", "5x"]
                    idx = speeds.index(game.speed)
                    idx = (idx + 1) % len(speeds)
                    game.speed = speeds[idx]
                    game.speed_text = speed_labels[idx]
                    game.auto_delay = max(150, 1000 // game.speed)
                    game.message = f"⚡ Speed: {game.speed_text}"
                    game.message_timer = pygame.time.get_ticks()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.paused = not game.paused
                elif event.key == pygame.K_r:
                    game.set_start(start_dropdown.selected)
                    game.set_goal(goal_dropdown.selected)
                    game.paused = False
                    game.auto_timer = pygame.time.get_ticks()
                elif event.key == pygame.K_ESCAPE:
                    game.running = False
        
        if game.auto_mode and not game.paused:
            game.auto_play()
        
        if game.done and game.found:
            game.update_player()
        
        screen.fill(WHITE)
        draw_campus_map(game)
        draw_title()
        draw_buttons(game)
        go_rect = draw_math_panel(game, start_dropdown, goal_dropdown)
        draw_message(game)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()