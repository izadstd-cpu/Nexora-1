# enemy.py
import pygame
import random
import math
from entities import Character, EnemyBullet
from utils import load_image_safe
from settings import WIDTH 

class BaseEnemy(Character): 
    def __init__(self, x, y, player, stage): 
        super().__init__(x, y)
        self.player = player 
        self.stage = stage
        self.hp = 10 
        self.speed = 1.0
        self.animations = []
        self.frame_index = 0
        self.animation_speed = 0.1 
        self.facing_right = True 
        self.gravity = 0.5 
        self.enemy_type = 'normal'
        
        self.original_faces_left = False # Kondisi gambar awal

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations): 
            self.frame_index = 0
        current_image = self.animations[int(self.frame_index)]
        
        # Logika gambar agar tidak berjalan mundur
        if self.original_faces_left:
            # Jika gambar aslinya hadap KIRI, maka kita balik (flip) saat dia bergerak ke KANAN
            self.image = pygame.transform.flip(current_image, True, False) if self.facing_right else current_image
        else:
            # Normal: Jika gambar asli hadap KANAN, maka dibalik saat dia bergerak ke KIRI
            self.image = pygame.transform.flip(current_image, True, False) if not self.facing_right else current_image

    def default_ground_movement(self):
        if self.rect.x < self.player.rect.x:
            self._vel_x = self.speed
            self.facing_right = True
        elif self.rect.x > self.player.rect.x:
            self._vel_x = -self.speed
            self.facing_right = False
        else: 
            self._vel_x = 0
        self._vel_y += self.gravity

class NormalEnemy(BaseEnemy):
    def __init__(self, x, y, player, stage):
        super().__init__(x, y, player, stage)
        for i in range(1, 8): 
            self.animations.append(load_image_safe("enemies", f"enemy{i}.png", (45, 55)))
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, enemy_bullets):
        self.default_ground_movement()
        self.animate()
        self.apply_movement()

class PlaneEnemy(BaseEnemy):
    def __init__(self, x, y, player, stage):
        super().__init__(x, y, player, stage)
        self.enemy_type = 'plane'
        self.gravity = 0
        self.shoot_timer = 0
        for i in range(1, 3): 
            self.animations.append(load_image_safe("enemies", f"enemy_plane{i}.png", (50, 40)))
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, enemy_bullets):
        self.shoot_timer += 1
        if self.shoot_timer >= 90:
            vel_x = -7 if self.rect.x > self.player.rect.x else 7
            enemy_bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, vel_x, 0))
            self.shoot_timer = 0
        self._vel_y = 0
        if self.rect.x < self.player.rect.x: 
            self._vel_x = 1.5; self.facing_right = True
        else: 
            self._vel_x = -1.5; self.facing_right = False
        self.animate()
        self.apply_movement()

class DroneEnemy(BaseEnemy):
    def __init__(self, x, y, player, stage):
        super().__init__(x, y, player, stage)
        self.enemy_type = 'drone'
        self.gravity = 0 
        self.shoot_timer = 0
        self.speed = 2.0
        
        # Memberitahu sistem bahwa gambar asli Drone menghadap ke kiri
        self.original_faces_left = True 
        
        for i in range(1, 7): 
            img = load_image_safe("enemies", f"qw{i}.png", (60, 60))
            img.set_colorkey((0, 0, 0)) 
            self.animations.append(img)
        
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=(x, random.randint(80, 200)))
        self.move_dir = -1 if x > player.rect.x else 1

    def update(self, enemy_bullets):
        self.shoot_timer += 1
        if self.shoot_timer >= 90:
            dx = self.player.rect.centerx - self.rect.centerx
            dy = self.player.rect.centery - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                enemy_bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, (dx/dist)*7, (dy/dist)*7))
            self.shoot_timer = 0
            
        self._vel_x = self.move_dir * self.speed
        self.facing_right = True if self._vel_x > 0 else False
        
        if abs(self.rect.x - self.player.rect.x) > WIDTH:
            self.move_dir *= -1

        self.animate()
        self.apply_movement()

