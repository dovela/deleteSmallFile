import argparse
import os
import time
import pathlib


def removeSmallFile(work_dir, less_threshold, wait_time):  # 获取处理目录，带不带/都可以
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
                        print(item_path)
                        os.remove(item_path)  # 删除零碎文件
    f.close()
    os.remove(to_be_removed_files)  # 删除临时txt


if __name__ == '__main__':
    # 需提供路径argv[1]，进行判断
    # argv[2]字节，阈值3MB
    # argv[3]等待正常录播的时间
    parser = argparse.ArgumentParser(description="Delete the small file generated by the error of the recording "
                                                 "software. It is recommended to execute periodically")

    parser.add_argument('work_dir', type=pathlib.Path,
                        help="path. If the directory include space,the \"\" will be necessary.")
    parser.add_argument('-s', '--size', type=int, default=3145728,
                        help="int. Default 3145728 byte, file volume which less than this args will be removed.")
    parser.add_argument('-t', '--wait', type=int, default=60,
                        help="int. Default 60 s, waiting for normal file volume to exceed threshold.")
    parser.add_argument('-y', action="store_true", help="skip delete confirmation.")

    args = parser.parse_args()

    if args.y:
        removeSmallFile(work_dir=args.work_dir, less_threshold=args.size, wait_time=args.wait)
    else:
        input_confirm = input("Do you want to continue? [Y/n] ")
        if input_confirm.strip() in ["y", "Y", "yes", "YES"]:
            removeSmallFile(work_dir=args.work_dir, less_threshold=args.size, wait_time=args.wait)
        else:
            print("Abort.")