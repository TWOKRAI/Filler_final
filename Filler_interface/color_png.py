import os
from PIL import Image, ImageOps, ImageDraw


def recolor_image(input_image_path, output_image_path, color):
    image = Image.open(input_image_path)

    if image.mode != "RGBA":
        image = image.convert("RGBA")

    mask = ImageOps.expand(image, border=1, fill=(0, 0, 0, 255))
    mask = ImageOps.grayscale(mask)
    mask = mask.point(lambda x: 255 if x > 0 else 0, mode="1")

    color_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(color_image)
    draw.rectangle(image.getbbox(), fill=color)

    result_image = image.copy()
    result_image.paste(color, mask=mask)

    result_image.save(output_image_path)


def recolor_images_in_folder(folder_path, output_folder_path, color):
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".png"):
            continue

        input_image_path = os.path.join(folder_path, filename)
        output_image_path = os.path.join(output_folder_path, filename)

        recolor_image(input_image_path, output_image_path, color)


if __name__ == '__main__':
    recolor_images_in_folder("Style_windows\icons", "Style_windows\icons_black", (42, 122, 96, 255))
