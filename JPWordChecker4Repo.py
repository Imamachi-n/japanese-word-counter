# coding: utf-8
# #! env/bin/python
from __future__ import print_function

import os
import re
import unicodedata


def find_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


def is_japanese(char):
    try:
        name = unicodedata.name(char)
        if "CJK UNIFIED" in name or "HIRAGANA" in name or "KATAKANA" in name:
            return True
    except:
        # 絵文字などでエラーになるケースがある（ごくまれ）
        # print(char)
        pass
    return False


TARGET_DIRECTORY = "."

# CHECKME: 必要に応じて設定値を変更してください。
TARGET_FILE_EXTENSION = "ja.md"
GITHUB_ORGANIZATION_URL = "https://github.com/codechrysalis/"

for file in find_all_files(TARGET_DIRECTORY):
    # .ja.mdファイルのみ検出
    if re.search(TARGET_FILE_EXTENSION, file.split("/")[-1]):
        input_file = open(file, "r")
        counter = 0
        jp_chars = ""
        for line in input_file:
            # 改行コード、句読点を削除
            line = line.rstrip().replace("。", "").replace("、", "")

            for char in line:
                if is_japanese(char):
                    counter += 1
                    jp_chars += char

        url = GITHUB_ORGANIZATION_URL + file.split("/")[1]
        print(file, counter, jp_chars, url, sep="\t")
        input_file.close()
