import pygame
from pygame.locals import *
pygame.init()
from time import time as timer
import random

#TODO Змінні
W = 800
H = 600
win = pygame.display.set_mode((W,H))
pygame.font.init()
text1 = pygame.font.Font("ZnikomitNo25.ttf", 150)
text2 = pygame.font.Font("Alexander.ttf", 30)
text3 = pygame.font.Font("Comfortaa.ttf",30)
text4 = pygame.font.Font("Comfortaa.ttf",100)
clock = pygame.time.Clock()
FPS = 30
controller = "AD"
show_text = True
text_start_time = pygame.time.get_ticks()
text_duration = 2000
blocks_group = pygame.sprite.Group()

pygame.mixer.init()
pygame.mixer.music.load('game_music.mp3')
pygame.mixer.music.play()
volume_level = 50
volume = volume_level // 100.0
pygame.mixer.music.set_volume(volume)

#TODO Кольори
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


#TODO Classe's
class Draw_Button:
    def __init__(self, surface, color, x, y, width, height, text='', font_size=30):
        self.surface = surface
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font_size = font_size

        self.font = pygame.font.Font(None, self.font_size)

    def draw(self):
        pygame.draw.rect(self.surface, self.color, (self.x, self.y, self.width, self.height))
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.x + self.width/2, self.y + self.height/2))
        self.surface.blit(text_surface, text_rect)

    def is_clicked(self, mouse_pos):
        return self.x <= mouse_pos[0] <= self.x + self.width and self.y <= mouse_pos[1] <= self.y + self.height

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, img, x, y, w, h, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img), (w,h))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        win.blit(self.image, (self.rect.x,self.rect.y))

class Platform(GameSprite):
    def update(self, controller) -> None:
        if controller == "AD":
            keys = pygame.key.get_pressed()
            if keys[K_a] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_d] and self.rect.x < W-150:
                self.rect.x += self.speed
        elif controller == "LR":
            keys = pygame.key.get_pressed()
            if keys[K_LEFT] and self.rect.x > 5:
                self.rect.x -= self.speed
            if keys[K_RIGHT] and self.rect.x < W-150:
                self.rect.x += self.speed

class Ball(GameSprite):
    BALL_SPEED = 5

    def __init__(self, image, x, y, width, height, speed):
        super().__init__(image, x, y, width, height, speed)
        self.ball_dx = random.choice([-1, 1]) * self.BALL_SPEED  # Випадковий напрямок по X
        self.ball_dy = random.choice([-1, 1]) * self.BALL_SPEED  # Швидкість по Y (можна залишити сталою)

    def update(self, ) -> None:
        self.rect.x += self.ball_dx
        self.rect.y += self.ball_dy
        if self.rect.x <= 0 or self.rect.x >= W-50:
            self.ball_dx *= -1
        if self.rect.y <= 0 or self.rect.y >= H:
            self.ball_dy *= -1


#TODO def's
def display_text(screen, font, text, x, y):
    text_surface = font.render(text, True, BLACK)
    screen.blit(text_surface, (x, y))

#TODO scene's
current_scene = None
def switch_scene(scene):
    global current_scene
    current_scene = scene

def main_menu():
    game = True
    text_arcanoid = text1.render("ARCANOID", 1, RED)
    button_exit = Draw_Button(win, RED, 250, 500, 300, 50, "EXIT")
    button_settings = Draw_Button(win, RED, 250, 400, 300, 50, "SETTINGS")
    button_play = Draw_Button(win, RED, 250, 300, 300, 50, "PLAY")
    while game:
        mouse_pos = pygame.mouse.get_pos()
        for e in pygame.event.get():
            if e.type == QUIT:
                game = False
                switch_scene(None)
            elif e.type == MOUSEBUTTONDOWN:
                if button_exit.is_clicked(mouse_pos):
                    switch_scene(None)
                    game = False
                elif button_settings.is_clicked(mouse_pos):
                    switch_scene(scene_settings)
                    game = False
                elif button_play.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill((255, 255, 255))
        button_exit.draw()
        button_settings.draw()
        button_play.draw()
        win.blit(text_arcanoid, (25, 50))
        pygame.display.flip()


