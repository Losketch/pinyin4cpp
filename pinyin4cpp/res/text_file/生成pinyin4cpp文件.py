import re
import os
from collections import OrderedDict

# 打开 Unihan_Readings.txt 文件
with open("Unihan_Readings.txt", "r", encoding="utf-8") as f:
    # 读取文件内容
    lines = f.readlines()

# 去掉开头有 # 号的行
lines = [line for line in lines if not line.startswith("#")]

# 去掉含有 kCantonese kDefinition kHangul kJapanese kJapaneseKun kJapaneseOn kKorean kSMSZD2003Readings kTang kTGHZ2013 kVietnamese kXHC1983 的行
lines = [line for line in lines if not re.search(r"kCantonese", line)]
lines = [line for line in lines if not re.search(r"kDefinition", line)]
lines = [line for line in lines if not re.search(r"kHangul", line)]
lines = [line for line in lines if not re.search(r"kJapanese", line)]
lines = [line for line in lines if not re.search(r"kJapaneseKun", line)]
lines = [line for line in lines if not re.search(r"kJapaneseOn", line)]
lines = [line for line in lines if not re.search(r"kKorean", line)]
lines = [line for line in lines if not re.search(r"kSMSZD2003Readings", line)]
lines = [line for line in lines if not re.search(r"kTang", line)]
lines = [line for line in lines if not re.search(r"kTGHZ2013", line)]
lines = [line for line in lines if not re.search(r"kVietnamese", line)]
lines = [line for line in lines if not re.search(r"kXHC1983", line)]

