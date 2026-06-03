# player.py
import pygame
from entities import Character, Bullet
from utils import load_image_safe
from settings import FPS

class Player(Character):
    def __init__(self, x, y, bullet_list, shoot_sound): 
        super().__init__(x, y)
        self.bullet_list = bullet_list
        self.shoot_sound = shoot_sound 
        
        self.speed = 3
        self.jump_power = -12
        self.gravity = 0.6
        self.on_ground = False
        self.facing_right = True
        self.shoot_cooldown = 0 
        self.weapon_type = 'normal'
        self.weapon_timer = 0
        self.__hp = 100       
        self.__lives = 3      
        self.invincible_timer = 0 
        
        self.shield_active = False
        self.shield_energy = 100
        
        self.state = 'leonberdiri'
        self.frame_index = 0
        self.animation_speed = 0.15
        
        self.animations = {'leonberdiri': [], 'run': [], 'tembak_samping': [], 'tembak_bawah': [], 'tembak_atas': [], 'pesawat': []}
        self.load_animations()
        
        self.image = self.animations[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

    def get_hp(self): return self.__hp
    def set_hp(self, value): self.__hp = value
    def get_lives(self): return self.__lives
    def set_lives(self, value): self.__lives = value

    def load_animations(self):
        char_size = (40, 50) 
        self.animations['leonberdiri'].append(load_image_safe("player", "leonberdiri.png", char_size, (0, 0, 255)))
        run_frames = ["leon1.png", "leon2.png", "leon3.png", "leon4.png", "leon5.png", "leon6.png", "leon7.png", "leon8.png", "leon9.png", "leon10.png"]
        for frame in run_frames: self.animations['run'].append(load_image_safe("player", frame, char_size, (0, 0, 200)))
        
        self.animations['tembak_samping'].append(load_image_safe("player", "tembak_samping.png", char_size, (0, 0, 150)))
        self.animations['tembak_bawah'].append(load_image_safe("player", "tembak_bawah.png", char_size, (0, 0, 100)))
        self.animations['tembak_atas'].append(load_image_safe("player", "tembak_atas.png", char_size, (0, 0, 100))) 
        
        # MENJADI SEPERTI INI (ubah 8 jadi 3):
        for i in range(1, 3): self.animations['pesawat'].append(load_image_safe("player", f"player_plane{i}.png", (50, 40), (0, 255, 255)))

    def take_damage(self, amount):
        if self.invincible_timer == 0:
            self.__hp -= amount        
            self.invincible_timer = FPS * 1.5 
            if self.__hp <= 0:
                self.__lives -= 1      
                if self.__lives > 0: self.__hp = 100 

    def move(self, keys, stage):
        self._vel_x = 0 
        if stage == 2: self._vel_y = 0 
            
        self.state = 'leonberdiri'
        
        if stage == 2:
            self.state = 'pesawat'
            self._vel_x = 1.0 
            if keys[pygame.K_d]: self._vel_x += 3.0
            elif keys[pygame.K_a]: self._vel_x -= 3.0
            if keys[pygame.K_w]: self._vel_y = -3.5
            elif keys[pygame.K_s]: self._vel_y = 3.5
        else:
            if keys[pygame.K_d]: 
                self._vel_x = self.speed; self.facing_right = True; self.state = 'run'
            elif keys[pygame.K_a]:
                self._vel_x = -self.speed; self.facing_right = False; self.state = 'run'
            if keys[pygame.K_w] and self.on_ground: 
                self._vel_y = self.jump_power; self.on_ground = False

        if stage >= 3 and keys[pygame.K_SPACE]:
            if self.shield_energy > 0:
                self.shield_active = True; self.shield_energy -= 1 
            else: self.shield_active = False
        else:
            self.shield_active = False
            if self.shield_energy < 100: self.shield_energy += 0.2

        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1 

        if keys[pygame.K_RIGHT]:
            self.facing_right = True
            if stage != 2: self.state = 'tembak_samping'
            if self.shoot_cooldown == 0:
                if self.shoot_sound: self.shoot_sound.play() 
                self.shoot(12, 0)
        elif keys[pygame.K_LEFT]:
            self.facing_right = False
            if stage != 2: self.state = 'tembak_samping'
            if self.shoot_cooldown == 0:
                if self.shoot_sound: self.shoot_sound.play() 
                self.shoot(-12, 0)
        elif keys[pygame.K_UP] and stage != 2: 
            self.state = 'tembak_atas'
            if self.shoot_cooldown == 0:
                if self.shoot_sound: self.shoot_sound.play() 
                self.shoot(0, -12) 
        elif keys[pygame.K_DOWN] and stage != 2: 
            self.state = 'tembak_bawah'
            if self.shoot_cooldown == 0:
                if self.shoot_sound: self.shoot_sound.play() 
                self.shoot(0, 12) 

    def shoot(self, vel_x, vel_y):
        if self.weapon_type == 'normal':
            self.bullet_list.append(Bullet(self.rect.centerx, self.rect.centery, vel_x, vel_y))
            self.shoot_cooldown = 15
        elif self.weapon_type == 'machine_gun':
            self.bullet_list.append(Bullet(self.rect.centerx, self.rect.centery, vel_x, vel_y))
            self.shoot_cooldown = 5 
        elif self.weapon_type == 'shotgun':
            if vel_x != 0: 
                self.bullet_list.append(Bullet(self.rect.centerx, self.rect.centery, vel_x, vel_y))
                self.bullet_list.append(Bullet(self.rect.centerx, self.rect.centery, vel_x, vel_y - 2))
                self.bullet_list.append(Bullet(self.rect.centerx, self.rect.centery, vel_x, vel_y + 2))
            else: 
                self.bullet_list.append(Bullet(self.rect.centerx, self.rect.centery, vel_x, vel_y))
                self.bullet_list.append(Bullet(self.rect.centerx, self.rect.centery, vel_x - 2, vel_y))
                self.bullet_list.append(Bullet(self.rect.centerx, self.rect.centery, vel_x + 2, vel_y))
            self.shoot_cooldown = 25 

    def animate(self):
        if len(self.animations[self.state]) > 1:
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.animations[self.state]): self.frame_index = 0
        else: self.frame_index = 0
        
        current_image = self.animations[self.state][int(self.frame_index)]
        self.image = pygame.transform.flip(current_image, True, False) if not self.facing_right else current_image
        
        if self.invincible_timer > 0 and (self.invincible_timer // 5) % 2 == 0: self.image.set_alpha(100)
        else: self.image.set_alpha(255)

    def draw_shield(self, screen, camera_x):
        if self.shield_active:
            pygame.draw.circle(screen, (0, 255, 255), (self.rect.centerx - camera_x, self.rect.centery), 40, 3)

    def update(self, stage):
        self.animate()
        if stage != 2: self._vel_y += self.gravity 
        self.apply_movement()
        if self.invincible_timer > 0: self.invincible_timer -= 1
        if self.weapon_timer > 0:
            self.weapon_timer -= 1
            if self.weapon_timer <= 0: self.weapon_type = 'normal'