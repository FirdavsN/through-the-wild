"""
A Coin class to represent an animated coin in the game.
"""

# Import modules
import pygame as pg
import os

class Coin:
    """Coin Class."""

    # counter to go through frames of images in animation
    counter = 0

    def __init__(self, 
                 screen: pg.surface, 
                 init_pos: list[int], 
                 animation_dir: str, 
                 animation_speed=.1):
        """Initialization method.
        
        Arguments:
            screen
                pygame screen to display contents
            pos 
                coin position; [pos_x, pos_y]
            animation_dir
                directory containing all of the images needed to animate coins
            animation_speed : float

        """
        
        self.screen = screen
        self.pos = init_pos
        self.animation_dir = animation_dir
        self.animation_speed = animation_speed
        
        # Number of images in animation
        self.num_files = self.num_files_in_dir(animation_dir)

        # Whether or not Coin is displayed on the screen
        self.on_screen = True

    def num_files_in_dir(self, dir: str):
        """Determine the number of files in dir.
        
        Args:
            dir
                directory to find number of files in
        """

        count = 0
        for path in os.listdir(dir):
            if os.path.isfile(os.path.join(dir, path)):
                count += 1

        return count

    def move(self, boat_vel: list[float]):
        """Move the coin in the river.

        Arguments:
            boat_vel
                the boat's velocity vector; [vel_x, vel_y]
        """

        self.pos[1] += boat_vel[1]

    def draw(self):
        """Display Coin on screen by flipping through each animation image on 
        repeat."""
        
        if self.on_screen:
            if self.counter % 1 == 0:
                # Current animation frame filename
                self.filename = \
            f"{self.animation_dir}/{int(self.counter % self.num_files + 1)}.png"
            
            # Current animation frame
            img = pg.image.load(self.filename)

            # Determine the top left coords
            x = self.pos[0] - img.get_size()[0]/2
            y = self.pos[1] - img.get_size()[1]/2

            self.screen.blit(img, (x, y))

            # Increment the counter by animation_speed
            self.counter += self.animation_speed
            self.counter = round(self.counter, 1)

