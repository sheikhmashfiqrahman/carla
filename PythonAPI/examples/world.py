
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

def main(): 
  #world creation and connection of the client
    client = carla.Client('localhost',2000)

    client.set_timeout(10)
    world=client.get_world()
    world=client.load_world('Town03')
    
    #world =client.get_world()

    #print(client.get_available_maps())

    #changing weather

    weather = carla.WeatherParameters(
    cloudiness=80.0,
    precipitation=30.0,
    sun_altitude_angle=70.0)

    world.set_weather(weather)

    print(world.get_weather())

    # Retrieve a snapshot of the world at current frame.
    world_snapshot = world.get_snapshot()
    timestamp = world_snapshot.timestamp
    for actor_snapshot in world_snapshot: # Get the actor and the snapshot information
        actual_actor = world.get_actor(actor_snapshot.id)
        actor_snapshot.get_transform()
        actor_snapshot.get_velocity()
        actor_snapshot.get_angular_velocity()
        actor_snapshot.get_acceleration()  

    actor_snapshot = world_snapshot.find(actual_actor.id)



if __name__== '__main__':
    main()


 





