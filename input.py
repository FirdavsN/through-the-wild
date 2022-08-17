"""
An Input class to represent an input box in the title screen.
"""

# Import modules
import pygame as pg

class Input:
    """Input class."""

    def __init__(self,
                 screen: pg.surface,
                 pos: tuple[int],
                 dims: tuple[int], 
                 font: pg.font,
                 bg_colors=((255, 255, 255), (128, 128, 128)),
                 text_color=(0, 0, 0),
                 border_radius=5):
        """Initialization method.
        
        Arugments:
            screen
                pygame screen to display contents
            pos
                button position with the position in the center of the button;
                [pos_x, pos_y]
            dims
                button dimensions; [width, height]
            font
                font to render the text for the button
            bg_colors : tuple[int]
                background colors in RGB; one for two states of selection
            text_color : tuple[int]
                text color in RGB
            border_radius : int
                button border_radius
        """
        
        self.screen = screen
        self.pos = pos
        self.dims = dims
        self.font = font
        self.bg_colors = bg_colors
        self.text_color = text_color
        self.border_radius = border_radius

        # Whether or not the input box is selected to type in
        self.selected = False

    def draw(self, text: str):
        """Draw the input box and the text in it.
        
        Arguments:
            text
                input box text
        """

        self.text = text

        self.draw_bg()
        self.draw_text()

    def draw_bg(self):
        """Draw the input box itself."""

        # Swap input box background colors based on selection
        if self.selected:
            bg_color = self.bg_colors[0]
        else:
            bg_color = self.bg_colors[1]
        
        # pos_x, pos_y, width, height
        rect = [self.pos[0] - self.dims[0]/2, self.pos[1] - self.dims[1]/2,
                self.dims[0], self.dims[1]]
        
        pg.draw.rect(self.screen, bg_color, 
                     rect, border_radius=self.border_radius)
    
    def draw_text(self):
        """Draw the input box text."""

        # Render the text as a pygame surface
        label = self.font.render(self.text, False, self.text_color)
        label_size = label.get_size()

        # Offset the position of the text from the left side of the input box
        offset = 10
        # Convert the position from the center to the top left
        label_top_left_pos = (self.pos[0] - self.dims[0]/2 + offset, 
                              self.pos[1] - label_size[1]/2)
        
        self.screen.blit(label, label_top_left_pos)

    def check_for_select(self, inputs: list):
        """Check if the input box has been selected"""

        # Check if any input box has been selected and whether or not none have
        # been selected
        any_input_selected = False
        all_inputs_not_selected = True
        for input in inputs:
            if input.is_selected():
                any_input_selected = True
                all_inputs_not_selected = False
        
        # Only select this input box is any other is selected or if none, 
        # including this input, are selected
        if any_input_selected or (all_inputs_not_selected and \
                                                          not self.selected):
            # If mouse is left clicked
            left_click = pg.mouse.get_pressed()[0]
            # The mouse position
            mouse_pos = pg.mouse.get_pos()

             # If the mouse is in the button borders
            mouse_in_border = self.pos[0] - self.dims[0]/2 < \
                              mouse_pos[0] < \
                              self.pos[0] + self.dims[0]/2 and \
                              self.pos[1] - self.dims[1]/2 < \
                              mouse_pos[1] < \
                              self.pos[1] + self.dims[1]/2


            if left_click and mouse_in_border: self.select()

    def select(self):
        """Select the input box."""

        self.selected = True

    def deselect(self):
        """Unselect the input box."""

        self.selected = False

    def is_selected(self) -> bool:
        """Return whether or not the input box is selected."""

        return self.selected