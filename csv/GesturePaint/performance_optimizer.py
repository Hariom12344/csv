import cv2
import numpy as np
from collections import deque


class PerformanceOptimizer:
    """Performance optimization and monitoring for GesturePaint"""
    
    def __init__(self, target_fps=30):
        self.target_fps = target_fps
        self.frame_times = deque(maxlen=30)
        self.current_fps = 0
        self.frame_skip = 0
        self.hand_detection_interval = 1  # Process every N frames
        self.frame_count = 0
        self.skip_gesture_recognition = False
        self.use_roi = True  # Region of interest optimization
        self.adaptive_quality = True
        
    def optimize_frame_size(self, frame, quality='medium'):
        """Resize frame based on quality setting for faster processing"""
        if quality == 'low':
            scale = 0.5
        elif quality == 'medium':
            scale = 0.75
        else:  # high
            scale = 1.0
        
        if scale < 1.0:
            h, w = frame.shape[:2]
            frame = cv2.resize(frame, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_LINEAR)
        
        return frame
    
    def should_process_hand_detection(self):
        """Determine if hand detection should run this frame"""
        if self.adaptive_quality and self.current_fps < self.target_fps * 0.8:
            # Skip hand detection frames if FPS is low
            result = self.frame_count % self.hand_detection_interval == 0
            self.frame_count += 1
            return result
        else:
            self.hand_detection_interval = 1
            self.frame_count += 1
            return True
    
    def get_roi_for_hand(self, frame, hand_region=None):
        """Extract region of interest to reduce processing area"""
        if not self.use_roi or hand_region is None:
            return frame, (0, 0)
        
        h, w = frame.shape[:2]
        x1, y1, x2, y2 = hand_region
        
        # Expand ROI slightly for safety
        margin = 30
        x1 = max(0, x1 - margin)
        y1 = max(0, y1 - margin)
        x2 = min(w, x2 + margin)
        y2 = min(h, y2 + margin)
        
        roi = frame[y1:y2, x1:x2]
        return roi, (x1, y1)
    
    def update_fps(self, elapsed_time):
        """Update FPS tracking and adaptive settings"""
        if elapsed_time > 0:
            fps = 1.0 / elapsed_time
            self.frame_times.append(fps)
            self.current_fps = np.mean(list(self.frame_times)) if self.frame_times else fps
            
            # Adaptive hand detection skipping
            if self.current_fps < self.target_fps * 0.7:
                self.hand_detection_interval = min(3, self.hand_detection_interval + 1)
            elif self.current_fps > self.target_fps:
                self.hand_detection_interval = max(1, self.hand_detection_interval - 1)
    
    def optimize_canvas_blending(self, frame, canvas_image, use_fast_blend=True):
        """Optimized canvas blending with option for faster processing"""
        if use_fast_blend:
            # Fast blending using simple addition instead of complex bitwise ops
            mask = cv2.cvtColor(canvas_image, cv2.COLOR_BGR2GRAY) > 10
            frame[mask] = cv2.addWeighted(frame[mask], 0.3, canvas_image[mask], 0.7, 0)
            return frame
        else:
            # Original method (slower but better quality)
            imgGray = cv2.cvtColor(canvas_image, cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
            
            frame = cv2.bitwise_and(frame, imgInv)
            frame = cv2.bitwise_or(frame, canvas_image)
            return frame
    
    def reduce_hand_landmark_complexity(self, landmarks, skip_every=3):
        """Use fewer landmarks for gesture recognition (faster processing)"""
        if landmarks is None:
            return None
        
        # Keep only every Nth landmark for quick gesture detection
        simplified = landmarks[::skip_every] if hasattr(landmarks, '__getitem__') else landmarks
        return simplified
    
    def downsample_canvas_for_display(self, canvas, quality='high'):
        """Downsample canvas for display without losing actual quality"""
        if quality == 'low':
            # Simple downsampling for preview
            return cv2.resize(canvas, None, fx=0.8, fy=0.8, interpolation=cv2.INTER_LINEAR)
        return canvas
    
    def get_performance_stats(self):
        """Return current performance metrics"""
        return {
            'fps': round(self.current_fps, 1),
            'hand_detection_interval': self.hand_detection_interval,
            'frame_count': self.frame_count,
        }
    
    def enable_adaptive_mode(self, enabled=True):
        """Enable/disable adaptive quality adjustment"""
        self.adaptive_quality = enabled
    
    def enable_roi_mode(self, enabled=True):
        """Enable/disable region of interest optimization"""
        self.use_roi = enabled
