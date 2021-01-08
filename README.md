# Kitchen_Helper
**厨房好帮手**  
下厨房网址：[http://www.xiachufang.com](http://www.xiachufang.com)  
**功能要求**  
1. 每周爬取下厨房网站的本周最受欢迎（最近流行）菜品做法数据，存入数据库。  
数据项：菜品名字、材料、做法、效果图、链接地址。  
2. 开发Python页面，实现可通过搜索关键字查询数据库里的菜品做法，若数据库里无相关菜品数据，可实时到下厨房网站查询。  
查询结果显示信息包括：菜品名字、材料、做法、效果图、链接地址。  
  
**注意：为了减少频繁访问对下厨房网站的影响，本项目减少了实际数据获取数量，仅获取少量数据用于学习用途**  
**访问下厨房网的次数过多会导致网页返回 403 响应码，练习时请尽量减少获取数据量**  
  
~~**发现问题：** 由于下厨房网站有防盗链措施，目前可视化界面无法加载效果图。~~  
  
**2021年1月8日更新：** 已解决效果图无法加载问题，可视化展示时自动下载对应效果图到本地（不会重复下载相同的效果图，当本地的效果图数量达到100时会自动清理文件）  