def scene_settings():
    global FPS
    global volume_level
    global controller
    FPS_text = text3.render(str(FPS), 1, BLACK)
    Volume_text = text3.render(str(volume_level), 1, BLACK)
    AD_text = text3.render("AD", 1, BLACK)
    LR_text = text3.render("LR", 1, BLACK)
    game = True
    button_license = Draw_Button(win, RED, 50, 500, 200, 50, "LICENSE")
    button_s_exit = Draw_Button(win, RED, 300, 500, 200, 50, "EXIT")
    button_info = Draw_Button(win, RED, 550, 500, 200, 50, "INFO")
    button_FPS_p = Draw_Button(win, RED, 125,100,50,50, "+")
    button_FPS_m = Draw_Button(win, RED, 25,100,50,50, "-")
    button_Volume_p = Draw_Button(win, RED, 325, 100, 50, 50, "+")
    button_Volume_m = Draw_Button(win, RED, 225, 100, 50, 50, "-")
    button_AD_switch = Draw_Button(win, RED, 525, 100, 50, 50, "LR")
    button_LR_switch = Draw_Button(win, RED, 425, 100, 50, 50, "AD")
    text_FPS = text3.render("FPS", 1, BLACK)
    text_Volume = text3.render("Volume", 1, BLACK)
    text_Controls = text3.render("Controls", 1, BLACK)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                game = False
                switch_scene(None)
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_s_exit.is_clicked(mouse_pos):
                    switch_scene(main_menu)
                    game = False
                elif button_license.is_clicked(mouse_pos):
                    switch_scene(scene_license)
                    game = False
                elif button_info.is_clicked(mouse_pos):
                    switch_scene(scene_info)
                    game = False
                elif button_FPS_p.is_clicked(mouse_pos) and FPS < 100:
                    FPS += 5
                elif button_FPS_m.is_clicked(mouse_pos) and FPS > 5:
                    FPS -= 5
                elif button_Volume_p.is_clicked(mouse_pos) and volume_level < 100:
                    volume_level += 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_Volume_m.is_clicked(mouse_pos) and volume_level > 0:
                    volume_level -= 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_AD_switch.is_clicked(mouse_pos):
                    controller = "LR"
                elif button_LR_switch.is_clicked(mouse_pos):
                    controller = "AD"
                
        
        FPS_text = text3.render(str(FPS), 1, BLACK)
        Volume_text = text3.render(str(volume_level), 1, BLACK)

        win.fill((255,255,255))
        button_AD_switch.draw()
        button_LR_switch.draw()
        button_Volume_p.draw()
        button_Volume_m.draw()
        button_FPS_p.draw()
        button_FPS_m.draw()
        button_license.draw()
        button_s_exit.draw()
        button_info.draw()
        win.blit(text_Volume, ((240,50)))
        win.blit(text_FPS, ((70,50)))
        win.blit(Volume_text,((283,110)))
        win.blit(FPS_text, ((83,110)))
        win.blit(text_Controls, ((430,50)))
        if controller == "AD":
            win.blit(AD_text, ((478, 110)))
        elif controller == "LR":
            win.blit(LR_text, ((478, 110)))


        pygame.display.flip()

def l1_scene_settings():
    global FPS
    global volume_level
    global controller
    FPS_text = text3.render(str(FPS), 1, BLACK)
    Volume_text = text3.render(str(volume_level), 1, BLACK)
    AD_text = text3.render("AD", 1, BLACK)
    LR_text = text3.render("LR", 1, BLACK)
    game = True
    button_license = Draw_Button(win, RED, 50, 500, 200, 50, "LICENSE")
    button_s_exit = Draw_Button(win, RED, 300, 500, 200, 50, "EXIT")
    button_info = Draw_Button(win, RED, 550, 500, 200, 50, "INFO")
    button_FPS_p = Draw_Button(win, RED, 125,100,50,50, "+")
    button_FPS_m = Draw_Button(win, RED, 25,100,50,50, "-")
    button_Volume_p = Draw_Button(win, RED, 325, 100, 50, 50, "+")
    button_Volume_m = Draw_Button(win, RED, 225, 100, 50, 50, "-")
    button_AD_switch = Draw_Button(win, RED, 525, 100, 50, 50, "LR")
    button_LR_switch = Draw_Button(win, RED, 425, 100, 50, 50, "AD")
    text_FPS = text3.render("FPS", 1, BLACK)
    text_Volume = text3.render("Volume", 1, BLACK)
    text_Controls = text3.render("Controls", 1, BLACK)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                game = False
                switch_scene(None)
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_s_exit.is_clicked(mouse_pos):
                    switch_scene(scene_pause_l1)
                    game = False
                elif button_FPS_p.is_clicked(mouse_pos) and FPS < 100:
                    FPS += 5
                elif button_FPS_m.is_clicked(mouse_pos) and FPS > 5:
                    FPS -= 5
                elif button_Volume_p.is_clicked(mouse_pos) and volume_level < 100:
                    volume_level += 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_Volume_m.is_clicked(mouse_pos) and volume_level > 0:
                    volume_level -= 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_AD_switch.is_clicked(mouse_pos):
                    controller = "LR"
                elif button_LR_switch.is_clicked(mouse_pos):
                    controller = "AD"
                
        
        FPS_text = text3.render(str(FPS), 1, BLACK)
        Volume_text = text3.render(str(volume_level), 1, BLACK)

        win.fill((255,255,255))
        button_AD_switch.draw()
        button_LR_switch.draw()
        button_Volume_p.draw()
        button_Volume_m.draw()
        button_FPS_p.draw()
        button_FPS_m.draw()
        button_s_exit.draw()
        win.blit(text_Volume, ((240,50)))
        win.blit(text_FPS, ((70,50)))
        win.blit(Volume_text,((283,110)))
        win.blit(FPS_text, ((83,110)))
        win.blit(text_Controls, ((430,50)))
        if controller == "AD":
            win.blit(AD_text, ((478, 110)))
        elif controller == "LR":
            win.blit(LR_text, ((478, 110)))


        pygame.display.flip()

def handle_events(button):
    for e in pygame.event.get():
        if e.type == QUIT:
            switch_scene(None)
            return False
        elif e.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button.is_clicked(mouse_pos):
                switch_scene(scene_settings)
                return False
    return True
