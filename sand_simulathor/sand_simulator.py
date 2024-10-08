import random

from .trashcan import Metal, Sand


class SandSimulator:
    def __init__(self, colorWorld):
        self.color = colorWorld

        self.allelements = {}

        self.MAX_X_VALUE_MAYBE = 65
        self.MAX_Y_VALUE_MAYBE = 36

        self.MAX_NUM_PARTICLES = self.MAX_X_VALUE_MAYBE * self.MAX_Y_VALUE_MAYBE

        self.bucket_on = True


        self.pensize = 1

        self.is_init = False


    def globalchecktarget(self, x,y):
        return self.allelements.get( (x,y) ) == None

    def draw_sand(self,elementtype,x,y,pensize,surface):
        for xdisp in range(-pensize,pensize):
            for ydisp in range(-pensize,pensize):
                if self.globalchecktarget(x+xdisp,y+ydisp):
                    self.allelements[(x+xdisp,y+ydisp)] = elementtype(x+xdisp,y+ydisp,self.allelements,surface, self.color)

    def set_bucket_bottom(self, set_on : bool, surface):
        for x in range (0, self.MAX_X_VALUE_MAYBE):
            for i in range(4):
                if set_on:
                    self.allelements[(x,self.MAX_Y_VALUE_MAYBE+i)] = Metal(x,self.MAX_Y_VALUE_MAYBE+i,self.allelements,surface,self.color)
                else:
                    del self.allelements[(x,self.MAX_Y_VALUE_MAYBE+i)]

    def init_sand_bucket(self, surface):
        self.set_bucket_bottom(True, surface)
        for y in range (0, self.MAX_Y_VALUE_MAYBE):
            self.allelements[(0,y)] = Metal(0-1,y,self.allelements,surface,self.color)
            self.allelements[(self.MAX_X_VALUE_MAYBE,y)] = Metal(self.MAX_X_VALUE_MAYBE,y,self.allelements,surface,self.color)

    def update_particles(self):
        compteur = 0
        for element in list(self.allelements.keys()):
            try:
                self.allelements[element].update()
            except KeyError:
                pass

    def draw_particles(self, overflow_ammount, surface):
        for element in list(self.allelements.keys()):
            x = self.allelements[element].x - 1
            y = self.allelements[element].y
            self.allelements[element].draw(x, y, self.color)

        if not self.is_init:
            self.init_sand_bucket(surface)
        if len(self.allelements) / self.MAX_NUM_PARTICLES * 100.0 < overflow_ammount:
            if not self.bucket_on:
                self.set_bucket_bottom(True, surface)
                self.bucket_on = True
            for _ in range(3):
                self.draw_sand(Sand,random.randint(0,self.MAX_X_VALUE_MAYBE),0,self.pensize, surface)
        if self.bucket_on and len(self.allelements) / self.MAX_NUM_PARTICLES * 100.0 > overflow_ammount + 2.0:
            self.set_bucket_bottom(False, surface)
            self.bucket_on = False
