# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。

# 首先处理原始文件raw_DAS_data.txt部分行存在编码错误的问题，舍弃了编码错误的行。
with open('data/raw_DAS_data.txt', 'r', encoding='utf-8', errors='ignore') as file:
    lines = file.readlines()
    with open('data/encoding_fixed_DAS_data.txt', 'w', encoding='utf-8') as new_file:
        # 遍历每一行文本
        for line in lines:
            try:
                # 尝试将有效的文本写入新文件中
                new_file.write(line)
            except UnicodeDecodeError:
                # 如果遇到无效字节，则跳过该行
                pass


# 再处理编码修复后的文件中，部分行并不满足40个数字的格式问题。跳过了不满足格式行，并记录行号。
skipped_lines = []  # 用于存储被跳过的行号范围

with (open('data/encoding_fixed_DAS_data.txt', 'r', encoding='utf-8') as input_file,
      open('data/processed_DAS_data.txt', 'w', encoding='utf-8') as output_file,
      open('logs/skipped_lines.txt', 'w', encoding='utf-8') as log_file):
    for line_number, line in enumerate(input_file, 1):  # 使用enumerate获取行号，从1开始计数
        line = line.strip()
        if line.count('\t') == 39 and all(char.isdigit() or char == '\t' or char == '-' for char in line):
            output_file.write(line + '\n')
        else:
            skipped_lines.append(line_number)

    # 将被跳过的行号范围写入日志文件
    if skipped_lines:
        start = end = skipped_lines[0]
        for i in range(1, len(skipped_lines)):
            if skipped_lines[i] == end + 1:  # 连续的行号
                end = skipped_lines[i]
            else:
                if start == end:
                    log_file.write(f'跳过了第{start}行' + '\n')
                else:
                    log_file.write(f'跳过了第{start}-{end}行' + '\t' + f'共{end - start + 1}行' + '\n')
                start = end = skipped_lines[i]
        if start == end:
            log_file.write(f'跳过了第{start}行' + '\n')
        else:
            log_file.write(f'跳过了第{start}-{end}行' + '\t' + f'共{end - start + 1}行' + '\n')
    else:
        log_file.write("No lines were skipped.\n")
