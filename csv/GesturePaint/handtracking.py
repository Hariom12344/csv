import cv2
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os


class HandTracker:
    def __init__(self):
        """Initialize hand tracker with MediaPipe tasks API"""
        # Download model if not exists
        model_path = self._get_model_path()
        
        try:
            base_options = python.BaseOptions(model_asset_path=model_path)
            options = vision.HandLandmarkerOptions(base_options=base_options)
            self.detector = vision.HandLandmarker.create_from_options(options)
        except Exception as e:
            print(f"Error initializing hand detector: {e}")
            print("Make sure the hand_landmarker.task model file exists")
            self.detector = None
    
    def _get_model_path(self):
        """Get or download the hand landmarker model"""
        model_name = 'hand_landmarker.task'
        model_path = os.path.join(os.path.dirname(__file__), model_name)
        
        if not os.path.exists(model_path):
            print(f"Downloading {model_name}...")
            try:
                import urllib.request
                url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
                urllib.request.urlretrieve(url, model_path)
                print(f"Model downloaded to {model_path}")
            except Exception as e:
                print(f"Failed to download model: {e}")
        
        return model_path
    
    def process_frame(self, img):
        """Process frame and detect hand landmarks"""
        if self.detector is None:
            return None
        
        try:
            # Convert BGR to RGB
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Convert to MediaPipe Image
            import mediapipe as mp
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=imgRGB)
            
            # Detect hands
            results = self.detector.detect(mp_image)
            return results
        except Exception as e:
            print(f"Error processing frame: {e}")
            return None
    
    def draw_landmarks(self, img, results):
        """Draw hand landmarks on the image"""
        if results and results.hand_landmarks:
            h, w, c = img.shape
            
            for hand_landmarks in results.hand_landmarks:
                # Draw connections
                connections = [
                    (0, 1), (1, 2), (2, 3), (3, 4),
                    (0, 5), (5, 6), (6, 7), (7, 8),
                    (0, 9), (9, 10), (10, 11), (11, 12),
                    (0, 13), (13, 14), (14, 15), (15, 16),
                    (0, 17), (17, 18), (18, 19), (19, 20)
                ]
                
                for start, end in connections:
                    if start < len(hand_landmarks) and end < len(hand_landmarks):
                        x1 = int(hand_landmarks[start].x * w)
                        y1 = int(hand_landmarks[start].y * h)
                        x2 = int(hand_landmarks[end].x * w)
                        y2 = int(hand_landmarks[end].y * h)
                        cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                # Draw landmarks
                for landmark in hand_landmarks:
                    x = int(landmark.x * w)
                    y = int(landmark.y * h)
                    cv2.circle(img, (x, y), 3, (255, 0, 0), -1)
            
            return results.hand_landmarks[0] if results.hand_landmarks else None
        return None
    
    def get_finger_position(self, hand_landmarks, img):
        """Get index finger tip position (landmark 8)"""
        if hand_landmarks and len(hand_landmarks) > 8:
            h, w, c = img.shape
            landmark = hand_landmarks[8]
            cx = int(landmark.x * w)
            cy = int(landmark.y * h)
            return (cx, cy)
        return None
    
    def release(self):
        """Release hand detector resources"""
        if self.detector:
            try:
                self.detector = None
            except:
                pass


