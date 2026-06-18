import cv2
import numpy as np


class DrawingGrid:
    """Grid overlay for precise drawing"""
    
    def __init__(self, frame_width=640, frame_height=480, grid_size=20):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.grid_size = grid_size
        self.enabled = False
        self.color = (50, 50, 50)  # Dark gray
        self.line_thickness = 1
        self.min_grid = 10
        self.max_grid = 100
    
    def toggle(self):
        """Toggle grid visibility"""
        self.enabled = not self.enabled
        return self.enabled
    
    def set_grid_size(self, size):
        """Set grid cell size"""
        self.grid_size = max(self.min_grid, min(size, self.max_grid))
        return self.grid_size
    
    def increase_grid_size(self):
        """Increase grid size"""
        return self.set_grid_size(self.grid_size + 5)
    
    def decrease_grid_size(self):
        """Decrease grid size"""
        return self.set_grid_size(self.grid_size - 5)
    
    def draw_grid(self, frame):
        """Draw grid on frame"""
        if not self.enabled:
            return frame
        
        # Draw vertical lines
        for x in range(0, self.frame_width, self.grid_size):
            cv2.line(frame, (x, 0), (x, self.frame_height), self.color, self.line_thickness)
        
        # Draw horizontal lines
        for y in range(0, self.frame_height, self.grid_size):
            cv2.line(frame, (0, y), (self.frame_width, y), self.color, self.line_thickness)
        
        return frame
    
    def snap_to_grid(self, point):
        """Snap a point to the nearest grid intersection"""
        if not self.enabled:
            return point
        
        x = (point[0] // self.grid_size) * self.grid_size
        y = (point[1] // self.grid_size) * self.grid_size
        return (x, y)
    
    def set_grid_color(self, color_bgr):
        """Change grid color"""
        self.color = color_bgr
    
    def get_grid_stats(self):
        """Get grid statistics"""
        return {
            'enabled': self.enabled,
            'grid_size': self.grid_size,
            'color': self.color
        }
