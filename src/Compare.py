import os
import difflib
import chardet
from datetime import datetime


def save_to_file(file_path: str, text: str):
    """
    Сохранение результатов в файл

    :param file_path:
    :param text:
    """
    with open(file_path, 'a') as file:
        file.write(text + '\n')


def get_all_files(directory: str):
    """
    Получить список всех файлов в директории, включая файлы в поддиректориях.

    :param directory:
    :return files_list:
    """
    files_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))

    return files_list


def get_relative_path(base_path: str, full_path: str):
    """
    Получить относительный путь к файлу.

    :param base_path:
    :param full_path:
    :return relative_path:
    """
    return os.path.relpath(full_path, base_path)


def read_file(file_path: str):
    """
    Чтение файла с автоматическим определением кодировки.

    :param file_path:
    :return content:
    """
    with open(file_path, 'rb') as f:
        raw_data = f.read()

    result = chardet.detect(raw_data)
    encoding = result['encoding']

    try:
        with open(file_path, 'r', encoding=encoding) as f:
            return f.readlines()
    except UnicodeDecodeError:
        with open(file_path, 'r', encoding='latin1') as f:
            return f.readlines()


def compare_files(file1: str, file2: str):
    """
    Сравнить два файла и вернуть изменения.

    :param file1:
    :param file2:
    :return diff:
    """
    file1_lines = read_file(file1)
    file2_lines = read_file(file2)

    diff = difflib.unified_diff(file1_lines, file2_lines, lineterm='', fromfile=file1, tofile=file2)
    return list(diff)


def compare_directories(dir1: str, dir2: str, mode: str, save_path: str):
    """
    Сравнить два проекта (директории) и вывести изменения.

    :param dir1:
    :param dir2:
    :param mode:
    :param save_path:
    """
    dir1_files = get_all_files(dir1)
    dir2_files = get_all_files(dir2)

    relative_files1 = {get_relative_path(dir1, file): file for file in dir1_files}
    relative_files2 = {get_relative_path(dir2, file): file for file in dir2_files}

    all_files = set(relative_files1.keys()).union(set(relative_files2.keys()))

    if save_path:
        save_path += "/result_" + datetime.now().strftime("%d_%m_%Y_%H-%M") + ".txt"

    for relative_file in all_files:
        file1 = relative_files1.get(relative_file)
        file2 = relative_files2.get(relative_file)

        if file1 and file2:
            changes = compare_files(file1, file2)
            if changes:
                if mode == '1':
                    print(f'=======\n\nИсходный файл: {file1}')
                    print(''.join([line for line in changes if line.startswith('-') and not line.startswith('---')]))

                    print(f'-------\n\nИзмененный файл: {file2}')
                    print(''.join([line for line in changes if line.startswith('+') and not line.startswith('+++')]))
                else:
                    save_to_file(save_path, f'=======\n\nИсходный файл: {file1}')
                    save_to_file(save_path, ''.join(
                        [line for line in changes if line.startswith('-') and not line.startswith('---')]))

                    save_to_file(save_path, f'-------\n\nИзмененный файл: {file2}')
                    save_to_file(save_path, ''.join(
                        [line for line in changes if line.startswith('+') and not line.startswith('+++')]))

        elif file1:
            if mode == '1':
                print(f'=======\n\nИсходный файл:{file1}\nУДАЛЕН\n')
            else:
                save_to_file(save_path, f'=======\n\nИсходный файл: {file1}\nУДАЛЕН\n')
        elif file2:
            if mode == '1':
                print(f'=======\n\nИзмененный файл:{file2}\nДОБАВЛЕН\n')
            else:
                save_to_file(save_path, f'=======\n\nИзмененный файл: {file2}\nДОБАВЛЕН\n')
    if mode == '1':
        print('=======')
    else:
        save_to_file(save_path, f'=======')
