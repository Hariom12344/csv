import cv2
import numpy as np
from copy import deepcopy


class LayerManager:
    """Multi-layer support for drawing"""
    
    def __init__(self, frame_width=640, frame_height=480, max_layers=5):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.max_layers = max_layers
        self.layers = []
        self.layer_names = []
        self.layer_visibility = []
        self.current_layer_index = 0
        
        # Create default layer
        self.add_layer("Layer 1")
    
    def add_layer(self, name=None):
        """Add a new layer"""
        if len(self.layers) >= self.max_layers:
            return False
        
        if name is None:
            name = f"Layer {len(self.layers) + 1}"
        
        # Create new blank layer
        new_layer = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
        self.layers.append(new_layer)
        self.layer_names.append(name)
        self.layer_visibility.append(True)
        
        return True
    
    def delete_layer(self, index):
        """Delete a layer (keep at least one)"""
        if len(self.layers) <= 1:
            return False
        
        if 0 <= index < len(self.layers):
            self.layers.pop(index)
            self.layer_names.pop(index)
            self.layer_visibility.pop(index)
            
            # Update current layer index if needed
            if self.current_layer_index >= len(self.layers):
                self.current_layer_index = len(self.layers) - 1
            
            return True
        
        return False
    
    def select_layer(self, index):
        """Select a layer to draw on"""
        if 0 <= index < len(self.layers):
            self.current_layer_index = index
            return True
        return False
    
    def get_current_layer(self):
        """Get current active layer"""
        if 0 <= self.current_layer_index < len(self.layers):
            return self.layers[self.current_layer_index]
        return None
    
    def toggle_layer_visibility(self, index):
        """Toggle layer visibility"""
        if 0 <= index < len(self.layer_visibility):
            self.layer_visibility[index] = not self.layer_visibility[index]
            return self.layer_visibility[index]
        return False
    
    def merge_down(self, index):
        """Merge layer with layer below"""
        if index <= 0 or index >= len(self.layers):
            return False
        
        # Blend current layer onto layer below
        below_layer = self.layers[index - 1]
        current_layer = self.layers[index]
        
        # Get non-transparent pixels from current layer
        gray = cv2.cvtColor(current_layer, cv2.COLOR_BGR2GRAY)
        mask = cv2.cvtColor(gray > 10, cv2.COLOR_GRAY2BGR)
        
        # Blend
        result = cv2.addWeighted(below_layer, 0.7, current_layer, 0.3, 0)
        self.layers[index - 1] = result
        
        # Delete current layer
        return self.delete_layer(index)
    
    def merge_all(self):
        """Merge all visible layers into first layer"""
        result = self.layers[0].copy()
        
        for i in range(1, len(self.layers)):
            if self.layer_visibility[i]:
                result = cv2.addWeighted(result, 0.8, self.layers[i], 0.2, 0)
        
        self.layers[0] = result
        
        # Delete other layers
        while len(self.layers) > 1:
            self.delete_layer(1)
        
        return True
    
    def composite_layers(self):
        """Composite all visible layers into single image"""
        result = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
        
        for i, layer in enumerate(self.layers):
            if self.layer_visibility[i]:
                # Add layer with alpha blending
                result = cv2.addWeighted(result, 0.9, layer, 0.1, 0)
        
        return result
    
    def rename_layer(self, index, new_name):
        """Rename a layer"""
        if 0 <= index < len(self.layer_names):
            self.layer_names[index] = new_name
            return True
        return False
    
    def duplicate_layer(self, index):
        """Duplicate a layer"""
        if len(self.layers) >= self.max_layers:
            return False
        
        if 0 <= index < len(self.layers):
            new_layer = self.layers[index].copy()
            self.layers.insert(index + 1, new_layer)
            self.layer_names.insert(index + 1, f"{self.layer_names[index]} copy")
            self.layer_visibility.insert(index + 1, True)
            return True
        
        return False
    
    def next_layer(self):
        """Select next layer"""
        self.current_layer_index = (self.current_layer_index + 1) % len(self.layers)
        return self.current_layer_index
    
    def prev_layer(self):
        """Select previous layer"""
        self.current_layer_index = (self.current_layer_index - 1) % len(self.layers)
        return self.current_layer_index
    
    def get_layer_info(self):
        """Get info about all layers"""
        layers_info = []
        for i, (name, visible) in enumerate(zip(self.layer_names, self.layer_visibility)):
            is_current = i == self.current_layer_index
            layers_info.append({
                'index': i,
                'name': name,
                'visible': visible,
                'current': is_current
            })
        
        return layers_info
    
    def clear_current_layer(self):
        """Clear current layer"""
        self.layers[self.current_layer_index] = np.zeros((self.frame_height, self.frame_width, 3), np.uint8)