def l2_scene_settings():
    global FPS
    global volume_level
    global controller
    FPS_text = text3.render(str(FPS), 1, BLACK)
    Volume_text = text3.render(str(volume_level), 1, BLACK)
    AD_text = text3.render("AD", 1, BLACK)
    LR_text = text3.render("LR", 1, BLACK)
    game = True
    button_license = Draw_Button(win, RED, 50, 500, 200, 50, "LICENSE")
    button_s_exit = Draw_Button(win, RED, 300, 500, 200, 50, "EXIT")
    button_info = Draw_Button(win, RED, 550, 500, 200, 50, "INFO")
    button_FPS_p = Draw_Button(win, RED, 125,100,50,50, "+")
    button_FPS_m = Draw_Button(win, RED, 25,100,50,50, "-")
    button_Volume_p = Draw_Button(win, RED, 325, 100, 50, 50, "+")
    button_Volume_m = Draw_Button(win, RED, 225, 100, 50, 50, "-")
    button_AD_switch = Draw_Button(win, RED, 525, 100, 50, 50, "LR")
    button_LR_switch = Draw_Button(win, RED, 425, 100, 50, 50, "AD")
    text_FPS = text3.render("FPS", 1, BLACK)
    text_Volume = text3.render("Volume", 1, BLACK)
    text_Controls = text3.render("Controls", 1, BLACK)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                game = False
                switch_scene(None)
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_s_exit.is_clicked(mouse_pos):
                    switch_scene(scene_pause_l2)
                    game = False
                elif button_FPS_p.is_clicked(mouse_pos) and FPS < 100:
                    FPS += 5
                elif button_FPS_m.is_clicked(mouse_pos) and FPS > 5:
                    FPS -= 5
                elif button_Volume_p.is_clicked(mouse_pos) and volume_level < 100:
                    volume_level += 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_Volume_m.is_clicked(mouse_pos) and volume_level > 0:
                    volume_level -= 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_AD_switch.is_clicked(mouse_pos):
                    controller = "LR"
                elif button_LR_switch.is_clicked(mouse_pos):
                    controller = "AD"
                
        
        FPS_text = text3.render(str(FPS), 1, BLACK)
        Volume_text = text3.render(str(volume_level), 1, BLACK)

        win.fill((255,255,255))
        button_AD_switch.draw()
        button_LR_switch.draw()
        button_Volume_p.draw()
        button_Volume_m.draw()
        button_FPS_p.draw()
        button_FPS_m.draw()
        button_s_exit.draw()
        win.blit(text_Volume, ((240,50)))
        win.blit(text_FPS, ((70,50)))
        win.blit(Volume_text,((283,110)))
        win.blit(FPS_text, ((83,110)))
        win.blit(text_Controls, ((430,50)))
        if controller == "AD":
            win.blit(AD_text, ((478, 110)))
        elif controller == "LR":
            win.blit(LR_text, ((478, 110)))


        pygame.display.flip()

def handle_events(button):
    for e in pygame.event.get():
        if e.type == QUIT:
            switch_scene(None)
            return False
        elif e.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button.is_clicked(mouse_pos):
                switch_scene(scene_settings)
                return False
    return True
def l3_scene_settings():
    global FPS
    global volume_level
    global controller
    FPS_text = text3.render(str(FPS), 1, BLACK)
    Volume_text = text3.render(str(volume_level), 1, BLACK)
    AD_text = text3.render("AD", 1, BLACK)
    LR_text = text3.render("LR", 1, BLACK)
    game = True
    button_license = Draw_Button(win, RED, 50, 500, 200, 50, "LICENSE")
    button_s_exit = Draw_Button(win, RED, 300, 500, 200, 50, "EXIT")
    button_info = Draw_Button(win, RED, 550, 500, 200, 50, "INFO")
    button_FPS_p = Draw_Button(win, RED, 125,100,50,50, "+")
    button_FPS_m = Draw_Button(win, RED, 25,100,50,50, "-")
    button_Volume_p = Draw_Button(win, RED, 325, 100, 50, 50, "+")
    button_Volume_m = Draw_Button(win, RED, 225, 100, 50, 50, "-")
    button_AD_switch = Draw_Button(win, RED, 525, 100, 50, 50, "LR")
    button_LR_switch = Draw_Button(win, RED, 425, 100, 50, 50, "AD")
    text_FPS = text3.render("FPS", 1, BLACK)
    text_Volume = text3.render("Volume", 1, BLACK)
    text_Controls = text3.render("Controls", 1, BLACK)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                game = False
                switch_scene(None)
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_s_exit.is_clicked(mouse_pos):
                    switch_scene(scene_pause_l3)
                    game = False
                elif button_FPS_p.is_clicked(mouse_pos) and FPS < 100:
                    FPS += 5
                elif button_FPS_m.is_clicked(mouse_pos) and FPS > 5:
                    FPS -= 5
                elif button_Volume_p.is_clicked(mouse_pos) and volume_level < 100:
                    volume_level += 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_Volume_m.is_clicked(mouse_pos) and volume_level > 0:
                    volume_level -= 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_AD_switch.is_clicked(mouse_pos):
                    controller = "LR"
                elif button_LR_switch.is_clicked(mouse_pos):
                    controller = "AD"
                
        
        FPS_text = text3.render(str(FPS), 1, BLACK)
        Volume_text = text3.render(str(volume_level), 1, BLACK)

        win.fill((255,255,255))
        button_AD_switch.draw()
        button_LR_switch.draw()
        button_Volume_p.draw()
        button_Volume_m.draw()
        button_FPS_p.draw()
        button_FPS_m.draw()
        button_s_exit.draw()
        win.blit(text_Volume, ((240,50)))
        win.blit(text_FPS, ((70,50)))
        win.blit(Volume_text,((283,110)))
        win.blit(FPS_text, ((83,110)))
        win.blit(text_Controls, ((430,50)))
        if controller == "AD":
            win.blit(AD_text, ((478, 110)))
        elif controller == "LR":
            win.blit(LR_text, ((478, 110)))


        pygame.display.flip()

