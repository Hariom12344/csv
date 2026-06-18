import pyttsx3
import threading


class VoiceAssistant:
    """Iron Man JARVIS-style voice assistant"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Speed of speech
        self.engine.setProperty('volume', 0.7)  # Volume
        
        # Try to set to a nice voice
        try:
            voices = self.engine.getProperty('voices')
            if len(voices) > 0:
                self.engine.setProperty('voice', voices[0].id)
        except:
            pass
    
    def speak(self, text):
        """Speak text in a separate thread to avoid blocking"""
        thread = threading.Thread(target=self._speak, args=(text,), daemon=True)
        thread.start()
    
    def _speak(self, text):
        """Internal speak method"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass
    
    def get_greeting(self):
        """Get a greeting based on time"""
        return "GesturePaint system online. Ready to paint, sir."
    
    def on_color_change(self, color):
        """Announce color change"""
        self.speak(f"Color changed to {color}")
    
    def on_clear(self):
        """Announce clearing canvas"""
        self.speak("Canvas cleared, sir.")
    
    def on_gesture(self, gesture):
        """Announce gesture detection"""
        if gesture == 'pointing':
            self.speak("Drawing mode activated")
        elif gesture == 'pinch':
            self.speak("Clear command executed")
    
    def on_save(self):
        """Announce saving"""
        self.speak("Image saved successfully")
    
    def on_error(self):
        """Announce error"""
        self.speak("Error detected. Please try again")
