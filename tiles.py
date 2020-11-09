import pygame as pg
import json

from os.path import join 
from concurrent.futures import ThreadPoolExecutor

background__tile_size = 100
road_size             = 125
SCREEN_WIDTH          = 1000
SCREEN_HEIGHT         = 800


class Tile(pg.sprite.Sprite):

    def __init__(self , image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

    def update(self , x , y):
        self.rect.x = x
        self.rect.y = y 

    def rotate(self, angle):
        """
        rotate image while keeping its center and size
    
        """
        orig_rect = self.image.get_rect()
        rot_image = pg.transform.rotate(self.image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        self.image = rot_image.subsurface(rot_rect).copy()


class Soil(Tile):

    def __init__(self):
        path_soil       = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Background_Tiles")
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join(path_soil , "Soil_Tile.png")) , (background__tile_size , background__tile_size)))

class Road_02_01(Tile):

    def __init__(self):
        path_road_02_01 = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Road_02" , "Road_02_Tile_01" )
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join( path_road_02_01 ,  "Road_02_Tile_01.png")) , (road_size , road_size)))

class Road_02_02(Tile):

    def __init__(self):
        path_road_02_02 = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Road_02" , "Road_02_Tile_02" )
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join( path_road_02_02 ,  "Road_02_Tile_02.png")) , (road_size , road_size)))

class Road_02_03(Tile):

    def __init__(self):
        path_road_02_03 = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Road_02" , "Road_02_Tile_03" )
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join( path_road_02_03 ,  "Road_02_Tile_03.png")) , (road_size , road_size)))
        

class Road_02_04(Tile):

    def __init__(self):
        path_road_02_04 = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Road_02" , "Road_02_Tile_04" )
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join( path_road_02_04 ,  "Road_02_Tile_04.png")) , (road_size , road_size)))
        
class Road_02_05(Tile):

    def __init__(self):
        path_road_02_05 = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Road_02" , "Road_02_Tile_05" )
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join( path_road_02_05 ,  "Road_02_Tile_05.png")) , (road_size , road_size)))

class Road_02_06(Tile):

    def __init__(self):
        path_road_02_06 = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Road_02" , "Road_02_Tile_06" )
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join( path_road_02_06 ,  "Road_02_Tile_06.png")) , (road_size , road_size)))

class Road_02_07(Tile):

    def __init__(self):
        path_road_02_07 = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Road_02" , "Road_02_Tile_07" )
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join( path_road_02_07 ,  "Road_02_Tile_07.png")) , (road_size , road_size)))

class Road_02_08(Tile):

    def __init__(self):
        path_road_02_08 = join("assets" , "Race-Track-Tile-Set-PNG" , "PNG" , "Road_02" , "Road_02_Tile_08" )
        Tile.__init__(self ,  pg.transform.scale( pg.image.load( join( path_road_02_08 ,  "Road_02_Tile_08.png")) , (road_size , road_size)))
        

def _switch(arg ):
    switcher = {
        "Soil" : Soil(),
        "Road_02_01" : Road_02_01(),
        "Road_02_02" : Road_02_02(),
        "Road_02_03" : Road_02_03(),
        "Road_02_04" : Road_02_04(),
        "Road_02_05" : Road_02_05(),
        "Road_02_06" : Road_02_06(),
        "Road_02_07" : Road_02_07(),
        "Road_02_08" : Road_02_08()
    }
    return switcher.get(arg, None) 


def load_map(map_number):
    tiles = []
    collisions = []
    path_map = join("assets" , "map")

    columns = int(SCREEN_WIDTH / background__tile_size)
    lines = int(SCREEN_HEIGHT / background__tile_size)


    def load_background():

        tls = []
        # Background
        for y in range(lines):
            for x in range(columns):
                soil = Soil()
                soil.update(x * background__tile_size , y * background__tile_size)
                tls.append(soil)

        return tls

    def load_racing_map(race_tiles):
        tls = []
        for tile in race_tiles:
            tile_map = _switch(tile["tile"])
            tile_map.update(tile["positionX"] , tile["positionY"])
            tile_map.rotate(tile["angle"])
            tls.append(tile_map)

        return tls

    def load_collisions(race_colissions):
        cols = []
        for collision in race_colissions:
            collision_rect = pg.Rect(collision["positionX"] , collision["positionY"] ,
                                     collision["width"]     , collision["height"])

            cols.append(collision_rect)

        return cols

    with open(join(path_map , map_number), "r") as myfile:
        data = myfile.read()
        obj  = json.loads(data)
        with ThreadPoolExecutor(max_workers = 3) as executor:
            bk_tiles = executor.submit(load_background)  
            rc_tiles = executor.submit(load_racing_map , obj["map"])   
            co_tiles = executor.submit(load_collisions , obj["collisions"]) 

            tiles.extend(bk_tiles.result())
            tiles.extend(rc_tiles.result())
            collisions.extend(co_tiles.result())  

          
    return tiles , collisions

