# 论文标题主题概览

语料为用户提供的中英文论文及其 Google Scholar 记录，共15篇：现有主页14篇，
加上 Scholar 页面所列2026年 Dehydrocostus Lactone/PTK7 肝癌论文。
包含1篇JCO会议摘要与1篇Asian Journal of Surgery读者来信；不按作者贡献或被引次数加权。
数据来源：https://scholar.google.com/citations?user=3xfQGl0AAAAJ
标题、年份、逐篇关键词/主题和词频见 publication-topics.json。

方法：人工制定可审查的中英关键词短语词典，再对标题进行不区分大小写的规则匹配。
合并文献计量/bibliometric、肿瘤/cancer/tumor/carcinoma等对应词。
每个词每篇最多计一次，词云字号由文献频次决定，不是标题中单词重复次数。
不等于作者关键词、摘要挖掘或系统文献计量研究；上位词与下位词可同时出现。

年份采用主页的正式卷期年：复吸干预论文2022（CNKI网络日期2021），PND为2024。
LMO7采用Scholar卷期年2026（导师页在线发表日期2025）；所以在线发表年口径会改变时间图。
JCO条目由用户提供，尚未独立核实正式链接。
演化图为标题主题的年份分布，圆点面积和数字表示篇数，线仅连接出现年份。
四个主题是解释性归类，不代表本人所有研究活动；未出现年份不代表没有科研工作。
免疫检查点词典归并了标题中的PD-1、TIM-3、Nectin-4相关表述。

复现：Python安装matplotlib、wordcloud、Pillow，运行 scripts/build_research_visuals.py。
默认中文字体为Windows微软雅黑；其他平台需修改font路径为本机可用CJK字体。
输出 assets/research-wordcloud.png、assets/research-evolution.png。
随机种子固定为42。语料增加或标题段落格式变化后，应复核抽取和主题分配。