class TankEnemy(BaseEnemy):
    def __init__(self, x, y, player, stage):
        super().__init__(x, y, player, stage)
        self.enemy_type = 'tank'
        self.hp = 30 
        self.speed = 1.5
        
        # Memberitahu sistem bahwa gambar asli Truk menghadap ke kiri
        self.original_faces_left = True
        
        self.anim_walk = []
        for i in range(1, 4):
            self.anim_walk.append(load_image_safe("enemies", f"truk{i}.png", (150, 100), (200, 0, 0)))
            
        self.anim_shoot = []
        for i in range(1, 5):
            self.anim_shoot.append(load_image_safe("enemies", f"truk_nembak{i}.png", (150, 100), (200, 0, 0)))
            
        self.animations = self.anim_walk
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.state = 'walk'
        self.shoot_delay = 0
        self.bullets_fired = 0
        self.cooldown = 0

    def update(self, enemy_bullets):
        self._vel_y += self.gravity
        
        if self.state == 'walk':
            self.animations = self.anim_walk
            
            # Truk selalu bergerak maju mendekati Player
            if self.rect.centerx > self.player.rect.centerx:
                self._vel_x = -self.speed
                self.facing_right = False
            else:
                self._vel_x = self.speed
                self.facing_right = True
            
            if abs(self.rect.centerx - self.player.rect.centerx) <= (WIDTH // 3):
                self.state = 'shoot'
                self._vel_x = 0
                self.frame_index = 0
                
        elif self.state == 'shoot':
            self.animations = self.anim_shoot
            self._vel_x = 0
            
            # Arahkan wajah saat nembak
            self.facing_right = True if self.player.rect.centerx > self.rect.centerx else False
            
            if self.cooldown > 0:
                self.cooldown -= 1
                self.frame_index = 0 
            else:
                self.shoot_delay -= 1
                if self.shoot_delay <= 0:
                    
                    # Arah Peluru sama dengan drone
                    dx = self.player.rect.centerx - self.rect.centerx
                    dy = self.player.rect.centery - self.rect.centery
                    dist = math.hypot(dx, dy)
                    
                    if dist != 0:
                        bullet_speed = 8
                        vel_x = (dx / dist) * bullet_speed
                        vel_y = (dy / dist) * bullet_speed
                        enemy_bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, vel_x, vel_y))
                        
                    self.bullets_fired += 1
                    self.shoot_delay = 15 
                    
                    if self.bullets_fired >= 3:
                        self.bullets_fired = 0
                        self.cooldown = 60 

        self.animate()
        self.apply_movement()

