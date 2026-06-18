import cv2
import numpy as np


class ToolbarUI:
    """On-canvas toolbar for quick tool access"""
    
    def __init__(self, frame_width=640, frame_height=480):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.button_size = 45
        self.button_spacing = 5
        self.toolbar_height = self.button_size + 10
        self.toolbar_bg_color = (20, 20, 20)
        self.toolbar_border_color = (0, 255, 255)  # Cyan border
        self.button_bg_color = (40, 40, 40)
        self.button_active_color = (0, 255, 255)
        self.button_inactive_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
        
        # Define toolbar buttons (top-left corner)
        self.buttons = {
            'paint': {'pos': (5, 5), 'label': 'P', 'tooltip': 'Paint'},
            'rect': {'pos': (55, 5), 'label': 'R', 'tooltip': 'Rectangle'},
            'circle': {'pos': (105, 5), 'label': 'C', 'tooltip': 'Circle'},
            'line': {'pos': (155, 5), 'label': 'L', 'tooltip': 'Line'},
            'triangle': {'pos': (205, 5), 'label': 'T', 'tooltip': 'Triangle'},
            'eraser': {'pos': (255, 5), 'label': 'E', 'tooltip': 'Eraser'},
            'undo': {'pos': (305, 5), 'label': 'U', 'tooltip': 'Undo'},
            'redo': {'pos': (355, 5), 'label': 'Y', 'tooltip': 'Redo'},
            'clear': {'pos': (405, 5), 'label': 'X', 'tooltip': 'Clear'},
            'save': {'pos': (455, 5), 'label': 'S', 'tooltip': 'Save'},
        }
    
    def draw_toolbar(self, frame, active_tool=None, can_undo=False, can_redo=False):
        """Draw toolbar on the frame"""
        # Draw toolbar background
        cv2.rectangle(frame, (0, 0), (self.frame_width, self.toolbar_height),
                     self.toolbar_bg_color, cv2.FILLED)
        cv2.rectangle(frame, (0, 0), (self.frame_width, self.toolbar_height),
                     self.toolbar_border_color, 2)
        
        # Draw buttons
        for tool_name, button_info in self.buttons.items():
            x, y = button_info['pos']
            
            # Determine if button is active or disabled
            if tool_name in ['undo'] and not can_undo:
                button_color = (50, 50, 50)
                disabled = True
            elif tool_name in ['redo'] and not can_redo:
                button_color = (50, 50, 50)
                disabled = True
            elif tool_name == active_tool:
                button_color = self.button_active_color
                disabled = False
            else:
                button_color = self.button_inactive_color
                disabled = False
            
            # Draw button rectangle
            cv2.rectangle(frame, (x, y), (x + self.button_size, y + self.button_size),
                         button_color, cv2.FILLED)
            cv2.rectangle(frame, (x, y), (x + self.button_size, y + self.button_size),
                         (150, 150, 150), 1)
            
            # Draw button label
            text_color = self.text_color if not disabled else (80, 80, 80)
            cv2.putText(frame, button_info['label'], (x + 14, y + 32),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, text_color, 2)
        
        return frame
    
    def get_button_at_position(self, x, y):
        """Get button name at given position"""
        if y < self.toolbar_height:
            for tool_name, button_info in self.buttons.items():
                bx, by = button_info['pos']
                if bx <= x <= bx + self.button_size and by <= y <= by + self.button_size:
                    return tool_name
        return None
    
    def draw_color_palette(self, frame, colors_dict, active_color=None):
        """Draw color palette below toolbar"""
        palette_y = self.toolbar_height + 5
        palette_x = 5
        color_size = 30
        
        color_index = 0
        for color_name, color_bgr in colors_dict.items():
            x = palette_x + (color_index * (color_size + 3))
            y = palette_y
            
            # Draw color box
            cv2.rectangle(frame, (x, y), (x + color_size, y + color_size),
                         color_bgr, cv2.FILLED)
            
            # Highlight active color
            border_color = (255, 255, 255) if color_name == active_color else (100, 100, 100)
            border_width = 3 if color_name == active_color else 1
            cv2.rectangle(frame, (x, y), (x + color_size, y + color_size),
                         border_color, border_width)
            
            color_index += 1
        
        return frame
    
    def draw_brush_size_indicator(self, frame, brush_size, max_brush=25):
        """Draw brush size indicator in top-right corner"""
        bar_width = 100
        bar_height = 20
        bar_x = self.frame_width - bar_width - 10
        bar_y = 10
        
        # Draw background
        cv2.rectangle(frame, (bar_x - 5, bar_y), (bar_x + bar_width + 5, bar_y + bar_height),
                     (30, 30, 30), cv2.FILLED)
        
        # Draw border
        cv2.rectangle(frame, (bar_x - 5, bar_y), (bar_x + bar_width + 5, bar_y + bar_height),
                     (0, 255, 255), 1)
        
        # Draw progress bar
        fill_width = int((brush_size / max_brush) * bar_width)
        cv2.rectangle(frame, (bar_x, bar_y + 3), (bar_x + fill_width, bar_y + bar_height - 3),
                     (0, 200, 255), cv2.FILLED)
        
        # Draw text
        text = f"Size: {brush_size}"
        cv2.putText(frame, text, (bar_x + 5, bar_y + 15),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
        
        return frame
    
    def draw_canvas_stats(self, frame, stats):
        """Draw canvas statistics in bottom-right corner"""
        x = 10
        y = self.frame_height - 90
        line_height = 15
        bg_color = (20, 20, 20)
        text_color = (0, 255, 255)
        
        # Draw background panel
        cv2.rectangle(frame, (x, y - 5), (x + 200, y + line_height * 5 + 5),
                     bg_color, cv2.FILLED)
        cv2.rectangle(frame, (x, y - 5), (x + 200, y + line_height * 5 + 5),
                     (0, 255, 255), 1)
        
        # Draw stats
        stats_lines = [
            f"Strokes: {stats['strokes']}",
            f"Fill: {stats['fill_percentage']}%",
            f"Brush: {stats['brush_size']}px",
            f"Undo: {'Yes' if stats['undo_available'] else 'No'}",
            f"Redo: {'Yes' if stats['redo_available'] else 'No'}",
        ]
        
        for i, line in enumerate(stats_lines):
            cv2.putText(frame, line, (x + 10, y + (i + 1) * line_height),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.35, text_color, 1)
        
        return frame
