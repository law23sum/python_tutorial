"""Add a border to any image."""

import image_functions as img_fns
from cli import process_cli_args

# Process image.
path, options = process_cli_args()
img = img_fns.load_image(path)
new_img = img_fns.process_image(img, options)
img_fns.save_image(path, new_img)
