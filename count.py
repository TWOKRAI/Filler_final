import os

def count_lines_and_chars_in_directory(directory):
    total_lines = 0
    total_chars = 0
    extensions = ('.py', '.html', '.css', '.js')
    for root, dirs, files in os.walk(directory):
        # Пропускаем папку виртуального окружения
        if 'myenv' in root:
            continue
        for file in files:
            if file.endswith(extensions):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        lines = sum(1 for line in f if line.strip())
                        total_lines += lines
                        f.seek(0)  # Сброс указателя файла на начало
                        chars = sum(len(line) for line in f if line.strip())
                        total_chars += chars
                except Exception as e:
                    print(f"Ошибка при чтении файла {file_path}: {e}")
    return total_lines, total_chars

# Укажите путь к текущей директории
current_directory = os.path.dirname(os.path.abspath(__file__))
total_lines, total_chars = count_lines_and_chars_in_directory(current_directory)
print(f"Общее количество строк: {total_lines}")
print(f"Общее количество символов: {total_chars}")
