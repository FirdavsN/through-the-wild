"""
A Boat class to represen the boat's visuals, mechanics and interactions in
the game.
"""

# Import modules
import math
import pygame as pg

class Boat:
    """Boat class."""

    def __init__(self, screen: pg.surface, img: pg.image, 
                 init_pos: tuple[int], speed: int):
        """Initialization method.
        
        Arguments:
            screen
                pygame screen to display contents
            img
                boat image
            init_pos
                the boat's initial position on the screen
            speed
                the boat's constant speed throughout the game
                NOTE: speed is the magnitude of its velocity vector
        """
        
        self.screen = screen
        self.img = img
        self.pos = list(init_pos)
        self.speed = speed

        # Angle at which boat is pointing; 0 is straight up, 90 is to the left
        self.boat_dir = 0

        # Boat's velocity vector
        self.vel = []
        # Set the boat's initial velocity
        self.update_vel()

        # Coordinates that represent the boat as a polygon by mapping out its
        # vertices; represents its hit box
        self.poly_coords = []
        # Set the boat's initial poly coords
        self.update_poly_coords()

        # THe boat image's alpha value or transparency
        self.transparency = 255 # 0 (fully) - 255 (opaque)
    
    def get_vel(self) -> list[float]:
        """Return the boat's velocity vector.
        
        Returns:
            vel
                velocity vector
        """

        return self.vel

    def update(self, turn_dir: str, river_edges: list[int]):
        """Update the boat's velocity, direction, position, and poly coords.
        
        Arguments:
            turn_dir
                whether to turn the boat counter-clockwise or clockwise
            river_edges:
                x-coords of the left and right of the river
        """

        self.update_vel()
        self.update_boat_dir(turn_dir)
        self.update_pos(river_edges)
        self.update_poly_coords()
    
    def update_vel(self):
        """Update the boat's velocity vector."""

        # Determine the components of the velocity vector based on the boat 
        # direction and the speed (the magnitude of the vector)
        vel_x = self.speed * math.cos((self.boat_dir + 90) * math.pi/180)
        vel_y = self.speed * math.sin((self.boat_dir + 90)  * math.pi/180)

        self.vel = [vel_x, vel_y]
    
    def update_boat_dir(self, turn_dir: str):
        """Update the boat's angle of movement.
        
        Arguments:
            turn_dir
                whether to turn the boat counter-clockwise or clockwise
        """

        # The rate at which to change the boat's direction
        dt = 1

        # Only turn the boat until it is fully pointing left or right
        if turn_dir == "cc" and self.boat_dir <= 90:
            self.boat_dir += dt
        elif turn_dir == "c" and self.boat_dir >= -90:
            self.boat_dir -= dt
        
        
        t = .3

        # If the boat is leaning some way then make the water act as resistance 
        # and make it lean more that way until it is fully pointing that way
        if 0 < self.boat_dir < 90:
            self.boat_dir += dt * t
        elif -90 < self.boat_dir < 0:
            self.boat_dir -= dt * t
        
    def update_pos(self, river_edges: list[int]):
        """Update the boat's position"""

        # Factor to increment the boat's position by its velocity
        # The larger the faster the boat moves.
        t = .25

        self.pos[0] += t * self.vel[0]

        # Offset from the edges of the river when
        offset = 35
        # Make sure boat stays in the water
        if self.pos[0] <= river_edges[0] + offset:
            self.pos[0] = river_edges[0] + offset
        elif self.pos[0] >= river_edges[1] - offset:
            self.pos[0] = river_edges[1] - offset
    
    def update_poly_coords(self):
        """Update the boat's polygon coordinates"""

        # Convert the boat's direction from degrees to radians
        boat_dir_rad = self.boat_dir * math.pi/180

        # Pre determined coordinates of the polygon when the baot is in the 
        # position (0, 0)
        points = [(0, -75), (25, -37), (25, 53), (16, 75), (-16, 75), 
                  (-25, 53), (-25, -37)]
        
        # Reset poly coords
        self.poly_coords = []

        # Calculate each vertix of the polygon and append it to poly_coords
        for point in points:
            x = (point[0]) * math.cos(boat_dir_rad) + \
                (point[1]) * math.sin(boat_dir_rad) + \
                self.pos[0]
            y = (point[1]) * math.cos(boat_dir_rad) - \
                (point[0]) * math.sin(boat_dir_rad) + \
                self.pos[1]

            self.poly_coords.append([x, y])

    def get_poly_coords(self) -> list[list[float]]:
        """Return poly_coords.
        
        Returns:
            poly_coords
                the boat's polygon coordinates
        """

        return self.poly_coords
    
    def get_pos(self) -> list[float]:
        """Return the boat's position.

        Returns
            pos
                the boat's position on the screen
        """

        return self.pos

    def sink(self, dt: int):
        """Sink the boat.
        
        Arguments:
            dt
                the rate at which to make the boat sink
        """

        # Make the boat's image more transparent only if it is any visible
        if self.transparency > 0:
            self.transparency -= dt

    def has_sunk(self) -> bool:
        """Return whether or not the boat has sunk.
        
        Returns:
            whether or not the boat has sunk
        """

        if self.transparency <= 0:
            return True
        return False

    def draw(self):
        """Draw the boat on the screen."""

        # Retrieve x and y coords
        x = self.pos[0]
        y = self.pos[1]

        # Rotate image based on boat_dir
        rotated_img = pg.transform.rotozoom(self.img, self.boat_dir, 1)

        # Translate iamge to ensure the rotated image is positioned correctly
        x -= rotated_img.get_size()[0] / 2
        y -= rotated_img.get_size()[1] / 2

        # Set the boat's transparency (or alpha) value
        rotated_img.set_alpha(self.transparency)

        self.screen.blit(rotated_img, (x, y)) 

        # Draw the polygon coordinates
        # NOTE: used for debugging
        # self.draw_poly_points()

    def draw_poly_points(self):
        for dot in self.poly_coords:
            pg.draw.circle(self.screen, (255, 0, 0), dot, 5)