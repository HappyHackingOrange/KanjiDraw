# KanjiDraw

A simple, elegant kanji drawing practice application for Ubuntu. Draw Japanese characters with a smooth, antialiased brush on a traditional black drawing surface.

## Features

- Smooth, antialiased stroke rendering
- Keyboard shortcuts (Q: undo, E: clear)
- Centered guide lines for proper character alignment
- Minimalist interface focused on practice
- Debug mode with adjustable stroke thickness
- Scalable window with maintained aspect ratio

## Requirements

- Python 3.12+
- Tkinter (install with: `sudo apt-get install python3-tk`)

## Installation

```bash
# Clone the repository
git clone https://github.com/HappyHackingOrange/KanjiDraw.git
cd KanjiDraw

# Install system dependency
sudo apt-get install python3-tk
```

## Usage

```bash
# Run the application
python3 src/kanjidraw.py

# Run with debug controls (thickness slider, antialiasing toggle)
python3 src/kanjidraw.py --debug
```

## Controls

- **Draw**: Click and drag with mouse
- **Q**: Undo last stroke  
- **E**: Clear all strokes
- **Window resize**: Canvas scales proportionally

## Debug Mode Features

When running with `--debug` flag:
- **Thickness Slider**: Adjust stroke thickness (1-30)
- **Antialiasing Toggle**: Enable/disable smooth edges
- **Fast Drawing Toggle**: Performance mode for slower systems

## Screenshots

![KanjiDraw Interface](screenshots/main.png)
*Simple, distraction-free drawing interface*

## Technical Details

- Built with Python's Tkinter for simplicity and no external dependencies
- Multi-layer antialiasing system for smooth strokes
- Optimized rendering with separate drawing and display modes
- Stroke-based undo system

## License

MIT License - feel free to use and modify!

## Contributing

Contributions are welcome! Feel free to submit issues and pull requests.

---

Perfect for practicing kanji, hiragana, katakana, or any freehand drawing!