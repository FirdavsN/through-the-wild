"""
An Obstacles class to represent all of the obstacles displayed on the screen.
"""

# Import modules
from obstacle import Obstacle
import pygame as pg
import random

class Obstacles:
    """Obstacles class."""
    
    def __init__(self, screen: pg.surface, imgs: list):
        """Initialization method.
        
        Arguments:
            screen
                pygame screen to display contents
            imgs
                images for all types of obstacles
        """

        self.screen = screen
        self.imgs = imgs

        # List to store all obstacles
        self.obstacles = []
    
    def gen_new_obs(self, 
                    gen_chance: float, 
                    dist_btwn_obs: int, 
                    river_lanes: list[int]):
        """Generate a new obstacles.
        
        Arguments:
            gen_chance
                chance to generate new obstacles; 0-1
            dist_btwn_obs
                the minimum number of vertical pixels between each coin
            river_lanes
                middle x-coords of the three lanes in the river
        """

        # Check if enough distance between last obstacle and randomly generate
        if len(self.obstacles) == 0 or \
            self.obstacles[-1].pos[1] >= dist_btwn_obs and \
                random.random() < gen_chance:

            # Generate random lane number and random type of obstacle 
            # (log or rock)
            rand_lane = random.randint(0, 2)
            rand_obs_type = random.randint(0, 1)

            # Place obstacle off of screen in the random lane
            pos = [river_lanes[rand_lane], -100]

            # Index random obstacle image
            img = self.imgs[rand_obs_type]

            self.obstacles.append(Obstacle(self.screen, img, pos))

    def update(self, boat_vel: list[float], SCREEN_H: int):
        """Update every obstacle's position.

        Arguments:
            boat_vel
                boat velocity vector; [vel_x. vel_y]
            SCREEN_H
                screen height in pixels
        """

        # NOTE: using a while loop instead of a for loop due to removing from
        # array in the middle of loop
        count = 0
        while count < len(self.obstacles):
            obs = self.obstacles[count]
            # Move the obstacle based on the boat's velocity -> in sync with 
            # background and coins
            obs.move(boat_vel)

            # If the obstacle is out of the screen, remove it from the list
            if obs.pos[1] > SCREEN_H + 50:
                self.obstacles.remove(obs)
                count += 1
            count += 1
        
    def is_colliding_boat(self, boat_poly_coords: list[list[float]]) -> bool:
        """Check whether or not the boat has collided with any obstacles.
        
        Arguments:
            boat_poly_coords
                boat polygon coordinates
        
        Returns:
            whether or not any collision occured
        """

        for obs in self.obstacles:
            # Update the rectangle representing the obstacle's hit box
            obs.update_obs_rect()
            if obs.is_colliding_boat(boat_poly_coords):
                return True
        return False

    def get_obstacles(self) -> list[Obstacle]:
        """Return the list of all obstacles.
        
        Returns:
            obstacles
        """

        return self.obstacles

    def draw(self):
        """Draw all obstacles on the screen."""

        for obs in self.obstacles:
            obs.draw()