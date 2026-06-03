# utils.py
import pygame
import os

def load_image_safe(folder_name, filename, size, fallback_color=(255, 0, 255)):
    path = os.path.join("assets", folder_name, filename)
    try:
        image = pygame.image.load(path).convert_alpha()
        return pygame.transform.scale(image, size)
    except:
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf

def load_sound_safe(folder_name, filename):
    path = os.path.join("assets", folder_name, filename)
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except:
        return None 

def load_gif_safe(folder_name, filename, size):
    path = os.path.join("assets", folder_name, filename)
    frames = []
    try:
        from PIL import Image, ImageSequence 
        
        img = Image.open(path)
        for frame in ImageSequence.Iterator(img):
            frame = frame.convert("RGBA")
            mode = frame.mode
            size_img = frame.size
            data = frame.tobytes()
            py_image = pygame.image.fromstring(data, size_img, mode)
            py_image = pygame.transform.scale(py_image, size)
            frames.append(py_image)
        return frames
    except:
        surf = pygame.Surface(size)
        surf.fill((20, 20, 25)) 
        return [surf]
    
def load_font_safe(filename, size, fallback_font="Arial"):
    path = os.path.join("assets", "fonts", filename)
    try:
        return pygame.font.Font(path, size)
    except:
        return pygame.font.SysFont(fallback_font, size, bold=True)