# doubanBookComment
豆瓣读书Top250图书评论数据集

小文件保存在GitHub里，大文件存储在百度网盘
链接：https://pan.baidu.com/s/1u7sD0rDyiBHrfK8sdPSqGw 
提取码：7461

评论数据于2022年采集，过程实在不易，假如这个数据集对你的研究有帮助，我也很会高兴。有什么需要沟通交流的也可以issue me。

数据集规模有367万条评论数据，68万本图书信息

## 数据打开方式
文件格式是Python的pickle序列化文件，经过实验可以通过以下方式打开

import pandas as pd

newBookInformation = pd.read_pickle("./newBookInformation")

df = pd.DataFrame(newBookInformation )

打开即为DataFrame类型
想要保存为csv文件可以通过这行代码保存

df.to_csv("./newBookInformation.csv",index=False)

数据应该是gb2312编码

## 有兴趣的话也可以引用在下的文章，万分感谢：

[1]杨群峰. 基于知识图谱的可解释图书推荐研究[D].安徽工程大学,2024.DOI:10.27763/d.cnki.gahgc.2023.000087.

[2]杨群峰,王忠群,皇苏斌.基于情感分析和概念词典的图书推荐方法[J].安徽工程大学学报,2022,37(05):59-65.
