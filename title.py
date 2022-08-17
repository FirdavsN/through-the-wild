"""
Class to represent the title screen parts: login, signup, main menu, 
leaderboard, rules.
"""

# Import modules
from background import Background
from button import Button
from database import Database
from input import Input
import numpy as np
import pygame as pg

class TitleScreen:
    """Title screen class"""
        
    def __init__(self, screen: pg.surface, bg_img: pg.image, 
                 database: Database):
        """Initialization method.
        
        Arguments:
            screen
                pygame screen to display contents
            bg_img
                background image for title_screen
            database
                Database object that can access all user data
        """

        self.screen = screen
        self.background = Background(screen, bg_img)
        self.database = database

        # Game title
        self.title = "Through the Wild"
        
        # Strings to contain the username, password, and confirm password inputs
        self.un = ""
        self.pw = ""
        self.pw_confirm = ""

        # Strings to contain error messages to be displayed with an incorrect
        # login or signup
        self.invalid_login = ""
        self.invalid_signup = ""

        # Whether or not game has started
        self.enter_game = False

        # Whether or not highest_score, coin_count, and leaderboard data have 
        # been retrieved from database
        self.got_data_from_db = False
        
        # Which part of title_screen is displaying
        self.displaying_screen = "login"

        # Initialize the contents of the login screen
        self.init_login_screen()

    def reset(self):
        """Reset title screen."""

        self.enter_game = False
        self.displaying_screen = "main"
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

    def display(self):
        """Display the title screen on the screen."""

        if self.displaying_screen == "login":
            self.display_login_screen()
        elif self.displaying_screen == "signup":
            self.display_signup_screen()
        elif self.displaying_screen == "main":
            # Retrieve highest_score, coin_count, and leaderboard data the 
            # first time the main menu is displayed whether after login or boat 
            # collision
            if self.got_data_from_db is not True:
                self.got_data_from_db = True
                self.highest_score, self.coin_count, self.lb = self.get_data()
            
            self.display_main_screen()
        elif self.displaying_screen == "game":
            # Game has started
            self.enter_game = True
        elif self.displaying_screen == "shop":
            self.display_shop_screen()  
        elif self.displaying_screen == "leaderboard":
            self.display_leaderboard_screen()
        elif self.displaying_screen == "rules":
            self.display_rules_screen()
    
    def check_for_game(self) -> bool:
        """Return whether or not game has started.
        
        Returns:
            enter_game
        """

        return self.enter_game

    def input(self, key_pressed: str):
        """Input key_pressed into input fields or as keys for actions."""

        if key_pressed is not None:
            # Change input field with TAB
            if key_pressed == "TAB":
                if self.un_input.is_selected():
                    self.un_input.deselect()
                    self.pw_input.select()
                elif self.pw_input.is_selected():
                    if self.displaying_screen == "login":
                        self.pw_input.deselect()
                        self.un_input.select()
                    if self.displaying_screen == "signup":
                        self.pw_input.deselect()
                        self.pw_confirm_input.select()
                elif self.displaying_screen == "signup":
                    if self.pw_confirm_input.is_selected():
                        self.pw_confirm_input.deselect()
                        self.un_input.select()
            # Press play button with RETURN or SPACE
            elif self.displaying_screen == "main":
                if key_pressed in ["RETURN", "SPACE"]:
                    self.play_button.press()
            # Press submit button with return
            elif key_pressed == "RETURN":
                self.submit_button.press()
            # Accept all other keys as inputs for input boxes
            else:
                if self.un_input.is_selected():
                    if key_pressed == "DEL":
                        self.un = self.un[:-1]
                    else:
                        self.un += key_pressed
                elif self.pw_input.is_selected():
                    if key_pressed == "DEL":
                        self.pw = self.pw[:-1]
                    else:
                        self.pw += key_pressed
                elif self.displaying_screen == "signup":
                    if self.pw_confirm_input.is_selected():
                        if key_pressed == "DEL":
                            self.pw_confirm = self.pw_confirm[:-1]
                        else:
                            self.pw_confirm += key_pressed

    def init_login_screen(self):
        """Initialize the contents of the login screen."""

        self.un_input = Input(self.screen,
                              pos=(500, 400),
                              dims=(200, 40),
                              font=self.get_font(20))
        
        self.pw_input = Input(self.screen,
                              pos=(500, 450),
                              dims=(200, 40),
                              font=self.get_font(20))

        self.submit_button = Button(self.screen, 
                                    pos=(450, 520), 
                                    dims=(150, 50), 
                                    font=self.get_font(20), 
                                    text="Submit", 
                                    bg_color=(31, 92, 172), 
                                    text_color=(0, 0, 0))

        self.create_new_button = Button(self.screen, 
                                        pos=(450, 580), 
                                        dims=(250, 50),
                                        font=self.get_font(20), 
                                        text="Create New Account", 
                                        bg_color=(31, 92, 172), 
                                        text_color=(0, 0, 0))

        self.invalid_login = ""
    
    def init_signup_screen(self):
        """Initialize the contents of the signup screen."""

        self.un_input = Input(self.screen,
                              pos=(500, 400),
                              dims=(200, 40),
                              font=self.get_font(20))
        
        self.pw_input = Input(self.screen,
                              pos=(500, 450),
                              dims=(200, 40),
                              font=self.get_font(20))
        
        self.pw_confirm_input = Input(self.screen,
                                      pos=(500, 500),
                                      dims=(200, 40),
                                      font=self.get_font(20))

        self.submit_button = Button(self.screen, 
                                    pos=(450, 570), 
                                    dims=(150, 50), 
                                    font=self.get_font(20), 
                                    text="Submit", 
                                    bg_color=(31, 92, 172), 
                                    text_color=(0, 0, 0))

        self.back_button = Button(self.screen, 
                                  pos=(450, 630), 
                                  dims=(100, 50),
                                  font=self.get_font(20), 
                                  text="Back", 
                                  bg_color=(31, 92, 172), 
                                  text_color=(0, 0, 0))
        
        self.invalid_signup = ""

    def init_main_screen(self):
        """Initialize the contents of the main menu screen."""

        self.play_button = Button(self.screen,
                                  pos=(450, 450),
                                  dims=(150, 50),
                                  font=self.get_font(30),
                                  text="Play",
                                  bg_color=(31, 92, 172), 
                                  text_color=(0, 0, 0))
        
        self.leaderboard_button = Button(self.screen,
                                         pos=(450,510),
                                         dims=(250, 50),
                                         font=self.get_font(30),
                                         text="Leaderboard",
                                         bg_color=(31, 92, 172), 
                                         text_color=(0, 0, 0))

        self.rules_button = Button(self.screen,
                                   pos=(450, 570),
                                   dims=(150, 50),
                                   font=self.get_font(30),
                                   text="Rules",
                                   bg_color=(31, 92, 172), 
                                   text_color=(0, 0, 0))
    
    # NOTE: CURRENTLY NOT USED
    def init_shop_screen(self):
        """Initialize the contents of the shop screen."""

        self.back_button = Button(self.screen,
                                  pos=(450, 650),
                                  dims=(150, 50),
                                  font=self.get_font(30),
                                  text="Back",
                                  bg_color=(31, 92, 172), 
                                  text_color=(0, 0, 0))
    
    def init_leaderboard_screen(self):
        """Initialize the contents of the leaderboard screen."""

        self.back_button = Button(self.screen,
                                  pos=(450, 650),
                                  dims=(150, 50),
                                  font=self.get_font(30),
                                  text="Back",
                                  bg_color=(31, 92, 172), 
                                  text_color=(0, 0, 0))
    
    def init_rules_screen(self):
        """Initialize the contents of the rules screen."""

        self.back_button = Button(self.screen,
                                  pos=(450, 650),
                                  dims=(150, 50),
                                  font=self.get_font(30),
                                  text="Back",
                                  bg_color=(31, 92, 172), 
                                  text_color=(0, 0, 0))

    def display_login_screen(self):
        """Display the contents of the the login screen."""

        if self.submit_button.is_pressed():
            # Attempt to login through user data in database
            self.login()
        elif self.create_new_button.is_pressed():
            # Initialize signup screen and switch screens
            self.init_signup_screen()
            self.displaying_screen = "signup"
        
        self.background.draw()

        # Display title of game
        self.display_text(self.title, 60, (450, 100))

        # Display title of screen
        self.display_text("Login", 50, (450, 210))

        # Display invalid_login text if any
        self.display_text(self.invalid_login, 30, (450, 300))

        # Display Username and Password labels
        self.display_text("Username: ", 
                          20, 
                          (self.un_input.pos[0] - 160,
                           self.un_input.pos[1]))

        self.display_text("Password: ", 
                          20, 
                          (self.pw_input.pos[0] - 160,
                           self.pw_input.pos[1]))

        # Check if username and password input boxes have bee selected
        self.un_input.check_for_select([self.pw_input])
        self.pw_input.check_for_select([self.un_input])

        # Draw username and password input boxes with their respective strings
        self.un_input.draw(self.un)
        self.pw_input.draw('*' * len(self.pw))

        # Draw the buttons for the screen
        self.submit_button.draw()
        self.create_new_button.draw()

        # Continuely unpress the submit button to ensure the press from the 
        # display method is not active
        self.submit_button.unpress()
    
    def display_signup_screen(self):
        """Display the contents of the the signup screen.
        
        NOTE: Logic very similar to display_login_screen.
        """

        if self.submit_button.is_pressed():
            self.signup()
        elif self.back_button.is_pressed():
            self.init_login_screen()
            self.displaying_screen = "login"

        self.background.draw()

        self.display_text(self.title, 60, (450, 100))

        self.display_text("Create New Account", 50, (450, 210))

        self.display_text(self.invalid_signup, 30, (450, 300))

        self.display_text("Username: ", 
                          20, 
                          (self.un_input.pos[0] - 160,
                           self.un_input.pos[1]))

        self.display_text("Password: ", 
                          20, 
                          (self.pw_input.pos[0] - 160,
                           self.pw_input.pos[1]))
        self.display_text("Confirm Password: ", 
                          20, 
                          (self.pw_confirm_input.pos[0] - 204,
                           self.pw_confirm_input.pos[1]))

        self.un_input.check_for_select([self.pw_input, self.pw_confirm_input])
        self.pw_input.check_for_select([self.un_input, self.pw_confirm_input])
        self.pw_confirm_input.check_for_select([self.un_input, self.pw_input])

        self.un_input.draw(self.un)
        self.pw_input.draw('*' * len(self.pw))
        self.pw_confirm_input.draw('*' * len(self.pw_confirm))

        self.submit_button.draw()
        self.back_button.draw()

        self.submit_button.unpress()

    def display_main_screen(self):
        """Display the contents of the the main menu screen."""

        # Check for any button presses -> navigate to corresponding screen
        if self.play_button.is_pressed():
            self.displaying_screen = "game"
        elif self.leaderboard_button.is_pressed():
            self.displaying_screen = "leaderboard"
            self.init_leaderboard_screen()
        elif self.rules_button.is_pressed():
            self.displaying_screen = "rules"
            self.init_rules_screen()
            
        self.background.draw()

        self.display_text(self.title, 60, (450, 100))

        self.display_text("Main Menu", 50, (450, 200))

        self.display_text(text=f"Username: {self.un}", 
                          font_size=30,
                          pos=(450, 280))

        self.display_text(text=f"Highest Score: {int(self.highest_score)}", 
                          font_size=30,
                          pos=(450, 320))

        self.display_text(text=f"Coins: {self.coin_count}", 
                          font_size=30,
                          pos=(450, 360))

        self.play_button.draw()
        self.leaderboard_button.draw()
        self.rules_button.draw()

        self.play_button.unpress()

    # NOTE: CURRENTLY NOT USED
    def display_shop_screen(self):
        """Display the contents of the the shop screen."""

        if self.back_button.is_pressed():
            self.displaying_screen = "main"
            self.init_main_screen()
            
        self.background.draw()

        self.display_text(self.title, 60, (450, 100))

        self.display_text("Shop", 50, (450, 210))

        self.back_button.draw()

    def display_leaderboard_screen(self):
        """Display the contents of the the leaderboard screen."""

        if self.back_button.is_pressed():
            self.displaying_screen = "main"
            self.init_main_screen()
            
        self.background.draw()

        self.display_text(self.title, 60, (450, 100))

        self.display_text("Highest Scores", 50, (450, 210))

        # Retrieve leaderboard information fromm lb
        self.lb_usernames, self.lb_scores, self.lb_scores_order = \
            self.lb[0], self.lb[1], self.lb[2]
        
        # Only display the top 8 highest scores
        n = len(self.lb_usernames)
        if len(self.lb_usernames) > 8:
            n = 8
        
        # Display as centered 
        for i in range(n):
            index = self.lb_scores_order[-1-i]
            self.display_text(text=f"{self.lb_usernames[index]}: \
{int(self.lb_scores[index])}",
                              font_size=30,
                              pos=(450, 300+i*40))

        self.back_button.draw()
    
    def display_rules_screen(self):
        """Display the contents of the the rules screen."""

        if self.back_button.is_pressed():
            self.displaying_screen = "main"
            self.init_main_screen()
            
        self.background.draw()

        self.display_text(self.title, 60, (450, 100))

        self.display_text("Rules", 50, (450, 210))

        rules = """Navigate the boat with the baby through\nthe river while \
dodging obstacles and\ncollecting coins."""

        # Centered position of the rules text
        rules_pos = (450, 350)

        # Separte the long string to make sure all of it is visible on the 
        # screen
        lines = rules.splitlines()
        for i, l in enumerate(lines):
            t = self.get_font(30).render(l, 0, (0, 0, 0))
            self.screen.blit(t, (rules_pos[0] - t.get_size()[0]/2, 
                                 rules_pos[1] - t.get_size()[1]/2 + 50*i))

        self.back_button.draw()

    def login(self):
        """Attempt to login user."""

        # Retrieve a table of all user data
        user_data = self.database.get_table("USER_DATA")

        # Parse the usernames and passwords from the user data
        usernames = list(user_data["username"])
        passwords = list(user_data["password"])

        # Check that the user's username is in the database and that the user's
        # password matches that in the database
        if self.un in usernames and \
           self.pw == passwords[usernames.index(self.un)]:
            
            self.invalid_login = ""
            # Switch to main menu screen
            self.init_main_screen()
            self.displaying_screen = "main"
        else:
            # Notify user of an invalid username/password input
            self.invalid_login = "Invalid username or password"
        
    def signup(self):
        """Attempt to signup a new user."""

        # Retrieve a table of all user data
        user_data = self.database.get_table("USER_DATA")
        
        # Parse all user ids and usernames
        ids = list(user_data["id"])
        usernames = list(user_data["username"])

        # Check if a user with the saem username exists
        if self.un in usernames:
            self.invalid_signup = "Username taken"
        # CHeck if a new user but if the passwords don't match
        elif self.un not in usernames and (self.pw != self.pw_confirm):
            self.invalid_signup = "Passwords do not match up"
        # Check if username or password fields are empty
        elif len(self.un.split()) == 0 or len(self.pw.split()) == 0:
            self.invalid_signup = "Username and/or password cannot be empty"
        # If no errors, then signup
        else:
            self.invalid_signup = ""

            # Attempt to sign up with the expectation of already having users
            try:
                self.database.add_data("USER_DATA", 
                                       [ids[-1]+1, self.un, self.pw, 0, 0])
            # If signing up the first ever user
            except IndexError:
                self.database.add_data("USER_DATA", 
                                       [0, self.un, self.pw, 0, 0])
            # Switch to main menu screen
            self.init_main_screen()
            self.displaying_screen = "main"

    def get_username(self) -> str:
        """Retrieve the player's username.
        
        Returns:
            un
                user's username
        """

        return self.un

    def get_data(self) -> list[int, int, list[list[str], list[int], list[int]]]:
        """Retrieve highest_score, coin_count and leaderboard data from the
        database.
        
        Returns:
            highest_score
                the player's highest ever score
            coin_count
                the player's total number of collected coins
            lb
                the leaderboard information 
                 : usernames, highest_scores, score_order
                usernames
                    all of the usernames in the database
                highest_scores
                    the highest_score linked to each username
                scores_order
                    an array containing the argsort of highest_scores

        NOTE: all of this done in one method to reduce the number of times the 
        database is accessed -> improves latency 
        """
        
        # Retrieve a table of all user data
        user_data = self.database.get_table("USER_DATA")

        # Parse usernames, highest_scores, and coin_counts from the database
        usernames = list(user_data["username"])
        highest_scores = list(user_data["highest_score"])
        coin_counts = list(user_data["coin_count"])

        # Index the id of the current used
        id = usernames.index(self.un)
        
        # Index the user's highest_score and coin_count with their id
        highest_score = highest_scores[id]
        coin_count = coin_counts[id]

        # Argsort highest_scores
        scores_order = np.argsort(highest_scores)

        lb = [usernames, highest_scores, scores_order]

        return highest_score, coin_count, lb