import cv2
import numpy as np


class ColorPickerUI:
    """Interactive color picker with RGB sliders"""
    
    def __init__(self, frame_width=640, frame_height=480):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.is_open = False
        self.window_width = 300
        self.window_height = 250
        self.window_x = (frame_width - self.window_width) // 2
        self.window_y = (frame_height - self.window_height) // 2
        
        # RGB sliders (0-255)
        self.r = 255
        self.g = 0
        self.b = 0
        
        self.slider_height = 25
        self.slider_margin = 10
        self.slider_width = 200
        self.slider_y_base = self.window_y + 80
    
    def toggle(self):
        """Toggle color picker visibility"""
        self.is_open = not self.is_open
        return self.is_open
    
    def draw(self, frame):
        """Draw color picker on frame"""
        if not self.is_open:
            return frame
        
        # Draw window background
        cv2.rectangle(frame, (self.window_x, self.window_y),
                     (self.window_x + self.window_width, self.window_y + self.window_height),
                     (30, 30, 30), cv2.FILLED)
        cv2.rectangle(frame, (self.window_x, self.window_y),
                     (self.window_x + self.window_width, self.window_y + self.window_height),
                     (0, 255, 255), 2)
        
        # Draw title
        cv2.putText(frame, "Color Picker", (self.window_x + 10, self.window_y + 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Draw color preview
        preview_x = self.window_x + 10
        preview_y = self.window_y + 40
        preview_size = 50
        cv2.rectangle(frame, (preview_x, preview_y),
                     (preview_x + preview_size, preview_y + preview_size),
                     (self.b, self.g, self.r), cv2.FILLED)
        cv2.rectangle(frame, (preview_x, preview_y),
                     (preview_x + preview_size, preview_y + preview_size),
                     (255, 255, 255), 2)
        
        # Draw RGB sliders
        slider_x = self.window_x + self.slider_margin
        
        # Red slider
        self._draw_slider(frame, "R", self.r, slider_x,
                         self.slider_y_base, (0, 0, 255))
        
        # Green slider
        self._draw_slider(frame, "G", self.g, slider_x,
                         self.slider_y_base + 40, (0, 255, 0))
        
        # Blue slider
        self._draw_slider(frame, "B", self.b, slider_x,
                         self.slider_y_base + 80, (255, 0, 0))
        
        # Draw close button
        close_x = self.window_x + self.window_width - 30
        close_y = self.window_y + 5
        cv2.rectangle(frame, (close_x, close_y), (close_x + 25, close_y + 25),
                     (100, 50, 50), cv2.FILLED)
        cv2.putText(frame, "X", (close_x + 7, close_y + 18),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return frame
    
    def _draw_slider(self, frame, label, value, x, y, color):
        """Draw a single RGB slider"""
        # Label
        cv2.putText(frame, label, (x - 15, y + 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
        
        # Slider background
        cv2.rectangle(frame, (x, y), (x + self.slider_width, y + self.slider_height),
                     (60, 60, 60), cv2.FILLED)
        cv2.rectangle(frame, (x, y), (x + self.slider_width, y + self.slider_height),
                     (100, 100, 100), 1)
        
        # Slider fill
        fill_width = int((value / 255) * self.slider_width)
        cv2.rectangle(frame, (x, y), (x + fill_width, y + self.slider_height),
                     color, cv2.FILLED)
        
        # Value text
        value_text = f"{value}"
        cv2.putText(frame, value_text, (x + self.slider_width + 10, y + 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
    
    def get_current_color(self):
        """Get current color as BGR tuple"""
        return (self.b, self.g, self.r)
    
    def update_slider(self, slider_index, x_position):
        """Update slider value based on click position"""
        # slider_index: 0=R, 1=G, 2=B
        relative_x = x_position - (self.window_x + self.slider_margin)
        if relative_x < 0:
            relative_x = 0
        elif relative_x > self.slider_width:
            relative_x = self.slider_width
        
        value = int((relative_x / self.slider_width) * 255)
        
        if slider_index == 0:
            self.r = value
        elif slider_index == 1:
            self.g = value
        elif slider_index == 2:
            self.b = value
    
    def is_close_button_clicked(self, x, y):
        """Check if close button was clicked"""
        close_x = self.window_x + self.window_width - 30
        close_y = self.window_y + 5
        return (close_x <= x <= close_x + 25 and close_y <= y <= close_y + 25)
    
    def get_slider_at_position(self, x, y):
        """Get which slider was clicked (0=R, 1=G, 2=B, -1=none)"""
        slider_x = self.window_x + self.slider_margin
        
        for slider_idx, slider_y in enumerate([self.slider_y_base,
                                               self.slider_y_base + 40,
                                               self.slider_y_base + 80]):
            if (slider_x <= x <= slider_x + self.slider_width and
                slider_y <= y <= slider_y + self.slider_height):
                return slider_idx
        
        return -1
