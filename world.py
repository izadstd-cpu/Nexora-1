# world.py
import pygame
import os
from settings import WIDTH, HEIGHT

class World:
    def __init__(self, screen_width, screen_height, stage):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stage = stage
        
        filename = "mapcok.png" if stage == 1 else f"mapcok{stage}.png"
        path = os.path.join("assets", "maps", filename)
        try:
            self.image = pygame.image.load(path).convert()
            self.image = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        except FileNotFoundError:
            try:
                default_path = os.path.join("assets", "maps", "mapcok.png")
                self.image = pygame.image.load(default_path).convert()
                self.image = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
            except:
                self.image = pygame.Surface((self.screen_width, self.screen_height))
                self.image.fill((30, 30, 40))

        self.ground_heights = [self.screen_height] * self.screen_width
        self.generate_heightmap()
        self.max_x = float('inf') 

    def generate_heightmap(self):
        for x in range(self.screen_width):
            for y in range(self.screen_height - 1, -1, -1):
                color = self.image.get_at((x, y))
                if color.r > 240 and color.g > 240 and color.b > 240:
                    self.ground_heights[x] = y
                    break

    def get_ground_y(self, x):
        idx = int(x) % self.screen_width 
        return self.ground_heights[idx]

    def draw(self, screen, camera_x):
        rel_x = camera_x % self.screen_width
        screen.blit(self.image, (-rel_x, 0))
        if rel_x > 0:
            screen.blit(self.image, (-rel_x + self.screen_width, 0))
            
    def change_map(self, filename):
        path = os.path.join("assets", "maps", filename)
        try:
            self.image = pygame.image.load(path).convert()
            self.image = pygame.transform.scale(self.image, (self.screen_width, self.screen_height))
        except FileNotFoundError:
            # Jika gambar tidak ada, kita beri warna merah sebagai fallback
            self.image = pygame.Surface((self.screen_width, self.screen_height))
            self.image.fill((100, 0, 0))
        
        # Buat ulang pijakan tanah (heightmap) untuk map bos baru ini
        self.ground_heights = [self.screen_height] * self.screen_width
        self.generate_heightmap()

class Camera:
    def __init__(self, screen_width):
        self.x = 0
        self.screen_width = screen_width
        self.max_x = float('inf')

    def update(self, target_x):
        kamera_ideal = target_x - (self.screen_width / 2)
        if kamera_ideal > self.x:
            self.x = kamera_ideal
        if self.x > self.max_x - self.screen_width:
            self.x = self.max_x - self.screen_width
            