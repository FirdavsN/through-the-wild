"""
Class to represent the Background of the game, whether in the actual game or 
the title screen.
"""

# Import modules
import pygame as pg

class Background:
    """Background class. In the game, the background is a loop of two identical
    images that move based on the boat's vertical velocity."""

    def __init__(self, screen: pg.surface, img: pg.image):
        """Intialization method.
        
        Arguments:
            screen
                pygame screen to display contents
            img
                background image
        """

        self.screen = screen
        self.img = img

        # The vetical amount of pixels in the background image
        self.img_height = img.get_size()[1]

        # Initial positions of the two images
        self.pos_1 = [0, 0]
        self.pos_2 = [0, -self.img_height]

    def move(self, boat_vel: list[float]):
        """Move the two images based on the boat's vertical velocity."""

        self.pos_1[1] += boat_vel[1]
        self.pos_2[1] += boat_vel[1]

    def loop_imgs(self):
        """Loop or swap the images once the bottom images is out of the screen.
        """
        
        # If the first image is out of the screen, swap images and reset
        # positions
        if self.pos_1[1] > self.img.get_size()[1]:
            self.pos_1 = self.pos_2
            self.pos_2 = [0, -self.img_height]

    def draw(self):
        """Draw the two images on the screen."""

        self.screen.blit(self.img, self.pos_1)
        self.screen.blit(self.img, self.pos_2)
