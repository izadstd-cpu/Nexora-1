# game.py
import pygame
import sys
import random
import json
import datetime
import os
from settings import WIDTH, HEIGHT, FPS
from utils import load_image_safe, load_sound_safe, load_gif_safe, load_font_safe
from world import World, Camera
from entities import MysteryBox, Explosion, EnergyItem
from enemy import NormalEnemy, TankEnemy, PlaneEnemy, DroneEnemy, BossEnemy
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        # Mengaktifkan FULLSCREEN dan SCALED untuk performa dan tampilan konsisten
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.SCALED)
        pygame.display.set_caption("Nexora")
        self.clock = pygame.time.Clock()
        
    # --- 1. FONTS (TETAP SESUAIKAN DENGAN FILE KAMU) ---
        # Gunakan variabel khusus untuk judul utama agar tidak bentrok
        self.game_title_font = load_font_safe("Cyber Blast.otf", 150)
        
        # Font untuk UI, Menu, dan angka pakai Orbitron
        ui_font = "Orbitron.ttf" 
        self.font = load_font_safe(ui_font, 24)
        self.big_font = load_font_safe(ui_font, 60)
        self.title_font = load_font_safe(ui_font, 65) # Digunakan untuk judul menu lain
        self.stage_font = load_font_safe(ui_font, 40)

        # --- 2. MENU BACKGROUND (GIF) ---
        self.menu_bg_frames = load_gif_safe("backgrounds", "menu.gif", (WIDTH, HEIGHT))
        self.menu_bg_index = 0
        self.menu_bg_speed = 0.2

        # --- 3. SISTEM AUDIO ---
        self.master_vol = 0.5 
        self.music_vol = 0.5
        self.sfx_vol = 1
        
        self.shoot_sound = load_sound_safe("sounds", "shoot.wav")
        self.player_hit_sound = load_sound_safe("sounds", "hit_player.wav")
        self.enemy_hit_sound = load_sound_safe("sounds", "hit_enemy.wav")
        self.drone_hit_sound = load_sound_safe("sounds", "hit_drone.wav")
        self.menu_move_sound = load_sound_safe("sounds", "ketika_milih.mp3")
        self.menu_enter_sound = load_sound_safe("sounds", "ketika_enter.mp3")
        self.next_stage_sound = load_sound_safe("sounds", "next_stage.mp3")
        self.warning_sound = load_sound_safe("sounds", "warning.mp3")

        self.apply_volumes() 

        bgm_path = os.path.join("assets", "sounds", "bgm.mp3")
        try:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(self.music_vol * self.master_vol)
        except: pass

        # --- 4. ASET ITEMS & UI ---
        # Portal dan Tombol New Game
        self.portal_frames = [
            load_image_safe("items", "portal1.png", (60, 100)),
            load_image_safe("items", "portal2.png", (60, 100)),
            load_image_safe("items", "portal3.png", (60, 100)),
            load_image_safe("items", "portal4.png", (60, 100))
        ]
        self.portal_index = 0
        self.portal_speed = 0.2 
        
        # Tombol UI Baru
        btn_size = (220, 60)
        self.btn_new_game = load_image_safe("ui", "Button1.png", btn_size)
        self.btn_load_game = load_image_safe("ui", "Button2.png", btn_size)
        self.btn_options = load_image_safe("ui", "Button3.png", btn_size)
        self.btn_exit = load_image_safe("ui", "Button4.png", btn_size)
        
        self.menu_button_images = [
            self.btn_new_game,
            self.btn_load_game,
            self.btn_options,
            self.btn_exit
        ]

        # Ikon Nyawa (Love)
        love_size = (30, 30)
        self.icon_love_green = load_image_safe("ui", "LoveGreen.png", love_size)
        self.icon_love_grey = load_image_safe("ui", "LoveGrey.png", love_size)
        
        # --- ASET ENDING (CREDITS & STORY) ---
        self.story_box_img = load_image_safe("ui", "Story.png", (850, 400))
        self.credits_img = load_image_safe("ui", "Credits.png", (WIDTH, HEIGHT)) 
        self.enter_frames = [
            load_image_safe("ui", "Enter.png", (100, 40)),
            load_image_safe("ui", "Enter2.png", (100, 40))
        ]
        self.enter_anim_index = 0
        self.credits_y = HEIGHT

        # ---> TAMBAHKAN KODE INI UNTUK ANIMASI BOS MATI <---
        self.boss_death_frames = []
        for i in range(1, 8): 
            # Jika format aslimu .jpg, ubah tulisan ".png" di bawah ini menjadi ".jpg"
            nama_file = f"bos_mati{i}.png" 
            img = load_image_safe("enemies", nama_file, (200, 200))
            
            if img is not None:
                self.boss_death_frames.append(img)
                # Mencetak pesan di terminal jika gambar berhasil ditemukan
                print(f"[DEBUG] Berhasil memuat aset: {nama_file}") 
            else:
                # Mencetak peringatan jika gambar gagal ditemukan
                print(f"[ERROR] GAGAL memuat: {nama_file} - Cek kembali letak dan nama filenya!")
            
        self.boss_death_index = 0
        self.boss_death_x = 0
        self.boss_death_y = 0

        # --- 5. PENGATURAN MENU & STATE ---
        self.state = "MENU"
        self.menu_options = ["NEW GAME", "LOAD GAME", "OPTIONS", "EXIT"]
        self.menu_index = 0
        
        self.options_menu = ["MASTER VOL", "MUSIC VOL", "SFX VOL", "BACK"]
        self.options_index = 0
        self.exit_index = 0
        self.ingame_exit_index = 1
        
        self.save_file = "savegame.json"
        self.saved_games_list = []
        self.load_menu_index = 0
        self.warmup_timer = 0
        
        self.reset_game_data()

    def apply_volumes(self):
        """Menerapkan pengaturan volume ke musik dan seluruh SFX."""
        pygame.mixer.music.set_volume(self.music_vol * self.master_vol)
        current_sfx_power = self.sfx_vol * self.master_vol
        sfx_list = [self.shoot_sound, self.player_hit_sound, self.enemy_hit_sound, 
                    self.drone_hit_sound, self.menu_move_sound, self.menu_enter_sound, 
                    self.next_stage_sound, self.warning_sound]
        for snd in sfx_list:
            if snd: snd.set_volume(current_sfx_power)

    def reset_game_data(self, load_data=None):
        """Mereset data permainan untuk New Game atau Load Game."""
        self.bullets = []; self.enemy_bullets = []; self.enemies = []; self.items = [] 
        self.player = Player(150, 100, self.bullets, self.shoot_sound)
        self.camera = Camera(WIDTH)
        self.score = 0; self.stage = 1
        self.portal_active = False; self.portal_rect = None
        self.explosions = []
        
        if load_data:
            self.score = load_data.get("score", 0)
            self.stage = load_data.get("stage", 1)
            self.player.set_lives(load_data.get("lives", 3))
            self.player.set_hp(load_data.get("hp", 100))
            self.player.rect.x = load_data.get("player_x", 150)
            self.camera.x = load_data.get("camera_x", 0)
            
        self.world = World(WIDTH, HEIGHT, self.stage)
        self.enemy_spawn_timer = 0; self.item_spawn_timer = 0
        self.boss_spawned = False

    def fetch_saves(self):
        """Membaca daftar save game dari file JSON."""
        if os.path.exists(self.save_file):
            with open(self.save_file, "r") as f:
                try:
                    data = json.load(f)
                    return [data] if isinstance(data, dict) else data
                except: return []
        return []

    def save_game(self):
        """Menyimpan data permainan saat ini ke file JSON."""
        new_save = {
            "score": self.score, "stage": self.stage,
            "lives": self.player.get_lives(), "hp": self.player.get_hp(),       
            "player_x": self.player.rect.x, "camera_x": self.camera.x,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        saves = self.fetch_saves()
        saves.insert(0, new_save) 
        if len(saves) > 5: saves = saves[:5] # Batasi maksimal 5 save
        with open(self.save_file, "w") as f: json.dump(saves, f)

    def load_specific_game(self, data):
        """Memuat data permainan spesifik dan mengatur kamera."""
        self.reset_game_data(load_data=data)
        self.camera.update(self.player.rect.centerx) 

    def check_portal_and_stage(self, keys):
        """Mengecek apakah score cukup untuk memunculkan portal stage selanjutnya."""
        current_score = int(self.camera.x // 10) + self.score
        if current_score >= self.stage * 500 and not self.portal_active and self.stage < 5:
            self.portal_active = True
            portal_x = self.camera.x + WIDTH + 50
            self.world.max_x = portal_x + 150 
            self.camera.max_x = self.world.max_x
            self.portal_rect = pygame.Rect(portal_x, self.world.get_ground_y(portal_x + 30) - 100, 60, 100)

        if self.portal_active and self.portal_rect and self.player.rect.colliderect(self.portal_rect) and keys[pygame.K_RETURN]:
            if self.next_stage_sound: self.next_stage_sound.play()
            self.next_stage()
            
    def check_boss_spawn(self):
        """Mengecek apakah skor di stage 5 sudah cukup untuk memanggil Bos."""
        current_score = int(self.camera.x // 10) + self.score
        if self.stage == 5 and current_score >= 2500 and not self.boss_spawned:
            self.boss_spawned = True
            self.state = "BOSS_WARNING"
            self.warning_timer = FPS * 3 
            if self.warning_sound: 
                self.warning_sound.play()

    def next_stage(self):
        """Mengatur transisi ke stage berikutnya."""
        self.score += int(self.camera.x // 10) 
        self.stage += 1
        self.bullets.clear(); self.enemy_bullets.clear(); self.enemies.clear(); self.items.clear(); self.explosions.clear()
        self.player.rect.x = 150; self.player.rect.y = 50
        self.camera.x = 0; self.world = World(WIDTH, HEIGHT, self.stage)
        self.camera.max_x = float('inf'); self.portal_active = False; self.portal_rect = None

    def spawn_enemies(self): 
        boss_shielded = False
        if getattr(self, 'boss_spawned', False):
            for enemy in self.enemies:
                if getattr(enemy, 'enemy_type', '') == 'boss' and getattr(enemy, 'shield_active', False):
                    boss_shielded = True
        
        if self.portal_active or (getattr(self, 'boss_spawned', False) and not boss_shielded):
            return
        
        self.enemy_spawn_timer += 1
        
        screen_min = self.camera.x - 300
        screen_max = self.camera.x + WIDTH + 300
        visible_enemies = [e for e in self.enemies if screen_min <= e.rect.centerx <= screen_max]
        
        normal_count = sum(1 for e in visible_enemies if e.enemy_type == 'normal')
        drone_count = sum(1 for e in visible_enemies if e.enemy_type == 'drone')
        plane_count = sum(1 for e in visible_enemies if e.enemy_type == 'plane')
        
        tank_exists = any(e.enemy_type == 'tank' for e in self.enemies)

        max_normal = 6 if self.stage == 1 else (8 if self.stage in [3, 4] else (10 if self.stage == 5 else 0))

        available_types = []
        if self.stage in [1, 3, 4, 5] and normal_count < max_normal:
            available_types.append('normal')
        if self.stage == 2 and plane_count < 5:
            available_types.append('plane')
        if self.stage in [3, 4, 5] and drone_count < 2:
            available_types.append('drone')
        
        if self.stage in [4, 5] and not tank_exists and not boss_shielded:
            available_types.append('tank')

        if not available_types:
            return

        base_delay = 30 if ('drone' in available_types and drone_count < 2) else max(20, (120 - (self.stage * 15)) - (self.score // 20))
        if self.stage >= 5 and 'drone' not in available_types: base_delay = 15
        
        if boss_shielded: base_delay = 20

        if self.enemy_spawn_timer >= base_delay:
            self.enemy_spawn_timer = 0
            chosen_type = random.choice(available_types)
        
            if chosen_type == 'tank':
                x = self.camera.x + WIDTH + 100 
            else:
                x = self.camera.x - 100 if random.choice(["kiri", "kanan"]) == "kiri" else self.camera.x + WIDTH + 100
                
            spawn_y = random.randint(50, HEIGHT - 150) if chosen_type in ['plane', 'drone'] else 100
            
            if chosen_type == 'plane': self.enemies.append(PlaneEnemy(x, spawn_y, self.player, self.stage))
            elif chosen_type == 'drone': self.enemies.append(DroneEnemy(x, spawn_y, self.player, self.stage))
            elif chosen_type == 'tank': self.enemies.append(TankEnemy(x, spawn_y, self.player, self.stage))
            else: self.enemies.append(NormalEnemy(x, spawn_y, self.player, self.stage))

    def spawn_items(self):
        self.item_spawn_timer += 1
        if self.item_spawn_timer > 300:
            if random.randint(1, 100) <= 50:
                max_x = self.world.max_x - 50 if self.world.max_x != float('inf') else self.camera.x + WIDTH
                x = max(self.camera.x + 50, min(self.player.rect.x + random.randint(100, 300), max_x))
                self.items.append(MysteryBox(x, 0, self.stage))
            self.item_spawn_timer = 0

    def collision_check(self):
        """Menangani seluruh logika kolisi dan batasan dunia."""
        if self.player.rect.left < self.camera.x: self.player.rect.left = self.camera.x
        if self.player.rect.right > self.world.max_x: self.player.rect.right = self.world.max_x

        if self.stage == 2:
            if self.player.rect.top < 0: self.player.rect.top = 0
            if self.player.rect.bottom > HEIGHT: self.player.rect.bottom = HEIGHT
            self.player.on_ground = False
        else:
            player_ground_y = self.world.get_ground_y(self.player.rect.centerx)
            if self.player.rect.bottom >= player_ground_y:
                self.player.rect.bottom = player_ground_y; self.player._vel_y = 0; self.player.on_ground = True
            else: self.player.on_ground = False
                
        for enemy in self.enemies:
            if enemy.enemy_type not in ['plane', 'drone', 'boss']:
                enemy_ground_y = self.world.get_ground_y(enemy.rect.centerx)
                if enemy.rect.bottom >= enemy_ground_y: enemy.rect.bottom = enemy_ground_y; enemy._vel_y = 0   

        for item in self.items:
            if item.rect.bottom >= self.world.get_ground_y(item.rect.centerx): item.rect.bottom = self.world.get_ground_y(item.rect.centerx); item._vel_y = 0    
            if self.player.rect.colliderect(item.rect):
                item.active = False
                if isinstance(item, EnergyItem):
                    self.player.shield_energy = min(100, self.player.shield_energy + 50)
                else:
                    self.player.weapon_type = random.choice(['machine_gun', 'shotgun'])
                    self.player.weapon_timer = FPS * 5 

        for bullet in self.bullets:
            for enemy in self.enemies:
                if getattr(enemy, 'shield_active', False):
                    continue
                    
                if bullet.rect.colliderect(enemy.rect):
                    bullet.active = False; enemy.hp -= 10 
                    
                    if enemy.hp <= 0:
                        if getattr(enemy, 'enemy_type', '') == 'boss' and getattr(enemy, 'phase', 1) < 4:
                            enemy.phase = 4
                            enemy.hp = enemy.max_hp
                            enemy.state = 'fall_to_ground'
                        else:
                            enemy.active = False   
                            self.explosions.append(Explosion(enemy.rect.centerx, enemy.rect.centery))
                            
                            # --- MODIFIKASI: TRIGGER ANIMASI BOS MATI ---
                            if enemy.enemy_type == 'boss':
                                self.score += 2000 
                                
                                # Simpan posisi bos terakhir untuk memutar animasi di titik yang sama
                                self.boss_death_x = enemy.rect.x
                                self.boss_death_y = enemy.rect.y
                                self.boss_death_index = 0 # Mulai dari frame pertama
                                
                                # Masuk ke state animasi
                                self.state = "BOSS_DYING" 
                                
                                self.enemies.clear() 
                                self.enemy_bullets.clear() 
                            else:
                                if self.stage >= 3 and random.randint(1, 100) <= 35: 
                                    self.items.append(EnergyItem(enemy.rect.centerx, enemy.rect.centery))
                                
                                if enemy.enemy_type in ['drone', 'plane']:
                                    if self.drone_hit_sound: self.drone_hit_sound.play()
                                else:
                                    if self.enemy_hit_sound: self.enemy_hit_sound.play()
                                    
                                if enemy.enemy_type == 'tank': self.score += 30
                                else: self.score += 10 
                    break

        for eb in self.enemy_bullets[:]:
            if eb.rect.colliderect(self.player.rect):
                eb.active = False
                if not getattr(self.player, 'shield_active', False): 
                    self.player.take_damage(10)
                    if self.player_hit_sound: self.player_hit_sound.play() 
            
        for enemy in self.enemies:
            # Hitbox dinamis untuk bos
            hitbox = enemy.rect.inflate(-15, -10)
            
            if getattr(enemy, 'enemy_type', '') == 'boss' and getattr(enemy, 'state', '') in ['charge', 'dash']:
                hitbox = pygame.Rect(enemy.rect.left + 20, enemy.rect.bottom - 60, enemy.rect.width - 40, 60)
            
            if self.player.rect.colliderect(hitbox):
                old_hp = self.player.get_hp()
                
                if getattr(enemy, 'enemy_type', '') == 'boss' and getattr(enemy, 'state', '') == 'dash':
                    self.player.take_damage(25) 
                else:
                    self.player.take_damage(20)
                    
                if self.player.get_hp() < old_hp: 
                    if self.player_hit_sound: self.player_hit_sound.play()
                    
                if self.player.get_lives() <= 0: self.state = "GAME_OVER"

    def draw_ui(self):
        """Menggambar seluruh elemen Heads-Up Display (HUD) saat bermain."""
        self.screen.blit(self.font.render(f"Score: {int(self.camera.x // 10) + self.score}", True, (255, 255, 255)), (20, 60))
        
        stage_text = self.stage_font.render("FINAL STAGE" if self.stage >= 5 else f"Stage {self.stage}", True, (255, 0, 0) if self.stage >= 5 else (255, 255, 255))
        self.screen.blit(stage_text, (WIDTH // 2 - stage_text.get_width() // 2, 20))
        
        bar_x = (self.player.rect.centerx - self.camera.x) - 15; bar_y = self.player.rect.top - 10
        pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, 30, 5)) 
        pygame.draw.rect(self.screen, (0, 255, 0), (bar_x, bar_y, int(30 * (self.player.get_hp() / 100.0)), 5)) 
        
        if self.stage >= 3:
            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y - 8, 30, 5)) 
            pygame.draw.rect(self.screen, (0, 255, 255), (bar_x, bar_y - 8, int(30 * (self.player.shield_energy / 100.0)), 5)) 
        
        lives_text_surf = self.font.render("Lives:", True, (255, 215, 0))
        text_x, text_y = 20, 20
        self.screen.blit(lives_text_surf, (text_x, text_y))
        
        icon_x_start = text_x + lives_text_surf.get_width() + 10
        icon_y = text_y + (lives_text_surf.get_height() // 2) - (self.icon_love_green.get_height() // 2)
        icon_spacing = 35 
        
        current_lives = self.player.get_lives()
        max_lives_possible = 3 
        
        for i in range(max_lives_possible):
            x_pos = icon_x_start + i * icon_spacing
            if i < current_lives:
                self.screen.blit(self.icon_love_green, (x_pos, icon_y))
            else:
                self.screen.blit(self.icon_love_grey, (x_pos, icon_y))
        
        if self.player.weapon_timer > 0:
            weapon_icon = load_image_safe("items", f"{self.player.weapon_type}.png", (30, 30))
            icon_x = WIDTH - 350
            icon_y = 10
            self.screen.blit(weapon_icon, (icon_x, icon_y))
            weapon_text = self.font.render(f"{self.player.weapon_type.upper()} ({self.player.weapon_timer // FPS + 1}s)", True, (0, 255, 255))
            self.screen.blit(weapon_text, (icon_x + 40, icon_y + 5))

        if self.portal_active and self.portal_rect:
            self.portal_index += self.portal_speed
            if self.portal_index >= len(self.portal_frames):
                self.portal_index = 0
            
            layar_portal_x = self.portal_rect.x - self.camera.x
            self.screen.blit(self.portal_frames[int(self.portal_index)], (layar_portal_x, self.portal_rect.y))
            
            if self.player.rect.colliderect(self.portal_rect):
                self.screen.blit(self.font.render("PRESS ENTER", True, (255, 255, 0)), (layar_portal_x - 30, self.portal_rect.y - 40))
                
        # --- BAR HP BOSS ---
        if getattr(self, 'boss_spawned', False):
            for enemy in self.enemies:
                if enemy.enemy_type == 'boss':
                    bar_w = 400
                    bar_h = 20
                    bar_x = (WIDTH // 2) - (bar_w // 2)
                    bar_y = 70  
                    
                    pygame.draw.rect(self.screen, (50, 50, 50), (bar_x, bar_y, bar_w, bar_h))
                    hp_ratio = max(0, enemy.hp) / enemy.max_hp
                    pygame.draw.rect(self.screen, (255, 0, 0), (bar_x, bar_y, int(bar_w * hp_ratio), bar_h))
                    pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, bar_w, bar_h), 2)
                    
                    boss_font = self.font.render("BOSS", True, (255, 255, 255))
                    self.screen.blit(boss_font, (WIDTH // 2 - boss_font.get_width() // 2, bar_y - 25))
                    break 

    def run(self):
        """Loop utama permainan (Game Loop)."""
        while True:
            self.screen.fill((0, 0, 0)) 
            keys = pygame.key.get_pressed()
            
            # --- MENANGANI INPUT EVENT (Keyboard/Quit) ---
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.state in ["PLAYING", "PAUSED", "INGAME_MENU"]: self.save_game()
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    if self.state == "MENU":
                        if event.key in [pygame.K_UP, pygame.K_DOWN]:
                            if self.menu_move_sound: self.menu_move_sound.play()
                            if event.key == pygame.K_UP: self.menu_index = (self.menu_index - 1) % len(self.menu_options)
                            elif event.key == pygame.K_DOWN: self.menu_index = (self.menu_index + 1) % len(self.menu_options)
                        elif event.key == pygame.K_RETURN:
                            if self.menu_enter_sound: self.menu_enter_sound.play()
                            selected = self.menu_options[self.menu_index]
                            if selected == "NEW GAME":
                                self.reset_game_data(); self.state = "WARMUP"; self.warmup_timer = FPS * 4 
                            elif selected == "LOAD GAME":
                                self.saved_games_list = self.fetch_saves(); self.state = "LOAD_MENU"; self.load_menu_index = 0
                            elif selected == "OPTIONS": self.state = "OPTIONS"; self.options_index = 0 
                            elif selected == "EXIT": self.state = "EXIT_CONFIRM"; self.exit_index = 1 

                    elif self.state == "LOAD_MENU":
                        if event.key == pygame.K_ESCAPE: 
                            if self.menu_enter_sound: self.menu_enter_sound.play()
                            self.state = "MENU"
                        elif event.key in [pygame.K_UP, pygame.K_DOWN] and len(self.saved_games_list) > 0: 
                            if self.menu_move_sound: self.menu_move_sound.play()
                            if event.key == pygame.K_UP: self.load_menu_index = (self.load_menu_index - 1) % len(self.saved_games_list)
                            elif event.key == pygame.K_DOWN: self.load_menu_index = (self.load_menu_index + 1) % len(self.saved_games_list)
                        elif event.key == pygame.K_RETURN and len(self.saved_games_list) > 0:
                            if self.menu_enter_sound: self.menu_enter_sound.play()
                            self.load_specific_game(self.saved_games_list[self.load_menu_index])
                            self.state = "WARMUP"; self.warmup_timer = FPS * 4
                        elif event.key == pygame.K_DELETE and len(self.saved_games_list) > 0:
                            if self.menu_enter_sound: self.menu_enter_sound.play()
                            self.saved_games_list.pop(self.load_menu_index)
                            with open(self.save_file, "w") as f: 
                                json.dump(self.saved_games_list, f)
                            if self.load_menu_index >= len(self.saved_games_list):
                                self.load_menu_index = max(0, len(self.saved_games_list) - 1)

                    elif self.state == "EXIT_CONFIRM":
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]: 
                            if self.menu_move_sound: self.menu_move_sound.play(); self.exit_index = 1 - self.exit_index 
                        elif event.key == pygame.K_RETURN:
                            if self.menu_enter_sound: self.menu_enter_sound.play()
                            if self.exit_index == 0: pygame.quit(); sys.exit() 
                            else: self.state = "MENU" 
                                
                    elif self.state == "OPTIONS":
                        if event.key == pygame.K_ESCAPE: 
                            if self.menu_enter_sound: self.menu_enter_sound.play(); self.state = "MENU"
                        elif event.key in [pygame.K_UP, pygame.K_DOWN]:
                            if self.menu_move_sound: self.menu_move_sound.play()
                            if event.key == pygame.K_UP: self.options_index = (self.options_index - 1) % len(self.options_menu)
                            elif event.key == pygame.K_DOWN: self.options_index = (self.options_index + 1) % len(self.options_menu)
                        elif event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                            if self.menu_move_sound: self.menu_move_sound.play()
                            sel_opt = self.options_menu[self.options_index]
                            change = -0.1 if event.key == pygame.K_LEFT else 0.1
                            if sel_opt == "MASTER VOL": self.master_vol = max(0.0, min(1.0, self.master_vol + change))
                            elif sel_opt == "MUSIC VOL": self.music_vol = max(0.0, min(1.0, self.music_vol + change))
                            elif sel_opt == "SFX VOL": self.sfx_vol = max(0.0, min(1.0, self.sfx_vol + change))
                            self.apply_volumes()
                        elif event.key == pygame.K_RETURN and self.options_menu[self.options_index] == "BACK": 
                            if self.menu_enter_sound: self.menu_enter_sound.play(); self.state = "MENU"

                    elif self.state == "PLAYING" and event.key == pygame.K_ESCAPE:
                        if self.menu_enter_sound: self.menu_enter_sound.play()
                        self.state = "INGAME_MENU"; self.ingame_exit_index = 1 
                    elif self.state == "INGAME_MENU":
                        if event.key in [pygame.K_LEFT, pygame.K_RIGHT]: 
                            if self.menu_move_sound: self.menu_move_sound.play(); self.ingame_exit_index = 1 - self.ingame_exit_index 
                        elif event.key == pygame.K_RETURN:
                            if self.menu_enter_sound: self.menu_enter_sound.play()
                            if self.ingame_exit_index == 0: self.save_game(); self.state = "MENU" 
                            else: self.state = "PLAYING" 
                        elif event.key == pygame.K_ESCAPE: 
                            if self.menu_enter_sound: self.menu_enter_sound.play(); self.state = "PLAYING" 
                    elif self.state == "PLAYING" and event.key == pygame.K_p: self.state = "PAUSED"
                    elif self.state == "PAUSED" and event.key == pygame.K_r: self.state = "PLAYING"
                    elif self.state == "GAME_OVER" and event.key == pygame.K_RETURN: 
                        if self.menu_enter_sound: self.menu_enter_sound.play(); self.state = "MENU"

                    # KODE KEYBOARD UNTUK ENDING
                    elif self.state == "ENDING_STORY":
                        if event.key == pygame.K_RETURN:
                            if self.menu_enter_sound: self.menu_enter_sound.play()
                            self.state = "ENDING_CREDITS"
                            self.credits_y = HEIGHT 
                            
                    elif self.state == "ENDING_CREDITS":
                        target_y = 0 
                        if event.key == pygame.K_RETURN and self.credits_y <= target_y:
                            if self.menu_enter_sound: self.menu_enter_sound.play()
                            self.state = "MENU" 

            # --- RENDERING MENU UTAMA ---
            if self.state == "MENU":
                if len(self.menu_bg_frames) > 0:
                    self.menu_bg_index += self.menu_bg_speed
                    if self.menu_bg_index >= len(self.menu_bg_frames): self.menu_bg_index = 0
                    self.screen.blit(self.menu_bg_frames[int(self.menu_bg_index)], (0, 0))
                title = self.game_title_font.render("N E X O R A", True, (0, 255, 255))
                self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 80))
                
                y_start = 260
                y_step = 70 

                for i, option in enumerate(self.menu_options):
                    current_btn_img = self.menu_button_images[i]
                    target_y = y_start + i * y_step

                    if i == self.menu_index:
                        orig_size = current_btn_img.get_size()
                        scale_factor = 1.1 
                        scaled_size = (int(orig_size[0] * scale_factor), int(orig_size[1] * scale_factor))
                        scaled_btn = pygame.transform.scale(current_btn_img, scaled_size)
                        
                        btn_rect = scaled_btn.get_rect(center=(WIDTH//2, target_y))
                        self.screen.blit(scaled_btn, btn_rect)
                        pygame.draw.rect(self.screen, (255, 255, 0), btn_rect.inflate(6, 6), 3, border_radius=10)
                    else:
                        btn_rect = current_btn_img.get_rect(center=(WIDTH//2, target_y))
                        self.screen.blit(current_btn_img, btn_rect)
                    
            elif self.state == "LOAD_MENU":
                title = self.title_font.render("LOAD GAME", True, (0, 255, 255))
                self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
                
                if len(self.saved_games_list) == 0:
                    text = self.font.render("TIDAK ADA DATA SAVE", True, (255, 0, 0))
                    self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 250))
                else:
                    for i, save in enumerate(self.saved_games_list):
                        color = (255, 255, 0) if i == self.load_menu_index else (255, 255, 255)
                        text = self.font.render(f"Stage {save['stage']} - Score: {save['score']} - {save['timestamp']}", True, color)
                        self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 150 + i * 40))
                
                instruction_text = "ENTER: Load  |  DELETE: Hapus  |  ESC: Kembali"
                back_text = self.font.render(instruction_text, True, (150, 150, 150))
                self.screen.blit(back_text, (WIDTH//2 - back_text.get_width()//2, HEIGHT - 50))

            elif self.state == "OPTIONS":
                title = self.title_font.render("OPTIONS", True, (0, 255, 255))
                self.screen.blit(title, (WIDTH//2 - title.get_width()//2, 50))
                for i, opt in enumerate(self.options_menu):
                    color = (255, 255, 0) if i == self.options_index else (255, 255, 255)
                    val_text = ""
                    if opt == "MASTER VOL": val_text = f": {int(self.master_vol * 100)}%"
                    elif opt == "MUSIC VOL": val_text = f": {int(self.music_vol * 100)}%"
                    elif opt == "SFX VOL": val_text = f": {int(self.sfx_vol * 100)}%"
                    text = self.font.render(f"{opt}{val_text}", True, color)
                    self.screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i * 50))

            elif self.state == "EXIT_CONFIRM":
                q_text = self.title_font.render("KELUAR DARI GAME?", True, (255, 0, 0))
                self.screen.blit(q_text, (WIDTH//2 - q_text.get_width()//2, HEIGHT//2 - 80))
                yes_col = (255, 255, 0) if self.exit_index == 0 else (255, 255, 255)
                no_col = (255, 255, 0) if self.exit_index == 1 else (255, 255, 255)
                y_text = self.font.render("YES", True, yes_col); n_text = self.font.render("NO", True, no_col)
                self.screen.blit(y_text, (WIDTH//2 - 100 - y_text.get_width()//2, HEIGHT//2 + 20))
                self.screen.blit(n_text, (WIDTH//2 + 100 - n_text.get_width()//2, HEIGHT//2 + 20))

            elif self.state == "WARMUP":
                self.world.draw(self.screen, self.camera.x)
                self.screen.blit(self.player.image, (self.player.rect.x - self.camera.x, self.player.rect.y))
                overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(150); overlay.fill((0, 0, 0))
                self.screen.blit(overlay, (0,0))
                welcome = self.title_font.render("WELCOME TO CYBERPUNK", True, (255, 0, 255))
                self.screen.blit(welcome, (WIDTH//2 - welcome.get_width()//2, 100))
                secs = self.warmup_timer // FPS
                count_text = self.title_font.render(str(secs) if secs > 0 else "READY, SET, GO!", True, (0, 255, 255) if secs > 0 else (0, 255, 0))
                self.screen.blit(count_text, (WIDTH//2 - count_text.get_width()//2, HEIGHT//2))
                self.warmup_timer -= 1
                if self.warmup_timer <= -FPS // 2: self.state = "PLAYING"
                
            elif self.state == "BOSS_WARNING":
                self.player.move(keys, self.stage)
                self.player.update(self.stage)
                self.collision_check() 
                
                self.world.draw(self.screen, self.camera.x)
                self.screen.blit(self.player.image, (self.player.rect.x - self.camera.x, self.player.rect.y))
                self.draw_ui()
                
                if (self.warning_timer // 15) % 2 == 0:
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.set_alpha(120)
                    overlay.fill((255, 0, 0))
                    self.screen.blit(overlay, (0, 0))
                    
                    warn_text = self.game_title_font.render("WARNING!!!", True, (255, 255, 0))
                    self.screen.blit(warn_text, (WIDTH//2 - warn_text.get_width()//2, HEIGHT//2 - warn_text.get_height()//2))
                
                self.warning_timer -= 1
                
                if self.warning_timer <= 0:
                    self.world.change_map("mapbos.png")
                    
                    self.enemies.clear() 
                    self.enemy_bullets.clear()
                    
                    min_x = self.camera.x + 50
                    max_x = self.camera.x + WIDTH - 150
                    boss_x = max_x
                    boss_y = 100 
                    self.enemies.append(BossEnemy(boss_x, boss_y, self.player, self.stage, min_x, max_x))
                    
                    self.world.max_x = self.camera.x + WIDTH
                    self.camera.max_x = self.world.max_x
                    
                    self.state = "PLAYING"

            elif self.state in ["PLAYING", "PAUSED", "GAME_OVER", "INGAME_MENU"]: 
                if self.state == "PLAYING":
                    self.check_portal_and_stage(keys)
                    self.check_boss_spawn() 
                    
                    if self.stage == 5 and getattr(self, 'boss_spawned', False):
                        current_score = int(self.camera.x // 10) + self.score
                        for enemy in self.enemies:
                            if getattr(enemy, 'enemy_type', '') == 'boss':
                                if getattr(enemy, 'phase', 1) == 2 and not hasattr(self, 'phase2_target_score'):
                                    self.phase2_target_score = current_score + 250
                                if getattr(enemy, 'phase', 1) == 2 and hasattr(self, 'phase2_target_score'):
                                    if current_score >= self.phase2_target_score:
                                        enemy.shield_active = False
                                        enemy.state = 'stunned'
                                        enemy.stun_timer = FPS * 3
                                        enemy.phase = 3
                                        del self.phase2_target_score
                                        self.enemies = [e for e in self.enemies if getattr(e, 'enemy_type', '') == 'boss']
                    
                    self.player.move(keys, self.stage)
                    self.spawn_enemies() 
                    self.spawn_items()
                    self.player.update(self.stage)
                    
                    for list_ent in [self.bullets, self.enemy_bullets, self.items, self.explosions]:
                        for ent in list_ent: ent.update(self.camera.x) if hasattr(ent, 'update') and 'camera_x' in ent.update.__code__.co_varnames else ent.update()
                    
                    for enemy in self.enemies: enemy.update(self.enemy_bullets) 
                    
                    self.camera.update(self.player.rect.centerx)
                    self.collision_check()
                    
                    self.bullets[:] = [b for b in self.bullets if b.active]
                    self.enemy_bullets[:] = [eb for eb in self.enemy_bullets if eb.active]
                    self.enemies[:] = [e for e in self.enemies if e.active]
                    self.items[:] = [i for i in self.items if i.active]
                    self.explosions[:] = [ex for ex in self.explosions if ex.active]

                # --- DRAWING / RENDERING GAMEPLAY ---
                self.world.draw(self.screen, self.camera.x)
                
                entity_lists = [self.items, [self.player], self.enemies, self.explosions]
                for e_list in entity_lists:
                    for e in e_list: 
                        self.screen.blit(e.image, (e.rect.x - self.camera.x, e.rect.y))
                        if hasattr(e, 'draw_shield'): e.draw_shield(self.screen, self.camera.x)
                        
                        if getattr(e, 'enemy_type', '') == 'boss':
                            if getattr(e, 'shield_active', False):
                                pygame.draw.circle(self.screen, (0, 255, 255), (e.rect.centerx - self.camera.x, e.rect.centery), 100, 5)
                            if getattr(e, 'state', '') == 'stunned':
                                stun_text = self.font.render("STUNNED!", True, (255, 255, 0))
                                self.screen.blit(stun_text, (e.rect.centerx - self.camera.x - stun_text.get_width()//2, e.rect.top - 30))
                
                for bullet in self.bullets: 
                    self.screen.blit(bullet.image, (bullet.rect.x - self.camera.x, bullet.rect.y))
                
                for eb in self.enemy_bullets: 
                    eb.draw(self.screen, self.camera.x)
                
                self.draw_ui()

                if self.state == "PAUSED":
                    overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(150); overlay.fill((0, 0, 0))
                    self.screen.blit(overlay, (0,0))
                    p_text = self.big_font.render("PAUSED", True, (255, 255, 0))
                    r_text = self.font.render("Press 'R' to Resume", True, (255, 255, 255))
                    self.screen.blit(p_text, (WIDTH//2 - p_text.get_width()//2, HEIGHT//2 - 50))
                    self.screen.blit(r_text, (WIDTH//2 - r_text.get_width()//2, HEIGHT//2 + 30))
                
                if self.state == "GAME_OVER":
                    overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(200); overlay.fill((50, 0, 0))
                    self.screen.blit(overlay, (0,0))
                    go_text = self.title_font.render("GAME OVER", True, (255, 0, 0))
                    m_text = self.font.render("Press ENTER to return to Menu", True, (255, 255, 255))
                    self.screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - 50))
                    self.screen.blit(m_text, (WIDTH//2 - m_text.get_width()//2, HEIGHT//2 + 50))

                if self.state == "INGAME_MENU":
                    overlay = pygame.Surface((WIDTH, HEIGHT)); overlay.set_alpha(200); overlay.fill((0, 0, 0))
                    self.screen.blit(overlay, (0,0))
                    q_text = self.big_font.render("KEMBALI KE MAIN MENU?", True, (255, 255, 0))
                    self.screen.blit(q_text, (WIDTH//2 - q_text.get_width()//2, HEIGHT//2 - 80))
                    yes_col = (255, 255, 0) if self.ingame_exit_index == 0 else (255, 255, 255)
                    no_col = (255, 255, 0) if self.ingame_exit_index == 1 else (255, 255, 255)
                    y_text = self.font.render("YES", True, yes_col); n_text = self.font.render("NO", True, no_col)
                    self.screen.blit(y_text, (WIDTH//2 - 100 - y_text.get_width()//2, HEIGHT//2 + 20))
                    self.screen.blit(n_text, (WIDTH//2 + 100 - n_text.get_width()//2, HEIGHT//2 + 20))

            # --- RENDERING UNTUK ANIMASI BOS MATI ---
            elif self.state == "BOSS_DYING":
                # 1. Tetap gambar map dunia dan pemain agar layar tidak kosong
                self.world.draw(self.screen, self.camera.x)
                self.screen.blit(self.player.image, (self.player.rect.x - self.camera.x, self.player.rect.y))
                self.draw_ui()
                
                # 2. Mainkan animasi bos mati
                if len(self.boss_death_frames) > 0:
                    current_frame = self.boss_death_frames[int(self.boss_death_index)]
                    # Gambar bos sesuai koordinat kameranya
                    self.screen.blit(current_frame, (self.boss_death_x - self.camera.x, self.boss_death_y))
                    
                    # 3. Kecepatan animasi (0.1 berarti butuh 10 frame game untuk ganti 1 gambar)
                    self.boss_death_index += 0.03
                    
                    # 4. Kalau animasi sudah melebihi gambar terakhir
                    if self.boss_death_index >= len(self.boss_death_frames):
                        self.state = "ENDING_STORY" # Pindah ke kotak cerita
                else:
                    # Jaga-jaga jika gambar bos mati gagal dimuat
                    self.state = "ENDING_STORY"

            # --- RENDERING UNTUK ENDING CERITA DAN KREDIT ---
            elif self.state == "ENDING_STORY":
                # Tetap gambar map dan player
                self.world.draw(self.screen, self.camera.x)
                self.screen.blit(self.player.image, (self.player.rect.x - self.camera.x, self.player.rect.y))
                
                # Biarkan animasi ledakan bos selesai
                for ex in self.explosions:
                    ex.update()
                    if ex.active: 
                        self.screen.blit(ex.image, (ex.rect.x - self.camera.x, ex.rect.y))
                
                # 1. Gambar Kotak Cerita di bawah
                box_x = WIDTH // 2 - self.story_box_img.get_width() // 2
                box_y = HEIGHT - self.story_box_img.get_height() - 20
                self.screen.blit(self.story_box_img, (box_x, box_y))
                
                # --- Posisi Teks Cerita (Rata Tengah Kotak) ---
                story_texts = [
                    "SELAMAT! BOS TELAH DIKALAHKAN!",
                    "Game ini masih dalam versi DEMO.",
                    "Tunggu update terbaru untuk petualangan selanjutnya..."
                ]
                
                # Cari titik tengah sumbu X dari kotak gambar
                box_center_x = box_x + (self.story_box_img.get_width() // 2)
                # Beri jarak 50 piksel dari atas kotak untuk teks pertama
                start_text_y = box_y + 160
                
                for i, text in enumerate(story_texts):
                    txt_surf = self.font.render(text, True, (255, 255, 255))
                    txt_rect = txt_surf.get_rect(center=(box_center_x, start_text_y + (i * 45)))
                    self.screen.blit(txt_surf, txt_rect)
                
                # 3. Animasi gambar Enter berkedip di pojok kanan bawah
                self.enter_anim_index += 0.05
                if self.enter_anim_index >= len(self.enter_frames): self.enter_anim_index = 0
                
                current_enter = self.enter_frames[int(self.enter_anim_index)]
                enter_x = box_x + self.story_box_img.get_width() - current_enter.get_width() - 30
                enter_y = box_y + self.story_box_img.get_height() - current_enter.get_height() - 20
                self.screen.blit(current_enter, (enter_x, enter_y))

            elif self.state == "ENDING_CREDITS":
                # Layar hitam untuk credits
                self.screen.fill((0, 0, 0))
                
                # --- Animasi Full Screen ---
                target_y = 0 
                if self.credits_y > target_y:
                    self.credits_y -= 2 # Kecepatan teks naik
                
                self.screen.blit(self.credits_img, (0, self.credits_y))
                
                # Tampilkan instruksi untuk keluar saat gambar sudah berhenti
                if self.credits_y <= target_y:
                    exit_text = self.font.render("Press ENTER to return to Main Menu", True, (255, 255, 255))
                    self.screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT - 60))

            pygame.display.flip() 
            self.clock.tick(FPS)          

if __name__ == "__main__":
    game = Game()
    game.run()