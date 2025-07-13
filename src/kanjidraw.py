#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import math


class KanjiDrawApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KanjiDraw")
        self.root.configure(bg='black')
        
        # Store strokes as separate paths
        self.strokes = []
        self.current_stroke = []
        self.is_drawing = False
        
        # Set up the main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create canvas frame
        self.canvas_frame = tk.Frame(self.main_frame, bg='black')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create canvas with white square
        self.canvas_size = 400  # Initial size
        self.canvas = tk.Canvas(
            self.canvas_frame,
            bg='white',
            width=self.canvas_size,
            height=self.canvas_size,
            highlightthickness=0
        )
        self.canvas.pack(expand=True)
        
        # Draw guide lines
        self.draw_guide_lines()
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        # Create button frame
        self.button_frame = tk.Frame(self.main_frame, bg='black')
        self.button_frame.pack(side=tk.BOTTOM, pady=10)
        
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
        
        # Bind window resize event
        self.canvas_frame.bind("<Configure>", self.on_resize)
        
    def draw_guide_lines(self):
        """Draw horizontal and vertical dashed lines across the center"""
        center = self.canvas_size / 2
        
        # Horizontal line
        self.canvas.create_line(
            0, center, self.canvas_size, center,
            fill='#CCCCCC',
            width=1,
            dash=(5, 5),
            tags='guide'
        )
        
        # Vertical line
        self.canvas.create_line(
            center, 0, center, self.canvas_size,
            fill='#CCCCCC',
            width=1,
            dash=(5, 5),
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
                    fill='black',
                    width=3,
                    capstyle=tk.ROUND,
                    joinstyle=tk.ROUND,
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
                    fill='black',
                    width=3,
                    capstyle=tk.ROUND,
                    joinstyle=tk.ROUND,
                    tags='stroke'
                )
    
    def on_resize(self, event):
        """Handle window resize to maintain square canvas"""
        # Get the smaller dimension to maintain square aspect ratio
        new_size = min(event.width - 40, event.height - 40)  # 40 for padding
        
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
    root = tk.Tk()
    root.geometry("600x650")  # Initial window size
    root.minsize(300, 350)    # Minimum window size
    
    app = KanjiDrawApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()