import random

import pygame

from constants import PURPLE

aircolor = (0,0,0)    
scale = 20


class Particle:
    def __init__(self,x,y,allelements,SURFACE):
        #allelements is a REFERENCE to a dictionary containing all element instances
        self.changed = {}
        self.x = x
        self.y = y
        self.allelements = allelements
        self.SURFACE = SURFACE
        
        self.MAX_X_VALUE_MAYBE = 64
        self.MAX_Y_VALUE_MAYBE = 36
    
    def checkkill(self,x,y): #checks to see if particle can be deleted
        if not 0 <= self.x <= self.MAX_X_VALUE_MAYBE:
            self.draw(x,y,aircolor) #wipe pixel
            del self.allelements[(x,y)]
            return True
        elif not 0 <= self.y <= self.MAX_Y_VALUE_MAYBE:
            self.draw(x,y,aircolor)
            del self.allelements[(x,y)]
            return True
        return False
        
    def checktarget(self,x,y):
        if self.allelements.get( (x,y) ) == None: #return whatever object is at target location, or False if not
            return True #if space is EMPTY return TRUE
        else: #if space is occupied, return FALSE (used to return occupier but i nixed that functionality)
            return False
    
    def targetcolor(self,x,y): #very similar to the above, but instead of returning boolean, returns occupier object
        if self.allelements.get( (x,y) ) == None: #return whatever object is at target location, or False if not
            return self.allelements.get( (None,None) ).color #if space is empty return NULLELEMENT
        else:
            return self.allelements.get( (x,y) ).color
    
    def draw(self,x,y,color):
        self.SURFACE.fill(color, pygame.Rect(x*scale, y*scale, scale, scale))
        return

    def goto(self, newx,newy, overwritechance = 0.0):
        global changed
        if (self.checktarget(newx,newy) ) or random.random()<overwritechance: #go ahead with move IF space is free
            (oldx,oldy) = (self.x,self.y)
            del self.allelements[(oldx,oldy)] #delete current location from instance dictionary
            self.draw(oldx,oldy,aircolor) #delete old pixel
            (self.x,self.y) = (newx,newy)
            self.allelements[(newx,newy)] = self
            self.draw(newx,newy,PURPLE)
            self.changed[(oldx,oldy)] = True
            self.changed[(newx,newy)] = True
            return True
        return False #otherwise return "failed" boolean
        
class Metal(Particle): #metal just sits there and doesnt move
    def __init__(self,x,y,allelements,SURFACE):
        self.color = PURPLE
        Particle.__init__(self,x,y,allelements,SURFACE) 
        self.draw(self.x, self.y,self.color) 
        
    def update(self):
        pass
    
            
    
class Sand(Particle): #sand behaves like a very viscous liquid, BUT is CLASSED as a solid
    def __init__(self,x,y,allelements,SURFACE):
        self.color = PURPLE
        self.flowchance = 0.03 #chance to behave as liquid per tick (CAN CHANGE IF WET)
        Particle.__init__(self,x,y,allelements,SURFACE)
        self.draw(self.x, self.y,self.color) 
        
        
    def update(self):
        if self.checkkill(self.x,self.y):
            return
        
        updates = 0 #start with zero actions
            
        flowdirection = random.randint(0,1) * 2 - 1 #returns +-1, decides if particle moves left or right
        if random.random() > self.flowchance: #LARGE chance to not flow at all for sand
            flowdirection = 0 #i.e: dont flow   
        while updates < 2:
            #if self.goto( self.x, self.y + 2): #if space is available to fall down 2 spaces
            #    updates += 2
            if self.goto( self.x, self.y + 1):
                updates +=1 #log one cycle as complete
            if self.goto(self.x + flowdirection, self.y): #if space is available to go sideways
                pass
            updates += 2
            
class NullElement(Particle): #this placeholder sits at (None,None) and does NOTHING
    def __init__(self,allelements,SURFACE):
        self.color = None
        self.x = None
        self.y = None
        Particle.__init__(self,self.x,self.y,allelements,SURFACE)
    def update(self):
        pass
        
