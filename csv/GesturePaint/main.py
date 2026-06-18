import cv2
import numpy as np
from handtracking import HandTracker
from gesture_recognition import GestureRecognizer
from canvas_engine import CanvasEngine
from hud_interface import HUDInterface
from voice_assistant import VoiceAssistant
from sound_effects import SoundEffects
from shape_drawer import ShapeDrawer
from color_mixer import ColorMixer, ColorThemes
from voice_command import VoiceCommandRecognizer
from toolbar_ui import ToolbarUI
from color_picker_ui import ColorPickerUI
from performance_optimizer import PerformanceOptimizer
from drawing_grid import DrawingGrid
from text_tool import TextTool
from layer_manager import LayerManager
from datetime import datetime
import time


def mouse_callback(event, x, y, flags, param):
    """Handle mouse clicks for toolbar and UI interactions"""
    if event == cv2.EVENT_LBUTTONDOWN:
        toolbar, shape_drawer, canvas, color_picker, sound = param
        
        # Check toolbar button clicks
        button = toolbar.get_button_at_position(x, y)
        if button:
            if button == 'paint':
                shape_drawer.set_mode('paint')
                sound.play_click()
                print("Mode: Paint")
            elif button == 'rect':
                shape_drawer.set_mode('rect')
                sound.play_click()
                print("Mode: Rectangle")
            elif button == 'circle':
                shape_drawer.set_mode('circle')
                sound.play_click()
                print("Mode: Circle")
            elif button == 'line':
                shape_drawer.set_mode('line')
                sound.play_click()
                print("Mode: Line")
            elif button == 'triangle':
                shape_drawer.set_mode('triangle')
                sound.play_click()
                print("Mode: Triangle")
            elif button == 'eraser':
                eraser_active = canvas.toggle_eraser()
                sound.play_click()
                print(f"Eraser: {'ON' if eraser_active else 'OFF'}")
            elif button == 'undo':
                canvas.undo()
                sound.play_click()
                print("Undo executed")
            elif button == 'redo':
                canvas.redo()
                sound.play_click()
                print("Redo executed")
            elif button == 'clear':
                canvas.clear()
                sound.play_alert()
                print("Canvas cleared")
            elif button == 'save':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"drawing_{timestamp}.png"
                cv2.imwrite(filename, canvas.get_canvas())
                sound.play_success()
                print(f"Drawing saved as {filename}")
        
        # Check color picker interaction
        if color_picker.is_open:
            if color_picker.is_close_button_clicked(x, y):
                color_picker.toggle()
                sound.play_click()
            else:
                slider_idx = color_picker.get_slider_at_position(x, y)
                if slider_idx >= 0:
                    color_picker.update_slider(slider_idx, x)
                    # Update canvas brush color with custom color
                    custom_color = color_picker.get_current_color()
                    canvas.brush_color = custom_color
                    canvas.eraser_mode = False
                    print(f"Custom color set: {custom_color}")


