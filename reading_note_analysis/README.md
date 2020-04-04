# 整理微信群读书打卡记录

张智帅 2020年4月4日

[TOC]

## 步骤一：从聊天记录开始

通过微信自带的邮件转发方式，把聊天记录转为文字，教程参考了[^聊天记录导出]。以下根据读书打卡群的聊天记录进行示范。**平台是华为手机 + 清华邮箱，苹果手机或者其他邮箱可能会略有不同。**

[^聊天记录导出]:https://baijiahao.baidu.com/s?id=1615015918880634712&wfr=spider&for=pc

首先长按聊天记录，多选需要转出的聊天记录（**每次最多 $100$ 条**），点击右下角的邮件符号。

![1585988953225](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585988953225.png)



弹出一个选项框，点击第一个<kbd>电子邮件</kbd>。

![1585989513519](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585989513519.png)

弹出邮件发送界面。**如果没有绑定过邮箱需要首先进行邮箱绑定，这个邮箱似乎无法更改（目前没有查到可行的更改办法，如果您有方法更改，希望您能告知）。**

![1585989708621](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585989708621.png)

前往发送到的邮箱查看邮件。

![1585989786339](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585989786339.png)

邮件内容如下：

![1585989917696](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585989917696.png)



**【注意】**有同学使用苹果 + QQ 邮箱，转发出的聊天记录所有的换行都没了，目前没有较好的处理办法。如果有类似的情况，建议换人来导出聊天记录。

![1585990058399](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585990058399.png)

## 步骤二：复制到 txt 文本文件

把聊天记录主题内容（除了首句“……，请查收。”和最后的小尾巴之外的内容，**如上上图所示**）复制，粘贴到一个 txt 文本文件中。

![1585990886710](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585990886710.png)



## 步骤三：使用 python 进行处理

代码放在了 Github 上：https://github.com/Arcadia-1/Xiaohuoban_bot/blob/master/reading_note_analysis/

运行程序 ``note_processing_v3.py``，首先弹出一个对话框，选择 txt 数据源文件。此处选择刚刚保存的”聊天记录.txt“。

![1585991160430](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585991160430.png)

其次弹出一个对话框，问聊天记录是用什么手机发出来的，本示例用的华为手机，所以选择 Android。点击 OK。

![1585991214531](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585991214531.png)

再次弹出一个对话框，问日期形式的正则表达式是什么。这是因为不同手机、不同邮箱导出的时间、日期格式不同，而本程序是依赖时间与日期来进行聊天记录划分的。

![1585991513810](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585991513810.png)

选哪个，取决于在导出的文本里日期是什么格式的。

【情况 1】Android 手机导出的日期在发言之前，其形式如下图第一行所示：四个数字-两个数字-两个数字，所以选第一个，如上图所示。

![1585991716754](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585991716754.png)

【情况 2】苹果手机导出的聊天记录可能会有这样的形式，日期在发言之后，则选择第二个选项。

![1585992111811](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585992111811.png)

【情况 3】苹果手机导出的聊天记录也可能会有这样的形式，日期在发言之后，**而且两边有 # 号（有的井号是半角符号#，也有的是全角符号＃）**，则选择第三个选项。

![1585991910483](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585991910483.png)



设置好以后，点击<kbd>OK</kbd>按钮，在目录下产生一个文件夹，与 txt 文件的文件名一致。

![1585992187129](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585992187129.png)

其中，每个发言者的发言都被整理到了相应的 Word 文件中了，并且有一个合集文件汇总了所有人的发言。

![1585992441408](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585992441408.png)

以上示例只有一个发言者，效果不明显。



## 效果示例

按照以上三个步骤，把《高效能人士的七个习惯》读书打卡群中的所有读书感想发言转出，复制到”高效能人士.txt“文件中，运行程序，则产生相应的文件夹。按照人名归好类的感想就整理好了。

![1585992570904](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585992570904.png)

打开合集文件可见，从2020年3月15日建群到2020年4月4日，$23 $ 位同学一共产生了近 $60$ 万字的读书感想。

![1585993032292](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585993032292.png)



各位参与者的发言也都按照日期顺序整理好了，以李济深老师的读书心得为例：

![1585992884285](C:\Users\hasee\AppData\Roaming\Typora\typora-user-images\1585992884285.png)



