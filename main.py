import os

import imageio
import matplotlib.colors
import numpy as np
from skimage.transform import resize
import plyer
import sqlite3


def load_discord_representations():
    database_location = os.getcwd() + '/emoji-colors.sqlite'
    con = sqlite3.connect(database_location)

    emoji_lvl_1 = {row[0]: row[1] for row in con.execute("SELECT * FROM boxes")}  # format emoji-code, hex-code
    emoji_lvl_2 = {row[0]: row[1] for row in con.execute("SELECT * FROM additional_colors")}
    return emoji_lvl_1, emoji_lvl_2


def user_input():
    print("please choose the location of a png or jpg file")
    img = imageio.imread(plyer.filechooser.open_file()[0])
    print(f'Found image with {img.shape[0]} x {img.shape[1]} pixel')

    try:
        x = input('please enter the amount of emojy you want to have horizontally (keep around 12)\n')
        x_width = int(x)
    except ValueError:
        print("error reading that number, using 12")
        x_width = 12

    if input("would you like to add additional emojis? (Yes/no)").upper() in ["YES", "Y", ""]:  # more levels planed
        emote_variety = 1
    else:
        emote_variety = 0

    return img, x_width, emote_variety


def scale_image(img, x_width):
    y_with = int(x_width * (img.shape[1] / img.shape[0]))  # preserve image ratio
    img = resize(img, (x_width, y_with))  # credits to https://stackoverflow.com/a/65807553/15581412
    print(f'scaled Image to {x_width} x {y_with} pixel')
    return img


def translate_image(img, emoji_level, emoji_lvl_1, emoji_lvl_2):
    discord_image = []
    for row in img:
        discord_row = []
        for pixel in row:
            discord_pixel = find_discord_match(pixel, emoji_level, emoji_lvl_1, emoji_lvl_2)
            discord_row.append(discord_pixel)
        discord_image.append(discord_row)

    return discord_image


def find_discord_match(rgb_pixel, e_lvl, emoji_lvl_1, emoji_lvl_2):  # finds  best matching discord emoji for a pixel
    # emoji_level is the amount of different emote sets to use
    if e_lvl > 1:
        emoji_lvl_1.update(emoji_lvl_2)

    best_match = [100, '']  # format: distance, emoji name

    for name, hexCode in emoji_lvl_1.items():
        rgbPixelDc = np.array(matplotlib.colors.to_rgb('#' + hexCode))  # converts hex to Rgb
        rgb_pixel = np.array([rgb_pixel[i] for i in range(3)])  # limit to 3 elements
        d = colour_distance(rgb_pixel, rgbPixelDc)

        if best_match[0] > d:
            best_match = [d, name]

    return best_match[1]


def colour_distance(rgb1, rgb2):  # best matching emoji credits to https://stackoverflow.com/a/14097641/15581412
    rm = 0.5 * (rgb1[0] + rgb2[0])
    d = sum((2 + rm, 4, 3 - rm) * (rgb1 - rgb2) ** 2) ** 0.5
    return d


def format_discord_img(dc_img):  # prints the image
    print("\n\ncopy discord image below:\n")
    r = ""
    for row in dc_img:
        for emote in row:
            r += emote
        r += "\n"
    print(r)


if __name__ == '__main__':
    emoji_lvl_1, emoji_lvl_2 = load_discord_representations()
    print('This is a a simple tool to convert jpg and png images to discord chat messages!')
    in_img, x_with, usr_emoji_level = user_input()
    scaled_img = scale_image(in_img, x_with)
    discord_img = translate_image(scaled_img, usr_emoji_level, emoji_lvl_1, emoji_lvl_2)
    format_discord_img(discord_img)
