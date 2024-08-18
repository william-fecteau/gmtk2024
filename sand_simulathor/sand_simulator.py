from .trashcan import Metal, Sand
import random

class SandSimulator:
    def __init__(self):
        self.allelements = {}

        self.MAX_NUM_PARTICLES = 128. * 72.

        self.bucket_on = True


        self.pensize = 5

        self.is_init = False


    def globalchecktarget(self, x,y):
        return self.allelements.get( (x,y) ) == None

    def draw_sand(self,elementtype,x,y,pensize,surface):
        for xdisp in range(-pensize,pensize):
            for ydisp in range(-pensize,pensize):
                if self.globalchecktarget(x+xdisp,y+ydisp):
                    self.allelements[(x+xdisp,y+ydisp)] = elementtype(x+xdisp,y+ydisp,self.allelements,surface)

    def set_bucket_bottom(self, set_on : bool, surface):
        for x in range (0, 128):
            for i in range(4):
                if set_on:
                    self.allelements[(x,71+i)] = Metal(x,71+i,self.allelements,surface)
                else:
                    del self.allelements[(x,71+i)]

    def init_sand_bucket(self, surface):
        self.set_bucket_bottom(True, surface)
        for y in range (0, 72):
            self.allelements[(0,y)] = Metal(0,y,self.allelements,surface)
            self.allelements[(127,y)] = Metal(127,y,self.allelements,surface)

    def update_particles(self):
        for element in list(self.allelements.keys()):
            try:
                self.allelements[element].update()
            except KeyError:
                pass

    def draw_particles(self, overflow_ammount, surface):
        for element in list(self.allelements.keys()):
            beige = (255,0,255)
            x = self.allelements[element].x
            y = self.allelements[element].y
            self.allelements[element].draw(x, y, beige)
            
        if not self.is_init:
            self.init_sand_bucket(surface)
        if len(self.allelements) / self.MAX_NUM_PARTICLES * 100.0 < overflow_ammount:
            print("producing")
            if not self.bucket_on:
                self.set_bucket_bottom(True, surface)
                self.bucket_on = True
            for _ in range(3):
                self.draw_sand(Sand,random.randint(0,128),0,self.pensize, surface)
        if self.bucket_on and len(self.allelements) / self.MAX_NUM_PARTICLES * 100.0 > overflow_ammount + 2.0:
            print("removing")
            self.set_bucket_bottom(False, surface)
            self.bucket_on = False
        print(len(self.allelements) / self.MAX_NUM_PARTICLES * 100)
