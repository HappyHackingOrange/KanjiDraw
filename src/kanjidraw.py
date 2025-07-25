#!/usr/bin/env python3
import tkinter as tk


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
        self.stroke_thickness = 15  # Default thickness
        
        # Set up the main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(fill='both', expand=True)
        
        # Create canvas frame
        self.canvas_frame = tk.Frame(self.main_frame, bg='black')
        self.canvas_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create canvas with black background
        self.canvas_size = 800  # Fixed size for good balance
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg='black',
            width=self.canvas_size,
            height=self.canvas_size,
            highlightthickness=2,
            highlightbackground='white',
            highlightcolor='white',
            bd=0
        )
        self.canvas.pack(expand=True)
        
        # Draw guidelines
        self.draw_guide_lines()
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        # Bind keyboard shortcuts
        self.root.bind("q", lambda e: self.undo_stroke())
        self.root.bind("Q", lambda e: self.undo_stroke())
        self.root.bind("e", lambda e: self.clear_all())
        self.root.bind("E", lambda e: self.clear_all())
        
        # Enable antialiasing by adding multiple stroke layers
        self.enable_antialiasing = True
        self.drawing_performance_mode = True  # Use simpler rendering while drawing
        
        # Initialize debug controls placeholder
        self.control_frame = None
        self.thick_scale = None
        self.aa_var = None
        self.aa_checkbox = None
        self.perf_var = None
        self.perf_checkbox = None
        
        # Bind window resize event
        self.canvas_frame.bind("<Configure>", self.on_resize)
        
    def draw_guide_lines(self):
        """Draw horizontal and vertical dashed lines that cross at center"""
        center = self.canvas_size / 2
        
        # Draw horizontal line in two segments from center outward
        self.canvas.create_line(
            center, center, self.canvas_size, center,
            fill='#666666',
            width=1,
            dash=(10, 10),
            tags='guide'
        )
        self.canvas.create_line(
            center, center, 0, center,
            fill='#666666',
            width=1,
            dash=(10, 10),
            tags='guide'
        )
        
        # Draw vertical line in two segments from center outward
        self.canvas.create_line(
            center, center, center, self.canvas_size,
            fill='#666666',
            width=1,
            dash=(10, 10),
            tags='guide'
        )
        self.canvas.create_line(
            center, center, center, 0,
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
            
            # Only add point if it moved enough to reduce lag
            if self.current_stroke:
                last_x, last_y = self.current_stroke[-1]
                distance = ((x - last_x) ** 2 + (y - last_y) ** 2) ** 0.5
                if distance < 3:  # Skip if moved less than 3 pixels
                    return
            
            self.current_stroke.append((x, y))
            
            # Use simple line drawing while drawing for better performance
            if len(self.current_stroke) >= 2:
                prev_x, prev_y = self.current_stroke[-2]
                if self.drawing_performance_mode:
                    # Simple single-line drawing while moving mouse
                    self.canvas.create_line(
                        prev_x, prev_y, x, y,
                        fill='white',
                        width=self.stroke_thickness,
                        capstyle='round',
                        joinstyle='round',
                        smooth=True,
                        tags='temp_stroke'
                    )
                else:
                    # Full antialiased rendering
                    self.canvas.delete('temp_stroke')
                    self.draw_stroke_path(self.current_stroke, 'temp_stroke')
    
    def stop_drawing(self, _event):
        """Finish the current stroke"""
        if self.is_drawing and self.current_stroke:
            # Convert temporary stroke to permanent stroke
            self.canvas.delete('temp_stroke')
            self.strokes.append(self.current_stroke)
            
            # If antialiasing is enabled, redraw everything to prevent borders between strokes
            if self.enable_antialiasing:
                self.redraw_canvas()
            else:
                # Draw the final stroke as permanent (no need to redraw everything)
                self.draw_stroke_path(self.current_stroke, 'stroke')
            
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
        # Clear all strokes but keep guidelines
        self.canvas.delete('stroke')
        
        # Redraw guidelines to ensure they're always centered
        self.canvas.delete('guide')
        self.draw_guide_lines()
        
        if self.enable_antialiasing:
            # Draw all strokes in layers to avoid borders between strokes
            # Use more layers for smoother antialiasing
            
            # First pass: Outermost edge (very light gray)
            for stroke in self.strokes:
                if len(stroke) >= 2:
                    self.draw_stroke_layer(stroke, self.stroke_thickness + 4, '#AAAAAA', 'stroke')
            
            # Second pass: Outer edge (light gray)
            for stroke in self.strokes:
                if len(stroke) >= 2:
                    self.draw_stroke_layer(stroke, self.stroke_thickness + 3, '#BBBBBB', 'stroke')
            
            # Third pass: Mid-outer edge
            for stroke in self.strokes:
                if len(stroke) >= 2:
                    self.draw_stroke_layer(stroke, self.stroke_thickness + 2, '#CCCCCC', 'stroke')
            
            # Fourth pass: Inner edge
            for stroke in self.strokes:
                if len(stroke) >= 2:
                    self.draw_stroke_layer(stroke, self.stroke_thickness + 1, '#DDDDDD', 'stroke')
            
            # Fifth pass: White core
            for stroke in self.strokes:
                if len(stroke) >= 2:
                    self.draw_stroke_layer(stroke, self.stroke_thickness, 'white', 'stroke')
        else:
            # Standard drawing without antialiasing
            for stroke in self.strokes:
                if len(stroke) >= 2:
                    self.draw_stroke_layer(stroke, self.stroke_thickness, 'white', 'stroke')
    
    def draw_stroke_layer(self, stroke_points, width, color, tag):
        """Draw a single layer of a stroke with specified width and color"""
        if len(stroke_points) < 2:
            return
            
        # Convert points to flat list for tkinter
        points = []
        for x, y in stroke_points:
            points.extend([x, y])
        
        self.canvas.create_line(
            points,
            fill=color,
            width=width,
            capstyle='round',
            joinstyle='round',
            smooth=True,
            splinesteps=48,
            tags=tag
        )
    
    def draw_stroke_path(self, stroke_points, tag):
        """Draw an entire stroke as a smooth path with antialiasing"""
        if len(stroke_points) < 2:
            return
            
        # Convert points to flat list for tkinter
        points = []
        for x, y in stroke_points:
            points.extend([x, y])
        
        # Use fewer spline steps for temp strokes to improve performance
        steps = 24 if tag == 'temp_stroke' else 48
        
        if self.enable_antialiasing:
            # Draw layers from largest to smallest for proper antialiasing
            # Outer edge (light gray)
            self.canvas.create_line(
                points,
                fill='#888888',
                width=self.stroke_thickness + 2,
                capstyle='round',
                joinstyle='round',
                smooth=True,
                splinesteps=steps,
                tags=tag
            )
            
            # Inner edge (very light gray)
            self.canvas.create_line(
                points,
                fill='#CCCCCC',
                width=self.stroke_thickness + 1,
                capstyle='round',
                joinstyle='round',
                smooth=True,
                splinesteps=steps,
                tags=tag
            )
            
            # Core layer (white)
            self.canvas.create_line(
                points,
                fill='white',
                width=self.stroke_thickness,
                capstyle='round',
                joinstyle='round',
                smooth=True,
                splinesteps=steps,
                tags=tag
            )
        else:
            # Standard drawing without antialiasing
            self.canvas.create_line(
                points,
                fill='white',
                width=self.stroke_thickness,
                capstyle='round',
                joinstyle='round',
                smooth=True,
                splinesteps=steps,
                tags=tag
            )
    
    def draw_antialiased_line(self, x1, y1, x2, y2):
        """Draw a line with simulated antialiasing using multiple layers"""
        if self.enable_antialiasing:
            # Draw layers from largest to smallest (background to foreground)
            # This ensures the white core is on top
            
            # Outer edge (light gray) - drawn first (background)
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill='#888888',
                width=self.stroke_thickness + 2,
                capstyle='round',
                joinstyle='round',
                smooth=True,
                tags='stroke'
            )
            
            # Inner edge (very light gray) - drawn second
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill='#CCCCCC',
                width=self.stroke_thickness + 1,
                capstyle='round',
                joinstyle='round',
                smooth=True,
                tags='stroke'
            )
            
            # Core layer (white) - drawn last (foreground)
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill='white',
                width=self.stroke_thickness,
                capstyle='round',
                joinstyle='round',
                smooth=True,
                tags='stroke'
            )
        else:
            # Standard drawing without antialiasing
            self.canvas.create_line(
                x1, y1, x2, y2,
                fill='white',
                width=self.stroke_thickness,
                capstyle='round',
                joinstyle='round',
                smooth=True,
                tags='stroke'
            )
    
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
        self.control_frame.pack(side='bottom', fill='x', padx=10, pady=5)
        self.control_frame.pack_propagate(False)  # Don't shrink to content
        
        # Debug label
        debug_label = tk.Label(
            self.control_frame,
            text="DEBUG CONTROLS",
            fg='white',
            bg='#333333',
            font=('Arial', 9, 'bold')
        )
        debug_label.pack(side='top', pady=2)
        
        # Create a sub-frame for controls
        control_frame = tk.Frame(self.control_frame, bg='#333333')
        control_frame.pack(side='top', expand=True, fill='both')
        
        # Thickness slider
        self.thick_scale = tk.Scale(
            control_frame,
            from_=1,
            to=30,
            orient='horizontal',
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
        self.thick_scale.pack(side='left', padx=20, pady=5)
        
        # Antialiasing toggle
        self.aa_var = tk.BooleanVar(value=self.enable_antialiasing)
        self.aa_checkbox = tk.Checkbutton(
            control_frame,
            text="Antialiasing",
            variable=self.aa_var,
            command=self.toggle_antialiasing,
            fg='white',
            bg='#333333',
            selectcolor='#555555',
            activebackground='#444444',
            activeforeground='white',
            font=('Arial', 8)
        )
        self.aa_checkbox.pack(side='left', padx=10, pady=5)
        
        # Performance mode toggle
        self.perf_var = tk.BooleanVar(value=self.drawing_performance_mode)
        self.perf_checkbox = tk.Checkbutton(
            control_frame,
            text="Fast Drawing",
            variable=self.perf_var,
            command=self.toggle_performance_mode,
            fg='white',
            bg='#333333',
            selectcolor='#555555',
            activebackground='#444444',
            activeforeground='white',
            font=('Arial', 8)
        )
        self.perf_checkbox.pack(side='left', padx=10, pady=5)
        
        # Force immediate visibility
        self.control_frame.update_idletasks()
        self.root.update_idletasks()
    
    def toggle_antialiasing(self):
        """Toggle antialiasing on/off"""
        self.enable_antialiasing = self.aa_var.get()
        self.redraw_canvas()
    
    def toggle_performance_mode(self):
        """Toggle performance mode for drawing"""
        self.drawing_performance_mode = self.perf_var.get()
    
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