import os
import sys
import re
import glob

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


def rename_exe_with_version(file_path, segments=4):
    # Use a breakpoint in the code line below to debug your script.
    print(f'待重命名文件: {file_path}')  # Press Ctrl+F8 to toggle the breakpoint.

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"{file_path}文件不存在")
    else:
        # 获取版本号
        version = get_version_number(file_path)

        # 根据配置的段数生成版本号字符串
        version_str = ".".join(map(str, version[:segments]))

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


def is_processed_file(filename, segments=4):
    """
    检查文件是否已经被处理过（格式：Hello_x.x.x.x.exe 或 Hello_x.x.x.x.exe）
    支持1-4段版本号，支持多种分隔符或直接连接
    """
    # 根据版本段数构建正则表达式
    # 支持格式：文件名[分隔符]版本号.exe
    # 分隔符可以是：_、-、. 或直接连接
    if segments == 1:
        pattern = r'^.+[._-]?\d+\.exe$'
    elif segments == 2:
        pattern = r'^.+[._-]?\d+\.\d+\.exe$'
    elif segments == 3:
        pattern = r'^.+[._-]?\d+\.\d+\.\d+\.exe$'
    else:  # segments == 4
        pattern = r'^.+[._-]?\d+\.\d+\.\d+\.\d+\.exe$'
    
    return bool(re.match(pattern, filename, re.IGNORECASE))


def find_exe_files_in_directory(directory, segments=4):
    """
    递归搜索目录下的所有exe文件，排除已处理的文件
    """
    exe_files = []
    
    if not os.path.exists(directory):
        print(f"警告：目录不存在 - {directory}")
        return exe_files
    
    # 递归搜索所有exe文件
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.exe'):
                file_path = os.path.join(root, file)
                # 只处理未处理的文件
                if not is_processed_file(file, segments):
                    exe_files.append(file_path)
                else:
                    print(f"跳过已处理的文件: {file_path}")
    
    return exe_files


def read_config_from_file(filename):
    """
    从配置文件中读取工作路径、版本段数和目标文件列表
    返回 (work_path, segments, target_files)
    """
    work_path = None
    segments = 4  # 默认4段
    target_files = []
    
    try:
        with open(filename, 'r', encoding='utf-8') as file0:
            for line in file0:
                line = line.strip()
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                
                # 检查是否是工作路径配置
                if line.startswith('work_path='):
                    work_path = line.split('=', 1)[1].strip()
                # 检查是否是版本段数配置
                elif line.startswith('segments='):
                    try:
                        segments = int(line.split('=', 1)[1].strip())
                        # 限制在1-4段之间
                        segments = max(1, min(4, segments))
                    except ValueError:
                        print(f"版本段数配置无效，使用默认值4: {line}")
                else:
                    # 其他行作为目标文件
                    target_files.append(line)
    except FileNotFoundError:
        print(f"配置文件不存在: {filename}")
    except Exception as e:
        print(f"读取配置文件时出错: {e}")
    
    return work_path, segments, target_files


def read_target_filenames_from_file(filename):
    """
    保持向后兼容，读取目标文件名列表
    """
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
                # 拖拽文件时使用默认4段版本号
                rename_exe_with_version(file, 4)

        if not all_files_valid:
            print('请只拖拽 .exe 文件到该程序上。')
            # 按任意键退出
            input("按任意键退出...")
    elif len(sys.argv) == 1:
        config_file = 'Magic.txt'

        # 读取配置文件
        work_path, segments, target_files = read_config_from_file(config_file)
        
        print(f"配置的版本段数: {segments}")
        
        files_to_process = []
        
        # 如果配置了工作路径，搜索该路径下的所有exe文件
        if work_path:
            print(f"搜索工作路径: {work_path}")
            files_to_process = find_exe_files_in_directory(work_path, segments)
            print(f"找到 {len(files_to_process)} 个未处理的exe文件")
        else:
            # 如果没有配置工作路径，使用目标文件列表
            print("未配置工作路径，使用目标文件列表")
            files_to_process = target_files

        # 处理所有找到的文件
        if files_to_process:
            for file_path in files_to_process:
                if file_path.lower().endswith('.exe'):
                    rename_exe_with_version(file_path, segments)
                else:
                    print(f"跳过非exe文件: {file_path}")
        else:
            print("没有找到需要处理的文件")

        input("按任意键退出...")
    else:
        print('未检测到拖拽的文件，请拖拽 .exe 文件到该程序上。')
        input("按任意键退出...")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
