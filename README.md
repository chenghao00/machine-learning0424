# machine-learning0424
0424开始机器学习

1、数据分析罗志祥微博评论
1）抓取api接口数据转换成DataFrame格式，保存至data.csv
2）进行数据预处理，评论去重，时间格式转换
3）合并评论信息，使用TF-IDF算法提取关键词， 同时导入停用词，并把关键词中的停用词筛选掉，返回word_num_selected
4）得到word_num_selected，生成词云
