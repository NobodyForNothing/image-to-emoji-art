import imageio
import matplotlib.colors
import numpy as np
from skimage.transform import resize
import plyer
from time import sleep



def scale_image(img):
    try:
        x = int(input('Enter the the amount of emojy you want to have horizontally (its recommended to keep around '
                      '12)\n'))  # max with
    except:
        print("error reading that number, using 12")
        x = 12

    y = int(x * (img.shape[1] / img.shape[0]))  # preserve image ratio
    img = resize(img, (x, y))  # credits to https://stackoverflow.com/a/65807553/15581412

    print(f'scaled Image to {x} x {y} pixel')
    return img


def translate_image(img):
    if input("would you like to add additional emojis? (Yes/no)").upper() in ["YES", "Y", ""]:
        emoji_level = 1
    else:
        emoji_level = 0

    discord_image = []
    for row in img:
        discord_row = []
        for pixel in row:
            discord_pixel = find_discord_match(pixel, emoji_level)

            discord_row.append(discord_pixel)
        discord_image.append(discord_row)

    return discord_image


def find_discord_match(rgb_pixel, emoji_level):  # finds  best matching discord emoji for a pixel
    # emoji_level is the amount of different emote sets to use
    dc_colours_boxes_hex = {
                         ':white_large_square:' : 'e7e8e8',
                         ':black_large_square:' : '31373d',
                         ':orange_square:'      : 'f4900c',
                         ':blue_square:'        : '55acee',
                         ':red_square:'         : 'dd2e44',
                         ':brown_square:'       : 'c1694f',
                         ':purple_square:'      : 'aa8dd7',
                         ':green_square:'       : '77b256',
                         ':yellow_square:'      : 'fdcb58'}  # format: emote-name, hex-colour
    if emoji_level > 1:
        dc_colours_others_hex = {
                         ':united_nations:'     : '5488be',
                         ':flag_cn:'            : 'bc321c',
                         ':fog:'                : 'dae2e7',
                         ':japan:'              : '7fbedf',
                         ':dollar:'             : '8fa96b',
                         ':credit_card:'        : '9e7f50',
                         ':tennis:'             : '7fa46b',
                         ':window:'             : 'b1bccd'}
        dc_colours_boxes_hex.update(dc_colours_others_hex)

    best_match = [100, '']  # format: distance, emoji name
    # dc_colours_boxes_hex.update(dc_colours_others_hex)  # temp

    for name, hexCode in dc_colours_boxes_hex.items():
        rgbPixelDc = matplotlib.colors.to_rgb('#' + hexCode)  # converts hex to Rgb

        rgb_pixel = np.array([rgb_pixel[i] for i in range(3)])  # limit to 3 elements for colour_distance to succeed
        rgbPixelDc = np.array([rgbPixelDc[i] for i in range(3)])
        d = colour_distance(rgb_pixel, rgbPixelDc)
        if best_match[0] > d:
            best_match = [d, name]

    return best_match[1]


def colour_distance(rgb1, rgb2):  # bestmatching emoji credits to https://stackoverflow.com/a/14097641/15581412
    rm = 0.5 * (rgb1[0] + rgb2[0])
    d = sum((2 + rm, 4, 3 - rm) * (rgb1 - rgb2) ** 2) ** 0.5
    return d


def img_input():  # open a file in imageIo arraylike format
    print("please choose the location of a png or jpg file")
    sleep(1)  # wait to give the user time to read
    file = plyer.filechooser.open_file()
    img = imageio.imread(file[0])
    print(f'Found image with {img.shape[0]} x {img.shape[1]} pixel')
    return img


def format_discord_img(dc_img):  # prints the image
    print("\n\ncopy discord image below:\n")
    for row in dc_img:
        r = ""
        for i in row: r += i
        print(r)


if __name__ == '__main__':
    print('This is a a simple tool to convert jpg and png images to discord chat messages!')
    in_img = img_input()
    scaled_img = scale_image(in_img)
    discord_img = translate_image(scaled_img)
    format_discord_img(discord_img)


