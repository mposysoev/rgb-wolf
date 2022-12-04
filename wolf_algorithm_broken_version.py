import numpy as np
from PIL import Image
from tqdm import tqdm


def initialize_img(colors, SIZE_X, SIZE_Y):
    for _ in range(SIZE_Y * SIZE_X):
        r = int(np.random.random() * 255)
        g = int(np.random.random() * 255)
        b = int(np.random.random() * 255)
        rgb = [r, g, b]
        colors.extend(rgb)


def rgb_distance_condition(
    r_old, g_old, b_old, cur_r, cur_g, cur_b, r_new, g_new, b_new, epsilon
):
    cond_1 = (
        (r_old - cur_r) ** 2 + (g_old - cur_g) ** 2 + (b_old - cur_b) ** 2
    ) < epsilon
    cond_2 = ((r_new - cur_r) ** 2 + (g_new - cur_g) ** 2 + (b_new - cur_b) ** 2) != 0

    return cond_1 and cond_2


def wolf_step(colors, epsilon, SIZE_X, SIZE_Y):
    global length_of_stack
    number_random_px = int(np.random.random() * (SIZE_X * SIZE_Y))

    i_r, i_g, i_b = (
        3 * number_random_px,
        3 * number_random_px + 1,
        3 * number_random_px + 2,
    )

    # remember old color
    r_old, g_old, b_old = colors[i_r], colors[i_g], colors[i_b]

    # generate new color for random-taken pixel
    r_new = int(np.random.random() * 255)
    g_new = int(np.random.random() * 255)
    b_new = int(np.random.random() * 255)

    # revert and push to stack
    colors[i_r], colors[i_r], colors[i_r] = r_new, g_new, b_new
    stack = [i_r, i_g, i_b]

    while stack != []:

        j_b = stack.pop()
        j_g = stack.pop()
        j_r = stack.pop()

        # LEFT
        if j_r % (SIZE_X * 3) != 0:
            if rgb_distance_condition(
                r_old,
                g_old,
                b_old,
                colors[j_r - 3],
                colors[j_g - 3],
                colors[j_b - 3],
                r_new,
                g_new,
                b_new,
                epsilon,
            ):
                colors[j_r], colors[j_g], colors[j_b] = r_new, g_new, b_new
                stack.append(j_r - 3)
                stack.append(j_g - 3)
                stack.append(j_b - 3)

        # RIGHT
        if j_r % (SIZE_X * 3) < SIZE_X * 3 - 3:
            if rgb_distance_condition(
                r_old,
                g_old,
                b_old,
                colors[j_r + 3],
                colors[j_g + 3],
                colors[j_b + 3],
                r_new,
                g_new,
                b_new,
                epsilon,
            ):
                colors[j_r], colors[j_g], colors[j_b] = r_new, g_new, b_new
                stack.append(j_r + 3)
                stack.append(j_g + 3)
                stack.append(j_b + 3)

        # UP
        if j_r > (SIZE_X * 3 - 1):
            if rgb_distance_condition(
                r_old,
                g_old,
                b_old,
                colors[j_r - SIZE_X * 3],
                colors[j_g - SIZE_X * 3],
                colors[j_b - SIZE_X * 3],
                r_new,
                g_new,
                b_new,
                epsilon,
            ):
                colors[j_r], colors[j_g], colors[j_b] = r_new, g_new, b_new
                stack.append(j_r - SIZE_X * 3)
                stack.append(j_g - SIZE_X * 3)
                stack.append(j_b - SIZE_X * 3)

        # DOWN
        if j_r < 3 * SIZE_X * (SIZE_Y - 1):
            if rgb_distance_condition(
                r_old,
                g_old,
                b_old,
                colors[j_r + SIZE_X * 3],
                colors[j_g + SIZE_X * 3],
                colors[j_b + SIZE_X * 3],
                r_new,
                g_new,
                b_new,
                epsilon,
            ):
                colors[j_r], colors[j_g], colors[j_b] = r_new, g_new, b_new
                stack.append(j_r + SIZE_X * 3)
                stack.append(j_g + SIZE_X * 3)
                stack.append(j_b + SIZE_X * 3)

        length_of_stack = len(stack)


def save_image(colors, name, SIZE_X, SIZE_Y):
    img = Image.frombytes("RGB", (SIZE_X, SIZE_Y), bytes(colors))
    img.save(name)


def main():
    colors = []
    SIZE_X = 8
    SIZE_Y = 8
    EPS = 50_000  # was 50_000, maximum: 195 075
    NUM_OF_STEPS = 500
    SAVE_FREQ = 1

    initialize_img(colors, SIZE_X, SIZE_Y)
    save_image(colors, f"output_raw_images/wolf_0.png", SIZE_X, SIZE_Y)

    for i in tqdm(range(NUM_OF_STEPS)):
        wolf_step(colors, EPS, SIZE_X, SIZE_Y)
        if i % SAVE_FREQ == 0:
            save_image(colors, f"output_raw_images/wolf_{i+1}.png", SIZE_X, SIZE_Y)
            if length_of_stack == 3 * SIZE_X * SIZE_Y - 1:
                print(f"Iteration number {i}, stack is full. Stopped!")
                break


if __name__ == "__main__":
    main()
