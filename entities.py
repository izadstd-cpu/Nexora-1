# entities.py
import pygame
from abc import ABC, abstractmethod
from utils import load_image_safe
from settings import WIDTH, HEIGHT

class Character(ABC): 
    def __init__(self, x, y):
        self._vel_y = 0  
        self._vel_x = 0  
        self.active = True 

    def apply_movement(self):
        self.rect.x += self._vel_x
        self.rect.y += self._vel_y

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

class Bullet(Character): 
    def __init__(self, x, y, vel_x, vel_y):
        super().__init__(x, y)
        self._vel_x = vel_x  
        self._vel_y = vel_y  
        bullet_size = (8, 4) if vel_y == 0 else (4, 8)
        self.image = load_image_safe("items", "peluru.png", bullet_size, (255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, camera_x):
        self.apply_movement()
        if self.rect.right < camera_x - 100 or self.rect.left > camera_x + WIDTH + 100 or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.active = False

class EnemyBullet(Character):
    def __init__(self, x, y, vel_x, vel_y):
        super().__init__(x, y)
        self.rect = pygame.Rect(x, y, 10, 10)
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.active = True

    def update(self, camera_x):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.right < camera_x - 100 or self.rect.left > camera_x + WIDTH + 100 or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.active = False

    def draw(self, screen, camera_x):
        pygame.draw.ellipse(screen, (255, 50, 50), (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height))

class MysteryBox(Character):
    def __init__(self, x, y, stage=1): # Tambahkan parameter stage di sini
        super().__init__(x, y)
        self.image = load_image_safe("items", "item_bonus.png", (20, 20), (0, 255, 255))
        if self.image.get_at((0,0)) == (0, 255, 255, 255): 
            font = pygame.font.SysFont("Arial", 15, bold=True)
            text = font.render("?", True, (0, 0, 0))
            self.image.blit(text, (6, 1))
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # --- ATUR KECEPATAN JATUH (GRAVITASI) ---
        if stage == 2:
            self.gravity = 0.1 # Jatuh sangat perlahan seperti parasut di Stage 2
        else:
            self.gravity = 0.5 # Jatuh normal di stage lainnya

    def update(self):
        self._vel_y += self.gravity 
        self.apply_movement()
        
class Explosion(Character):
    def __init__(self, x, y):
        super().__init__(x, y)
        # Baris ini bertugas mengambil gambar ledakan.png milikmu
        self.image = load_image_safe("enemies", "ledakan.png", (60, 60), (255, 100, 0))
        self.rect = self.image.get_rect(center=(x, y))
        
        # Angka 15 ini adalah durasi (stopwatch). Makin besar angkanya, ledakan makin lama hilangnya.
        self.timer = 15 

    def update(self):
        self.timer -= 1
        # Jika stopwatch habis, hapus gambar ledakan
        if self.timer <= 0:
            self.active = False
            
class EnergyItem(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Pastikan file energy.png ada di assets/items/
        self.image = load_image_safe("items", "energy.png", (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self._vel_y = 0
        self.gravity = 0.5
        self.active = True

    def update(self):
        self._vel_y += self.gravity
        self.rect.y += int(self._vel_y)
        # Hapus jika jatuh terlalu jauh
        if self.rect.y > 800: self.active = False