import re,json,collections
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from wordcloud import WordCloud
root=Path(__file__).resolve().parents[1]
s=(root/"README.md").read_text(encoding="utf-8")
section=s.split("## Publications")[1].split("## Selected public projects")[0]
papers=[];year=None
for line in section.splitlines():
    if re.fullmatch(r"### \d{4}",line): year=int(line[-4:])
    if line.startswith("**") and line.rstrip().endswith("**") and len(line)>15:
        title=line.strip()[2:-2]
        if title.startswith("基于CiteSpace"): y=2023
        elif title.startswith("社会医学"): y=2023
        elif title.startswith("预防脱毒"): y=2022
        elif title.startswith("基本公共"): y=2020
        elif title.startswith("大学生"): y=2019
        else:y=year
        papers.append(dict(year=y,title=title))
# Also supplied in the user's Google Scholar profile, but not previously featured in README.
papers.append(dict(year=2026,title="Dehydrocostus Lactone Suppresses Hepatocellular Carcinoma by Inhibiting Protein Tyrosine Kinase-7 Mediated β-Catenin Signaling"))
assert len(papers)==15,len(papers)
# Auditable phrase dictionary: one count per paper; bilingual equivalents share a label.
terms={
"文献计量 / Bibliometrics":r"bibliometric|文献计量",
"肿瘤 / Cancer":r"cancer|tumor|carcinoma",
"肺癌 / Lung cancer":r"lung cancer",
"CiteSpace":r"citespace",
"免疫检查点":r"immune checkpoint|TIM-3|programmed cell death protein-1",
"巨噬细胞":r"macrophage",
"吞噬 / Phagocytosis":r"phagocytosis",
"LMO7":r"LMO7","LRP1":r"LRP1","Nectin-4":r"Nectin-4","TIM-3":r"TIM-3",
"PD-1":r"programmed cell death protein-1",
"焦亡 / Pyroptosis":r"pyroptosis","腺病毒":r"adenovirus",
"肿瘤内皮细胞":r"tumor endothelial cells",
"孟德尔随机化":r"Mendelian randomization",
"人格与精神特征":r"personality and psychiatric traits",
"静脉麻醉":r"intravenous anesthesia","PND":r"\bPND\b",
"公共卫生服务":r"公共卫生服务","互联网医疗":r"互联网.医疗",
"社会医学教学":r"社会医学教学","戒毒与复吸":r"戒毒|脱毒|复吸",
"心理社会因素":r"心理社会因素","临床试验":r"clinical trials",
"回顾性队列":r"retrospective cohort","肝细胞癌":r"hepatocellular carcinoma",
"PTK7":r"protein tyrosine kinase.?7","β-Catenin":r"β.Catenin",
"Dehydrocostus lactone":r"Dehydrocostus Lactone"}
themes={
"公共卫生与社会医学":r"公共卫生|互联网|社会医学|戒毒|脱毒|复吸",
"麻醉与PND":r"anesthesia|\bPND\b",
"肺癌与临床/因果研究":r"lung cancer",
"肿瘤免疫与分子机制":r"LMO7|Nectin-4|TIM-3|pyroptosis|hepatocellular"}
freq=collections.Counter()
years=list(range(2019,2027))
counts={t:[0]*len(years) for t in themes}
for p in papers:
 p["keywords"]=[k for k,v in terms.items() if re.search(v,p["title"],re.I)]
 p["themes"]=[k for k,v in themes.items() if re.search(v,p["title"],re.I)]
 freq.update(p["keywords"])
 for t in p["themes"]:counts[t][years.index(p["year"])]+=1
(root/"research/publication-topics.json").write_text(json.dumps({"papers":papers,"keyword_document_frequency":dict(freq),"theme_counts":counts,"years":years},ensure_ascii=False,indent=2),encoding="utf-8")
font="C:/Windows/Fonts/msyh.ttc"
fp=FontProperties(fname=font)
plt.rcParams["font.family"]=fp.get_name()
plt.rcParams["axes.unicode_minus"]=False
bg="#0b1020"; fg="#e7edff";muted="#a8b6d8"
palette=["#68efd0","#86b8ff","#c3a0ff","#f4c66c"]
wc=WordCloud(font_path=font,width=2000,height=820,background_color=bg,prefer_horizontal=1,
             random_state=42,max_font_size=170,min_font_size=20,relative_scaling=.6,
             margin=14,collocations=False).generate_from_frequencies(freq)
wc.recolor(color_func=lambda word,**kw:palette[list(freq).index(word)%4],random_state=42)
fig,ax=plt.subplots(figsize=(16,8),facecolor=bg)
ax.imshow(wc);ax.axis("off")
fig.text(.06,.94,"RESEARCH VOCABULARY",color=fg,fontsize=25,weight="bold")
fig.text(.06,.89,"中英文论文标题关键词 · 15 篇 · 2019–2026",color=muted,fontsize=14)
fig.text(.06,.045,"字号反映包含该关键词的论文数；同义词归并，每篇最多计一次。主题词可重叠，不按被引次数加权。",color=muted,fontsize=11)
fig.savefig(root/"assets/research-wordcloud.png",dpi=180,facecolor=bg,bbox_inches="tight")
plt.close(fig)
fig,ax=plt.subplots(figsize=(16,7),facecolor=bg)
ax.set_facecolor(bg)
for i,(theme,values) in enumerate(counts.items()):
 active=[(y,n) for y,n in zip(years,values) if n]
 if len(active)>1:ax.plot([a[0] for a in active],[i]*len(active),color=palette[i],alpha=.35,lw=2,zorder=1)
 for y,n in active:
  ax.scatter(y,i,s=260*n,color=palette[i],edgecolors=bg,linewidth=2,zorder=2)
  ax.text(y,i,str(n),ha="center",va="center",color=bg,weight="bold",fontsize=12)
ax.set_yticks(range(4),list(counts),color=fg,fontsize=14)
ax.set_xticks(years,years,color=muted,fontsize=12)
ax.set_xlim(2018.6,2026.5);ax.set_ylim(3.65,-.65)
ax.grid(axis="x",color="#26314c",lw=.7);ax.tick_params(length=0,pad=15)
for spine in ax.spines.values():spine.set_visible(False)
fig.subplots_adjust(left=.25,top=.78,bottom=.2)
fig.text(.07,.94,"RESEARCH THROUGH TIME",color=fg,fontsize=25,weight="bold")
fig.text(.07,.87,"公共卫生 / 社会医学 → 临床与文献计量研究 → 肿瘤免疫与分子机制",color=muted,fontsize=14)
fig.text(.07,.075,"圆点面积及数字 = 当年该主题论文数；连线仅连接有记录年份，不表示中间年份持续产出或因果关系。",color=muted,fontsize=11)
fig.text(.07,.035,"标题规则归类，可多标签；2021 无本语料正式卷期论文。纳入会议摘要及读者来信，不等同于个人研究投入。",color=muted,fontsize=11)
fig.savefig(root/"assets/research-evolution.png",dpi=180,facecolor=bg,bbox_inches="tight")
plt.close(fig)
print("papers:",len(papers),"themes:",counts,"top keywords:",freq.most_common(5))

