import winsound
import threading


class SoundEffects:
    """Sound effects for user feedback"""
    
    @staticmethod
    def play_click(duration=100):
        """Play click sound"""
        thread = threading.Thread(target=winsound.Beep, args=(1000, duration), daemon=True)
        thread.start()
    
    @staticmethod
    def play_success(duration=200):
        """Play success sound"""
        thread = threading.Thread(target=winsound.Beep, args=(1200, duration), daemon=True)
        thread.start()
    
    @staticmethod
    def play_error(duration=300):
        """Play error sound"""
        thread = threading.Thread(target=winsound.Beep, args=(400, duration), daemon=True)
        thread.start()
    
    @staticmethod
    def play_alert(duration=150):
        """Play alert sound"""
        thread = threading.Thread(target=winsound.Beep, args=(800, duration), daemon=True)
        thread.start()
