# ftspiders

日常工作中自己用到的一些爬虫, 基于python3.5.

# 内容

* get_zycg: 爬取中央采购网所有软件类公司名称.
* get_zycg_detail: 从36Kr爬取公司详情, 由于36Kr每天只能查200个公司信息, 所以和上面的爬虫分开了.

# 用法

典型的**scrapy**项目, 首先使用`pip install -r requirments.txt`安装依赖, 然后使用`scrapy crawl <name of spider>`即可运行对应爬虫.
