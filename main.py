import os
import sys
import time

from win32api import GetFileVersionInfo, LOWORD, HIWORD

# Unicode 块字符
BLOCK_CHARS = ['█', '▉', '▊', '▋', '▌', '▍', '▎', '▏']


def countdown_progress_bar(total_duration, bar_length=40, direction='left_to_right'):
    def _print_progress_bar(remaining):
        # 计算剩余时间比例
        progress_ratio = remaining / total_duration
        # 全块进度块的个数
        full_blocks = int(progress_ratio * bar_length)
        # 确定进度条中剩余部分所用的Unicode字符的索引
        partial_block_index = int((progress_ratio * bar_length - full_blocks) * len(BLOCK_CHARS))
        # 根据方向构建进度条
        if direction == 'left_to_right':
            # 顺滑消失在左侧的效果
            bar = BLOCK_CHARS[0] * full_blocks
            if full_blocks < bar_length:
                bar += BLOCK_CHARS[partial_block_index]
            bar += ' ' * (bar_length - full_blocks - 1)
        elif direction == 'right_to_left':
            # 顺滑消失在右侧的效果
            bar = ' ' * (bar_length - full_blocks - 1)
            if full_blocks < bar_length:
                bar = BLOCK_CHARS[7 - partial_block_index] + bar
            bar = BLOCK_CHARS[0] * full_blocks + bar
        # 剩余时间的秒数
        time_str = f'{int(remaining):02d}s'
        sys.stdout.write(f'\r[{bar}] {time_str} remaining')
        sys.stdout.flush()

    start_time = time.time()
    _print_progress_bar(total_duration)
    # 一直倒计时直到时间为0
    while True:
        elapsed_time = time.time() - start_time
        remaining_time = total_duration - elapsed_time
        if remaining_time <= 0:
            break
        _print_progress_bar(remaining_time)
        time.sleep(0.1)  # 此处也可调整来改变刷新频率

    # 倒计时结束时确保进度条是空的，并打印信息
    _print_progress_bar(0)
    sys.stdout.write('\rDone!\n')


def get_version_number(exe_file):
    try:
        info = GetFileVersionInfo(exe_file, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return HIWORD(ms), LOWORD(ms), HIWORD(ls), LOWORD(ls)
    except Exception as e:  # Instead of 'except:', use 'except Exception as e:'
        print(f"An exception occurred: {e}")
        time.sleep(100)
        return 0, 0, 0, 0


def print_hi(file_path):
    # Use a breakpoint in the code line below to debug your script.
    print(f'待重命名文件: {file_path}')  # Press Ctrl+F8 to toggle the breakpoint.

    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"{file_path}文件不存在")
        total_duration = 100  # 10 seconds duration for the progress bar
        countdown_progress_bar(total_duration, direction='right_to_left')
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
    with open(filename, 'w') as file:
        file.write("hello.exe")  # 可以写入你想指定的默认内容


def read_target_filename_from_file(filename):
    try:
        with open(filename, 'r') as file:
            # 读取文件的第一行作为目标文件名
            return file.readline().strip()
    except FileNotFoundError:
        # 如果文件不存在，返回 None
        return None


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # 确保至少有一个文件被拖拽到了程序上
    if len(sys.argv) > 1:
        all_files_valid = True
        for file in sys.argv[1:]:
            # 检查文件扩展名是否为 .exe
            if not file.lower().endswith('.exe'):
                print(f'错误: 不支持的文件类型 - {file}')
                all_files_valid = False
            else:
                print_hi(file)

        if not all_files_valid:
            print('请只拖拽 .exe 文件到该程序上。')
            countdown_progress_bar(10, direction='right_to_left')
    elif len(sys.argv) == 1:
        hello_file = 'Magic.txt'

        # 尝试从 hello.txt 文件读取目标文件名
        target_filename = read_target_filename_from_file(hello_file)

        if target_filename is None:  # 文件不存在
            create_hello_file(hello_file)  # 如果不存在，创建文件
            print(f'请在{hello_file}中写上希望重命名的文件，例如：hello.exe')
            print('你也可以直接拖拽目标文件到本文件上')
            countdown_progress_bar(10, direction='right_to_left')
        else:
            print(f"目标文件名已从 {hello_file} 读取: {target_filename}")
            # 你的其他代码逻辑，可以使用 target_filename 变量...
            print_hi(target_filename)
    else:
        print('未检测到拖拽的文件，请拖拽 .exe 文件到该程序上。')
        countdown_progress_bar(10, direction='right_to_left')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
