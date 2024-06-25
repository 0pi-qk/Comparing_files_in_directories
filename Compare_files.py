"""
    Программа для нахождения различий в директориях (в файлах и их содержимом)

    Входные параметры:
      --path_1:         Путь к первой директории
      --path_2:         Путь ко второй директории
      --save_path:      Путь к сохранению результирующего файла (необязательный параметр)
"""

import argparse
import os

from src.Compare import compare_directories

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Сравнение файлов в директориях')

    parser.add_argument('--path_1', type=str, help='Путь к первой директории')
    parser.add_argument('--path_2', type=str, help='Путь ко второй директории')
    parser.add_argument('--save_path', type=str, help='Путь к сохранению результирующего файла')

    args = parser.parse_args()

    save_path = None
    mode = '1'

    try:
        # Если переданы аргументы при запуске
        if args.path_1 or args.path_2:
            if not args.path_1 or not args.path_2:
                raise ValueError("Не переданы аргументы! Используйте --path_1 '/path/to/directory' --path_1 "
                                 "'/path/to/directory'")

            dir1 = args.path_1
            if not os.path.exists(dir1):
                raise FileNotFoundError(f"Директория '{dir1}' не существует.")

            dir2 = args.path_2
            if not os.path.exists(dir2):
                raise FileNotFoundError(f"Директория '{dir2}' не существует.")

            if args.save_path:
                if not os.path.exists(args.save_path):
                    raise FileNotFoundError(f"Директория '{args.save_path}' не существует.")

                save_path = args.save_path
                mode = '2'

        # Ввод параметров в консоли
        else:
            while True:
                dir1 = input("Введите путь к первой директории (прошлая версия проекта): ")

                if os.path.exists(dir1):
                    break

                print(f"\nДиректория '{dir1}' не существует. Пожалуйста, введите еще раз.\n")

            while True:
                dir2 = input("Введите путь ко второй директории (проект с изменениями): ")

                if os.path.exists(dir2):
                    break

                print(f"\nДиректория '{dir2}' не существует. Пожалуйста, введите еще раз.\n")

            print("\nСпособ получения результата:")
            print("1. Вывести в консоль")
            print("2. Сохранить в файл")

            while True:
                mode = input("\n--> ")

                if mode == '1':
                    break
                elif mode == '2':
                    while True:
                        save_path = input("\nВведите директорию для сохранения результата: ")

                        # Проверка наличия директории
                        if os.path.exists(save_path):
                            break

                        print(f"\nДиректория '{save_path}' не существует. Пожалуйста, введите еще раз.\n")

                    break

                print("\nНа допустимое значение! Пожалуйста, выберите еще раз.")

        # Сравнение
        compare_directories(dir1, dir2, mode, save_path)

        if mode == '2':
            print("\nФайл успешно сохранен!")

    except FileNotFoundError as e:
        print(f"Ошибка: {e}")
    except ValueError as e:
        print(f"Ошибка: {e}")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Ошибка: {e}")
