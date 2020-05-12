# -*- coding: utf-8 -*-
# export LANG=zh_CN.UTF-8

import smtplib
import os, time, logging, re, json, csv
import easygui

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


# 设置收件人信息文件、邮件正文欢迎词
def reconfigure(config_json):
    configuration = {}
    configuration["info_csv"] = easygui.fileopenbox(msg="选择邮件对象信息文件", default="*.csv")
    configuration["greeting_txt"] = easygui.fileopenbox(msg="选择问候语文件", default="*.txt")
    configuration["picture_dir"] = easygui.diropenbox(msg="选择图片文件夹")

    for key in configuration.keys():
        if configuration[key] == None:
            logger.error("Invalid Input. Exit.")
            exit()

    json.dump(
        configuration, open(config_json, "w", encoding="utf-8"), ensure_ascii=False
    )

# 从问候语文本中读取“第*期”和“早安清华/晚安清华”
def get_mode(data):

    # 读取第几期
    re_date = re.search("第.期", data).group(0)

    # 早安世界/晚安清华
    re_morning = re.search("早安世界", data)
    re_night = re.search("晚安清华", data)

    if re_morning != None:
        attach_filename = "Certificate_morning.png"
        re_mode = re_morning.group(0)

    elif re_night != None:
        attach_filename = "Certificate_night.png"
        re_mode = re_night.group(0)

    subject = "【小伙伴计划】" + re_mode + "（" + re_date + "）打卡证书"
    return subject, attach_filename

# 发送邮件
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
            logger.error("Picture not found!")
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

        name_list = []
        address_list = []

        with open(self.config["info_csv"], "r") as csvfile:
            reader = csv.reader(csvfile)

            for row in reader:
                name_list.append(row[0])
                address_list.append(row[1])

        assert len(name_list) == len(address_list)

        for i in range(len(name_list)):
            to_address = address_list[i]
            name = name_list[i]
            picture_file = os.path.join(self.config["picture_dir"], name + ".jpg")
            msg = self.prepare_mail(name, to_address, picture_file)

            if msg != -1:
                info = str(i + 1) + ", " + name + ", " + to_address
            else:
                info = name + " 【未找到】"
                exit()

            # 发送真正的邮件
            # self.send_real_email(to_address, msg)

            logger.info(info)
        logger.info("All mails sent.")

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

    while True:
        config_json = "record.json"
        if not os.path.exists(config_json):
            reconfigure(config_json)

        configuration = load_configuration(config_json)

        get_file_tail = lambda n: os.path.split(configuration[n])[1]
        with open(configuration["greeting_txt"], "r", encoding="UTF-8") as f:
            greeting = f.read()

        subject, attach_filename = get_mode(greeting)

        info = (
            "标题 = "
            + subject
            + "\n\n附件名 = "
            + attach_filename
            + "\n\n收件人信息文件 = "
            + get_file_tail("info_csv")
            + "\n\n图片文件夹 = "
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
    
    # 以上是核查发送前的各项信息，确认无误后才发送
    # 注意MailSender.group_process中的send_real_email语句，建议在发送前先注释掉进行测试

    Bot = MailSender(configuration, greeting, subject, attach_filename)
    Bot.group_process()