def handle_events(button):
    for e in pygame.event.get():
        if e.type == QUIT:
            switch_scene(None)
            return False
        elif e.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button.is_clicked(mouse_pos):
                switch_scene(scene_settings)
                return False
    return True
def l4_scene_settings():
    global FPS
    global volume_level
    global controller
    FPS_text = text3.render(str(FPS), 1, BLACK)
    Volume_text = text3.render(str(volume_level), 1, BLACK)
    AD_text = text3.render("AD", 1, BLACK)
    LR_text = text3.render("LR", 1, BLACK)
    game = True
    button_license = Draw_Button(win, RED, 50, 500, 200, 50, "LICENSE")
    button_s_exit = Draw_Button(win, RED, 300, 500, 200, 50, "EXIT")
    button_info = Draw_Button(win, RED, 550, 500, 200, 50, "INFO")
    button_FPS_p = Draw_Button(win, RED, 125,100,50,50, "+")
    button_FPS_m = Draw_Button(win, RED, 25,100,50,50, "-")
    button_Volume_p = Draw_Button(win, RED, 325, 100, 50, 50, "+")
    button_Volume_m = Draw_Button(win, RED, 225, 100, 50, 50, "-")
    button_AD_switch = Draw_Button(win, RED, 525, 100, 50, 50, "LR")
    button_LR_switch = Draw_Button(win, RED, 425, 100, 50, 50, "AD")
    text_FPS = text3.render("FPS", 1, BLACK)
    text_Volume = text3.render("Volume", 1, BLACK)
    text_Controls = text3.render("Controls", 1, BLACK)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                game = False
                switch_scene(None)
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_s_exit.is_clicked(mouse_pos):
                    switch_scene(scene_pause_l4)
                    game = False
                elif button_FPS_p.is_clicked(mouse_pos) and FPS < 100:
                    FPS += 5
                elif button_FPS_m.is_clicked(mouse_pos) and FPS > 5:
                    FPS -= 5
                elif button_Volume_p.is_clicked(mouse_pos) and volume_level < 100:
                    volume_level += 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_Volume_m.is_clicked(mouse_pos) and volume_level > 0:
                    volume_level -= 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_AD_switch.is_clicked(mouse_pos):
                    controller = "LR"
                elif button_LR_switch.is_clicked(mouse_pos):
                    controller = "AD"
                
        
        FPS_text = text3.render(str(FPS), 1, BLACK)
        Volume_text = text3.render(str(volume_level), 1, BLACK)

        win.fill((255,255,255))
        button_AD_switch.draw()
        button_LR_switch.draw()
        button_Volume_p.draw()
        button_Volume_m.draw()
        button_FPS_p.draw()
        button_FPS_m.draw()
        button_s_exit.draw()
        win.blit(text_Volume, ((240,50)))
        win.blit(text_FPS, ((70,50)))
        win.blit(Volume_text,((283,110)))
        win.blit(FPS_text, ((83,110)))
        win.blit(text_Controls, ((430,50)))
        if controller == "AD":
            win.blit(AD_text, ((478, 110)))
        elif controller == "LR":
            win.blit(LR_text, ((478, 110)))


        pygame.display.flip()

def handle_events(button):
    for e in pygame.event.get():
        if e.type == QUIT:
            switch_scene(None)
            return False
        elif e.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button.is_clicked(mouse_pos):
                switch_scene(scene_settings)
                return False
    return True
