"""
    Program for finding differences in directories (in files and their content)

    Input parameters:
      --path_1:         Path to the first directory
      --path_2:         Path to the second directory
      --save_path:      Path to save the resulting file (optional parameter)
"""

import argparse
import os

from src.Compare import compare_directories

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Comparison of files in directories')

    parser.add_argument('--path_1', type=str, help='Path to the first directory')
    parser.add_argument('--path_2', type=str, help='Path to the second directory')
    parser.add_argument('--save_path', type=str, help='Path to save the resulting file')

    args = parser.parse_args()

    save_path = None
    mode = '1'

    try:
        # If arguments are passed when running the script
        if args.path_1 or args.path_2:
            if not args.path_1 or not args.path_2:
                raise ValueError("Arguments not passed! Use --path_1 '/path/to/directory' --path_1 '/path/to/directory'")

            dir1 = args.path_1
            if not os.path.exists(dir1):
                raise FileNotFoundError(f"Directory '{dir1}' does not exist.")

            dir2 = args.path_2
            if not os.path.exists(dir2):
                raise FileNotFoundError(f"Directory '{dir2}' does not exist.")

            if args.save_path:
                if not os.path.exists(args.save_path):
                    raise FileNotFoundError(f"Directory '{args.save_path}' does not exist.")

                save_path = args.save_path
                mode = '2'

        # Console input of parameters
        else:
            while True:
                dir1 = input("Enter the path to the first directory (previous project version): ")

                if os.path.exists(dir1):
                    break

                print(f"\nDirectory '{dir1}' does not exist. Please enter again.\n")

            while True:
                dir2 = input("Enter the path to the second directory (project with changes): ")

                if os.path.exists(dir2):
                    break

                print(f"\nDirectory '{dir2}' does not exist. Please enter again.\n")

            print("\nResult output method:")
            print("1. Print to console")
            print("2. Save to file")

            while True:
                mode = input("\n--> ")

                if mode == '1':
                    break
                elif mode == '2':
                    while True:
                        save_path = input("\nEnter the directory to save the result: ")

                        # Check if directory exists
                        if os.path.exists(save_path):
                            break

                        print(f"\nDirectory '{save_path}' does not exist. Please enter again.\n")

                    break

                print("\nInvalid value! Please choose again.")

        # Comparison
        compare_directories(dir1, dir2, mode, save_path)

        if mode == '2':
            print("\nFile saved successfully!")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}")
