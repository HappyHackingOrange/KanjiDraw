# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

KanjiDraw is a Python 3.12 project currently in initial setup phase. The project uses a virtual environment located at `.venv/`.

## Development Environment

- **Python Version**: 3.12.11
- **Virtual Environment**: `.venv/` (already created)
- **IDE**: PyCharm/IntelliJ IDEA (configuration in `.idea/`)

## Project Status

As of the last update, this is an empty Python project template. When development begins, this file should be updated with:

1. Build and installation commands
2. Test execution commands
3. Linting and code quality commands
4. High-level architecture description
5. Key module and component relationships

## Setup Commands

To activate the virtual environment:
```bash
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate  # On Windows
```

## Running the Application

To run KanjiDraw:
```bash
python src/kanjidraw.py
```

## Architecture Overview

KanjiDraw is a simple Tkinter-based drawing application with the following structure:

- **src/kanjidraw.py**: Main application file containing the KanjiDrawApp class
  - Canvas with white background for drawing
  - Black window background with responsive sizing
  - Stroke-based drawing system (each stroke stored separately for undo functionality)
  - Guide lines (horizontal and vertical dashed lines)
  - Button controls for undo and clear operations

## Key Features

- Scalable window that maintains square canvas aspect ratio
- Stroke-based drawing with smooth lines
- Undo last stroke functionality
- Clear all strokes functionality
- No external dependencies (uses only Python standard library)