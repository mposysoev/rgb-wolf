from dataclasses import dataclass
import dataclasses
from copy import deepcopy
import numpy as np
from PIL import Image
from os import system


@dataclass
class Pixel:
    red: int
    green: int
    blue: int

    def gen_rand_pix(self):
        self.red = int(np.random.random() * 255)
        self.green = int(np.random.random() * 255)
        self.blue = int(np.random.random() * 255)

        return self


@dataclass
class Picture:
    size_x: int
    size_y: int
    pixels: list[list[Pixel]] = dataclasses.field(init=False)

    def __post_init__(self):
        pixels = []
        for _ in range(self.size_y):
            line = []
            for _ in range(self.size_x):
                r = int(np.random.random() * 255)
                g = int(np.random.random() * 255)
                b = int(np.random.random() * 255)
                pix = Pixel(r, g, b)
                line.append(pix)
            pixels.append(line)
        self.pixels = pixels

    def flatten(self):
        pixels = dataclasses.astuple(self)[2]
        flat = []
        for line in pixels:
            for px in line:
                flat.append(px[0])
                flat.append(px[1])
                flat.append(px[2])

        return flat


# could be transfered to Picture class
def save_image(picture: Picture, name: str):
    img = Image.frombytes(
        "RGB", (picture.size_x, picture.size_y), bytes(picture.flatten())
    )
    img.save(name)


def rgb_distance_condition(
    previous_px: Pixel, current_px: Pixel, new_px: Pixel, epsilon: float
):
    def distRGB(px_1: Pixel, px_2: Pixel):
        return (
            (px_1.red - px_2.red) ** 2
            + (px_1.green - px_2.green) ** 2
            + (px_1.blue - px_2.blue) ** 2
        )

    cond_1 = distRGB(previous_px, current_px) < epsilon
    cond_2 = distRGB(new_px, current_px) != 0.0

    return cond_1 and cond_2


def get_rand_pix_index(size_x, size_y):
    rand1 = int(np.random.random() * size_x)
    rand2 = int(np.random.random() * size_y)
    return (rand1, rand2)


def wolf_step(picture: Picture, epsilon, SIZE_X, SIZE_Y, counter_changed_pixels):
    random_px_index = get_rand_pix_index(SIZE_X, SIZE_Y)

    old_pixel = deepcopy(picture.pixels[random_px_index[0]][random_px_index[1]])

    new_pixel = Pixel(0, 0, 0).gen_rand_pix()

    picture.pixels[random_px_index[0]][random_px_index[1]] = new_pixel
    stack = [random_px_index]

    counter_changed_pixels = 0

    while stack != []:
        cur_px_index = stack.pop()

        # LEFT
        if cur_px_index[1] != 0:
            if rgb_distance_condition(
                old_pixel,
                picture.pixels[cur_px_index[0]][cur_px_index[1] - 1],
                new_pixel,
                epsilon,
            ):
                picture.pixels[cur_px_index[0]][cur_px_index[1] - 1] = new_pixel
                stack.append((cur_px_index[0], cur_px_index[1] - 1))
                counter_changed_pixels += 1

        # RIGHT
        if cur_px_index[1] != SIZE_X - 1:
            if rgb_distance_condition(
                old_pixel,
                picture.pixels[cur_px_index[0]][cur_px_index[1] + 1],
                new_pixel,
                epsilon,
            ):
                picture.pixels[cur_px_index[0]][cur_px_index[1] + 1] = new_pixel
                stack.append((cur_px_index[0], cur_px_index[1] + 1))
                counter_changed_pixels += 1

        # UP
        if cur_px_index[0] != 0:
            if rgb_distance_condition(
                old_pixel,
                picture.pixels[cur_px_index[0] - 1][cur_px_index[1]],
                new_pixel,
                epsilon,
            ):
                picture.pixels[cur_px_index[0] - 1][cur_px_index[1]] = new_pixel
                stack.append((cur_px_index[0] - 1, cur_px_index[1]))
                counter_changed_pixels += 1

        # DOWN
        if cur_px_index[0] != SIZE_Y - 1:
            if rgb_distance_condition(
                old_pixel,
                picture.pixels[cur_px_index[0] + 1][cur_px_index[1]],
                new_pixel,
                epsilon,
            ):
                picture.pixels[cur_px_index[0] + 1][cur_px_index[1]] = new_pixel
                stack.append((cur_px_index[0] + 1, cur_px_index[1]))
                counter_changed_pixels += 1

    print(
        f"Cluster size: {round(counter_changed_pixels / (SIZE_X * SIZE_Y - 1) * 100, 3)} %          ",
        end="\r",
    )
    return counter_changed_pixels


def main():
    SIZE_X = 256
    SIZE_Y = 256
    EPS = 15_000  # distance between colors, maximum: 195 075
    SAVE_FREQ = 1  # frequency of saving pictures

    picture = Picture(SIZE_X, SIZE_Y)
    save_image(picture, "output_raw_images/0.png")

    counter_changed_pixels = 0
    i = 0
    while counter_changed_pixels != SIZE_X * SIZE_Y - 1:
        counter_changed_pixels = wolf_step(
            picture, EPS, SIZE_X, SIZE_Y, counter_changed_pixels
        )

        if i % SAVE_FREQ == 0:
            save_image(picture, f"output_raw_images/{i+1}.png")

        i += 1
        # print(f'Cluster size: {counter_changed_pixels / (SIZE_X * SIZE_Y - 1)} %')
        # system('clear')

    print(
        f"Cluster size reached: {round(counter_changed_pixels / (SIZE_X * SIZE_Y - 1) * 100, 3)} %          ",
        end="\n",
    )
    print(f"Done. {i} iterations.")


if __name__ == "__main__":
    system("mkdir output_raw_images")
    main()
