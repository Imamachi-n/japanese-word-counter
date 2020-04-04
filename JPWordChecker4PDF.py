# coding: utf-8
# #! env/bin/python

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage

import unicodedata
import io

# FIXME: ここを適宜修正！
# ["Google Forms の ID", "ダウンロードした PDF ファイル名"]
# PDF ファイルは pdf/ ディレクトリに保存してください。
input_path_list = [["XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                    'XXXX JP - Google フォーム.pdf'],
                   ["YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY",
                       'YYYY JP - Google フォーム.pdf'],
                   ["ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ",
                       'ZZZZ JP - Google フォーム.pdf']
                   ]


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


for input_path in input_path_list:
    retstr = io.StringIO()

    parser = PDFParser(open("pdf/" + input_path[1], 'rb'))

    try:
        doc = PDFDocument(parser)
    except Exception as e:
        print('is not a readable pdf')
    parser.set_document(doc)

    rsrcmgr = PDFResourceManager()
    device = TextConverter(rsrcmgr, retstr)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # doc.get_pages()はバージョンが古くて、PDFPage.create_pages(doc)とするべきみたいです。
    for page in PDFPage.create_pages(doc):
        # for page in PDFPage.get_pages(doc):
        interpreter.process_page(page)

    device.close()

    # output_file = open(input_path + ".txt", "w")
    lines = retstr.getvalue()

    counter = 0
    jp_chars = ""
    for char in str(lines):
        if is_japanese(char):
            counter += 1
            jp_chars += char

    url = "https://docs.google.com/forms/d/" + input_path[0]
    print(input_path[1][:-18], counter, jp_chars, url, sep="\t")
    # print(lines, file=output_file)
    # output_file.close()

    retstr.close()