def l5_scene_settings():
    global FPS
    global volume_level
    global controller
    FPS_text = text3.render(str(FPS), 1, BLACK)
    Volume_text = text3.render(str(volume_level), 1, BLACK)
    AD_text = text3.render("AD", 1, BLACK)
    LR_text = text3.render("LR", 1, BLACK)
    game = True
    button_license = Draw_Button(win, RED, 50, 500, 200, 50, "LICENSE")
    button_s_exit = Draw_Button(win, RED, 300, 500, 200, 50, "EXIT")
    button_info = Draw_Button(win, RED, 550, 500, 200, 50, "INFO")
    button_FPS_p = Draw_Button(win, RED, 125,100,50,50, "+")
    button_FPS_m = Draw_Button(win, RED, 25,100,50,50, "-")
    button_Volume_p = Draw_Button(win, RED, 325, 100, 50, 50, "+")
    button_Volume_m = Draw_Button(win, RED, 225, 100, 50, 50, "-")
    button_AD_switch = Draw_Button(win, RED, 525, 100, 50, 50, "LR")
    button_LR_switch = Draw_Button(win, RED, 425, 100, 50, 50, "AD")
    text_FPS = text3.render("FPS", 1, BLACK)
    text_Volume = text3.render("Volume", 1, BLACK)
    text_Controls = text3.render("Controls", 1, BLACK)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                game = False
                switch_scene(None)
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_s_exit.is_clicked(mouse_pos):
                    switch_scene(scene_pause_l5)
                    game = False
                elif button_FPS_p.is_clicked(mouse_pos) and FPS < 100:
                    FPS += 5
                elif button_FPS_m.is_clicked(mouse_pos) and FPS > 5:
                    FPS -= 5
                elif button_Volume_p.is_clicked(mouse_pos) and volume_level < 100:
                    volume_level += 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_Volume_m.is_clicked(mouse_pos) and volume_level > 0:
                    volume_level -= 10
                    pygame.mixer.music.set_volume(volume_level / 100.0)
                elif button_AD_switch.is_clicked(mouse_pos):
                    controller = "LR"
                elif button_LR_switch.is_clicked(mouse_pos):
                    controller = "AD"
                
        
        FPS_text = text3.render(str(FPS), 1, BLACK)
        Volume_text = text3.render(str(volume_level), 1, BLACK)

        win.fill((255,255,255))
        button_AD_switch.draw()
        button_LR_switch.draw()
        button_Volume_p.draw()
        button_Volume_m.draw()
        button_FPS_p.draw()
        button_FPS_m.draw()
        button_s_exit.draw()
        win.blit(text_Volume, ((240,50)))
        win.blit(text_FPS, ((70,50)))
        win.blit(Volume_text,((283,110)))
        win.blit(FPS_text, ((83,110)))
        win.blit(text_Controls, ((430,50)))
        if controller == "AD":
            win.blit(AD_text, ((478, 110)))
        elif controller == "LR":
            win.blit(LR_text, ((478, 110)))


        pygame.display.flip()

def handle_events(button):
    for e in pygame.event.get():
        if e.type == QUIT:
            switch_scene(None)
            return False
        elif e.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if button.is_clicked(mouse_pos):
                switch_scene(scene_settings)
                return False
    return True

button_l_exit = Draw_Button(win, RED, 250, 500, 300, 50, "EXIT")
text_license1 = text2.render('Гра створена у навчальних цілях для релізу у онлайн школі', 1, BLACK)
text_license2 = text2.render('"Logika", можливі допрацювання, творець: Дмитрів Андрій', 1, BLACK)

def draw_license():
    win.fill((255,255,255))
    win.blit(text_license1, (25, 50))
    win.blit(text_license2, (25, 100))
    button_l_exit.draw()
    pygame.display.flip()

def scene_license():
    game = True
    while game:
        game = handle_events(button_l_exit)
        draw_license()

def scene_info():
    game = True
    button_i_exit = Draw_Button(win, RED, 250, 500, 300, 50, "EXIT")
    text_info1 = text2.render("Головною метою гри є знищення усіх блоків на екрані,", 1, BLACK)
    text_info2 = text2.render("використовуючи платформу та м'яч.", 1, BLACK)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_i_exit.is_clicked(mouse_pos):
                    switch_scene(scene_settings)
                    game = False
        
        win.fill(WHITE)
        win.blit(text_info1, ((25,50)))
        win.blit(text_info2, ((25,100)))
        button_i_exit.draw()

        pygame.display.flip()

def scene_play():
    game = True
    button_level1 = Draw_Button(win, RED, 150, 100, 75, 75, "1", 60)
    button_level2 = Draw_Button(win, RED, 250, 100, 75, 75, "2", 60)
    button_level3 = Draw_Button(win, RED, 350, 100, 75, 75, "3", 60)
    button_level4 = Draw_Button(win, RED, 450, 100, 75, 75, "4", 60)
    button_level5 = Draw_Button(win, RED, 550, 100, 75, 75, "5", 60)
    button_exit = Draw_Button(win, RED, 300, 450, 200, 50, "Exit", 45)
    while game:
        for e in pygame.event.get():
                if e.type == QUIT:
                    switch_scene(None)
                    game = False
                elif e.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if button_level1.is_clicked(mouse_pos):
                        switch_scene(scene_level1)
                        game = False
                    elif button_level2.is_clicked(mouse_pos):
                        switch_scene(scene_level2)
                        game = False

                    elif button_level3.is_clicked(mouse_pos):
                        switch_scene(scene_level3)
                        game = False

                    elif button_level4.is_clicked(mouse_pos):
                        switch_scene(scene_level4)
                        game = False
                    elif button_level5.is_clicked(mouse_pos):
                        switch_scene(scene_level5)
                        game = False
                    elif button_exit.is_clicked(mouse_pos):
                        switch_scene(main_menu)
                        game = False

        win.fill(WHITE)
        button_level1.draw()
        button_level2.draw()
        button_level3.draw()
        button_level4.draw()
        button_level5.draw()
        button_exit.draw()
        pygame.display.flip()


