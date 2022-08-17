"""
A Coins class to represent all of the coins displayed on the screen.
"""

# Import modules
import pygame as pg
import random
from coin import Coin

class Coins:
    """Coins class."""

    def __init__(self, screen: pg.surface, animation_dir: str):
        """Initialization method.
        
        Arguments:
            screen
                pygame screen to display contents
            animation_dir
                directory containing all of the images needed to animate coins
        """

        self.screen = screen
        self.animation_dir = animation_dir

        # List to store all coins
        self.coins = []

    def gen_new_coin(self, 
                     dist_btwn_coins: int, 
                     river_lanes: list[int], 
                     obstacles: list):
        """Generate a new coin.
        
        Arguments:
            dist_btwn_coins
                the minimum number of vertical pixels between each coin
            river_lanes
                middle x-coords of the three lanes in the river
            obstacles
                contains all obstacles currently on the screen
        """

        # Check if enough distance between last coin
        if len(self.coins) == 0 or self.coins[-1].pos[1] >= dist_btwn_coins:
            # Generate random lane number
            randLane = random.randint(0, 2)

            # Place coin off of screen in the random lane
            pos = [river_lanes[randLane], -100]

            # Only generate a coin if there are no obstacles taking its spot
            if abs(pos[1] - obstacles[-1].pos[1]) > 300 and \
                pos[0] != obstacles[-1].pos[0]:

                self.coins.append(Coin(self.screen, pos, self.animation_dir))

    def update(self, boat_vel: list[float], SCREEN_H: int):
        """Update every coin's position.
        
        Arguments:
            boat_vel
                boat velocity vector; [vel_x. vel_y]
            SCREEN_H
                screen height in pixels
        """

        # NOTE: using a while loop instead of a for loop due to removing from
        # array in the middle of loop
        count = 0
        while count < len(self.coins):
            coin = self.coins[count]
            # Move the coin based on the boat's velocity -> in sync with 
            # background and obstacles
            coin.move(boat_vel)

            # If the coin is out of the screen, remove it from the list
            if coin.pos[1] > SCREEN_H + 50:
                self.coins.remove(coin)
                count += 1
            count += 1

    def is_colliding_boat(self, boat_pos: list[float, float]) -> bool:
        """Check whether or not the boat has collided (picked up) a coin.
        
        Arguments:
            boat_pos
                boat position; [pos_x, pos_y]
        
        Returns:
            whether or not any collisions occured
        """

        # Distance between boat_pos and coin_pos for collision to occur
        r = 50

        for coin in self.coins:
            # Only collide if coin on screen and is close enough to boat
            if coin.on_screen and \
                abs(boat_pos[0] - coin.pos[0]) < r and \
                    abs(boat_pos[1] - coin.pos[1]) < r:
                
                coin.on_screen = False
                self.coins.remove(coin)
                
                return True
        return False
        
    def draw(self):
        """Draw each coin on the screen."""

        for coin in self.coins:
            coin.draw()