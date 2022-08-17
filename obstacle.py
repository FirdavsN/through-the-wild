"""
An Obstacle class to represent an obstacle in the game.
"""

# Import modules
import pygame as pg

class Obstacle:
    """Obstacle class."""

    def __init__(self, screen: pg.surface, img: pg.image, init_pos: list[int]):
        """Initialization method.
        
        Arguments:
            screen
                pygame screen to display contents
            img
                obstacle image
            init_pos 
                initial obstacle position; [pos_x, pos_y]
        """
        
        self.screen = screen
        self.img = img
        self.pos = init_pos

        # The obstacle rectangle that represent its hitbox
        self.obs_rect = []
        # SEt the boat's initial obs rect
        self.update_obs_rect()
    
    def update_obs_rect(self):
        """Update the obstacle's rectangle."""

        # pos_x, pos_y, width, height
        self.obs_rect = pg.Rect(self.pos[0] - self.img.get_size()[0]/2, 
                                self.pos[1] - self.img.get_size()[1]/2, 
                                self.img.get_size()[0], 
                                self.img.get_size()[1])

    def move(self, boat_vel: list[float]):
        """Move the obstacle in the river.
        
        Arguments:
            boat_vel
                the boat's velocity vector; [vel_x, vel_y]
        """

        self.pos[1] += boat_vel[1]
    
    def is_colliding_boat(self, boat_poly_coords: list[list[float]]):
        """Determine whether or not the boat has collided with the obstacle.
        
        Arguments:
            boat_poly_coords
                coordinates that represent the boat as a polygon by mapping out 
                its vertices; represents its hit box
        """

        def collide_line_line(l1_p1, l1_p2, l2_p1, l2_p2):
            # normalized direction of the lines and start of the lines
            point_P  = pg.math.Vector2(*l1_p1)
            line1_vec = pg.math.Vector2(*l1_p2) - point_P
            point_R = line1_vec.normalize()
            point_Q  = pg.math.Vector2(*l2_p1)
            line2_vec = pg.math.Vector2(*l2_p2) - point_Q
            point_S = line2_vec.normalize()

            # normal vectors to the lines
            RNV = pg.math.Vector2(point_R[1], -point_R[0])
            SNV = pg.math.Vector2(point_S[1], -point_S[0])
            RdotSVN = point_R.dot(SNV)
            if RdotSVN == 0:
                return False

            # distance to the intersection point
            QP  = point_Q - point_P
            t = QP.dot(SNV) / RdotSVN
            u = QP.dot(RNV) / RdotSVN

            return t > 0 and u > 0 and t*t < line1_vec.magnitude_squared() and u*u < line2_vec.magnitude_squared()

        def collide_rect_line(rect, p1, p2):
            return (collide_line_line(p1, p2, rect.topleft, rect.bottomleft) or
                    collide_line_line(p1, p2, rect.bottomleft, rect.bottomright) or
                    collide_line_line(p1, p2, rect.bottomright, rect.topright) or
                    collide_line_line(p1, p2, rect.topright, rect.topleft))

        def collide_rect_polygon(rect, polygon):
            for i in range(len(polygon)-1):
                if collide_rect_line(rect, polygon[i], polygon[i+1]):
                    return True
            return False

        return collide_rect_polygon(self.obs_rect, boat_poly_coords)
    
    def draw(self):
        """Draw the obstacle on the screen."""

        # Determine the top left coords
        x = self.pos[0] - self.img.get_size()[0] / 2
        y = self.pos[1] - self.img.get_size()[1] / 2

        self.screen.blit(self.img, (x, y))