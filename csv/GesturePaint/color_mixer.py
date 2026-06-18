class ColorMixer:
    """RGB Color Mixer for fine-tuned color control"""
    
    def __init__(self):
        self.r = 0
        self.g = 0
        self.b = 255  # Start with blue
        self.custom_color = (self.b, self.g, self.r)  # BGR format
    
    def get_color(self):
        """Get current RGB color in BGR format"""
        return (self.b, self.g, self.r)
    
    def increase_red(self, amount=10):
        """Increase red value"""
        self.r = min(255, self.r + amount)
        self.custom_color = (self.b, self.g, self.r)
        return self.r
    
    def decrease_red(self, amount=10):
        """Decrease red value"""
        self.r = max(0, self.r - amount)
        self.custom_color = (self.b, self.g, self.r)
        return self.r
    
    def increase_green(self, amount=10):
        """Increase green value"""
        self.g = min(255, self.g + amount)
        self.custom_color = (self.b, self.g, self.r)
        return self.g
    
    def decrease_green(self, amount=10):
        """Decrease green value"""
        self.g = max(0, self.g - amount)
        self.custom_color = (self.b, self.g, self.r)
        return self.g
    
    def increase_blue(self, amount=10):
        """Increase blue value"""
        self.b = min(255, self.b + amount)
        self.custom_color = (self.b, self.g, self.r)
        return self.b
    
    def decrease_blue(self, amount=10):
        """Decrease blue value"""
        self.b = max(0, self.b - amount)
        self.custom_color = (self.b, self.g, self.r)
        return self.b
    
    def reset(self):
        """Reset to default blue"""
        self.r = 0
        self.g = 0
        self.b = 255
        self.custom_color = (self.b, self.g, self.r)
    
    def set_rgb(self, r, g, b):
        """Set RGB values directly"""
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.custom_color = (self.b, self.g, self.r)
    
    def get_rgb_string(self):
        """Get RGB values as string"""
        return f"R:{self.r} G:{self.g} B:{self.b}"


class ColorThemes:
    """Color theme presets"""
    
    THEMES = {
        'dark': {
            'name': 'Dark Mode',
            'colors': [(50, 50, 50), (100, 100, 100), (200, 200, 200), (255, 255, 255)]
        },
        'neon': {
            'name': 'Neon Mode',
            'colors': [(255, 255, 0), (255, 0, 255), (0, 255, 255), (0, 255, 0)]
        },
        'pastel': {
            'name': 'Pastel Mode',
            'colors': [(200, 100, 150), (100, 200, 200), (200, 200, 100), (150, 100, 200)]
        },
        'fire': {
            'name': 'Fire Mode',
            'colors': [(0, 0, 255), (0, 100, 255), (0, 165, 255), (0, 255, 255)]
        },
        'ice': {
            'name': 'Ice Mode',
            'colors': [(255, 0, 0), (255, 100, 0), (200, 150, 100), (255, 255, 255)]
        },
        'ocean': {
            'name': 'Ocean Mode',
            'colors': [(255, 0, 0), (255, 100, 0), (0, 150, 255), (0, 255, 255)]
        }
    }
    
    def __init__(self):
        self.current_theme = 'neon'
        self.color_index = 0
    
    def get_theme_colors(self):
        """Get current theme colors"""
        return self.THEMES[self.current_theme]['colors']
    
    def get_current_color(self):
        """Get current color from theme"""
        colors = self.get_theme_colors()
        return colors[self.color_index % len(colors)]
    
    def next_color_in_theme(self):
        """Switch to next color in current theme"""
        colors = self.get_theme_colors()
        self.color_index = (self.color_index + 1) % len(colors)
        return self.get_current_color()
    
    def set_theme(self, theme_name):
        """Change color theme"""
        if theme_name in self.THEMES:
            self.current_theme = theme_name
            self.color_index = 0
            return True
        return False
    
    def get_theme_name(self):
        """Get current theme name"""
        return self.THEMES[self.current_theme]['name']
    
    def list_themes(self):
        """List all available themes"""
        return list(self.THEMES.keys())
