import os, sys
import time

less_threshold = 3145728  # 字节，阈值3MB
wait_time = 60  # 等待正常录播的时间


def removeSmallFile(work_dir):  # 获取处理目录，带不带/都可以
    to_be_removed_files = os.path.join(work_dir, ".TBRF.txt")  # 暂存需删除文件
    if os.path.exists(to_be_removed_files):  # 预删除临时txt
        os.remove(to_be_removed_files)

    all_files = os.listdir(work_dir)
    f = open(to_be_removed_files, "a", encoding='utf-8')
    for file in all_files:
        item_path = os.path.join(work_dir, file)
        if not os.path.isdir(item_path):
            # 获取文件的大小
            file_size = os.path.getsize(item_path)
            # 小于阈值就写入到删除列表
            if file_size < less_threshold:
                f.write(item_path + '\n')
    f.close()

    time.sleep(wait_time)  # 等待正常生成的录播文件大小超出阈值，

    f = open(to_be_removed_files, "r", encoding='utf-8')
    to_be_removed_lists = f.read().splitlines()  # 读取预删除列表
    for file in all_files:
        item_path = os.path.join(work_dir, file)
        if not os.path.isdir(item_path):
            # 获取文件的大小
            file_size = os.path.getsize(item_path)
            if file_size < less_threshold:  # 剔除正常文件
                for wait_removed_files in to_be_removed_lists:
                    if item_path == wait_removed_files:
                        os.remove(item_path)  # 删除零碎文件
    f.close()
    os.remove(to_be_removed_files)  # 删除临时txt


if __name__ == '__main__':
    # 需提供路径，进行判断
    if len(sys.argv) == 2 and os.path.isdir(sys.argv[1]):
        removeSmallFile(sys.argv[1])
    else:
        print(r"请提供处理路径，路径含空格须加引号，例：python deleteSmallFile.py 'e:\21452505'")
