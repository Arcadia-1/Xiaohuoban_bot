
# 获取学堂在线讨论区评论

这是一个动态渲染的页面，所以从对 Ajax 请求的响应中获取数据。



### 用法

除了 `main`  函数中可以改的保存文件名之外，仅需要改动两处。

![1588490360925](https://github.com/Arcadia-1/Xiaohuoban_bot/blob/master/xuetang_comment_spider/pictures%20for%20readme/1.png)

把 `INDEX_URL` 改成需要爬取的网站地址，把 `COOKIE` 改成对应的响应cookie。



### 具体说明

具体来说，以上二者可以通过网络→ <kbd>XHR</kbd> 获取。在浏览器中按 <kbd>F12</kbd> 应该可以得到以下界面，把右边的请求网址置换到上述 `INDEX_URL` 中，注意保留 `f-string` 中的括号（即把offset=和limit=后面的数字换成上述的括号）

![1588490490590](https://github.com/Arcadia-1/Xiaohuoban_bot/blob/master/xuetang_comment_spider/pictures%20for%20readme/2.png)



在下面的请求头中可以找到cookie，非常长的一串参数，替换代码中的COOKIE全局变量。注意保留r，因为cookie中含有一些字符可能会有转义问题。

![1588490635152](https://github.com/Arcadia-1/Xiaohuoban_bot/blob/master/xuetang_comment_spider/pictures%20for%20readme/3.png)