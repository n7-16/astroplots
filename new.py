import pygame
import numpy as np
from pygame.locals import *
import sys
size = width, height = 1000, 562.5
_display_surf = pygame.display.set_mode(size,pygame.HWSURFACE|pygame.DOUBLEBUF)

class construct:
    def elip(self, width, height, semimajor, semiminor, perihelion, _render_surf, color="red"):
        self.semimajor, self.semiminor, self.perihelion, self.width, self.height, self._render_surf = semimajor, semiminor, perihelion, width, height, _render_surf 
        self._target_rect = pygame.Rect((self.width/2-self.perihelion/2, self.height/2-self.semiminor/2), (self.semimajor, self.semiminor))
        return self._target_rect

class rotate:
    def rotate_elip(self, _render_surf, omega):
        self._render_surf = _render_surf
        self._rotated_surf = pygame.transform.rotate(self._render_surf, omega)
        return self._rotated_surf
    
class draw:
    def draw_elip(self, _render_surf, _target_rect, color="red"):
        self._render_surf, self._target_rect = _render_surf, _target_rect
        pygame.draw.ellipse(self._render_surf, color,(0, 0, self._target_rect.width, self._target_rect.height), 3)
    
class planet:  
    def __init__(self, a, e, p, omega, color = "red"):
        self._render_surf = None
        # self._display_surf = None
        self.size = self.width,self.height = 1000, 562.5
        self.rotated = False
        self.printdebug = False
        self.semimajor = a
        self.semiminor = int(self.semimajor*np.sqrt(1-e**2))
        self.perihelion = p
        self._rotated_surf = None
        self.omega = omega
        self.color = color
        global _display_surf
        self.on_init()

    def on_init(self):
        pygame.init()
        self._running = True
        self._render_surf = pygame.Surface((self.semimajor, self.semiminor),pygame.SRCALPHA, 32)
        self._render_surf = self._render_surf.convert_alpha()
        self.render()
        
    def render(self):
        constructpl = construct()
        drawpl = draw()
        rotatepl = rotate()
        self._target_rect = constructpl.elip(self.width, self.height, self.semimajor, self.semiminor, self.perihelion, self._render_surf)
        drawpl.draw_elip(self._render_surf, self._target_rect)
        self._rotated_surf = rotatepl.rotate_elip(self._render_surf, self.omega)
        _display_surf.blit(self._rotated_surf, self._rotated_surf.get_rect(center=self._target_rect.center))
        
    
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pass
        
    

class run:
    def __init__(self):  
        self._running = False
        self.planet1 = planet(150, 0, 15, 180)
        self.planet2 = planet(500, 0.9, 20, 30)
        
        self.loop()
    def on_event(self, event):
        if event == pygame.QUIT:
            self._running = False
    def cleanup():
        pygame.display.quit()
        pygame.quit()
        sys.exit()
    def loop(self):
        self._running = True
        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            pygame.display.update()
        self.cleanup()
    
        
if __name__ == "__main__":
    run1 = run()
    print()
