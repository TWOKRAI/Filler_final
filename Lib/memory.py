import shelve
import os
import shutil

class Memory():
    def __init__(self, db_path='memory_db', db_file='db'):
        self.db_path = db_path
        self.db_file = db_file
        # Создаем директорию, если она не существует
        os.makedirs(self.db_path, exist_ok=True)
        self.file_path = os.path.join(self.db_path, self.db_file)

    def memory_write(self, key, data):
        with shelve.open(self.file_path) as db: 
            db[f'{key}'] = data 
            #print('записал', key, data)

    def memory_read(self, key, default):
        with shelve.open(self.file_path) as db: 
            try:
                data = db[f'{key}']
                #print('считал', key, data)
                return data  # Десериализация не требуется, shelve сам позаботится об этом
            except KeyError:
                print('Ключ не найден, записываю значение по умолчанию')
                self.memory_write(key, default)
                return default
            except Exception as e:
                print(f'Ошибка при чтении данных: {e}')
                return default


    def recreate_database(self):
        try:
            # Удаляем все файлы в директории базы данных
            for filename in os.listdir(self.db_path):
                file_path = os.path.join(self.db_path, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)

            # Создаем новый файл базы данных
            with shelve.open(self.file_path) as db:
                pass  # Создаем пустой файл базы данных

            print(f"Database '{self.file_path}' has been recreated.")
        except Exception as e:
            print(f"Error recreating database: {e}")
