import math


class GestureRecognizer:
    def __init__(self):
        self.last_gesture = None
    
    def recognize_gesture(self, hand_landmarks, img):
        """
        Recognize hand gestures from landmarks
        Returns: 'pointing', 'pinch', 'palm', or None
        """
        if not hand_landmarks or len(hand_landmarks) < 21:
            return None
        
        # Check if index and middle fingers are raised (pointing gesture)
        if self._is_pointing(hand_landmarks):
            return 'pointing'
        
        # Check if thumb and index finger are close (pinch gesture)
        if self._is_pinch(hand_landmarks):
            return 'pinch'
        
        # Default: palm open
        return 'palm'
    
    def _is_pointing(self, landmarks):
        """Check if pointing gesture (index finger extended, others folded)"""
        # Index finger tip above knuckle
        index_tip_y = landmarks[8].y
        index_pip_y = landmarks[6].y
        
        # Middle finger folded
        middle_tip_y = landmarks[12].y
        middle_pip_y = landmarks[10].y
        
        return (index_tip_y < index_pip_y - 0.05 and 
                middle_tip_y > middle_pip_y)
    
    def _is_pinch(self, landmarks):
        """Check if pinch gesture (thumb and index close together)"""
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        
        distance = math.sqrt(
            (thumb_tip.x - index_tip.x) ** 2 + 
            (thumb_tip.y - index_tip.y) ** 2
        )
        
        return distance < 0.05
    
    def get_last_gesture(self):
        return self.last_gesture
