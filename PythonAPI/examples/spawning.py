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
    actor_list=[]
    try:
        client = carla.Client('localhost',2000)
        client.set_timeout(10)
        world=client.load_world('Town01')

        bp=world.get_blueprint_library()
        car_bp=bp.filter("cybertruck")[0]
        transform = carla.Transform(carla.Location(x=230, y=195, z=40),carla.Rotation(yaw=180))
        car =world.spawn_actor(car_bp,transform)
        actor_list.append(car)

        time.sleep(15)

    finally:
        pass


if __name__=='__main__':
    main()