def scene_pause_l1():
    global show_text
    global text_start_time
    game = True
    button_resume = Draw_Button(win, RED, 250, 100, 250, 50, "Play", 45)
    button_settings_p = Draw_Button(win, RED, 250, 200, 250, 50, "Settings", 45)
    button_exit_p = Draw_Button(win, RED, 250, 300, 250, 50, "Exit", 45)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN or e.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if button_resume.is_clicked(mouse_pos) or keys[K_ESCAPE]:
                    game = False
                    switch_scene(scene_level1)
                elif button_settings_p.is_clicked(mouse_pos):
                    switch_scene(l1_scene_settings)
                    game = False
                elif button_exit_p.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_resume.draw()
        button_settings_p.draw()
        button_exit_p.draw()
        pygame.display.flip()
def scene_pause_l2():
    global show_text
    global text_start_time
    game = True
    button_resume = Draw_Button(win, RED, 250, 100, 250, 50, "Play", 45)
    button_settings_p = Draw_Button(win, RED, 250, 200, 250, 50, "Settings", 45)
    button_exit_p = Draw_Button(win, RED, 250, 300, 250, 50, "Exit", 45)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN or e.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if button_resume.is_clicked(mouse_pos) or keys[K_ESCAPE]:
                    game = False
                    switch_scene(scene_level2)
                elif button_settings_p.is_clicked(mouse_pos):
                    switch_scene(l2_scene_settings)
                    game = False
                elif button_exit_p.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_resume.draw()
        button_settings_p.draw()
        button_exit_p.draw()
        pygame.display.flip()
def scene_pause_l3():
    global show_text
    global text_start_time
    game = True
    button_resume = Draw_Button(win, RED, 250, 100, 250, 50, "Play", 45)
    button_settings_p = Draw_Button(win, RED, 250, 200, 250, 50, "Settings", 45)
    button_exit_p = Draw_Button(win, RED, 250, 300, 250, 50, "Exit", 45)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN or e.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if button_resume.is_clicked(mouse_pos) or keys[K_ESCAPE]:
                    game = False
                    switch_scene(scene_level3)
                elif button_settings_p.is_clicked(mouse_pos):
                    switch_scene(l3_scene_settings)
                    game = False
                elif button_exit_p.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_resume.draw()
        button_settings_p.draw()
        button_exit_p.draw()
        pygame.display.flip()
def scene_pause_l4():
    global show_text
    global text_start_time
    game = True
    button_resume = Draw_Button(win, RED, 250, 100, 250, 50, "Play", 45)
    button_settings_p = Draw_Button(win, RED, 250, 200, 250, 50, "Settings", 45)
    button_exit_p = Draw_Button(win, RED, 250, 300, 250, 50, "Exit", 45)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN or e.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if button_resume.is_clicked(mouse_pos) or keys[K_ESCAPE]:
                    game = False
                    switch_scene(scene_level4)
                elif button_settings_p.is_clicked(mouse_pos):
                    switch_scene(l4_scene_settings)
                    game = False
                elif button_exit_p.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_resume.draw()
        button_settings_p.draw()
        button_exit_p.draw()
        pygame.display.flip()
def scene_pause_l5():
    global show_text
    global text_start_time
    game = True
    button_resume = Draw_Button(win, RED, 250, 100, 250, 50, "Play", 45)
    button_settings_p = Draw_Button(win, RED, 250, 200, 250, 50, "Settings", 45)
    button_exit_p = Draw_Button(win, RED, 250, 300, 250, 50, "Exit", 45)
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN or e.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if button_resume.is_clicked(mouse_pos) or keys[K_ESCAPE]:
                    game = False
                    switch_scene(scene_level5)
                elif button_settings_p.is_clicked(mouse_pos):
                    switch_scene(l5_scene_settings)
                    game = False
                elif button_exit_p.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_resume.draw()
        button_settings_p.draw()
        button_exit_p.draw()
        pygame.display.flip()

def scene_lose_l1():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_lose = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_lose_text = text4.render("You lose...", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level1)
                    game = False
                elif button_exit_lose.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_again.draw()
        button_exit_lose.draw()
        win.blit(you_lose_text,(150, 100))
        pygame.display.flip()

def scene_lose_l2():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_lose = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_lose_text = text4.render("You lose...", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level2)
                    game = False
                elif button_exit_lose.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_again.draw()
        button_exit_lose.draw()
        win.blit(you_lose_text,(150, 100))
        pygame.display.flip()

def scene_lose_l3():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_lose = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_lose_text = text4.render("You lose...", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level3)
                    game = False
                elif button_exit_lose.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_again.draw()
        button_exit_lose.draw()
        win.blit(you_lose_text,(150, 100))
        pygame.display.flip()

def scene_lose_l4():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_lose = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_lose_text = text4.render("You lose...", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level4)
                    game = False
                elif button_exit_lose.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_again.draw()
        button_exit_lose.draw()
        win.blit(you_lose_text,(150, 100))
        pygame.display.flip()

def scene_lose_l5():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_lose = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_lose_text = text4.render("You lose...", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level5)
                    game = False
                elif button_exit_lose.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False

        win.fill(WHITE)
        button_again.draw()
        button_exit_lose.draw()
        win.blit(you_lose_text,(150, 100))
        pygame.display.flip()

