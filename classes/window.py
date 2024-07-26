import pygame as pyg
import sys
import os

class WindowManager:
    """Houses the components of the window and the video buffer other classes render to
    
    Attributes:
        display_width, display_height: The size of the video buffer (default to 1920x1080)
        width, height: The size of the pygame window (default to user's active display size)
        display: The video buffer that gets scaled according to how large the pygame window is
        window: The actual window that the user sees
    """
    def __init__(self, caption: str, window_size: tuple=(0, 0)):
        """Initializes the pygame window
        
        Parameters:
            caption: The display caption of this application or game
            window_size: An optional size that the window can be set to
        """
        pyg.init()
        self.info_obj = pyg.display.Info()

        self.display_width, self.display_height = (1920, 1080)
        self.display = pyg.Surface((self.display_width, self.display_height))
        
        if window_size == (0, 0):
            self.width, self.height = self.info_obj.current_w, self.info_obj.current_h
        else:
            self.width, self.height = window_size
        
        self.window = pyg.display.set_mode((self.width, self.height), pyg.FULLSCREEN)        
        self.draw_center_line = False

        self.dimmed_display = pyg.Surface(self.display.get_size())
        self.dimmed_display.fill((2, 2, 2))
        self.dimmed_display.set_alpha(100)
        
        pyg.display.set_caption(caption)
        
        if os.name == "posix":
            os.system("clear")
        else:
            os.system("cls")

    def get_scale(self):
        """Returns the x/y scale that the internal display is being scaled to to fit the window size"""
        return (self.display_width / self.width, self.display_height / self.height)

    def get_size(self):
        """Returns the size of the pygame window"""
        return self.window.get_size()

    def toggle_fullscreen(self):
        if self.width == 1067:
            self.width, self.height = self.info_obj.current_w, self.info_obj.current_h
            self.window = pyg.display.set_mode((self.width, self.height), pyg.FULLSCREEN)    
        else:
            self.width, self.height = 1067, 600
            self.window = pyg.display.set_mode((self.width, self.height))        


    def render(self):
        """Renders the video buffer to the window and refreshes the screen"""
        if self.draw_center_line:
            pyg.draw.line(self.display, (50, 50, 50), (self.display.get_width() / 2, 0), (self.display.get_width() / 2, self.display.get_height()))

        self.window.blit(pyg.transform.scale(self.display, (self.width, self.height)), (0, 0))
        
        pyg.display.update()

    def quit(self):
        pyg.quit()
        sys.exit()