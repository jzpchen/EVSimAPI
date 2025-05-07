from PIL import Image
import os

class ElectronMagnifier:
    def __init__(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        self.image = Image.open(image_path).convert('RGB')
        self.img_width, self.img_height = self.image.size
        self.survey_x = 0
        self.survey_y = 0
        self.survey_size = 1000  # 1000x1000 pixel area for coarse survey
        self.detail_grid = 10    # 10x10 grid for detail view
        self.detail_size = 100   # Each detail cell is 100x100 pixels

    def set_survey_area(self, x, y):
        # Clamp the survey area to stay within image boundaries
        x = max(0, min(x, self.img_width - self.survey_size))
        y = max(0, min(y, self.img_height - self.survey_size))
        self.survey_x = x
        self.survey_y = y

    def get_survey_view(self):
        # Crop the 1000x1000 area and resize to 100x100
        box = (
            self.survey_x,
            self.survey_y,
            self.survey_x + self.survey_size,
            self.survey_y + self.survey_size
        )
        cropped = self.image.crop(box)
        coarse_view = cropped.resize((100, 100), Image.LANCZOS)
        return coarse_view

    def get_detail_view(self, index):
        if not (0 <= index < self.detail_grid * self.detail_grid):
            raise ValueError(f"Detail index must be between 0 and {self.detail_grid * self.detail_grid - 1}")
        row = index // self.detail_grid
        col = index % self.detail_grid
        x0 = self.survey_x + col * self.detail_size
        y0 = self.survey_y + row * self.detail_size
        box = (
            x0,
            y0,
            x0 + self.detail_size,
            y0 + self.detail_size
        )
        detail_view = self.image.crop(box)
        return detail_view