def main():
    """
    GesturePaint - Iron Man Style Gesture Painting Application
    With Shape Tools & RGB Color Mixer & Enhanced UI
    """
    
    # Initialize components
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    tracker = HandTracker()
    gesture_recognizer = GestureRecognizer()
    canvas = CanvasEngine(width=640, height=480)
    hud = HUDInterface(width=640, height=480)
    shape_drawer = ShapeDrawer()
    color_mixer = ColorMixer()
    color_themes = ColorThemes()
    toolbar = ToolbarUI(frame_width=640, frame_height=480)
    color_picker = ColorPickerUI(frame_width=640, frame_height=480)
    perf_optimizer = PerformanceOptimizer(target_fps=30)
    drawing_grid = DrawingGrid(frame_width=640, frame_height=480)
    text_tool = TextTool(frame_width=640, frame_height=480)
    layer_manager = LayerManager(frame_width=640, frame_height=480)
    
    try:
        voice = VoiceAssistant()
        voice.speak("Shape painting system online. Ready to create, sir.")
    except:
        voice = None
    
    sound = SoundEffects()
    
    # Initialize Voice Command Recognizer
    try:
        voice_cmd = VoiceCommandRecognizer()
        if voice_cmd.start_listening():
            print("[OK] Voice recognition: ACTIVE")
            print("  Say 'change color red' or 'rectangle' etc.")
            if voice:
                voice.speak("Voice recognition activated. Ready to listen.")
        else:
            print("[ERR] Voice recognition: FAILED TO START")
            voice_cmd = None
    except Exception as e:
        print(f"[ERR] Voice recognition unavailable: {e}")
        print("  Make sure your microphone is connected")
        print("  And you have internet for Google Speech API")
        voice_cmd = None
    
    # State variables
    prev_finger_pos = None
    drawing = False
    shape_start_point = None
    power_level = 100
    
    print("=" * 60)
    print("GesturePaint - Iron Man Edition - Enhanced Phase 2")
    print("=" * 60)
    print("\nSHAPE TOOLS (Number Keys):")
    print("  0: Paint/Freehand")
    print("  1: Rectangle")
    print("  2: Circle")
    print("  3: Line")
    print("  4: Triangle")
    print("\nCOLOR & BRUSH:")
    print("  1-7: Quick colors | K: Color picker")
    print("  [/]: Brush size | ;/': Opacity decrease/increase")
    print("  V: Toggle Fill mode | Theme Keys: D,N,P,F,I,O")
    print("\nVOICE COMMANDS (Say these):")
    print("  'Change color red', 'rectangle', 'clear', 'undo', 'redo'")
    print("  'brush bigger/smaller', 'opacity more/less', 'toggle fill'")
    print("  'show/hide grid', 'dark/neon theme', 'save drawing'")
    print("\nKEYBOARD CONTROLS:")
    print("  E: Eraser | Z: Undo | Y: Redo | C: Clear | S: Save | Q: Quit")
    print("  [/]: Brush size | ;/': Opacity | V: Fill | G: Grid | K: Color Picker")
    print("=" * 60 + "\n")
    
    # Initialize window variable - will be created on first frame
    window_name = "GesturePaint - Iron Man Edition"
    window_created = False
    
    # Initialize performance tracking
    frame_start_time = time.time()
    
    while True:
        success, img = cap.read()
        if not success:
            break
        
        # Create window on first frame
        if not window_created:
            cv2.namedWindow(window_name)
            cv2.setMouseCallback(window_name, mouse_callback, param=(toolbar, shape_drawer, canvas, color_picker, sound))
            window_created = True
        
        img = cv2.resize(img, (640, 480))
        
        # Hand tracking
        results = tracker.process_frame(img)
        handLms = tracker.draw_landmarks(img, results)
        finger_pos = tracker.get_finger_position(handLms, img)
        gesture = gesture_recognizer.recognize_gesture(handLms, img)
        
        # Get current color (prioritize custom RGB mixer if in use)
        current_color = color_mixer.get_color()
        
        # Handle drawing based on mode
        if finger_pos:
            img = hud.draw_circular_animation(img, finger_pos, radius=25, color=(0, 255, 255))
            img = hud.draw_particles(img, finger_pos, (0, 255, 255), num_particles=3)
            
            if gesture == 'pointing':
                if shape_drawer.current_mode == 'paint':
                    # Freehand drawing
                    if prev_finger_pos and prev_finger_pos != (0, 0):
                        canvas.draw_line(prev_finger_pos, finger_pos, use_glow=True)
                        img = hud.draw_glow_line(img, prev_finger_pos, finger_pos, (0, 255, 255), thickness=5)
                    prev_finger_pos = finger_pos
                    drawing = True
                else:
                    # Shape drawing
                    if not shape_drawer.drawing_shape:
                        shape_drawer.start_shape(finger_pos)
                    else:
                        # Preview shape while dragging
                        img = shape_drawer.preview_shape(img, shape_drawer.start_point, finger_pos, (0, 255, 255), thickness=2)
                    
                    drawing = True
            
            elif gesture == 'pinch':
                canvas.clear()
                shape_drawer.end_shape()
                prev_finger_pos = None
                drawing = False
                sound.play_success()
                if voice:
                    voice.on_clear()
            else:
                # Finalize shape when gesture changes away from pointing
                if shape_drawer.drawing_shape and shape_drawer.start_point and finger_pos:
                    # Apply shape to canvas when gesture changes
                    if shape_drawer.current_mode == 'rect':
                        shape_drawer.draw_rectangle(canvas.canvas, shape_drawer.start_point, finger_pos, current_color, thickness=2, filled=canvas.use_fill)
                    elif shape_drawer.current_mode == 'circle':
                        radius = int(np.sqrt((finger_pos[0] - shape_drawer.start_point[0])**2 + (finger_pos[1] - shape_drawer.start_point[1])**2))
                        shape_drawer.draw_circle(canvas.canvas, shape_drawer.start_point, radius, current_color, thickness=2, filled=canvas.use_fill)
                    elif shape_drawer.current_mode == 'line':
                        shape_drawer.draw_line(canvas.canvas, shape_drawer.start_point, finger_pos, current_color, thickness=2)
                    elif shape_drawer.current_mode == 'triangle':
                        # Calculate third point for triangle
                        mid_x = (shape_drawer.start_point[0] + finger_pos[0]) // 2
                        mid_y = shape_drawer.start_point[1] - (finger_pos[1] - shape_drawer.start_point[1])
                        shape_drawer.draw_triangle(canvas.canvas, shape_drawer.start_point, finger_pos, (mid_x, mid_y), current_color, thickness=2, filled=canvas.use_fill)
                
                shape_drawer.end_shape()
                prev_finger_pos = None
                drawing = False
        else:
            # Hand lost - finalize any ongoing shape
            if shape_drawer.drawing_shape and shape_drawer.start_point:
                # The shape will be finalized when hand reappears with different gesture
                pass
            
            prev_finger_pos = None
            drawing = False
            if shape_drawer.drawing_shape:
                shape_drawer.end_shape()
        
        # Display with HUD
        img = canvas.blend_with_frame(img)
        
        # Process voice commands
        if voice_cmd and voice_cmd.get_last_command():
            last_cmd = voice_cmd.get_last_command()
            voice_cmd.last_command = None  # Reset
            
            parsed = voice_cmd.parse_command(last_cmd)
            
            if parsed['action'] == 'set_color':
                canvas.set_brush_color(parsed['value'])
                sound.play_click()
                print(f"[VOICE] Color changed to: {parsed['value'].upper()}")
                if voice:
                    voice.on_color_change(parsed['value'])
            
            elif parsed['action'] == 'set_shape':
                shape_drawer.set_mode(parsed['value'])
                sound.play_click()
                print(f"[VOICE] Mode changed to: {shape_drawer.get_mode()}")
                if voice:
                    voice.speak(f"Shape changed to {parsed['value']}")
            
            elif parsed['action'] == 'set_theme':
                color_themes.set_theme(parsed['value'])
                sound.play_click()
                print(f"[VOICE] Theme changed to: {color_themes.get_theme_name()}")
                if voice:
                    voice.speak(f"Theme changed to {parsed['value']}")
            
            elif parsed['action'] == 'clear':
                canvas.clear()
                shape_drawer.end_shape()
                prev_finger_pos = None
                sound.play_success()
                print("[VOICE] Canvas cleared")
                if voice:
                    voice.on_clear()
            
            elif parsed['action'] == 'undo':
                canvas.undo()
                sound.play_click()
                print("[VOICE] Undo executed")
                if voice:
                    voice.speak("Undo executed")
            
            elif parsed['action'] == 'redo':
                canvas.redo()
                sound.play_click()
                print("[VOICE] Redo executed")
                if voice:
                    voice.speak("Redo executed")
            
            elif parsed['action'] == 'brush_increase':
                new_size = canvas.increase_brush_size()
                sound.play_click()
                print(f"[VOICE] Brush size increased to {new_size}px")
                if voice:
                    voice.speak(f"Brush size increased to {new_size} pixels")
            
            elif parsed['action'] == 'brush_decrease':
                new_size = canvas.decrease_brush_size()
                sound.play_click()
                print(f"[VOICE] Brush size decreased to {new_size}px")
                if voice:
                    voice.speak(f"Brush size decreased to {new_size} pixels")
            
            elif parsed['action'] == 'toggle_color_picker':
                color_picker.toggle()
                sound.play_click()
                print(f"[VOICE] Color picker: {'OPEN' if color_picker.is_open else 'CLOSED'}")
                if voice:
                    voice.speak(f"Color picker {'opened' if color_picker.is_open else 'closed'}")
            
            elif parsed['action'] == 'opacity_increase':
                new_opacity = canvas.increase_opacity(10)
                sound.play_click()
                print(f"[VOICE] Opacity increased to {new_opacity}%")
                if voice:
                    voice.speak(f"Opacity at {new_opacity} percent")
            
            elif parsed['action'] == 'opacity_decrease':
                new_opacity = canvas.decrease_opacity(10)
                sound.play_click()
                print(f"[VOICE] Opacity decreased to {new_opacity}%")
                if voice:
                    voice.speak(f"Opacity at {new_opacity} percent")
            
            elif parsed['action'] == 'toggle_fill':
                fill_mode = canvas.toggle_fill_mode()
                sound.play_click()
                print(f"[VOICE] Fill mode: {'ON' if fill_mode else 'OFF'}")
                if voice:
                    voice.speak(f"Fill mode turned {'on' if fill_mode else 'off'}")
            
            elif parsed['action'] == 'toggle_grid':
                grid_state = drawing_grid.toggle()
                sound.play_click()
                print(f"[VOICE] Grid: {'ON' if grid_state else 'OFF'}")
                if voice:
                    voice.speak(f"Grid turned {'on' if grid_state else 'off'}")
            
            elif parsed['action'] == 'grid_on':
                drawing_grid.enabled = True
                sound.play_click()
                print("[VOICE] Grid enabled")
                if voice:
                    voice.speak("Grid enabled")
            
            elif parsed['action'] == 'grid_off':
                drawing_grid.enabled = False
                sound.play_click()
                print("[VOICE] Grid disabled")
                if voice:
                    voice.speak("Grid disabled")

            
            elif parsed['action'] == 'toggle_eraser':
                eraser_active = canvas.toggle_eraser()
                sound.play_click()
                print(f"[VOICE] Eraser: {'ON' if eraser_active else 'OFF'}")
                if voice:
                    voice.speak(f"Eraser turned {('on' if eraser_active else 'off')}")
            
            elif parsed['action'] == 'eraser_on':
                canvas.eraser_mode = True
                sound.play_click()
                print("[VOICE] Eraser ON")
                if voice:
                    voice.speak("Eraser activated")
            
            elif parsed['action'] == 'eraser_off':
                canvas.eraser_mode = False
                sound.play_click()
                print("[VOICE] Eraser OFF")
                if voice:
                    voice.speak("Eraser deactivated")
            
            elif parsed['action'] == 'save':
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"drawing_{timestamp}.png"
                cv2.imwrite(filename, canvas.get_canvas())
                sound.play_success()
                print(f"[VOICE] Drawing saved as {filename}")
                if voice:
                    voice.on_save()
        
        # Draw HUD elements
        hud.update_fps()
        
        # Update performance optimizer
        frame_time = time.time() - frame_start_time
        perf_optimizer.update_fps(frame_time)
        frame_start_time = time.time()
        
        img = hud.draw_hud_background(img)
        img = hud.draw_neon_border(img)
        img = hud.draw_status_panel(img, gesture, f"{shape_drawer.get_mode()}", drawing)
        img = hud.draw_shape_selector(img, shape_drawer.current_mode)
        img = hud.draw_rgb_mixer_display(img, color_mixer.r, color_mixer.g, color_mixer.b)
        img = hud.draw_theme_indicator(img, color_themes.get_theme_name())
        
        # Draw canvas statistics
        canvas_stats = canvas.get_canvas_stats()
        img = hud.draw_canvas_stats_display(img, canvas_stats)
        
        # Draw toolbar and brush size indicator
        img = toolbar.draw_toolbar(img, shape_drawer.current_mode, canvas_stats['undo_available'], canvas_stats['redo_available'])
        img = toolbar.draw_brush_size_indicator(img, canvas.brush_thickness, canvas.max_brush)
        
        # Draw color picker if open
        if color_picker.is_open:
            img = color_picker.draw(img)
        
        # Draw grid if enabled
        img = drawing_grid.draw_grid(img)
        
        # Draw performance stats
        perf_stats = perf_optimizer.get_performance_stats()
        img = hud.draw_performance_stats(img, perf_stats)
        
        # Draw voice status
        if voice_cmd:
            img = hud.draw_voice_status(img, voice_cmd.get_status(), x=10, y=450)
        
        img = hud.draw_control_panel(img)
        
        cv2.imshow(window_name, img)
        
        # Keyboard controls
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("System shutting down...")
            if voice:
                voice.speak("System shutting down")
            break
        
        # Shape selection
        elif key == ord('0'):
            shape_drawer.set_mode('paint')
            sound.play_click()
            print("Mode: Paint/Freehand")
        elif key == ord('1'):
            shape_drawer.set_mode('rect')
            sound.play_click()
            print("Mode: Rectangle")
        elif key == ord('2'):
            shape_drawer.set_mode('circle')
            sound.play_click()
            print("Mode: Circle")
        elif key == ord('3'):
            shape_drawer.set_mode('line')
            sound.play_click()
            print("Mode: Line")
        elif key == ord('4'):
            shape_drawer.set_mode('triangle')
            sound.play_click()
            print("Mode: Triangle")
        
        # RGB Mixer controls
        elif key == ord('+') or key == ord('='):  # Plus key
            # Determine which to increase (cycle: R -> G -> B)
            color_mixer.increase_red(5)
        elif key == ord('-') or key == ord('_'):  # Minus key
            color_mixer.decrease_red(5)
        
        # Theme selection
        elif key == ord('d'):
            color_themes.set_theme('dark')
            sound.play_click()
            print(f"Theme: {color_themes.get_theme_name()}")
        elif key == ord('n'):
            color_themes.set_theme('neon')
            sound.play_click()
            print(f"Theme: {color_themes.get_theme_name()}")
        elif key == ord('p'):
            color_themes.set_theme('pastel')
            sound.play_click()
            print(f"Theme: {color_themes.get_theme_name()}")
        elif key == ord('f'):
            color_themes.set_theme('fire')
            sound.play_click()
            print(f"Theme: {color_themes.get_theme_name()}")
        elif key == ord('i'):
            color_themes.set_theme('ice')
            sound.play_click()
            print(f"Theme: {color_themes.get_theme_name()}")
        elif key == ord('o'):
            color_themes.set_theme('ocean')
            sound.play_click()
            print(f"Theme: {color_themes.get_theme_name()}")
        
        # Other tools
        elif key == ord('c'):
            canvas.clear()
            sound.play_alert()
            if voice:
                voice.on_clear()
        elif key == ord('e'):
            eraser_active = canvas.toggle_eraser()
            sound.play_click()
            print(f"Eraser: {'ON' if eraser_active else 'OFF'}")
        elif key == ord('z'):
            canvas.undo()
            sound.play_click()
            print("Undo executed")
        elif key == ord('y'):
            canvas.redo()
            sound.play_click()
            print("Redo executed")
        elif key == ord('['):
            new_size = canvas.decrease_brush_size()
            sound.play_click()
            print(f"Brush size: {new_size}px")
        elif key == ord(']'):
            new_size = canvas.increase_brush_size()
            sound.play_click()
            print(f"Brush size: {new_size}px")
        elif key == ord('k'):
            color_picker.toggle()
            sound.play_click()
            print(f"Color picker: {'OPEN' if color_picker.is_open else 'CLOSED'}")
        elif key == ord(';'):
            new_opacity = canvas.decrease_opacity(5)
            sound.play_click()
            print(f"Opacity: {new_opacity}%")
        elif key == ord("'"):
            new_opacity = canvas.increase_opacity(5)
            sound.play_click()
            print(f"Opacity: {new_opacity}%")
        elif key == ord('v'):
            fill_mode = canvas.toggle_fill_mode()
            sound.play_click()
            print(f"Fill mode: {'ON' if fill_mode else 'OFF'}")
        elif key == ord('g'):
            grid_state = drawing_grid.toggle()
            sound.play_click()
            print(f"Grid: {'ON' if grid_state else 'OFF'}")
        elif key == ord('s'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"drawing_{timestamp}.png"
            cv2.imwrite(filename, canvas.get_canvas())
            sound.play_success()
            print(f"Drawing saved as {filename}")
            if voice:
                voice.on_save()
    
    # Cleanup
    if voice_cmd:
        voice_cmd.stop_listening()
    tracker.release()
    cap.release()
    cv2.destroyAllWindows()
    print("GesturePaint system offline")


if __name__ == "__main__":
    main()

