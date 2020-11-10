import pygame as pg
import math

from os.path import join 

WHITE = pg.Color(255, 255, 255)

class Car(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        path_car = join("assets" , "cars" , "BlackOut.png")
        self.image = pg.transform.scale( pg.image.load( path_car ) , (50 , 50)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rotate_image = self.image
        self.distance = 0
        self.isAlive = True
        self.radars = []

    def update(self , x , y):
        self.rect.x += x
        self.rect.y += y 

    def rotate(self, angle):
        """
        rotate image while keeping its center and size
        use the original image to rotate each time according to the angle
        """
        orig_rect = self.image.get_rect()
        rot_image = pg.transform.rotate(self.image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.rotate_image = rot_image.subsurface(rot_rect).copy()

    def calculate_new_xy(self , speed , angle):

        self.distance += speed
        self.rect.x += math.cos(math.radians(360 - angle)) * speed
        self.rect.y += math.sin(math.radians(360 - angle)) * speed

    def is_colliding(self , collisions):
        return self.rect.collidelist(collisions) >= 0

    def build_radars(self , collisions , angle ):
        self.radars.clear()
        for degree in range (-90, 120, 30): # Draw 7 radars for an angle of 30 degree each
            length , size_pad = 0 , 5
            pad = pg.Rect(self.rect.center[0], self.rect.center[1], size_pad, size_pad) # Use this pad to check collisions of the radars

            """
                Get the collisions of the radar, this is an important component for the NEAT to be able to know when car collision occur
                I am Limiting the distance to up to 180 for all directions of the radars

            """
            while not pad.collidelist(collisions) >= 0 and length < 180:
                
                x = int(self.rect.center[0] + math.cos(math.radians(360 - (angle - degree))) * length)
                y = int(self.rect.center[1] + math.sin(math.radians(360 - (angle - degree))) * length)
                length += 1
                pad = pg.Rect(x, y, size_pad, size_pad)

            dist = int(math.sqrt(math.pow(x - self.rect.center[0]   , 2) + math.pow(y - self.rect.center[1]  , 2)))
            self.radars.append(int(dist))
            #pg.draw.rect(screen, WHITE, pad)


   
