import os
from PIL import Image, ImageOps, ImageDraw


class Style():
    def __init__(self):
        self.icon_path_orig = os.path.join('/home/innotech/Project/Filler/Filler_interface/Style_windows/icons')
        self.icon_path  = os.path.join('/home/innotech/Project/Filler/Filler_interface/Style_windows/icons_black')
        
        # self.icon_path_orig = os.path.join('Filler_interface', 'Style_windows', 'icons')
        # self.icon_path = os.path.join('Filler_interface', 'Style_windows', 'icons_black')

        self.text_color = (65, 69, 67)

        self.r_border = 108
        self.g_border = 161
        self.b_border = 141

        self.r_icons_text = 108
        self.g_icons_text = 161
        self.b_icons_text = 141

        self.r_text = 108
        self.g_text = 161
        self.b_text = 141


    def style(self):
        file_path = os.path.join('/home/innotech/Project/Filler/Filler_interface/Style_windows', 'style_green.css')
        
        # file_path = os.path.join('Filler_interface', 'Style_windows', 'style_green.css')

        with open(file_path, 'r') as f:
            custom_style = f.read()

        return custom_style


    def recolor_css(self, style_text):
        delta_color = 30
        text_button_r = self.r_icons_text - delta_color
        if text_button_r < 0: text_button_r = 0

        text_button_g = self.g_icons_text - delta_color
        if text_button_g < 0: text_button_g = 0

        text_button_b = self.b_icons_text - delta_color
        if text_button_b < 0: text_button_b = 0

        new_color_text_button = f'color: rgba({text_button_r}, {text_button_g}, {text_button_b}, 255);'
        new_color_border = f'border: 4px solid rgba({self.r_border}, {self.g_border}, {self.b_border}, 255);'
        new_color_bottom = f'border-bottom: 5px solid rgb({self.r_icons_text}, {self.g_icons_text}, {self.b_icons_text});'
        
        new_stylesheet = style_text.replace("""QPushButton {
    color: rgba(63, 94, 83, 255);
    border: 4px solid rgba(108, 161, 141, 255);
    border-bottom: 5px solid rgb(87, 121, 101);
}""",

        f"""QPushButton {{
                {new_color_text_button};
                {new_color_border};
                {new_color_bottom};
        }}""")
            
        # color_icons = (self.r_icons_text, self.g_icons_text, self.b_icons_text)
        # self.recolor_icons(color_icons)

        #print(new_stylesheet)

        return new_stylesheet 


    def recolor_image(self, input_image_path, output_image_path, color):
        image = Image.open(input_image_path)
        color = (color[0] - 30, color[1] - 30, color[2] - 30)

        if image.mode != "RGBA":
            image = image.convert("RGBA")

        # Создаем маску контура
        mask = ImageOps.expand(image, border=0, fill=(0, 0, 0, 255))
        mask = ImageOps.grayscale(mask)
        mask = mask.point(lambda x: 255 if x > 0 else 0, mode="1")

        # Создаем изображение с новым цветом контура
        color_image = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(color_image)
        draw.rectangle(image.getbbox(), fill=color)

        # Накладываем маску контура на изображение с новым цветом
        result_image = image.copy()
        result_image.paste(color, mask=mask)

        result_image.save(output_image_path)


    def recolor_icons(self):
        color = (self.r_icons_text, self.g_icons_text, self.b_icons_text)
        # Проверяем, существует ли папка для результатов, и создаем ее, если необходимо
        if not os.path.exists(self.icon_path):
            os.makedirs(self.icon_path)

        # Перебираем все файлы в указанной папке
        for filename in os.listdir(self.icon_path_orig):
            # Пропускаем файлы, которые не являются изображениями PNG
            if not filename.lower().endswith(".png"):
                continue

            input_image_path = os.path.join(self.icon_path_orig, filename)
            output_image_path = os.path.join(self.icon_path, filename)

            self.recolor_image(input_image_path, output_image_path, color)


#style = Style()
#style.recolor_images_in_folder((42, 122, 96, 255))