import json,re,html
from pathlib import Path
from urllib.parse import quote
from wordcloud import WordCloud
root=Path(__file__).resolve().parents[1]
data=json.loads((root/"research/publication-topics.json").read_text(encoding="utf-8"))
readme=(root/"README.md").read_text(encoding="utf-8")
def norm(s):return re.sub(r"[\W_]+","",s).lower()
for p in data["papers"]:
    key=norm(p["title"])
    for block in re.split(r"\n\s*\n",readme):
        if key in norm(block):
            links=re.findall(r"\]\((https?://[^)]+)\)",block)
            if links:p["url"]=links[-1];break
    if "url" not in p:
        p["url"]="https://scholar.google.com/scholar?q="+quote('"'+p["title"]+'"')
        p["link_note"]="检索该题名"
    else:p["link_note"]="打开论文记录"
wc=WordCloud(font_path="C:/Windows/Fonts/msyh.ttc",width=1500,height=800,background_color="#0b1020",prefer_horizontal=1,random_state=42,max_font_size=125,min_font_size=18,margin=14,collocations=False).generate_from_frequencies(data["keyword_document_frequency"])
colors=["#68efd0","#86b8ff","#c3a0ff","#f4c66c"]
words=[]
for i,((word,freq),size,pos,orientation,color) in enumerate(wc.layout_):
    y,x=pos
    words.append(f'<text role="button" tabindex="0" aria-label="{html.escape(word)}，查看相关文章" data-word="{html.escape(word)}" x="{x}" y="{y}" font-size="{size}" fill="{colors[i%4]}" dominant-baseline="hanging">{html.escape(word)}</text>')
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Yu Qiao · 交互式论文词云</title><style>
*{box-sizing:border-box}body{margin:0;background:#0b1020;color:#e7edff;font:16px/1.6 system-ui,"Microsoft YaHei",sans-serif}
main{max-width:1400px;margin:auto;padding:40px 24px}h1{font-size:clamp(24px,4vw,40px);margin:0}p{color:#a8b6d8}
a{color:#68efd0}svg{width:100%;background:#10182a;border-radius:20px;margin:20px 0}
svg text{font-family:"Microsoft YaHei",sans-serif;cursor:pointer;transition:opacity .15s}svg text:hover,svg text:focus{opacity:.65;outline:none;stroke:currentColor;stroke-width:.5}
#results{background:#141e33;padding:24px;border-radius:16px}li{margin:16px 0}button,select{background:#1b2945;border:1px solid #435779;color:#e7edff;padding:10px;border-radius:8px}
small{color:#a8b6d8}footer{margin-top:30px}
</style><main><a href="https://github.com/Yu-Qiao-sjtu">← GitHub 主页</a>
<h1>Research vocabulary · 点击关键词探索论文</h1><p>15 篇中英文论文 · 2019–2026。点击词语：单篇直接打开，多篇显示列表。也可用键盘 Tab 和 Enter 操作。</p>
<label for="terms">按关键词查找：</label> <select id="terms"><option value="">选择关键词</option></select>
<svg viewBox="0 0 1500 800" aria-label="交互式论文关键词词云">WORDS</svg>
<section id="results" aria-live="polite"><h2>选择一个关键词</h2><p>这里将列出相关论文及发表年份。</p></section>
<footer><small>词频按包含关键词的论文数计，同义词归并；包括会议摘要与读者来信。无直接论文链接的条目提供题名检索。</small>
<br><a href="https://github.com/Yu-Qiao-sjtu/Yu-Qiao-sjtu/blob/main/research/README.md">方法与数据说明</a></footer></main>
<script>
const papers=DATA;const terms=document.querySelector('#terms'),results=document.querySelector('#results');
const keywords=[...new Set(papers.flatMap(p=>p.keywords))].sort();
keywords.forEach(k=>{const o=document.createElement('option');o.value=k;o.textContent=k;terms.append(o)});
function choose(word){
 const matches=papers.filter(p=>p.keywords.includes(word)).sort((a,b)=>b.year-a.year);
 terms.value=word;results.replaceChildren();
 const title=document.createElement('h2');title.textContent=word+' · '+matches.length+' 篇';results.append(title);
 const list=document.createElement('ol');
 matches.forEach(p=>{const item=document.createElement('li'),a=document.createElement('a');a.href=p.url;a.target='_blank';a.rel='noopener noreferrer';a.textContent=p.title;
 item.append(a,document.createElement('br'));const info=document.createElement('small');info.textContent=p.year+' · '+p.link_note;item.append(info);list.append(item)});
 results.append(list);
 if(matches.length===1)window.open(matches[0].url,'_blank','noopener,noreferrer');
 else results.scrollIntoView({behavior:'smooth',block:'nearest'});
}
document.querySelectorAll('[data-word]').forEach(el=>{
 el.addEventListener('click',()=>choose(el.dataset.word));
 el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();choose(el.dataset.word)}});
});
terms.addEventListener('change',()=>{if(terms.value)choose(terms.value)});
</script></html>'''
page=page.replace('WORDS',''.join(words)).replace('DATA',json.dumps(data["papers"],ensure_ascii=False).replace('</','<\\/'))
metrics=json.loads((root/"research/journal-metrics.json").read_text(encoding="utf-8"))
metric_rows="".join("<tr>"+"".join("<td>"+html.escape(str(v))+"</td>" for v in row[:4])+"<td><a href=\""+html.escape(row[5],quote=True)+"\">官方来源</a></td></tr>" for row in metrics["rows"])
metric_section='<section><h2>期刊影响因子与 JCR 分区</h2><p>核查于 2026-09-09，目标为 2025 JIF（2026 年发布）。未明确年度的官网展示值单独标注；JIF 为期刊指标。</p><div style="overflow-x:auto"><table><thead><tr><th>期刊</th><th>JIF</th><th>年度</th><th>分区 / 核实状态</th><th>来源</th></tr></thead><tbody>'+metric_rows+'</tbody></table></div><p><a href="https://github.com/Yu-Qiao-sjtu/Yu-Qiao-sjtu/blob/main/research/journal-metrics-2026.md">完整核实说明与论文对应关系</a></p></section>'
page=page.replace('<footer>',metric_section+'<footer>').replace('</style>','td,th{padding:10px;text-align:left;border-bottom:1px solid #435779}table{width:100%;border-collapse:collapse}</style>')
(root/"docs").mkdir(exist_ok=True)
(root/"docs/index.html").write_text(page,encoding="utf-8")
assert all(p.get("url","").startswith("https://") for p in data["papers"])
print("Interactive terms:",len(words),"papers:",len(data["papers"]))
