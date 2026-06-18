import speech_recognition as sr
import threading
import time


class VoiceCommandRecognizer:
    """Real-time voice command recognition with better error handling"""
    
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Calibrate for ambient noise
            print("Calibrating microphone... Please wait.")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                self.recognizer.energy_threshold = 4000  # Adjust sensitivity
            print("[OK] Microphone calibrated successfully")
            
            self.is_listening = False
            self.last_command = None
            self.last_raw_audio = None
            self.listening_status = "READY"
            self.command_callback = None
        except Exception as e:
            print(f"[ERR] Error initializing microphone: {e}")
            print("  Make sure your microphone is connected and working")
            self.recognizer = None
            self.microphone = None
    
    def start_listening(self, callback=None):
        """Start listening for voice commands in a background thread"""
        if not self.recognizer or not self.microphone:
            print("[ERR] Microphone not available")
            return False
        
        self.is_listening = True
        self.command_callback = callback
        self.listening_status = "LISTENING"
        
        # Start listening in background thread
        listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        listen_thread.start()
        return True
    
    def stop_listening(self):
        """Stop listening for voice commands"""
        self.is_listening = False
        self.listening_status = "STOPPED"
    
    def _listen_loop(self):
        """Continuous listening loop with better error handling"""
        if not self.recognizer or not self.microphone:
            return
        
        retry_count = 0
        max_retries = 3
        
        while self.is_listening:
            try:
                self.listening_status = "LISTENING"
                
                with self.microphone as source:
                    print("[MIC] Listening for voice command...")
                    self.listening_status = "CAPTURING"
                    
                    # Listen for audio with adjusted parameters
                    audio = self.recognizer.listen(
                        source,
                        timeout=5,           # Wait up to 5 seconds for speech
                        phrase_time_limit=10  # Max 10 seconds for phrase
                    )
                    
                    self.last_raw_audio = audio
                    self.listening_status = "PROCESSING"
                    print("[MIC] Processing audio...")
                
                # Try Google Speech Recognition
                try:
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"[OK] [VOICE INPUT] '{command}'")
                    self.last_command = command
                    self.listening_status = "RECOGNIZED"
                    retry_count = 0  # Reset retry on success
                    
                    if self.command_callback:
                        self.command_callback(command)
                    
                    # Brief pause before next listen
                    time.sleep(0.5)
                
                except sr.UnknownValueError:
                    print("[MIC] Could not understand audio - please speak clearly")
                    self.listening_status = "UNCLEAR"
                    retry_count += 1
                
                except sr.RequestError as e:
                    print(f"[MIC] Network error: {e}")
                    print("  (Need internet for Google Speech Recognition)")
                    self.listening_status = "NETWORK_ERROR"
                    retry_count += 1
                    time.sleep(2)  # Wait before retry
                
            except sr.WaitTimeoutError:
                self.listening_status = "WAITING"
                # Silently wait for next input
                pass
            
            except Exception as e:
                print(f"[MIC] Error: {str(e)}")
                self.listening_status = "ERROR"
                retry_count += 1
                time.sleep(1)
            
            # Reset if too many retries
            if retry_count >= max_retries:
                print("[MIC] Too many errors, restarting microphone...")
                retry_count = 0
                time.sleep(2)
    
    def parse_command(self, voice_input):
        """Parse voice input and return action"""
        voice_input = voice_input.lower().strip()
        
        # Color commands
        if 'color' in voice_input or 'change' in voice_input:
            for color in ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white']:
                if color in voice_input:
                    return {'action': 'set_color', 'value': color}
        
        # Shape commands
        if 'rectangle' in voice_input or 'rect' in voice_input or 'box' in voice_input or 'square' in voice_input:
            return {'action': 'set_shape', 'value': 'rect'}
        elif 'circle' in voice_input or 'oval' in voice_input or 'round' in voice_input:
            return {'action': 'set_shape', 'value': 'circle'}
        elif 'line' in voice_input or 'draw line' in voice_input:
            return {'action': 'set_shape', 'value': 'line'}
        elif 'triangle' in voice_input:
            return {'action': 'set_shape', 'value': 'triangle'}
        elif 'paint' in voice_input or 'freehand' in voice_input or 'draw' in voice_input or 'drawing' in voice_input:
            return {'action': 'set_shape', 'value': 'paint'}
        
        # Theme commands
        if 'dark' in voice_input:
            return {'action': 'set_theme', 'value': 'dark'}
        elif 'neon' in voice_input:
            return {'action': 'set_theme', 'value': 'neon'}
        elif 'pastel' in voice_input:
            return {'action': 'set_theme', 'value': 'pastel'}
        elif 'fire' in voice_input:
            return {'action': 'set_theme', 'value': 'fire'}
        elif 'ice' in voice_input:
            return {'action': 'set_theme', 'value': 'ice'}
        elif 'ocean' in voice_input:
            return {'action': 'set_theme', 'value': 'ocean'}
        
        # Tool commands
        if 'clear' in voice_input or 'erase all' in voice_input or 'reset' in voice_input:
            return {'action': 'clear'}
        elif 'undo' in voice_input or 'go back' in voice_input or 'back' in voice_input:
            return {'action': 'undo'}
        elif 'redo' in voice_input or 'forward' in voice_input or 'do again' in voice_input or 'repeat' in voice_input:
            return {'action': 'redo'}
        elif 'eraser' in voice_input:
            if 'on' in voice_input or 'turn on' in voice_input:
                return {'action': 'eraser_on'}
            elif 'off' in voice_input or 'turn off' in voice_input:
                return {'action': 'eraser_off'}
            else:
                return {'action': 'toggle_eraser'}
        elif 'save' in voice_input or 'export' in voice_input or 'save drawing' in voice_input:
            return {'action': 'save'}
        
        # Brush size commands
        if 'brush' in voice_input or 'size' in voice_input or 'thick' in voice_input:
            if 'bigger' in voice_input or 'larger' in voice_input or 'increase' in voice_input or 'up' in voice_input:
                return {'action': 'brush_increase'}
            elif 'smaller' in voice_input or 'decrease' in voice_input or 'thinner' in voice_input or 'down' in voice_input:
                return {'action': 'brush_decrease'}
        
        # Brush size commands
        if 'brush' in voice_input or 'size' in voice_input or 'thick' in voice_input:
            if 'bigger' in voice_input or 'larger' in voice_input or 'increase' in voice_input or 'up' in voice_input:
                return {'action': 'brush_increase'}
            elif 'smaller' in voice_input or 'decrease' in voice_input or 'thinner' in voice_input or 'down' in voice_input:
                return {'action': 'brush_decrease'}
        
        # Opacity commands
        if 'opacity' in voice_input or 'transparency' in voice_input or 'alpha' in voice_input:
            if 'increase' in voice_input or 'more' in voice_input or 'stronger' in voice_input:
                return {'action': 'opacity_increase'}
            elif 'decrease' in voice_input or 'less' in voice_input or 'lighter' in voice_input:
                return {'action': 'opacity_decrease'}
        
        # Fill mode command
        if 'fill' in voice_input or 'filled' in voice_input:
            if 'toggle' in voice_input or 'switch' in voice_input or 'mode' in voice_input:
                return {'action': 'toggle_fill'}
        
        # Grid command
        if 'grid' in voice_input:
            if 'on' in voice_input or 'show' in voice_input:
                return {'action': 'grid_on'}
            elif 'off' in voice_input or 'hide' in voice_input:
                return {'action': 'grid_off'}
            else:
                return {'action': 'toggle_grid'}
        
        # Color picker command
        if 'color picker' in voice_input or 'pick color' in voice_input:
            return {'action': 'toggle_color_picker'}
        
        return {'action': None}
    
    def get_last_command(self):
        """Get the last recognized command"""
        return self.last_command
    
    def get_status(self):
        """Get current listening status"""
        return self.listening_status

