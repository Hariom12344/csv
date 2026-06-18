import cv2
import numpy as np


class TextTool:
    """Text drawing tool for adding text to canvas"""
    
    def __init__(self, frame_width=640, frame_height=480):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.enabled = False
        self.current_text = ""
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.font_size = 1.0
        self.font_color = (255, 255, 255)  # White
        self.text_thickness = 2
        self.position = None
        self.min_font_size = 0.3
        self.max_font_size = 3.0
        
        # Available fonts
        self.fonts = {
            'simplex': cv2.FONT_HERSHEY_SIMPLEX,
            'plain': cv2.FONT_HERSHEY_PLAIN,
            'duplex': cv2.FONT_HERSHEY_DUPLEX,
            'complex': cv2.FONT_HERSHEY_COMPLEX,
            'triplex': cv2.FONT_HERSHEY_TRIPLEX,
        }
        self.current_font = 'simplex'
    
    def toggle(self):
        """Toggle text tool"""
        self.enabled = not self.enabled
        if not self.enabled:
            self.current_text = ""
        return self.enabled
    
    def add_character(self, char):
        """Add a character to current text"""
        if len(self.current_text) < 100:  # Limit text length
            self.current_text += char
        return self.current_text
    
    def backspace(self):
        """Remove last character"""
        if self.current_text:
            self.current_text = self.current_text[:-1]
        return self.current_text
    
    def clear_text(self):
        """Clear current text"""
        self.current_text = ""
    
    def set_font(self, font_name):
        """Set text font"""
        if font_name in self.fonts:
            self.current_font = font_name
            self.font = self.fonts[font_name]
            return True
        return False
    
    def set_font_size(self, size):
        """Set text font size"""
        self.font_size = max(self.min_font_size, min(size, self.max_font_size))
        return self.font_size
    
    def increase_font_size(self):
        """Increase font size"""
        return self.set_font_size(self.font_size + 0.2)
    
    def decrease_font_size(self):
        """Decrease font size"""
        return self.set_font_size(self.font_size - 0.2)
    
    def set_position(self, point):
        """Set text position on canvas"""
        if point and 0 <= point[0] < self.frame_width and 0 <= point[1] < self.frame_height:
            self.position = point
            return True
        return False
    
    def set_text_color(self, color_bgr):
        """Set text color"""
        self.font_color = color_bgr
    
    def draw_text(self, canvas, text=None, position=None):
        """Draw text on canvas"""
        if text is None:
            text = self.current_text
        if position is None:
            position = self.position
        
        if not text or position is None:
            return canvas
        
        cv2.putText(canvas, text, position, self.font, self.font_size, 
                   self.font_color, self.text_thickness)
        return canvas
    
    def draw_text_preview(self, frame, text=None, position=None):
        """Draw text preview on frame while editing"""
        if text is None:
            text = self.current_text
        if position is None:
            position = self.position
        
        if not text or position is None:
            return frame
        
        # Draw text
        cv2.putText(frame, text, position, self.font, self.font_size,
                   self.font_color, self.text_thickness)
        
        # Draw cursor
        text_size = cv2.getTextSize(text, self.font, self.font_size, self.text_thickness)[0]
        cursor_x = position[0] + text_size[0] + 3
        cursor_y = position[1] - text_size[1] + 3
        cv2.line(frame, (cursor_x, position[1] - text_size[1]), 
                (cursor_x, position[1]), (0, 255, 255), 2)
        
        return frame
    
    def get_text_stats(self):
        """Get text tool statistics"""
        text_size = cv2.getTextSize(self.current_text, self.font, self.font_size, self.text_thickness)[0]
        
        return {
            'text': self.current_text,
            'font': self.current_font,
            'font_size': round(self.font_size, 2),
            'position': self.position,
            'text_width': text_size[0],
            'text_height': text_size[1],
            'color': self.font_color,
        }