def scene_win_l1():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_win = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_win_text = text4.render("You win !!!", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level1)
                    game = False
                elif button_exit_win.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False
                
        win.fill(WHITE)
        button_again.draw()
        button_exit_win.draw()
        win.blit(you_win_text,(150, 100))
        pygame.display.flip()

def scene_win_l2():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_win = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_win_text = text4.render("You win !!!", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level2)
                    game = False
                elif button_exit_win.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False
        win.fill(WHITE)
        button_again.draw()
        button_exit_win.draw()
        win.blit(you_win_text,(150, 100))
        pygame.display.flip()

def scene_win_l3():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_win = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_win_text = text4.render("You win !!!", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level3)
                    game = False
                elif button_exit_win.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False
        win.fill(WHITE)
        button_again.draw()
        button_exit_win.draw()
        win.blit(you_win_text,(150, 100))
        pygame.display.flip()

def scene_win_l4():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_win = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_win_text = text4.render("You win !!!", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level4)
                    game = False
                elif button_exit_win.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False
        win.fill(WHITE)
        button_again.draw()
        button_exit_win.draw()
        win.blit(you_win_text,(150, 100))
        pygame.display.flip()

def scene_win_l5():
    button_again = Draw_Button(win, RED, 250, 300, 250, 50, "Again", 45)
    button_exit_win = Draw_Button(win, RED, 250, 400, 250, 50, "Exit", 45)
    you_win_text = text4.render("You win !!!", 1, BLACK)
    game = True
    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_again.is_clicked(mouse_pos):
                    switch_scene(scene_level5)
                    game = False
                elif button_exit_win.is_clicked(mouse_pos):
                    switch_scene(scene_play)
                    game = False
        win.fill(WHITE)
        button_again.draw()
        button_exit_win.draw()
        win.blit(you_win_text,(150, 100))
        pygame.display.flip()

def scene_level1():
    global controller
    global platform
    global ball
    global BALL_SPEED
    global ball_x
    global ball_y
    global show_text
    global text_start_time

    block_x = 200
    ball_x = W // 2
    ball_y = H // 1.7
    BALL_SPEED = 5
    game = True
    platform = Platform("platform.png", 300, 550, 150, 5, 10)
    ball = Ball("ball.png", ball_x, ball_y, 50, 50, BALL_SPEED)

    blocks_group = pygame.sprite.Group()
    for row in range(2):
        block_y = 100 + row * 200
        for i in range(3):
            block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
            blocks_group.add(block)
            block_x += 150
        block_x = 200  

    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    switch_scene(scene_pause_l1)
                    game = False

        win.fill(WHITE)

        current_time = pygame.time.get_ticks()
        if show_text and current_time - text_start_time < text_duration:
            win.fill(WHITE)
            display_text(win, text3, "Гра починається!", 250, 250)
        else:
            show_text = False

        platform.update(controller)
        platform.reset()
        ball.update()
        ball.reset()

        if ball.rect.colliderect(platform.rect):
            ball.ball_dy *= -1 

        for block in blocks_group:
            if ball.rect.colliderect(block.rect):
                ball.ball_dy *= -1 
                block.kill()

        if ball.rect.y > 550:
            switch_scene(scene_lose_l1)
            game = False

        elif len(blocks_group) == 0:
            switch_scene(scene_win_l1)
            game = False



        blocks_group.draw(win)

        pygame.display.flip()
        clock.tick(FPS)

def scene_level2():
    global controller
    global platform
    global ball
    global BALL_SPEED
    global ball_x
    global ball_y
    global show_text
    global text_start_time

    block_x = 25
    block_y = 450
    ball_x = W // 2
    ball_y = H // 1.7
    BALL_SPEED = 5
    game = True
    platform = Platform("platform.png", 300, 550, 150, 5, 10)
    ball = Ball("ball.png", ball_x, ball_y, 50, 50, BALL_SPEED)

    blocks_group = pygame.sprite.Group()
    for i in range(6):
        block = GameSprite("Block.png", block_x, block_y, 75, 25, 0)
        blocks_group.add(block)
        block_x += 125
        block_y -= 75

    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    switch_scene(scene_pause_l2)
                    game = False

        win.fill(WHITE)

        current_time = pygame.time.get_ticks()
        if show_text and current_time - text_start_time < text_duration:
            win.fill(WHITE)
            display_text(win, text3, "Гра починається!", 250, 250)
        else:
            show_text = False

        platform.update(controller)
        platform.reset()
        ball.update()
        ball.reset()

        if ball.rect.colliderect(platform.rect):
            ball.ball_dy *= -1 

        for block in blocks_group:
            if ball.rect.colliderect(block.rect):
                ball.ball_dy *= -1 
                block.kill()

        if ball.rect.y > 550:
            switch_scene(scene_lose_l2)
            game = False

        elif len(blocks_group) == 0:
            switch_scene(scene_win_l2)
            game = False



        blocks_group.draw(win)

        pygame.display.flip()
        clock.tick(FPS)

