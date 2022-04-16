
from ast import Lambda
from concurrent.futures import process
import glob
import os
import sys
import random
import time
from types import LambdaType
import numpy as np
import cv2


try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla

IM_WIDTH=640
IM_HEIGHT=480

actor_list= []

def process_img(image):
    i= np.array(image.raw_data) # raw data is the flatten array of image object
   # print(dir(image))
    print(i.shape)
    i2 = i.reshape(IM_HEIGHT,IM_WIDTH,4)
    i3 = i2[:,:,:3]
    # cv2.imshow("",i3)
    # cv2.waitKey(1)
    return i3/255.0

try: 
    # create the client to the world, set time out for 2 ms, 10 ms is too much 
    client = carla.Client("localhost", 2000)
    # world = client.get_world()
    # below code is for printing out the list of blue print actors
    # blueprints = [bp for bp in world.get_blueprint_library().filter('*')]
    # for blueprint in blueprints:
    #     print(blueprint.id)
    #     for attr in blueprint:
    #         print('  - {}'.format(attr))
    client.set_timeout(50.0)

    #A client can connect and retrieve the current world fairly easily.
    world = client.get_world()

    #The client can also get a list of available maps to change the current one. 
    # This will destroy the current world and create a new one.
    world = client.load_world('Town01')
    blueprint_library = world.get_blueprint_library()
    #select a vehicle model from the blue print
    bp = blueprint_library.filter("vehicle.dodge.charger_police")[0]
    print(bp)

    #spawning at random location
    spawn_point= random.choice(world.get_map().get_spawn_points())

    vehicle = world.spawn_actor(bp,spawn_point)
    #vehicle.set_autopilot(True)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0,steer=0.0))
    actor_list.append(vehicle)
    

    #attaching a RGB camera to the car

    cam_bp = blueprint_library.find('sensor.camera.rgb')
    cam_bp.set_attribute("image_size_x",f"{IM_WIDTH}")
    cam_bp.set_attribute("image_size_y",f"{IM_HEIGHT}")
    cam_bp.set_attribute("fov","110")
    
    spawn_point=carla.Transform(carla.Location(x=2.5,z=.7)) 

    #creating a sensor for collecting data from the world as image 
    sensor = world.spawn_actor(cam_bp,spawn_point,attach_to=vehicle)
    actor_list.append(sensor)

    sensor.listen(lambda data : process_img(data))
    #sensor.listen(lambda image: image.save_to_disk('output/%d064.png'%image.frame))

    time.sleep(20)

finally:
    for actor in actor_list:
        actor.destroy()
    print("All cleaned up")



