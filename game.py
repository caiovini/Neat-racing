import pygame as pg
import neat
import sys
import pickle

from tiles import load_map , SCREEN_WIDTH , SCREEN_HEIGHT
from car import Car

WHITE = pg.Color(255, 255, 255)

race_map           = "map.json"
config_file_path   = "config-feedforward.txt"
tiles , collisions = load_map(race_map)
clock              = pg.time.Clock()

def train(genomes , config):
    pg.init
    screen = pg.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
    nets  , cars = [] , []
    rotate_car_angle = 0

    #carTest = Car()
    #carTest.update(200 , 35)
    
    for id , gen in genomes:
        net = neat.nn.FeedForwardNetwork.create(gen, config)
        car = Car()
        car.update(380 , 45) #Initial position
        car.build_radars(collisions , rotate_car_angle )
        
        nets.append(net)
        cars.append(car)
        gen.fitness = 0.0    
    
    def build_map():  
        for tile in tiles:
            if tile:
                screen.blit(tile.image , tile.rect)            
    
    done = False
    while not done:
        build_map()
        #screen.blit(carTest.rotate_image , carTest.rect)  
        #carTest.build_radars(collisions , rotate_car_angle , screen)

        if (rotate_car_angle == 360 or rotate_car_angle == -360):
            rotate_car_angle = 0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                cars.clear()
                pg.quit()
                sys.exit(0)
            
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    cars.clear()
                    pg.quit()
                    sys.exit(0)

        remainders = 0
        for (id , gen) , net , car in zip(genomes , nets , cars):
            
            if car.isAlive:
                remainders += 1
                output = net.activate(car.radars)
                ind = output.index(max(output))

                if(ind == 0):
                    rotate_car_angle -= 1
                    car.rotate(rotate_car_angle) 

                else:
                    rotate_car_angle += 1
                    car.rotate(rotate_car_angle)
                

                car.calculate_new_xy( 10 , rotate_car_angle)
                car.build_radars(collisions , rotate_car_angle )                

                if car.is_colliding(collisions):
                    car.isAlive = False
                    continue       
                
                gen.fitness = car.distance / 100
            
            screen.blit(car.rotate_image , car.rect)  
        
        pg.display.flip()
        clock.tick(60)    

        if not remainders:
            done = True

        
def run_training():
    # Set configuration file
    config_path = config_file_path
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    winner = p.run(train)

    # Display the winning genome.
    print('\nBest genome:\n{!s}'.format(winner))

    with open("winner.pkl", "wb") as file:
        pickle.dump(winner, file)



if __name__ == "__main__":
    run_training()
       

