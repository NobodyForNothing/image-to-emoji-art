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
    discord_image = []
    for row in img:
        discord_row = []
        for pixel in row:
            discord_pixel = find_discord_match(pixel)

            discord_row.append(discord_pixel)
        discord_image.append(discord_row)

    return discord_image


def find_discord_match(rgb_pixel):  # finds  best matching discord emoji for a pixel
    discordColoursRGB = {'white_large': 'e7e8e8', 'black_large': '31373d', 'orange': 'f4900c', 'blue': '55acee',
                         'red': 'dd2e44', 'brown': 'c1694f', 'purple': 'aa8dd7', 'green': '77b256', 'yellow': 'fdcb58'}  # format: colour-name, hex-colour
    best_match = [100, '']  # format: distance, colour name

    for name, hexCode in discordColoursRGB.items():
        rgbPixelDc = matplotlib.colors.to_rgb('#' + hexCode)  # converts hex to Rgb

        rgb_pixel = np.array([rgb_pixel[i] for i in range(3)])  # limit to 3 elements for colour_distance to succeed
        rgbPixelDc = np.array([rgbPixelDc[i] for i in range(3)])
        d = colour_distance(rgb_pixel, rgbPixelDc)
        if best_match[0] > d:
            best_match = [d, name]

    return f':{best_match[1]}_square:'


def colour_distance(rgb1, rgb2):  # used to find bestmatching colour credits to https://stackoverflow.com/a/14097641/15581412
    rm = 0.5 * (rgb1[0] + rgb2[0])
    p1 = (2 + rm, 4, 3 - rm)
    p2 = (rgb1 - rgb2)
    d = sum(p1 * p2 ** 2) ** 0.5
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
    print('for this project to work, you need to run \"pip install -r requirements.txt\"')
    in_img = img_input()
    scaled_img = scale_image(in_img)
    discord_img = translate_image(scaled_img)
    format_discord_img(discord_img)


