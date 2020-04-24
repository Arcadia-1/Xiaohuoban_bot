# -*- coding: utf-8 -*-
# export LANG=zh_CN.UTF-8

import smtplib
import os, time, logging
import easygui
import json

from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
    # filename="record.txt",
)
logger = logging.getLogger(__name__)


# 包含中文，所以通过Header对象进行编码
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, "utf-8").encode(), addr))


def load_configuration(config_json):

    configuration = json.load(open(config_json, "rb"))
    for key in configuration.keys():
        if configuration[key] == None:
            logger.error("Please choose: " + key)
            return False

    return configuration


# 设置收件人地址文件、收件人姓名文件、邮件正文欢迎词
def reconfigure(config_json):
    configuration = {}
    configuration["address_txt"] = easygui.fileopenbox(msg="选择邮箱地址文件")
    configuration["name_txt"] = easygui.fileopenbox(msg="选择发送对象姓名文件")
    configuration["greeting_txt"] = easygui.fileopenbox(msg="选择问候语文件")
    configuration["picture_dir"] = easygui.diropenbox(msg="选择图片文件夹")

    for key in configuration.keys():
        if configuration[key] == None:
            logger.error("Invalid Input. Exit.")
            exit()

    json.dump(
        configuration, open(config_json, "w", encoding="utf-8"), ensure_ascii=False
    )


class MailSender(object):
    # 小伙伴计划公邮
    from_address = "thusada@163.com"
    authorization_code = "OCLHDUMNSUETPFQW"
    smtp_host = "smtp.163.com"
    smtp_port = 465

    config = {}
    greeting = ""
    subject = ""
    attach_filename = ""

    def __init__(self, config, greeting, subject, attach_filename):
        self.config = config
        self.greeting = greeting
        self.subject = subject
        self.attach_filename = attach_filename

    def prepare_mail(self, name, to_address, picture_file):
        if not os.path.exists(picture_file):
            return -1
        else:
            # 邮件对象:
            msg = MIMEMultipart()
            msg["From"] = _format_addr("小伙伴计划 <%s>" % self.from_address)
            msg["To"] = _format_addr("打卡同学 <%s>" % to_address)
            msg["Subject"] = Header(self.subject)

            # 邮件正文是MIMEText:
            msg.attach(MIMEText(name + "同学，您好！\n\n" + self.greeting, "plain", "utf-8"))

            # 打开对应的图片文件（包括扩展名）,读取并关闭他
            fp = open(picture_file, "rb")
            msgImage = MIMEImage(fp.read(), "utf-8")
            fp.close()

            # 把图片放到邮件的附件里
            msgImage["Content-Type"] = "application/octet-stream"
            msgImage["Content-Disposition"] = (
                "attachment; filename=" + self.attach_filename
            )
            msg.attach(msgImage)
            return msg

    def group_process(self):
        address_list = open(self.config["address_txt"], "r", encoding="UTF-8")
        name_list = open(self.config["name_txt"], "r", encoding="UTF-8")
        mailmsglt = name_list.readlines()

        i = 0
        for line in address_list.readlines():
            to_address = line.strip()
            name = mailmsglt[i][:-1]
            picture_file = os.path.join(self.config["picture_dir"], name + ".jpg")

            msg = self.prepare_mail(name, to_address, picture_file)
            self.send_real_email(to_address, msg)
            i = i + 1

            if msg != -1:
                info = str(i) + ", " + name + ", " + to_address
            else:
                info = name + " 【未找到】"
            logger.info(info)

        # 关闭两个txt文件
        address_list.close()
        name_list.close()

    def send_real_email(self, to_address, msg):
        # 登录邮箱
        server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)
        server.set_debuglevel(0)
        server.login(self.from_address, self.authorization_code)

        # 发送这个邮件
        server.sendmail(self.from_address, to_address, msg.as_string())

        server.quit()
        time.sleep(2)


if __name__ == "__main__":

    subject = "【小伙伴计划】晚安清华（第一期）打卡证书"
    attach_filename = "Certificate_night.png"

    while True:
        config_json = "record.json"
        if not os.path.exists(config_json):
            reconfigure(config_json)

        configuration = load_configuration(config_json)

        get_file_tail = lambda n: os.path.split(configuration[n])[1]
        with open(configuration["greeting_txt"], "r", encoding="UTF-8") as f:
            greeting = f.read()

        info = (
            "标题 = "
            + subject
            + "\n附件名 = "
            + attach_filename
            + "\n收件人地址文件 = "
            + get_file_tail("address_txt")
            + "\n收件人姓名文件 = "
            + get_file_tail("name_txt")
            + "\n图片文件夹 = "
            + get_file_tail("picture_dir")
            + "\n\n文案： \n"
            + greeting
        )

        option = easygui.ynbox(
            msg=info, choices=("重新设置", "不需要修改了，发送！"), title="发送前检查各项设置！！！"
        )
        if option == True:
            if reconfigure(config_json):
                logger.info("reconfigured successfully!")
        else:
            break

    Bot = MailSender(configuration, greeting, subject, attach_filename)
    Bot.group_process()
