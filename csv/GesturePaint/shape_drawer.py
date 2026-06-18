import cv2
import numpy as np


class ShapeDrawer:
    """Shape drawing modes - rectangles, circles, lines, triangles"""
    
    # Shape modes
    MODES = {
        'paint': 'PAINT',
        'rect': 'RECTANGLE',
        'circle': 'CIRCLE',
        'line': 'LINE',
        'triangle': 'TRIANGLE'
    }
    
    def __init__(self):
        self.current_mode = 'paint'
        self.start_point = None
        self.drawing_shape = False
    
    def set_mode(self, mode):
        """Set drawing mode"""
        if mode in self.MODES:
            self.current_mode = mode
            return True
        return False
    
    def get_mode(self):
        """Get current mode"""
        return self.MODES[self.current_mode]
    
    def start_shape(self, point):
        """Start drawing a shape"""
        self.start_point = point
        self.drawing_shape = True
    
    def draw_rectangle(self, canvas, pt1, pt2, color, thickness=2, filled=False):
        """Draw rectangle on canvas"""
        if filled:
            cv2.rectangle(canvas, pt1, pt2, color, -1)
        else:
            cv2.rectangle(canvas, pt1, pt2, color, thickness)
    
    def draw_circle(self, canvas, center, radius, color, thickness=2, filled=False):
        """Draw circle on canvas"""
        if filled:
            cv2.circle(canvas, center, radius, color, -1)
        else:
            cv2.circle(canvas, center, radius, color, thickness)
    
    def draw_line(self, canvas, pt1, pt2, color, thickness=2):
        """Draw line on canvas"""
        cv2.line(canvas, pt1, pt2, color, thickness)
    
    def draw_triangle(self, canvas, pt1, pt2, pt3, color, thickness=2, filled=False):
        """Draw triangle on canvas"""
        pts = np.array([pt1, pt2, pt3], np.int32)
        pts = pts.reshape((-1, 1, 2))
        if filled:
            cv2.fillPoly(canvas, [pts], color)
        else:
            cv2.polylines(canvas, [pts], True, color, thickness)
    
    def preview_shape(self, frame, pt1, pt2, color, thickness=2):
        """Draw shape preview on frame while dragging"""
        if self.current_mode == 'rect':
            cv2.rectangle(frame, pt1, pt2, color, thickness)
        elif self.current_mode == 'circle':
            radius = int(np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2))
            cv2.circle(frame, pt1, radius, color, thickness)
        elif self.current_mode == 'line':
            cv2.line(frame, pt1, pt2, color, thickness)
        elif self.current_mode == 'triangle':
            # Triangle preview: pt1 to pt2 to midpoint
            mid_x = (pt1[0] + pt2[0]) // 2
            mid_y = pt1[1] - (pt2[1] - pt1[1])
            self.draw_triangle(frame, pt1, pt2, (mid_x, mid_y), color, thickness)
        
        return frame
    
    def end_shape(self):
        """End shape drawing"""
        self.start_point = None
        self.drawing_shape = False
