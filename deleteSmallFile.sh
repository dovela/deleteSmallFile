#!/bin/bash
IFS=$' \t\n'

less_threshold="3M"  # 阈值3MB
work_dir=$1  # 获取处理目录，带不带/都可以

removeSmallFile(){
    IFS=$'\n'
    for i in `find  $work_dir -size -$less_threshold -type f`
    do
        echo $i >> $work_dir/.WTBR.txt  # 生成待处理文件列表
    done
    IFS=$' \t\n'

    sleep 60s  # 等待正常生成的录播文件大小超出阈值

    IFS=$'\n'
    for i in `find  $work_dir -size -$less_threshold -type f`
    do
        for j in `cat $work_dir/.WTBR.txt`
        do
            if [[ $j == $i ]]; then  # 对比列表，剔除正常文件
                rm -f $i  # 删除零碎小文件
            fi
        done
    done
    IFS=$' \t\n'
}

# 传入目录参数后，等待5s防止误操作
[[ ! -z $1 ]] && sleep 5s && removeSmallFile &&  rm -f $work_dir/.WTBR.txt  

# 示例 bash deleteSmallFile.sh "/bilirecord/21452505"
# 建议搭配定时任务使用，我这里 */10 * * * * bash /root/deleteSmallFile.sh "/bilirecord/21452505"