# Electron Magnifier Simulator

A Python-based simulator for exploring high-resolution specimen images as if using an electron magnifier. This tool provides both a coarse survey and a detail view, allowing interactive exploration of large images (e.g., 4K microscopy specimens).

## Features

- **Load Specimen Image:** Supports `.png`, `.jpg`, and `.jpeg` images. Place your image in the `./specimen` directory.
- **Coarse Survey View:** Select a 1000x1000 pixel region of the specimen, rendered as a 100x100 pixel overview (10x compression per axis).
- **Draggable Survey Box:** Move the survey area with sliders (simulating a draggable box overlay).
- **Detail View:** The survey area is divided into a 10x10 grid. Select any grid cell to view a 100x100 pixel detail at full resolution.
- **Interactive UI:** Built with Streamlit for easy, web-based interaction. The main specimen image fills the browser window width for optimal viewing.

## Usage

### 1. Prerequisites
- Python 3.8+
- [Streamlit](https://streamlit.io/) and [Pillow](https://python-pillow.org/)

### 2. Installation

It's recommended to use a virtual environment:

```sh
python3 -m venv venv
source venv/bin/activate
pip install streamlit pillow
```

### 3. Add Your Specimen

- Place a `.png`, `.jpg`, or `.jpeg` image file in the `./specimen` directory (create it if it doesn't exist).

### 4. Run the Simulator

```sh
streamlit run electron_magnifier_ui.py
```

- Open the provided local URL (usually http://localhost:8501) in your browser.

## How It Works

1. **Specimen Image Display:** The top of the UI shows the entire specimen image, scaled to the browser window width. A red box overlays the selected 1000x1000 survey area.
2. **Survey Area Selection:** Move the survey box using the X and Y sliders below the image.
3. **Survey and Detail Views:**
   - The left 100x100 box shows the coarse survey area with a 10x10 grid overlay.
   - Use the row/column sliders to select a grid cell. The right 100x100 box displays the detail view of the selected cell.

## File Structure

```
/SimAPI
├── electron_magnifier.py         # Core logic for magnifier
├── electron_magnifier_ui.py      # Streamlit UI
├── specimen/                     # Place your specimen images here
│   └── your_image.png
└── README.md                     # This documentation
```

## Customization
- You can easily extend the UI for true mouse dragging, saving views, or additional image analysis.
- The code is modular and easy to adapt for more advanced microscopy simulation scenarios.

## Troubleshooting
- If you see a warning about missing images, ensure your image is in the `specimen` folder and is `.png`, `.jpg`, or `.jpeg`.
- If Streamlit does not start, ensure you are in your virtual environment and all dependencies are installed.
- For large images, performance is optimized using Pillow's efficient image processing.

## License
This project is provided for educational and research purposes. Feel free to adapt and extend for your own microscopy or simulation needs.