# 写入新文件
with open("utemp1.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line)


# B部分代码

# 打开 temp_Unihan_Readings.txt 文件
with open("utemp1.txt", "r", encoding="utf-8") as f:
    # 读取文件内容
    lines = f.readlines()

# 将每行的空格替换为逗号
lines = [line.replace(' ', ',') for line in lines]

# 将每行的特殊声调替换为正常声调
lines = [line.replace('ê̄', 'ē') for line in lines]
lines = [line.replace('ế', 'é') for line in lines]
lines = [line.replace('ê̌', 'ě') for line in lines]
lines = [line.replace('ề', 'è') for line in lines]

# 一步处理包含kHanyuPinlu的行
lines = [re.sub(r'kHanyuPinlu.*?\t', '', re.sub(r'\(.*?\)', '', line.replace(' ', ','))) for line in lines]

# 去掉包含kHanyuPinyin的行中的kHanyuPinyin和:号以及它们之间的内容
lines = [re.sub(r'kHanyuPinyin.*?:', '', line) for line in lines]

# 去掉包含kMandarin的行中的kMandarin和制表符
lines = [line.replace('\tkMandarin', '') for line in lines]

# 修改部分：在包含 5个阿拉伯数字.3个阿拉伯数字: 的行中去掉这部分数据
lines = [re.sub(r'[0-9]{5}\.[0-9]{3}:', '', line) for line in lines]

# 写入新文件
with open("utemp2.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line)


# C部分代码

# 处理有,符号的行，把它分开并删除新的行
def process_comma_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    new_lines = []
    for line in lines:
        if ',' in line:
            # Check if there is a tab character before attempting to split
            if '\t' in line:
                code_point, readings = line.split('\t')
                readings = readings.split(',')
                for reading in readings:
                    new_lines.append(f"{code_point}\t{reading.strip()}\n")
            else:
                # Handle the case where there is no tab character in the line
                # You may want to log or handle this differently based on your requirements
                print(f"Warning: Line without tab character: {line}")
        else:
            new_lines.append(line)

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(new_lines)

if __name__ == "__main__":
    input_filename = "utemp2.txt"
    output_filename = "utemp3.txt"
    
    process_comma_lines(input_filename, output_filename)
    print(f"文件已处理，并保存为 {output_filename}。")


# D部分代码

def remove_duplicate_lines(input_file, output_file):
    unique_lines = OrderedDict()

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            unique_lines[line] = None

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.writelines(unique_lines.keys())

if __name__ == "__main__":
    input_filename = "utemp3.txt"
    output_filename = "utemp4.txt"
    
    remove_duplicate_lines(input_filename, output_filename)
    print(f"重复行已从文件中移除，并保存为 {output_filename}。")


# E部分代码

# 打开 temp4_Unihan_Readings.txt 文件
with open("utemp4.txt", "r", encoding="utf-8") as f:
    # 读取文件内容
    lines = f.readlines()

# 定义字符替换和后缀的字典
replace_dict = {
    'ā': ('1', 'a'),
    'á': ('2', 'a'),
    'ǎ': ('3', 'a'),
    'à': ('4', 'a'),
    'ē': ('1', 'e'),
    'é': ('2', 'e'),
    'ě': ('3', 'e'),
    'è': ('4', 'e'),
    'ī': ('1', 'i'),
    'í': ('2', 'i'),
    'ǐ': ('3', 'i'),
    'ì': ('4', 'i'),
    'ō': ('1', 'o'),
    'ó': ('2', 'o'),
    'ǒ': ('3', 'o'),
    'ò': ('4', 'o'),
    'ń': ('2', 'n'),
    'ň': ('3', 'n'),
    'ǹ': ('4', 'n'),
    'ḿ': ('2', 'm'),
    'm̀': ('4', 'm'),
    'ū': ('1', 'u'),
    'ú': ('2', 'u'),
    'ǔ': ('3', 'u'),
    'ù': ('4', 'u'),
    'ü': ('1', 'u'),
    'ǘ': ('2', 'u'),
    'ǚ': ('3', 'u'),
    'ǜ': ('4', 'u'),
}

# 处理每一行
for i in range(len(lines)):
    line = lines[i]
    
    # 遍历字典，进行字符替换和后缀添加
    for char, (suffix, replace_char) in replace_dict.items():
        if char == 'ü' and 'ǘ' in line:
            # 避免提前替换，等到处理 'ǘ' 时再替换 'ü'
            continue
        
        if char in line:
            line = line.rstrip() + suffix + '\n'  # 在行末添加后缀和回车符
            line = line.replace(char, replace_char)  # 替换字符
    
    # 替换 'ü'，确保在 'ǘ' 之后替换
    line = line.replace('ü', 'u')
    
    # 更新行内容
    lines[i] = line

# 写入新文件
with open("utemp5.txt", "w", encoding="utf-8") as f:
    for line in lines:
        f.write(line)


# 添开头部分

# 定义要添加的文本内容
additional_content = """9FC3 (shan3)
9FCD (gang4)
9FCE (ta3)
9FCF (mai4)
9FD4 (ge1)
9FD5 (dan1)
9FEB (ao4)
9FEC (tian2)
9FED (ni3)
"""

# 打开 unicode_to_hanyu_pinyin.txt 文件
with open("unicode_to_hanyu_pinyin.txt", "r", encoding="utf-8") as f:
    # 读取原文件内容
    content = f.read()

# 在开头添加文本内容
new_content = content + additional_content

# 写入新文件
with open("unicode_to_hanyu_pinyin_temp.txt", "w", encoding="utf-8") as f:
    f.write(new_content)


# 打开 utemp5.txt 文件
input_file_path = "utemp5.txt"
output_file_path = "utemp6.txt"

try:
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        # 读取文件内容
        lines = input_file.readlines()

    # 处理每一行
    for i in range(len(lines)):
        # 删除每行开头的“U+”并将“	”替换为一个空格
        lines[i] = lines[i].replace("U+", "").replace("\t", " ")

    # 写入修改后的内容到新文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(lines)

    print(f"处理完成，修改后的内容已保存到 {output_file_path}")

except FileNotFoundError:
    print(f"{input_file_path} 文件未找到。")
except Exception as e:
    print(f"处理文件时发生错误: {e}")


# 打开 utemp6.txt 文件
input_file_path = "utemp6.txt"
output_file_path = "utemp7.txt"

try:
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        # 读取文件内容
        lines = input_file.readlines()

    # 删除开头是 4E00~9FFF 的行
    lines = [line for line in lines if len(line.split()) > 0 and not (line.startswith('4E00') or ('4E00' <= line.split()[0] <= '9FFF'))]

    # 写入修改后的内容到新文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.writelines(lines)

    print(f"处理完成，修改后的内容已保存到 {output_file_path}")

except FileNotFoundError:
    print(f"{input_file_path} 文件未找到。")
except Exception as e:
    print(f"处理文件时发生错误: {e}")


# 打开 utemp7.txt 文件
input_file_path = "utemp7.txt"
output_file_path = "utemp.txt"

try:
    with open(input_file_path, 'r', encoding='utf-8') as input_file:
        # 读取文件内容
        lines = input_file.readlines()

    # 创建一个字典，用于存储每个开头的行的内容
    lines_dict = {}

    # 遍历每一行
    for line in lines:
        parts = line.split()
        if len(parts) == 2:
            key = parts[0]
            value = parts[1]
            # 如果字典中已有该开头的行，则合并内容
            if key in lines_dict:
                lines_dict[key].append(value)
            else:
                lines_dict[key] = [value]

    # 将合并后的内容写入新文件
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for key, values in lines_dict.items():
            joined_values = ','.join(values)
            output_file.write(f"{key} ({joined_values})\n")

    print(f"处理完成，修改后的内容已保存到 {output_file_path}")

except FileNotFoundError:
    print(f"{input_file_path} 文件未找到。")
except Exception as e:
    print(f"处理文件时发生错误: {e}")


# 打开 unicode_to_hanyu_pinyin_temp.txt 文件
input_file1_path = "unicode_to_hanyu_pinyin_temp.txt"
input_file2_path = "utemp.txt"
output_file_path = "unicode_to_hanyu_pinyin_New.txt"

try:
    with open(input_file1_path, 'r', encoding='utf-8') as input_file1:
        with open(input_file2_path, 'r', encoding='utf-8') as input_file2:
            # 读取 unicode_to_hanyu_pinyin_temp.txt 文件内容
            content1 = input_file1.read()

            # 读取 utemp.txt 文件内容
            content2 = input_file2.read()

        # 将 utemp.txt 的内容追加到 unicode_to_hanyu_pinyin_temp.txt 的末尾
        combined_content = content1 + content2

        # 将合并后的内容保存到 unicode_to_hanyu_pinyin_temp2.txt 文件
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(combined_content)

    print(f"处理完成，utemp.txt 的内容已添加到 {input_file1_path}，保存到 {output_file_path}")

except FileNotFoundError:
    print(f"文件未找到。")
except Exception as e:
    print(f"处理文件时发生错误: {e}")


# 删除文件部分
# 要删除的文件列表
files_to_delete = ["utemp1.txt", "utemp2.txt", "utemp3.txt", "utemp4.txt", "utemp5.txt", "utemp6.txt", "utemp7.txt", "utemp.txt", "unicode_to_hanyu_pinyin_temp.txt"]

for file_to_delete in files_to_delete:
    try:
        os.remove(file_to_delete)
        print(f"{file_to_delete} 文件已成功删除。")
    except FileNotFoundError:
        print(f"{file_to_delete} 文件未找到。")
    except Exception as e:
        print(f"删除文件时发生错误: {e}")
