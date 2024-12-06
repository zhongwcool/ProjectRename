import os
import sys

from win32api import GetFileVersionInfo, LOWORD, HIWORD


def get_version_number(exe_file):
    try:
        info = GetFileVersionInfo(exe_file, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
    except Exception as e:  # Instead of 'except:', use 'except Exception as e:'
        print(f"An exception occurred: {e}")
        return 0, 0, 0, 0


def rename_exe_with_version(file_path):
    # Use a breakpoint in the code line below to debug your script.
    print(f'待重命名文件: {file_path}')  # Press Ctrl+F8 to toggle the breakpoint.

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"{file_path}文件不存在")
    else:
        # 获取版本号
        version = get_version_number(file_path)

        # 生成版本号字符串
        # 只需要前三个字段
        # version_str = ".".join(map(str, version[:3]))
        version_str = "{}.{}.{}.{}".format(*version)

        # 为文件名添加版本号
        file_dir, file_name = os.path.split(file_path)
        name, ext = os.path.splitext(file_name)
        new_name = "{}_{}{}".format(name, version_str, ext)
        new_file_path = os.path.join(file_dir, new_name)

        # 重命名文件
        if os.path.exists(new_file_path):
            counter = 1
            new_name = f"{name}_{version_str}_{counter}{ext}"
            while os.path.exists(new_file_path):
                counter += 1
                new_name = f"{name}_{version_str}_{counter}{ext}"
                new_file_path = os.path.join(file_dir, new_name)

            os.rename(file_path, new_file_path)

        else:
            os.rename(file_path, new_file_path)

        print("The file has been renamed to: " + new_name)


def create_hello_file(filename):
    with open(filename, 'w') as file0:
        file0.write("hello.exe")  # 可以写入你想指定的默认内容


def read_target_filenames_from_file(filename):
    try:
        with open(filename, 'r') as file0:
            # 读取文件的每一行作为目标文件名，并去除两端的空白字符
            return [line.strip() for line in file0.readlines()]
    except FileNotFoundError:
        # 如果文件不存在，返回空列表
        return []


def print_hi():
    exe_name = os.path.basename(sys.argv[0])
    version0 = get_version_number(exe_name)
    version_str0 = "{}.{}.{}".format(*version0)
    box_width = 50
    info_str = f"{exe_name} v{version_str0}"
    print("-" * (box_width + 2))
    print(f"|{info_str:^{box_width}}|")
    print("-" * (box_width + 2))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi()

    # 确保至少有一个文件被拖拽到了程序上
    if len(sys.argv) > 1:
        all_files_valid = True
        for file in sys.argv[1:]:
            # 检查文件扩展名是否为 .exe
            if not file.lower().endswith('.exe'):
                print(f'错误: 不支持的文件类型 - {file}')
                all_files_valid = False
            else:
                rename_exe_with_version(file)

        if not all_files_valid:
            print('请只拖拽 .exe 文件到该程序上。')
            # 按任意键退出
            input("按任意键退出...")
    elif len(sys.argv) == 1:
        hello_file = 'Magic.txt'

        # 尝试从 hello.txt 文件读取目标文件名
        targets = read_target_filenames_from_file(hello_file)

        for target in targets:
            rename_exe_with_version(target)

        input("按任意键退出...")
    else:
        print('未检测到拖拽的文件，请拖拽 .exe 文件到该程序上。')
        input("按任意键退出...")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