class BossEnemy(BaseEnemy):
    def __init__(self, x, y, player, stage, min_x, max_x):
        super().__init__(x, y, player, stage)
        self.enemy_type = 'boss'
        self.hp = 1000
        self.max_hp = 1000
        self.gravity = 0
        self.speed = 2.0
        
        self.min_x = min_x
        self.max_x = max_x
        self.move_dir = -1
        
        # Variabel Fase 
        self.phase = 1               
        self.shield_active = False   
        self.stun_timer = 0          
        self.charge_timer = 0        # Timer untuk ngeden
        
        # --- MEMUAT ASET GAMBAR ---
        self.anim_terbang = []
        for i in range(1, 6):
            self.anim_terbang.append(load_image_safe("enemies", f"bos_terbang{i}.png", (150, 150), (255, 0, 0)))
        
        self.anim_nembak = []
        self.anim_nembak.append(load_image_safe("enemies", "bos_nembak.png", (150, 150), (255, 255, 0)))
        
        self.anim_dash = []
        for i in range(1, 6):
            self.anim_dash.append(load_image_safe("enemies", f"bos_dash{i}.png", (150, 150), (255, 100, 0)))
        
        self.animations = self.anim_terbang
        self.image = self.animations[0]
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.state = 'fly'
        self.shoot_timer = 0
        self.shoot_cooldown = 120

    def update(self, enemy_bullets):
        # Cek masuk Fase 2 (Darah setengah di fase awal)
        if self.hp <= self.max_hp / 2 and self.phase == 1:
            self.phase = 2
            self.state = 'fly_to_center'
            self.shield_active = True
            self.shoot_timer = 0

        # --- LOGIKA FASE 1, 2, 3 (TERBANG & NEMBAK) ---
        if self.state == 'fly_to_center':
            self.animations = self.anim_terbang
            target_x = (self.min_x + self.max_x) // 2
            target_y = 100
            
            if abs(self.rect.centerx - target_x) <= self.speed:
                self.rect.centerx = target_x
                self._vel_x = 0
            else:
                self._vel_x = self.speed if self.rect.centerx < target_x else -self.speed
                self.facing_right = (self._vel_x > 0)
                
            if abs(self.rect.y - target_y) <= self.speed:
                self.rect.y = target_y
                self._vel_y = 0
            else:
                self._vel_y = self.speed if self.rect.y < target_y else -self.speed
                
            if self._vel_x == 0 and self._vel_y == 0:
                self.state = 'shielded'
                
        elif self.state == 'shielded':
            self.animations = self.anim_terbang
            self._vel_x = 0
            self._vel_y = 0
            
        elif self.state == 'stunned':
            self.animations = self.anim_terbang 
            self._vel_x = 0
            self._vel_y = 0
            self.stun_timer -= 1
            if self.stun_timer <= 0:
                self.state = 'fly'
                self.phase = 3 
                self.shoot_timer = 0
                
        elif self.state == 'fly':
            self.animations = self.anim_terbang
            self._vel_x = self.speed * self.move_dir
            
            if self.rect.left <= self.min_x:
                self.move_dir = 1
                self.facing_right = True
            elif self.rect.right >= self.max_x:
                self.move_dir = -1
                self.facing_right = False
                
            self.shoot_timer += 1
            if self.shoot_timer >= self.shoot_cooldown:
                self.state = 'shoot'
                self._vel_x = 0
                self.shoot_timer = 0
                self.frame_index = 0
                
        elif self.state == 'shoot':
            self.animations = self.anim_nembak
            self._vel_x = 0
            self.shoot_timer += 1
            
            if self.shoot_timer == 10: 
                from entities import EnemyBullet 
                bullet_speed = 6
                directions = [(0, -1), (0, 1), (-1, 0), (1, 0), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)]
                for dx, dy in directions:
                    enemy_bullets.append(EnemyBullet(self.rect.centerx, self.rect.centery, dx * bullet_speed, dy * bullet_speed))
                    
            if self.shoot_timer >= 40:
                self.state = 'fly'
                self.shoot_timer = 0

        # --- LOGIKA FASE 4 (NGEDEN & DASH) ---
        elif self.state == 'fall_to_ground':
            self.animations = self.anim_dash
            self._vel_x = 0
            self._vel_y = 8 # Bos jatuh dengan cepat (dipercepat agar menegangkan)
            
            # Targetkan posisi tanah dengan melihat posisi kaki pemain
            target_ground = self.player.rect.bottom
            
            # Jika bos sudah sejajar dengan pemain (menyentuh tanah)
            if self.rect.bottom >= target_ground:
                self.rect.bottom = target_ground
                self._vel_y = 0
                self.state = 'charge'
                self.charge_timer = 180 # 3 Detik
                
        elif self.state == 'charge':
            self.animations = self.anim_dash
            self._vel_x = 0
            self._vel_y = 0
            self.charge_timer -= 1
            
            # Bos memutar badan menghadap player
            self.facing_right = True if self.player.rect.centerx > self.rect.centerx else False
            
            # Menyeruduk!
            if self.charge_timer <= 0:
                self.state = 'dash'
                self.move_dir = 1 if self.facing_right else -1
                
        elif self.state == 'dash':
            self.animations = self.anim_dash
            dash_speed = 15 # Kecepatan tinggi
            self._vel_x = dash_speed * self.move_dir
            self._vel_y = 0
            
            if self.rect.left <= self.min_x:
                self.rect.left = self.min_x
                self.state = 'charge'
                self.charge_timer = 180
            elif self.rect.right >= self.max_x:
                self.rect.right = self.max_x
                self.state = 'charge'
                self.charge_timer = 180

        self.animate()
        self.apply_movement()