import cv2
import numpy as np


class CanvasEngine:
    # Color palette (BGR format)
    COLORS = {
        'red': (0, 0, 255),
        'green': (0, 255, 0),
        'blue': (255, 0, 0),
        'yellow': (0, 255, 255),
        'magenta': (255, 0, 255),
        'cyan': (255, 255, 0),
        'white': (255, 255, 255),
    }
    
    COLOR_NAMES = list(COLORS.keys())
    
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), np.uint8)
        self.color_index = 0  # Start with red
        self.brush_color = self.COLORS[self.COLOR_NAMES[self.color_index]]
        self.brush_thickness = 5
        self.brush_opacity = 100  # Default opacity 100%
        self.eraser_mode = False
        self.stroke_history = []  # For undo functionality
        self.canvas_history = []  # Full canvas snapshots for redo
        self.redo_history = []  # For redo functionality
        self.min_brush = 1
        self.max_brush = 25
        self.background_color = (0, 0, 0)  # Black background
        self.use_fill = False  # Default to outline shapes
    
    def draw_line(self, start_point, end_point, use_glow=True):
        """Draw a line on canvas with optional glow effect and opacity"""
        if start_point and end_point:
            if self.eraser_mode:
                # Erase mode - draw with black (canvas background)
                cv2.line(self.canvas, start_point, end_point, (0, 0, 0), self.brush_thickness + 5)
            else:
                opacity_alpha = self.brush_opacity / 100.0
                if use_glow:
                    # Draw glow effect (multiple lines with decreasing thickness) with opacity
                    for i in range(self.brush_thickness + 5, 0, -2):
                        alpha = 0.3 * opacity_alpha
                        overlay = self.canvas.copy()
                        cv2.line(overlay, start_point, end_point, self.brush_color, i)
                        self.canvas = cv2.addWeighted(overlay, alpha, self.canvas, 1 - alpha, 0)
                else:
                    # Apply opacity blending
                    overlay = self.canvas.copy()
                    cv2.line(overlay, start_point, end_point, self.brush_color, self.brush_thickness)
                    self.canvas = cv2.addWeighted(overlay, opacity_alpha, self.canvas, 1 - opacity_alpha, 0)
            
            # Record stroke for history
            self.stroke_history.append((start_point, end_point, self.brush_color, self.eraser_mode))
    
    def draw_point(self, point, color=(255, 0, 255)):
        """Draw a point on the canvas"""
        if point:
            cv2.circle(self.canvas, point, 5, color, cv2.FILLED)
    
    def clear(self):
        """Clear the entire canvas"""
        # Save current state to redo history before clearing
        self.redo_history.append(self.canvas.copy())
        self.canvas = np.zeros((self.height, self.width, 3), np.uint8)
        self.stroke_history = []
    
    def undo(self):
        """Undo last stroke"""
        if self.stroke_history:
            # Save current state to redo history before undoing
            self.redo_history.append(self.canvas.copy())
            self.stroke_history.pop()
            # Redraw canvas from history
            self.canvas = np.zeros((self.height, self.width, 3), np.uint8)
            for start, end, color, is_eraser in self.stroke_history:
                if is_eraser:
                    cv2.line(self.canvas, start, end, (0, 0, 0), self.brush_thickness + 5)
                else:
                    cv2.line(self.canvas, start, end, color, self.brush_thickness)
    
    def redo(self):
        """Redo last undone stroke"""
        if self.redo_history:
            self.canvas = self.redo_history.pop()
            # Rebuild stroke history from canvas
            self.stroke_history = []
    
    def set_background_color(self, color_bgr):
        """Change canvas background color"""
        self.background_color = color_bgr
        new_canvas = np.zeros((self.height, self.width, 3), np.uint8)
        new_canvas[:] = color_bgr
        # Blend old canvas onto new background
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        
        canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        bg = cv2.bitwise_and(new_canvas, new_canvas, mask=mask_inv)
        self.canvas = cv2.add(canvas_fg, bg)
    
    def set_brush_color(self, color_name):
        """Set brush color by name"""
        if color_name in self.COLORS:
            self.brush_color = self.COLORS[color_name]
            self.color_index = self.COLOR_NAMES.index(color_name)
            self.eraser_mode = False
    
    def next_color(self):
        """Switch to next color"""
        self.color_index = (self.color_index + 1) % len(self.COLOR_NAMES)
        color_name = self.COLOR_NAMES[self.color_index]
        self.brush_color = self.COLORS[color_name]
        self.eraser_mode = False
        return color_name
    
    def prev_color(self):
        """Switch to previous color"""
        self.color_index = (self.color_index - 1) % len(self.COLOR_NAMES)
        color_name = self.COLOR_NAMES[self.color_index]
        self.brush_color = self.COLORS[color_name]
        self.eraser_mode = False
        return color_name
    
    def toggle_eraser(self):
        """Toggle eraser mode"""
        self.eraser_mode = not self.eraser_mode
        return self.eraser_mode
    
    def set_brush_thickness(self, thickness):
        """Set brush thickness"""
        thickness = max(self.min_brush, min(thickness, self.max_brush))
        self.brush_thickness = thickness
        return thickness
    
    def increase_brush_size(self):
        """Increase brush size"""
        new_size = min(self.brush_thickness + 2, self.max_brush)
        self.brush_thickness = new_size
        return new_size
    
    def decrease_brush_size(self):
        """Decrease brush size"""
        new_size = max(self.brush_thickness - 2, self.min_brush)
        self.brush_thickness = new_size
        return new_size
    
    def get_canvas_stats(self):
        """Get canvas statistics"""
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        pixels_drawn = np.count_nonzero(gray)
        percentage = (pixels_drawn / (self.width * self.height)) * 100
        return {
            'strokes': len(self.stroke_history),
            'pixels_drawn': pixels_drawn,
            'fill_percentage': round(percentage, 1),
            'brush_size': self.brush_thickness,
            'brush_opacity': self.brush_opacity,
            'undo_available': len(self.stroke_history) > 0,
            'redo_available': len(self.redo_history) > 0,
            'fill_mode': self.use_fill
        }
    
    def set_brush_opacity(self, opacity):
        """Set brush opacity (0-100%)"""
        self.brush_opacity = max(0, min(100, opacity))
        return self.brush_opacity
    
    def increase_opacity(self, amount=10):
        """Increase brush opacity"""
        return self.set_brush_opacity(self.brush_opacity + amount)
    
    def decrease_opacity(self, amount=10):
        """Decrease brush opacity"""
        return self.set_brush_opacity(self.brush_opacity - amount)
    
    def toggle_fill_mode(self):
        """Toggle between filled and outline shapes"""
        self.use_fill = not self.use_fill
        return self.use_fill
    
    def get_current_color(self):
        """Get current color name"""
        if self.eraser_mode:
            return "eraser"
        return self.COLOR_NAMES[self.color_index]
    
    def get_canvas(self):
        """Get the canvas image"""
        return self.canvas.copy()
    
    def blend_with_frame(self, frame):
        """Blend canvas with video frame"""
        imgGray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        
        # Apply canvas to frame
        frame = cv2.bitwise_and(frame, imgInv)
        frame = cv2.bitwise_or(frame, self.canvas)
        
        return frame
    
    def draw_color_palette_ui(self, frame):
        """Draw color palette selector on the frame"""
        # Draw color palette at the bottom
        palette_y = self.height - 50
        color_box_width = 80
        start_x = 10
        
        for i, color_name in enumerate(self.COLOR_NAMES):
            x = start_x + i * (color_box_width + 5)
            
            # Draw color box
            color_bgr = self.COLORS[color_name]
            cv2.rectangle(frame, (x, palette_y), (x + color_box_width, palette_y + 40), color_bgr, -1)
            
            # Highlight current color with glowing border
            if i == self.color_index and not self.eraser_mode:
                cv2.rectangle(frame, (x - 2, palette_y - 2), (x + color_box_width + 2, palette_y + 42), (255, 255, 255), 3)
            
            # Draw color name
            cv2.putText(frame, color_name[:3], (x + 10, palette_y + 25), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame

