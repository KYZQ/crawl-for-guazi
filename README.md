# crawl-for-guazi
   爬取瓜子二手车数据</br>
   瓜子二手车网运用的反爬虫措施主要有js混淆，根据发送的原始header和js混淆生成特定的cookie才能访问到网站。</br>
   deal_head.py处理的数js混淆和生成特定的header。</br>
   值得注意的是，原始header的user-agent必须和你的电脑是相同的平台（windows、linux），不一致返回不了有效的cookie。</br>
   github上抄了这么多代码，这次回馈下大家。</br>
   by the way,用到的库大家自己看看，应该很清楚。</br>
                                                              created by Yanzhiquan