def scene_level3():
    global platform
    global ball
    global BALL_SPEED
    global ball_x
    global ball_y
    global show_text
    global text_start_time

    block_x = 25
    block_y = 450
    ball_x = W // 2
    ball_y = H // 1.7
    BALL_SPEED = 5
    game = True
    platform = Platform("platform.png", 300, 550, 150, 5, 10)
    ball = Ball("ball.png", ball_x, ball_y, 50, 50, BALL_SPEED)

    blocks_group = pygame.sprite.Group()
    for i in range(3):
        block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
        blocks_group.add(block)
        block_y -= 75
        block_x += 150

    block_x = 475
    block_y = 375

    for i in range(2):
        block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
        blocks_group.add(block)
        block_y += 75
        block_x += 150


    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    switch_scene(scene_pause_l3)
                    game = False

        win.fill(WHITE)

        current_time = pygame.time.get_ticks()
        if show_text and current_time - text_start_time < text_duration:
            win.fill(WHITE)
            display_text(win, text3, "Гра починається!", 250, 250)
        else:
            show_text = False

        platform.update(controller)
        platform.reset()
        ball.update()
        ball.reset()

        if ball.rect.colliderect(platform.rect):
            ball.ball_dy *= -1 

        for block in blocks_group:
            if ball.rect.colliderect(block.rect):
                ball.ball_dy *= -1 
                block.kill()

        if ball.rect.y > 550:
            switch_scene(scene_lose_l3)
            game = False

        elif len(blocks_group) == 0:
            switch_scene(scene_win_l3)
            game = False

        blocks_group.draw(win)

        pygame.display.flip()
        clock.tick(FPS)

def scene_level4():
    global platform
    global ball
    global BALL_SPEED
    global ball_x
    global ball_y
    global show_text
    global text_start_time

    block_x = 25
    block_y = 25
    ball_x = W // 2
    ball_y = H // 1.7
    BALL_SPEED = 5
    game = True
    platform = Platform("platform.png", 300, 550, 150, 5, 10)
    ball = Ball("ball.png", ball_x, ball_y, 50, 50, BALL_SPEED)

    blocks_group = pygame.sprite.Group()
    for i in range(3):
        block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
        blocks_group.add(block)
        block_y += 75
        block_x += 150

    block_x = 475
    block_y = 100

    for i in range(2):
        block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
        blocks_group.add(block)
        block_y -= 75
        block_x += 150


    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    switch_scene(scene_pause_l4)
                    game = False

        win.fill(WHITE)

        current_time = pygame.time.get_ticks()
        if show_text and current_time - text_start_time < text_duration:
            win.fill(WHITE)
            display_text(win, text3, "Гра починається!", 250, 250)
        else:
            show_text = False

        platform.update(controller)
        platform.reset()
        ball.update()
        ball.reset()

        if ball.rect.colliderect(platform.rect):
            ball.ball_dy *= -1 

        for block in blocks_group:
            if ball.rect.colliderect(block.rect):
                ball.ball_dy *= -1 
                block.kill()

        if ball.rect.y > 550:
            switch_scene(scene_lose_l4)
            game = False

        elif len(blocks_group) == 0:
            switch_scene(scene_win_l4)
            game = False

        blocks_group.draw(win)

        pygame.display.flip()
        clock.tick(FPS)

def scene_level5():
    global platform
    global ball
    global BALL_SPEED
    global ball_x
    global ball_y
    global show_text
    global text_start_time

    block_x = 25
    block_y = 25
    ball_x = W // 2
    ball_y = H // 1.7
    BALL_SPEED = 5
    game = True
    platform = Platform("platform.png", 300, 550, 150, 5, 10)
    ball = Ball("ball.png", ball_x, ball_y, 50, 50, BALL_SPEED)

    blocks_group = pygame.sprite.Group()
    for i in range(3):
        block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
        blocks_group.add(block)
        block_y += 75
        block_x += 150

    block_x = 475
    block_y = 100

    for i in range(2):
        block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
        blocks_group.add(block)
        block_y -= 75
        block_x += 150
    
    block_x = 25
    block_y = 450

    for i in range(3):
        block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
        blocks_group.add(block)
        block_y -= 75
        block_x += 150

    block_x = 475
    block_y = 375

    for i in range(2):
        block = GameSprite("Block.png", block_x, block_y, 100, 25, 0)
        blocks_group.add(block)
        block_y += 75
        block_x += 150


    while game:
        for e in pygame.event.get():
            if e.type == QUIT:
                switch_scene(None)
                game = False
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    switch_scene(scene_pause_l5)
                    game = False

        win.fill(WHITE)

        current_time = pygame.time.get_ticks()
        if show_text and current_time - text_start_time < text_duration:
            win.fill(WHITE)
            display_text(win, text3, "Гра починається!", 250, 250)
        else:
            show_text = False

        platform.update(controller)
        platform.reset()
        ball.update()
        ball.reset()

        if ball.rect.colliderect(platform.rect):
            ball.ball_dy *= -1 

        for block in blocks_group:
            if ball.rect.colliderect(block.rect):
                ball.ball_dy *= -1 
                block.kill()

        if ball.rect.y > 550:
            switch_scene(scene_lose_l5)
            game = False

        elif len(blocks_group) == 0:
            switch_scene(scene_win_l5)
            game = False

        blocks_group.draw(win)

        pygame.display.flip()
        clock.tick(FPS)

switch_scene(main_menu)
while current_scene is not None:
    current_scene()
pygame.quit()