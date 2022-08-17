"""
Through The Wild

An endless runner game but with a boat. The player must avoid obstacles while 
going down a river and trying to stay alive.
"""

__author__ = "Firdavs Nasriddinov"
__version__ = 1.0

# Import modules
from background import Background
from boat import Boat
from coins import Coins
from database import Database
from obstacles import Obstacles
import pygame as pg
from title import TitleScreen

class Game:
    """Class to run the game."""

    # Screen dimensions
    SCREEN_W = 900
    SCREEN_H = 900

    FPS = 120

    # Initial boat posiion
    INIT_BOAT_POS = (450, 700)

    # Distance between obstacles and coins
    DIST_BTWN_OBS = 450         # larger -> easier
    DIST_BTWN_COINS = 200       # larger -> less coins
    
    # Connects to web-hosted database that stores all user data
    database = Database(host=
            "through-the-wild-db.c2qg3xrknhut.ap-south-1.rds.amazonaws.com",
                        port=3306,
                        user="admin",
                        password="master-password",
                        database="through_the_wild")

    def __init__(self):
        """Initialization method."""

        pg.init()
        pg.font.init()
        pg.display.set_caption("Through the Wild")

        # Pygame surface to draw all contents on
        self.screen = pg.display.set_mode([self.SCREEN_W, self.SCREEN_H])
        
        # Pygame clock to run game at constant FPS
        self.clock = pg.time.Clock()

        # x-coordinates of the left and right of the river
        self.river_edges = [300, 600]

        # The middle x-coords of the three lanes in the river
        self.river_lanes = [350, 450, 550]

        self.boat_speed = 5

        # WHich screen is currently displaying (title or game)
        self.displaying = "title"

        # Loading in images required for the game
        self.bg_img = pg.image.load('Images/river.png')
        self.title_bg_img = pg.image.load('Images/river_blur.png')
        self.boat_img = pg.image.load('Images/boat.png')
        self.obstacle_imgs = [pg.image.load('Images/rock.png'), 
                         pg.image.load('Images/log.png')]

        # Class to represent the title screen (everything that's not the game)
        self.title_screen = TitleScreen(self.screen, self.title_bg_img, 
                                        self.database)

        # Using the database initialized in TitleScreen
        self.database = self.title_screen.database
        
        # Starting the objects in the game
        self.background, self.boat, self.obstacles, self.coins = self.reset()
        
        self.score = 0

        # Whether or not highest_score and coin_count have been retrieved from
        # the database
        self.got_data_from_db = False
        
    def get_font(self, size: int) -> pg.font:
        """Retrieve a font of the inputted size.
        
        Arguments:
            size
                font size
        
        Returns:
            font
                requested font with correct size
        """

        return pg.font.Font('Fonts/Pixel.ttf', size)

    def reset(self) -> list[Background, Boat, Obstacles, Coins]:
        """Reset the game objects.
        
        Returns:
            background
                represents the background images of the river and trees
            boat
                represents the boat images and the boat's mechanics
            obstacles
                represents all of the individual obstacles in the river and
                their interactions in the game
            coins
                represents all of the invidual coins in the river and their 
                animations 
        """

        background = Background(self.screen, self.bg_img)
        boat = Boat(self.screen, 
                    self.boat_img, 
                    self.INIT_BOAT_POS, 
                    self.boat_speed)
        obstacles = Obstacles(self.screen, self.obstacle_imgs)
        coins = Coins(self.screen, animation_dir="Animations/Coin/64")

        return background, boat, obstacles, coins
    
    def display_text(self, text: str, font_size: int, pos: tuple, 
                     mode="CENTER"):
        """Display text at a requested font_size at a requested position.
        
        Arguments:
            text
                string to be displayed on screen
            font_size
                font size to render text in
            pos
                where to place text; [pos_x, pos_y]
            mode : str
                which mode to display text in
                    CENTER: pos is in the center of the text render
                    CORNER: pos is in the top-left of the text render

        """
        # Rendering the text with the requested font size
        text = self.get_font(font_size).render(text, False, (0, 0, 0))

        # Displaying the text with pos in the center of the render
        if mode == 'CENTER':
            self.screen.blit(text, (pos[0] - text.get_size()[0]/2, 
                                    pos[1] - text.get_size()[1]/2))
        # Displaying the text with pos in the top-left corner of the render
        elif mode == 'CORNER':
            self.screen.blit(text, pos)

    def get_data(self) -> list[int, int, int]:
        """Retrieve the id, highest_score, and coin_count of the user form the
        database
        
        Returns:
            id
                user id
            highest_score
                the user's highest_score reached ever
            coin_count
                the user's total number of coins in their inventory
        """
        # Table of all of the user data
        user_data = self.database.get_table("USER_DATA")

        # Parsing the usernames in user_data
        usernames = list(user_data["username"])

        id = usernames.index(self.title_screen.get_username())
        highest_score = list(user_data["highest_score"])[id]
        coin_count = list(user_data["coin_count"])[id]

        return id, highest_score, coin_count
    
    def store_data(self):
        """Store highest_score and coin_count in database."""

        # Update the respective cells for the data
        self.database.update_cells(table_name="USER_DATA", 
                                    id=self.id, 
                                    column_names=["highest_score",
                                                    "coin_count"], 
                                    new_vals=[int(self.highest_score),
                                              self.coin_count])
    
    def update_score(self, boat_vel: list[float]):
        """Update the user's score based on the boat's velocity.
        
        Arguments:
            boat_vel
                contains the velocity vector  components; [vel_x, vel_y]
        """

        # Increment score by the y component of the boat's velocity
        self.score += boat_vel[1]
    
    def update_highest_score(self):
        """Update the highest_score if needed."""

        if self.score > self.highest_score:
            self.highest_score = self.score

    def display_score(self):
        """Display the player's score on the screen."""

        self.display_text(text=f"Score: {int(self.score)}", 
                          font_size=30,
                          pos=(20, 20),
                          mode="CORNER")
    
    def display_highest_score(self):
        """Display the player's highest_score on the screen."""
        self.display_text(text=f"Highest Score: {int(self.highest_score)}", 
                          font_size=30,
                          pos=(20, 70),
                          mode="CORNER")

    def display_coin_count(self):
        """Display the player's coin_count on the screen."""

        self.display_text(text=f"Coins: {self.coin_count}", 
                          font_size=30,
                          pos=(20, 120),
                          mode="CORNER")

    def sink_boat(self):
        """Sink the boat in the river."""

        # Continue to draw the game objects
        self.background.draw()
        self.boat.draw()
        self.obstacles.draw()
        self.coins.draw()

        # Continue to display the user's game data to the screen
        self.display_score()
        self.display_highest_score()
        self.display_coin_count()

        # Sink the boat by changing it's images alpha value
        self.boat.sink(2)

    def run(self):
        """Run the main while loop for the game."""

        running = True
        while running:
            # Which key is currently being pressed
            key_pressed = None

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:
                    # Assign a keyword based on the special keys pressed
                    if event.key == pg.K_BACKSPACE:
                        key_pressed = "DEL"
                    elif event.key == pg.K_TAB:
                        key_pressed = "TAB"
                    elif event.key == pg.K_RETURN:
                        key_pressed = "RETURN"
                    elif event.key == pg.K_SPACE:
                        key_pressed = "SPACE"
                    # If not a special key used in the other parts of the game,
                    # key_pressed is the unicode of key
                    else:
                        key_pressed = event.unicode
            
            # Determine which direction to turn boat in
            keys = pg.key.get_pressed()

            # Turn left if pressing A or left arrow
            counterclockwise = keys[pg.K_a] or keys[pg.K_LEFT]

            # Turn right if pressing D or right arrow
            clockwise = keys[pg.K_d] or keys[pg.K_RIGHT]

            if counterclockwise:
                turn_dir = "cc"
            elif clockwise:
                turn_dir = "c"
            else:
                turn_dir = ''

            # Check if any of the obstacles are colliding with the boat
            if self.obstacles.is_colliding_boat(self.boat.get_poly_coords()):
                # Sink the boat
                self.sink_boat()

                # Display title screen
                self.displaying = "title"

                # Once the boat is finished sinking
                if self.boat.has_sunk():
                    # Store highest_score and coin_count in database
                    self.store_data()
                    # Reset the title_screen variables
                    self.title_screen.reset()
                    # Reset game objects
                    self.background, self.boat, self.obstacles, self.coins = \
                        self.reset()
                    self.score = 0

            if self.displaying == 'title':
                self.title_screen.display()
                # Pass any key pressed to title_screen
                self.title_screen.input(key_pressed)

                # Display the game once the play button is pressed
                if self.title_screen.check_for_game() is True:
                    self.displaying = "game"
                
                # Retrieve id, highest_score, coin_count the first time the 
                # main menu is displayed whether after login or boat collision
                if self.title_screen.displaying_screen == "main":
                    if self.got_data_from_db is not True:
                        self.got_data_from_db = True
                        self.id, self.highest_score, self.coin_count = \
                            self.get_data()
            
            elif self.displaying == 'game':
                # Move the background images based on the boat's velocity
                self.background.move(self.boat.get_vel())
                # Loop background images with 2 identical images
                self.background.loop_imgs()
                # Draw background on screen
                self.background.draw()

                # Update the velocity, direction, position, and polygon coords
                # of the boat
                self.boat.update(turn_dir, self.river_edges)
                # Draw the boat on screen
                self.boat.draw()

                # Generate new obstacles
                self.obstacles.gen_new_obs(gen_chance=.8, 
                                           dist_btwn_obs=self.DIST_BTWN_OBS, 
                                           river_lanes=self.river_lanes)
                # Update the position of each obstacle and check if any are out
                # of the screen
                self.obstacles.update(self.boat.get_vel(), self.SCREEN_H)
                # Draw each obstacle on the screen
                self.obstacles.draw()

                # Generate new coins
                self.coins.gen_new_coin(self.DIST_BTWN_COINS, 
                                        self.river_lanes, 
                                        self.obstacles.get_obstacles())
                # Update the position of each coins and check if any are out of
                # the screen
                self.coins.update(self.boat.get_vel(), self.SCREEN_H)
                # Draw each coin on the screen
                self.coins.draw()
                # Check if the player collects any coins
                if self.coins.is_colliding_boat(self.boat.get_pos()):
                    self.coin_count += 1

                # Update the score count
                self.update_score(self.boat.get_vel())
                # Update the highest_score count if needed
                self.update_highest_score()

                # Display score, highest_score, coin_count on the screen
                self.display_score()
                self.display_highest_score()
                self.display_coin_count()

            # Run game on constant fps
            self.clock.tick(self.FPS)

            # Change screen contents
            pg.display.flip()

        pg.quit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()