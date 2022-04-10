#!/usr/bin/env python3

import PIL.Image
from PIL import ImageOps
import os

from pathlib import Path
from string import Template


ASCII_CHARS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', ' ']

def resize_image(image, new_width):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image


def make_grayscale(image):

    # grayscaled = image.convert('L')
    grayscaled = ImageOps.grayscale(image)
    return grayscaled


def make_ascii(image):
    pixels = image.getdata()
    characters = ''.join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return characters


def main(width, input_path, output_path, letter_padding):
    image = PIL.Image.open(input_path)
    new_sized = resize_image(image, width)
    new_grayscale = make_grayscale(new_sized)
    raw_ascii = make_ascii(new_grayscale)
    the_ascii = ''
    for indx, i in enumerate(raw_ascii):
        if indx % width == 0:
            the_ascii += "\n"
        the_ascii += i
        for pad in range(0, letter_padding):
            the_ascii += " "
    return the_ascii

if __name__ == '__main__':

    pages = [
        {
            "id": "chrome",
            "template": 'template_chrome.html',
            "count": 17,
            "width": 28,
            "input_dir": "../../_assets/frames/pngs-v2",
            "output_dir": "../../site/frames-chrome",
            "letter_padding": 1,
        },

        {
            "id": "safari",
            "template": 'template_safari.html',
            "count": 9,
            "width": 28,
            "input_dir": "../../_assets/frames/pngs-v2-only-half",
            "output_dir": "../../site/frames",
            "letter_padding": 1,
        }
    ]

    for page in pages:
        # print(page['id'])
        with open(page['template']) as _template:
            frame = Template(_template.read())
            for i in range(1, page['count']):
                next_frame = i + 1
                if next_frame == page['count']:
                    next_frame = 1
                input_path = f"{page['input_dir']}/{i}.png"
                output_path = f"{page['output_dir']}/{i}.html"
                output_ascii = main(page['width'], input_path, output_path, page['letter_padding'])
                with open(output_path, 'w') as _out:
                    _out.write(frame.substitute(
                        next_frame = next_frame,
                        the_ascii = output_ascii
                    ))






