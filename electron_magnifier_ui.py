import streamlit as st
from electron_magnifier import ElectronMagnifier
from PIL import Image, ImageDraw
import os
import glob

SPECIMEN_DIR = "specimen"

# Find the first image in the specimen folder
def get_specimen_image_path():
    for ext in ('*.png', '*.jpg', '*.jpeg'):
        files = glob.glob(os.path.join(SPECIMEN_DIR, ext))
        if files:
            return files[0]
    return None

def draw_draggable_box(image, box_x, box_y, box_size, display_width):
    # Draw a rectangle on the resized image for the draggable box
    img_width, img_height = image.size
    scale = display_width / img_width
    display_height = int(img_height * scale)
    resized = image.resize((display_width, display_height), Image.LANCZOS)
    draw = ImageDraw.Draw(resized)
    # Scale box coordinates
    x0 = int(box_x * scale)
    y0 = int(box_y * scale)
    x1 = int((box_x + box_size) * scale)
    y1 = int((box_y + box_size) * scale)
    draw.rectangle([x0, y0, x1, y1], outline="red", width=3)
    return resized, scale

def draw_grid(image, grid_size=10):
    # Draw a 10x10 grid over the image
    draw = ImageDraw.Draw(image)
    w, h = image.size
    for i in range(1, grid_size):
        # Vertical lines
        x = i * w // grid_size
        draw.line([(x, 0), (x, h)], fill="gray", width=1)
        # Horizontal lines
        y = i * h // grid_size
        draw.line([(0, y), (w, y)], fill="gray", width=1)
    return image

# Streamlit UI
st.set_page_config(page_title="Electron Magnifier Simulator", layout="wide")
st.title("Electron Magnifier Simulator")

specimen_path = get_specimen_image_path()
if not specimen_path:
    st.warning(f"Please add a .png or .jpg image under ./{SPECIMEN_DIR}/ to begin.")
    st.stop()

em = ElectronMagnifier(specimen_path)
img_width, img_height = em.img_width, em.img_height

# No need for display_width; use original image width for overlays

# Draggable box state (simulate with sliders for now)
max_x = max(0, img_width - em.survey_size)
max_y = max(0, img_height - em.survey_size)
col1, col2 = st.columns(2)
with col1:
    box_x = st.slider("Survey Box X", min_value=0, max_value=max_x, value=0, step=1)
with col2:
    box_y = st.slider("Survey Box Y", min_value=0, max_value=max_y, value=0, step=1)
em.set_survey_area(box_x, box_y)

# Show image with box overlay
image_with_box, scale = draw_draggable_box(em.image, box_x, box_y, em.survey_size, img_width)
st.image(image_with_box, use_container_width=True)

# Survey and detail views
survey_view = em.get_coarse_survey_view()
survey_view_with_grid = draw_grid(survey_view.copy(), em.detail_grid)

# Select detail index using grid (simulate with two sliders for now)
st.subheader("Survey and Detail Views")
grid_row, grid_col = st.columns(2)
with grid_row:
    sel_row = st.slider("Grid Row", min_value=0, max_value=em.detail_grid-1, value=0)
with grid_col:
    sel_col = st.slider("Grid Col", min_value=0, max_value=em.detail_grid-1, value=0)
detail_index = sel_row * em.detail_grid + sel_col
detail_view = em.get_detail_view(detail_index)

# Highlight selected grid cell on survey view
grid_draw = ImageDraw.Draw(survey_view_with_grid)
cell_size = survey_view_with_grid.size[0] // em.detail_grid
x0 = sel_col * cell_size
y0 = sel_row * cell_size
x1 = x0 + cell_size
y1 = y0 + cell_size
grid_draw.rectangle([x0, y0, x1, y1], outline="yellow", width=2)

# Show survey and detail views
col_survey, col_detail = st.columns(2)
with col_survey:
    st.image(survey_view_with_grid, caption="Survey View (100x100, 10x10 grid)", width=150)
with col_detail:
    st.image(detail_view, caption=f"Detail View (Cell {detail_index})", width=150)

st.markdown("""
**Instructions:**
1. Place a .png or .jpg image under the `./specimen` folder.
2. Adjust the survey box position using the sliders.
3. Select a grid cell in the survey view using the row/col sliders to see the detail view.
""")
