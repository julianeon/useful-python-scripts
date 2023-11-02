# Useful Python Scripts

![example gif](output.gif)

Example gif created by make_gif.py.

To use these scripts, imagemagick must be installed.

## make_gif_images.py

This script generates the images for a gif using imagemagick.

The text to be used, and the filenames used for output, are coded into the script.

It doesn't create a gif in case you want to add a custom image or change the ordering before gif creation.

Run it like this:

python make_gif_images.py

## make_gif.py

This script generates a complete gif using imagemagick. 

It is very similar to make_gif_images.py, with an extra line at the end to create a gif from those images.

The text to be used, and the filenames used for output, are coded into the script.

Run it like this:

python make_gif.py

## annotate_image.py

![annotated image](linux.png)

This script annotates an image with text at the bottom using imagemagick.

If you have a screenshot for example, you can use it to add a quick description.

As written, the script will append a small caption at the bottom of the image, using the text you enter, in black text centered on a white background.

Run it like this, for an example input of input.png and output of output.png:

python annotate.py input.png output.png "Linus Torvalds created Linux."
