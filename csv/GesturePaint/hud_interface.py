import cv2
import numpy as np
from datetime import datetime


class HUDInterface:
    """Futuristic Iron Man style HUD Interface"""
    
    # Neon colors (BGR)
    NEON_CYAN = (255, 255, 0)
    NEON_PURPLE = (255, 0, 255)
    NEON_BLUE = (255, 0, 0)
    NEON_GREEN = (0, 255, 0)
    NEON_RED = (0, 0, 255)
    
    def __init__(self, width=640, height=480):
        self.width = width
        self.height = height
        self.fps = 0
        self.frame_count = 0
        self.start_time = datetime.now()
        self.animation_frame = 0
    
    def update_fps(self):
        """Calculate FPS"""
        self.frame_count += 1
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed > 0:
            self.fps = int(self.frame_count / elapsed)
    
    def draw_hud_background(self, frame):
        """Draw semi-transparent HUD background"""
        overlay = frame.copy()
        
        # Top HUD panel
        cv2.rectangle(overlay, (0, 0), (self.width, 100), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        # Bottom panel
        overlay = frame.copy()
        cv2.rectangle(overlay, (0, self.height - 100), (self.width, self.height), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)
        
        return frame
    
    def draw_neon_border(self, frame):
        """Draw glowing neon border"""
        thickness = 3
        cv2.rectangle(frame, (thickness, thickness), 
                     (self.width - thickness, self.height - thickness),
                     self.NEON_CYAN, thickness)
        
        # Add corner accents
        corner_size = 30
        # Top-left
        cv2.line(frame, (0, corner_size), (0, 0), self.NEON_CYAN, 2)
        cv2.line(frame, (corner_size, 0), (0, 0), self.NEON_CYAN, 2)
        # Top-right
        cv2.line(frame, (self.width - corner_size, 0), (self.width, 0), self.NEON_CYAN, 2)
        cv2.line(frame, (self.width, corner_size), (self.width, 0), self.NEON_CYAN, 2)
        # Bottom-left
        cv2.line(frame, (0, self.height - corner_size), (0, self.height), self.NEON_CYAN, 2)
        cv2.line(frame, (corner_size, self.height), (0, self.height), self.NEON_CYAN, 2)
        # Bottom-right
        cv2.line(frame, (self.width - corner_size, self.height), (self.width, self.height), self.NEON_CYAN, 2)
        cv2.line(frame, (self.width, self.height - corner_size), (self.width, self.height), self.NEON_CYAN, 2)
        
        return frame
    
    def draw_status_panel(self, frame, gesture, color, drawing):
        """Draw top status panel with info"""
        # Gesture status
        cv2.putText(frame, "GESTURE:", (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, self.NEON_CYAN, 1)
        gesture_text = gesture.upper() if gesture else "NONE"
        cv2.putText(frame, gesture_text, (120, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, 
                   self.NEON_GREEN if gesture == 'pointing' else self.NEON_RED, 2)
        
        # Color status
        cv2.putText(frame, "COLOR:", (250, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, self.NEON_CYAN, 1)
        cv2.putText(frame, color.upper(), (340, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, self.NEON_PURPLE, 2)
        
        # Drawing indicator
        cv2.putText(frame, "DRAWING:", (500, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, self.NEON_CYAN, 1)
        status = "ON" if drawing else "OFF"
        status_color = self.NEON_GREEN if drawing else self.NEON_RED
        cv2.putText(frame, status, (580, 30), cv2.FONT_HERSHEY_DUPLEX, 0.8, status_color, 2)
        
        # FPS Counter
        cv2.putText(frame, f"FPS: {self.fps}", (10, 70), cv2.FONT_HERSHEY_DUPLEX, 0.7, self.NEON_BLUE, 1)
        
        return frame
    
    def draw_control_panel(self, frame):
        """Draw bottom control instructions"""
        y_offset = self.height - 90
        
        cv2.putText(frame, "CONTROLS:", (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.NEON_CYAN, 1)
        cv2.putText(frame, "1-7: Color | Gestures: Point=Draw, Pinch=Clear, Palm=Stop", 
                   (10, y_offset + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.NEON_GREEN, 1)
        cv2.putText(frame, "C: Clear | E: Eraser | S: Save | Q: Quit", 
                   (10, y_offset + 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.NEON_GREEN, 1)
        
        return frame
    
    def draw_circular_animation(self, frame, position, radius=30, color=None):
        """Draw animated circular effect around finger"""
        if not position or color is None:
            return frame
        
        self.animation_frame = (self.animation_frame + 1) % 360
        
        # Draw multiple concentric circles with fade effect
        for i in range(3):
            r = radius + (i * 10)
            alpha = int(255 * (1 - i / 3))
            
            # Draw circle
            overlay = frame.copy()
            cv2.circle(overlay, position, r, color, 2)
            cv2.addWeighted(overlay, alpha / 255, frame, 1 - alpha / 255, 0, frame)
        
        # Draw center point
        cv2.circle(frame, position, 5, color, -1)
        
        return frame
    
    def draw_particles(self, frame, position, color, num_particles=5):
        """Draw particle trail effect"""
        if not position:
            return frame
        
        for i in range(num_particles):
            offset = int(i * 3)
            size = max(1, 5 - i)
            alpha = int(255 * (1 - i / num_particles))
            
            overlay = frame.copy()
            cv2.circle(overlay, position, size, color, -1)
            cv2.addWeighted(overlay, alpha / 255, frame, 1 - alpha / 255, 0, frame)
        
        return frame
    
    def draw_glow_line(self, frame, pt1, pt2, color, thickness=5):
        """Draw glowing line effect"""
        # Draw multiple lines with decreasing thickness for glow effect
        for i in range(thickness, 0, -2):
            alpha = 0.3 * (i / thickness)
            overlay = frame.copy()
            cv2.line(overlay, pt1, pt2, color, i)
            cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
        
        # Draw solid center line
        cv2.line(frame, pt1, pt2, color, thickness // 2)
        
        return frame
    
    def draw_shape_selector(self, frame, current_mode):
        """Draw shape tool selector in HUD"""
        shapes = ['PAINT', 'RECT', 'CIRCLE', 'LINE', 'TRIANGLE']
        y_pos = 140
        x_start = 10
        box_width = 70
        
        for i, shape in enumerate(shapes):
            x = x_start + i * (box_width + 5)
            
            # Highlight current shape
            color = self.NEON_GREEN if shape == current_mode.upper() else self.NEON_BLUE
            thickness = 3 if shape == current_mode.upper() else 1
            
            cv2.rectangle(frame, (x, y_pos), (x + box_width, y_pos + 35), color, thickness)
            cv2.putText(frame, shape, (x + 5, y_pos + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.35, color, 1)
        
        return frame
    
    def draw_rgb_mixer_display(self, frame, r, g, b):
        """Draw RGB mixer values on HUD"""
        y_offset = 185
        
        # RGB title
        cv2.putText(frame, "RGB MIXER:", (10, y_offset), cv2.FONT_HERSHEY_DUPLEX, 0.7, self.NEON_CYAN, 1)
        
        # R value with bar
        cv2.putText(frame, f"R: {r}", (10, y_offset + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.NEON_RED, 1)
        cv2.rectangle(frame, (50, y_offset + 15), (50 + int(r/2), y_offset + 30), self.NEON_RED, -1)
        cv2.rectangle(frame, (50, y_offset + 15), (50 + 127, y_offset + 30), self.NEON_RED, 1)
        
        # G value with bar
        cv2.putText(frame, f"G: {g}", (150, y_offset + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.NEON_GREEN, 1)
        cv2.rectangle(frame, (190, y_offset + 15), (190 + int(g/2), y_offset + 30), self.NEON_GREEN, -1)
        cv2.rectangle(frame, (190, y_offset + 15), (190 + 127, y_offset + 30), self.NEON_GREEN, 1)
        
        # B value with bar
        cv2.putText(frame, f"B: {b}", (290, y_offset + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, self.NEON_BLUE, 1)
        cv2.rectangle(frame, (330, y_offset + 15), (330 + int(b/2), y_offset + 30), self.NEON_BLUE, -1)
        cv2.rectangle(frame, (330, y_offset + 15), (330 + 127, y_offset + 30), self.NEON_BLUE, 1)
        
        return frame
    
    def draw_theme_indicator(self, frame, theme_name, x=480, y=185):
        """Draw current theme indicator"""
        cv2.putText(frame, f"THEME: {theme_name.upper()}", (x, y), cv2.FONT_HERSHEY_DUPLEX, 0.6, self.NEON_PURPLE, 1)
        return frame
    
    def draw_voice_status(self, frame, status, x=10, y=450):
        """Draw voice recognition status"""
        # Color based on status
        if status == "LISTENING":
            color = self.NEON_GREEN
            display_text = "🎤 LISTENING..."
        elif status == "CAPTURING":
            color = self.NEON_BLUE
            display_text = "🎤 CAPTURING..."
        elif status == "PROCESSING":
            color = self.NEON_CYAN
            display_text = "🎤 PROCESSING..."
        elif status == "RECOGNIZED":
            color = self.NEON_GREEN
            display_text = "[OK] RECOGNIZED"
        elif status == "UNCLEAR":
            color = self.NEON_RED
            display_text = "[!] UNCLEAR"
        elif status == "NETWORK_ERROR":
            color = self.NEON_RED
            display_text = "[!] NO INTERNET"
        elif status == "ERROR":
            color = self.NEON_RED
            display_text = "[!] ERROR"
        else:
            color = self.NEON_CYAN
            display_text = "○ READY"
        
        cv2.rectangle(frame, (x, y - 15), (x + 200, y + 10), color, 2)
        cv2.putText(frame, display_text, (x + 5, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)
        
        return frame


    
    def draw_power_gauge(self, frame, percentage):
        """Draw power/battery gauge"""
        x, y = 550, self.height - 50
        width, height = 70, 20
        
        # Draw gauge background
        cv2.rectangle(frame, (x, y), (x + width, y + height), self.NEON_CYAN, 2)
        
        # Draw filled portion
        filled_width = int((percentage / 100) * width)
        color = self.NEON_GREEN if percentage > 30 else self.NEON_RED
        cv2.rectangle(frame, (x, y), (x + filled_width, y + height), color, -1)
        
        # Draw percentage text
        cv2.putText(frame, f"{percentage}%", (x + 10, y + 15), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.NEON_CYAN, 1)
        
        return frame
    
    def draw_canvas_stats_display(self, frame, stats):
        """Draw canvas statistics display on HUD"""
        x, y = self.width - 250, 140
        line_height = 20
        
        # Draw stats panel background
        cv2.rectangle(frame, (x - 10, y - 30), (x + 240, y + 150),
                     (0, 0, 0), -1)
        cv2.rectangle(frame, (x - 10, y - 30), (x + 240, y + 150),
                     self.NEON_CYAN, 2)
        
        # Title
        cv2.putText(frame, "CANVAS STATS", (x - 5, y - 10),
                   cv2.FONT_HERSHEY_DUPLEX, 0.6, self.NEON_CYAN, 1)
        
        # Stats lines
        fill_mode = "FILLED" if stats.get('fill_mode', False) else "OUTLINE"
        stats_lines = [
            f"Strokes: {stats.get('strokes', 0)}",
            f"Fill: {stats.get('fill_percentage', 0):.1f}%",
            f"Brush: {stats.get('brush_size', 5)}px | Opacity: {stats.get('brush_opacity', 100)}%",
            f"Mode: {fill_mode}",
            f"Undo: {'Avail' if stats.get('undo_available', False) else 'None'}",
            f"Redo: {'Avail' if stats.get('redo_available', False) else 'None'}",
        ]
        
        for i, line in enumerate(stats_lines):
            cv2.putText(frame, line, (x, y + i * line_height),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.NEON_GREEN, 1)
        
        return frame
    
    def draw_performance_stats(self, frame, perf_stats):
        """Draw performance statistics on HUD"""
        x, y = 10, 100
        line_height = 18
        
        # Background
        cv2.rectangle(frame, (x - 5, y - 20), (x + 200, y + 80),
                     (20, 20, 20), cv2.FILLED)
        cv2.rectangle(frame, (x - 5, y - 20), (x + 200, y + 80),
                     self.NEON_BLUE, 1)
        
        cv2.putText(frame, "PERFORMANCE", (x, y - 5),
                   cv2.FONT_HERSHEY_DUPLEX, 0.6, self.NEON_BLUE, 1)
        
        fps = perf_stats.get('fps', 0)
        fps_color = self.NEON_GREEN if fps > 20 else self.NEON_RED
        
        cv2.putText(frame, f"FPS: {fps}", (x, y + line_height),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, fps_color, 1)
        cv2.putText(frame, f"Hand Det: {perf_stats.get('hand_detection_interval', 1)}x skip",
                   (x, y + line_height * 2), cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.NEON_CYAN, 1)
        
        return frame
