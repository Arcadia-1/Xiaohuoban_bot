import os, re, linecache
from datetime import datetime
import easygui


def get_line_context(file_path, line_number):
    return linecache.getline(file_path, line_number).strip()


def batch_rename_certificate(source_info, target_info):

    #     parse the parameters
    source_folder_name = source_info["folder"]
    source_txt_file_name = source_info["data_source"]
    source_file_format = source_info.get("format", "jpg")

    target_folder_prefix = target_info["folder_prefix"]
    target_file_prefix = target_info.get("file_prefix", "证书")
    target_file_format = target_info.get("format", "jpg")
    usrname = target_info.get("usrname", "bot")

    date_str = datetime.now().strftime("%Y%m%d")
    target_folder = target_folder_prefix + "-" + usrname + "-" + date_str
    target_folder_path = os.path.join(os.getcwd(), target_folder)
    source_folder_path = os.path.join(os.getcwd(), source_folder_name)
    source_txt_file_path = os.path.join(source_folder_path, source_txt_file_name)

    assert get_line_context(source_txt_file_path, 2).split("\t") != [""]

    #     if no target folder, then create one
    if not os.path.exists(target_folder_path):
        os.makedirs(target_folder_path)

    #     rename files in batch
    for file in os.listdir(source_folder_path):
        postfix = file.split(".")[1]

        if (postfix == source_file_format) and (target_file_prefix in file):
            number = re.split(r"_| |\.", file)  # split the filename
            number = int(number[1]) + 1

            line = get_line_context(source_txt_file_path, number).split("\t")

            new_name = (
                target_folder_prefix
                + "_"
                + line[0]
                + "_"
                + line[2]
                + "_"
                + line[1]
                + "天."
                + target_file_format
            )
            new_name = os.path.join(target_folder_path, new_name)

            print(new_name)

            # os.rename(os.path.join(source_folder_path,file),new_name)    # Don't rename without confirmation！！！


source_info = {}
source_info["folder"] = easygui.diropenbox(msg="请选择源文件夹：")
source_info["data_source"] = easygui.fileopenbox(msg="请选择txt数据文件：")
source_info["format"] = "jpg"

target_info = {}
target_info["folder_prefix"] = "小伙伴计划-寒假打卡证书"
target_info["file_prefix"] = "证书"
target_info["format"] = "jpg"

target_info["usrname"] = "张智帅"


batch_rename_certificate(source_info, target_info)

