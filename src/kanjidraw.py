#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import math


class KanjiDrawApp:
    def __init__(self, root, debug_mode=False):
        self.root = root
        self.debug_mode = debug_mode
        self.root.title("KanjiDraw" + (" - Debug Mode" if debug_mode else ""))
        self.root.configure(bg='black')
        
        # Store strokes as separate paths
        self.strokes = []
        self.current_stroke = []
        self.is_drawing = False
        self.stroke_thickness = 6  # Default thickness
        
        # Set up the main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas frame
        self.canvas_frame = tk.Frame(self.main_frame, bg='black')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create a container to center buttons and canvas together
        self.drawing_container = tk.Frame(self.canvas_frame, bg='black')
        self.drawing_container.pack(expand=True)
        
        # Create button frame at the top of the container
        self.button_frame = tk.Frame(self.drawing_container, bg='black')
        self.button_frame.pack(side=tk.TOP, pady=(0, 5))
        
        # Create canvas with black background
        self.base_resolution = 400  # Base resolution
        if self.debug_mode:
            self.resolution_scale = 16  # Default scale (6400 = 400 * 16)
            self.canvas_size = self.base_resolution * self.resolution_scale
        else:
            self.resolution_scale = 2  # Fixed scale for non-debug mode
            self.canvas_size = 800  # Fixed high resolution when not debugging
        self.canvas = tk.Canvas(
            self.drawing_container,
            bg='black',
            width=self.canvas_size,
            height=self.canvas_size,
            highlightthickness=2,
            highlightbackground='white',
            highlightcolor='white',
            bd=0
        )
        self.canvas.pack(side=tk.TOP)
        
        # Draw guide lines
        self.draw_guide_lines()
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        
        # Style for buttons
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('KanjiButton.TButton',
                       background='#333333',
                       foreground='white',
                       bordercolor='#555555',
                       focuscolor='none',
                       borderwidth=1)
        style.map('KanjiButton.TButton',
                 background=[('active', '#555555')])
        
        # Create buttons
        self.undo_button = ttk.Button(
            self.button_frame,
            text="Undo Stroke",
            command=self.undo_stroke,
            style='KanjiButton.TButton'
        )
        self.undo_button.pack(side=tk.LEFT, padx=5)
        
        self.clear_button = ttk.Button(
            self.button_frame,
            text="Clear All",
            command=self.clear_all,
            style='KanjiButton.TButton'
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Initialize debug controls placeholder
        self.control_frame = None
        
        # Bind window resize event
        self.canvas_frame.bind("<Configure>", self.on_resize)
        
    def draw_guide_lines(self):
        """Draw horizontal and vertical dashed lines across the center"""
        center = self.canvas_size / 2
        
        # Horizontal line
        self.canvas.create_line(
            0, center, self.canvas_size, center,
            fill='#666666',
            width=1,
            dash=(10, 10),
            tags='guide'
        )
        
        # Vertical line
        self.canvas.create_line(
            center, 0, center, self.canvas_size,
            fill='#666666',
            width=1,
            dash=(10, 10),
            tags='guide'
        )
    
    def start_drawing(self, event):
        """Start a new stroke"""
        self.is_drawing = True
        self.current_stroke = [(event.x, event.y)]
    
    def draw(self, event):
        """Continue drawing the current stroke"""
        if self.is_drawing and self.current_stroke:
            x, y = event.x, event.y
            self.current_stroke.append((x, y))
            
            # Draw line segment
            if len(self.current_stroke) > 1:
                prev_x, prev_y = self.current_stroke[-2]
                self.canvas.create_line(
                    prev_x, prev_y, x, y,
                    fill='white',
                    width=self.stroke_thickness,
                    capstyle=tk.ROUND,
                    joinstyle=tk.ROUND,
                    smooth=tk.TRUE,
                    tags='stroke'
                )
    
    def stop_drawing(self, event):
        """Finish the current stroke"""
        if self.is_drawing and self.current_stroke:
            self.strokes.append(self.current_stroke)
            self.current_stroke = []
        self.is_drawing = False
    
    def undo_stroke(self):
        """Remove the last stroke"""
        if self.strokes:
            self.strokes.pop()
            self.redraw_canvas()
    
    def clear_all(self):
        """Clear all strokes"""
        self.strokes = []
        self.current_stroke = []
        self.redraw_canvas()
    
    def redraw_canvas(self):
        """Redraw the entire canvas"""
        # Clear all strokes but keep guide lines
        self.canvas.delete('stroke')
        
        # Redraw all strokes
        for stroke in self.strokes:
            for i in range(1, len(stroke)):
                x1, y1 = stroke[i-1]
                x2, y2 = stroke[i]
                self.canvas.create_line(
                    x1, y1, x2, y2,
                    fill='white',
                    width=self.stroke_thickness,
                    capstyle=tk.ROUND,
                    joinstyle=tk.ROUND,
                    smooth=tk.TRUE,
                    tags='stroke'
                )
    
    def update_resolution(self, value):
        """Update canvas resolution while maintaining visual appearance"""
        if not self.debug_mode:
            return
            
        old_canvas_size = self.canvas_size
        self.resolution_scale = int(value)
        new_canvas_size = self.base_resolution * self.resolution_scale
        
        # Scale existing strokes to maintain their visual position
        if old_canvas_size != new_canvas_size and old_canvas_size > 0:
            scale_factor = new_canvas_size / old_canvas_size
            scaled_strokes = []
            for stroke in self.strokes:
                scaled_stroke = [(x * scale_factor, y * scale_factor) for x, y in stroke]
                scaled_strokes.append(scaled_stroke)
            self.strokes = scaled_strokes
        
        # Update canvas size
        self.canvas_size = new_canvas_size
        self.canvas.config(width=self.canvas_size, height=self.canvas_size)
        
        # Redraw everything
        self.canvas.delete('all')
        self.draw_guide_lines()
        self.redraw_canvas()
    
    def update_thickness(self, value):
        """Update stroke thickness"""
        if not self.debug_mode:
            return
            
        self.stroke_thickness = int(value)
        
        # Redraw all strokes with new thickness
        self.redraw_canvas()
    
    def create_debug_controls(self):
        """Create debug controls at the bottom"""
        # Create control frame directly in root window
        self.control_frame = tk.Frame(self.root, bg='#333333', height=80)
        self.control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)
        self.control_frame.pack_propagate(False)  # Don't shrink to content
        
        # Debug label
        debug_label = tk.Label(
            self.control_frame,
            text="DEBUG CONTROLS",
            fg='white',
            bg='#333333',
            font=('Arial', 9, 'bold')
        )
        debug_label.pack(side=tk.TOP, pady=2)
        
        # Create a sub-frame for sliders
        slider_frame = tk.Frame(self.control_frame, bg='#333333')
        slider_frame.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
        
        # Resolution slider
        self.res_scale = tk.Scale(
            slider_frame,
            from_=1,
            to=32,
            orient=tk.HORIZONTAL,
            command=self.update_resolution,
            bg='#555555',
            fg='white',
            troughcolor='#777777',
            highlightbackground='#333333',
            length=200,
            label="Resolution",
            font=('Arial', 8)
        )
        self.res_scale.set(self.resolution_scale)
        self.res_scale.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Thickness slider
        self.thick_scale = tk.Scale(
            slider_frame,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            command=self.update_thickness,
            bg='#555555',
            fg='white',
            troughcolor='#777777',
            highlightbackground='#333333',
            length=200,
            label="Thickness",
            font=('Arial', 8)
        )
        self.thick_scale.set(self.stroke_thickness)
        self.thick_scale.pack(side=tk.LEFT, padx=20, pady=5)
        
        # Force immediate visibility
        self.control_frame.update_idletasks()
        self.root.update_idletasks()
    
    def on_resize(self, event):
        """Handle window resize to maintain square canvas"""
        # Skip if this is not the canvas frame
        if event.widget != self.canvas_frame:
            return
            
        # Get the smaller dimension to maintain square aspect ratio
        # Account for debug controls if present
        height_adjustment = 120 if self.debug_mode else 40
        new_size = min(event.width - 40, event.height - height_adjustment)
        
        # Only resize if size changed significantly
        if abs(new_size - self.canvas_size) > 10 and new_size > 100:
            # Calculate scale factor
            scale_factor = new_size / self.canvas_size
            
            # Update canvas size
            self.canvas_size = new_size
            self.canvas.config(width=new_size, height=new_size)
            
            # Scale all strokes
            scaled_strokes = []
            for stroke in self.strokes:
                scaled_stroke = [(x * scale_factor, y * scale_factor) for x, y in stroke]
                scaled_strokes.append(scaled_stroke)
            self.strokes = scaled_strokes
            
            # Clear and redraw everything
            self.canvas.delete('all')
            self.draw_guide_lines()
            self.redraw_canvas()


def main():
    import sys
    debug_mode = "--debug" in sys.argv
    
    root = tk.Tk()
    if debug_mode:
        root.geometry("800x850")  # Extra space for debug controls
        root.minsize(600, 720)    # Higher minimum to prevent clipping
    else:
        root.geometry("600x650")  # Standard window size
        root.minsize(300, 350)
    
    app = KanjiDrawApp(root, debug_mode)
    
    # Create debug controls immediately if in debug mode
    if debug_mode:
        # Create controls immediately
        app.create_debug_controls()
        # Force window update
        root.update_idletasks()
        root.update()
    
    root.mainloop()


if __name__ == "__main__":
    main()