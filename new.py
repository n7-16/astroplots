import pygame
import numpy as np
from pygame.locals import *

class planet:
    def __init__(self, a, e, p):
        self._running = True
        self._display_surf = None
        self._render_surf = None
        self.size = self.width,self.height = 1000, 562.5
        self.rotated = False
        self.printdebug = False
        self.semimajor = a
        self.semiminor = self.semimajor*np.sqrt(1-e**2)
        self.perihelion = p
        self._rotated_surf = None
        pygame.clock = pygame.time.Clock()

    def on_init(self):
        pygame.init()
        self._running = True
        self._render_surf = pygame.Surface((self.semimajor, self.semiminor))
        self._display_surf = pygame.display.set_mode(self.size,pygame.HWSURFACE|pygame.DOUBLEBUF)
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self):
        pass
    def on_render(self):
        pass
    def on_cleanup(self):
        pygame.quit()
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while self._running:
            
            for event in pygame.event.get():
                
                self._target_rect = pygame.Rect((self.width/2-self.perihelion/2, self.height/2-self.semiminor/2), (self.semimajor, self.semiminor))
                self.on_event(event)
                pygame.draw.ellipse(self._render_surf, "#ff0000",(0, 0, self.semimajor, self.semiminor), 3)
                if not self.rotated:
                    self._rotated_surf = pygame.transform.rotate(self._render_surf, 180)
                    self.rotated =  True
                self._display_surf.blit(self._rotated_surf, self._rotated_surf.get_rect(center=self._target_rect.center))
                pygame.display.flip()
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    newPlanet = planet(150, 50, 15)
    newPlanet.on_execute()
