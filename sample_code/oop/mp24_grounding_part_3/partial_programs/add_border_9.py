"""Add a border to any image."""

import image_functions as img_fns
from cli import process_cli_args

# Set default options.
options = {
    'border_width': 2,
    'padding': 0,
    'border_color': 'lightgray'
}

# Process image.
path = process_cli_args(options)
img = img_fns.load_image(path)
new_img = img_fns.process_image(img, options)
img_fns.save_image(path, new_img)
