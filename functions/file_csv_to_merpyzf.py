import csv


def file_csv_to_merpyzf(file_name):
    """
    传入一个 csv 文件，将 csv 名作为书籍信息进行导入
    :return:
    """
    read_info = []
    # 从 CSV 文件中读取数据
    with open(file_name, "r", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            read_info.append(row)  # 打印每一行数据
    return read_info
