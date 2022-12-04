from os import listdir
from os import system

list_of_files = listdir("output_raw_images")
system('mkdir output_upscaled_images')

for file in list_of_files:
    system(
        f"./ffmpeg -i output_raw_images/{file} -vf scale=1080:1080 -sws_flags neighbor output_upscaled_images/{file}"
    )



system('./ffmpeg -framerate 30 -i output_upscaled_images/%d.png -c:v libx264 -pix_fmt yuv420p movie.mp4 -y')