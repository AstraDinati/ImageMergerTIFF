from PIL import Image
import os


# Функция определения количества изображений в ряду
def adaptive_images_per_row(total_images):
    if total_images <= 2:
        return total_images
    else:
        return max(2, min(total_images, min(int(total_images / 2), 4)))


def merge_images(folders, output_file):
    images = []

    for folder_path in folders:
        files = os.listdir(folder_path)
        image_files = [
            file for file in files if file.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            img = Image.open(image_path)
            images.append(img)

    if not images:
        print("Изображения не найдены.")
        return

    spacing = 120  # Расстояние между изображениями
    images_per_row = adaptive_images_per_row(len(images))
    num_rows = (len(images) + images_per_row - 1) // images_per_row

    max_width = max(img.size[0] for img in images)
    max_height = max(img.size[1] for img in images)

    total_width = images_per_row * (max_width + spacing) - spacing
    total_height = num_rows * (max_height + spacing) - spacing

    borderLR = 300  # Отступы слева и справа
    borderUD = int(borderLR * 1.3)  # Отступы сверху и снизу

    result = Image.new(
        "RGB", (total_width + borderLR * 2, total_height + borderUD * 2), "white"
    )

    x_offset, y_offset = borderLR, borderUD

    for i, img in enumerate(images):
        if i % images_per_row == 0 and i != 0:
            x_offset = borderLR
            y_offset += max_height + spacing
        result.paste(img, (x_offset, y_offset))
        x_offset += max_width + spacing

    x_offset -= spacing
    y_offset -= spacing
    result.save(output_file, format="TIFF")


folders = input("Введите путь к папке: ")
output_file = f"Results/{folders}_result.tif"
merge_images([folders], output_file)
