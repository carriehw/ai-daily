# -*- coding: utf-8 -*-
"""Build ai-daily index.html from data.json (single-file, inline CSS/JS)."""
import json, html, io, sys
from pathlib import Path

ROOT = Path(__file__).parent
data = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))

MKT = {"國際": "intl", "香港": "hk", "中國": "cn", "台灣": "tw"}
SEC_ID = {s: f"sec{i}" for i, s in enumerate(data["sections"])}

# group items preserving section order, global numbering
groups = {s: [] for s in data["sections"]}
for it in data["items"]:
    groups[it["section"]].append(it)

cards, n = {}, 0
for s in data["sections"]:
    out = []
    for it in groups[s]:
        n += 1
        e = {k: html.escape(str(it[k])) for k in it}
        out.append(f'''<article class="card">
<div class="ctop"><span class="no">{n:02d}</span><span class="chips"><span class="chip src">{e["source"]}</span><span class="chip mkt {MKT[it["market"]]}">{e["market"]}</span></span></div>
<h3><a href="{e["url"]}" target="_blank" rel="noopener noreferrer">{e["title"]}</a></h3>
<p class="sum">{e["summary"]}</p>
<p class="why"><b>點解重要</b>{e.get("why", "")}</p>
<div class="cfoot"><time>{e["time"]}</time><a class="more" href="{e["url"]}" target="_blank" rel="noopener noreferrer">閱讀原文 ↗</a></div>
</article>''')
    cards[s] = "\n".join(out)

total = n
stats = "".join(
    f'<a class="stat" href="#{SEC_ID[s]}"><b>{len(groups[s])}</b><span>{html.escape(s)}</span></a>'
    for s in data["sections"])
nav = "".join(
    f'<a href="#{SEC_ID[s]}">{html.escape(s)}<i>{len(groups[s])}</i></a>'
    for s in data["sections"])
sections_html = "\n".join(
    f'<section id="{SEC_ID[s]}"><h2>{html.escape(s)}<em>{len(groups[s])} 條</em></h2><div class="grid">{cards[s]}</div></section>'
    for s in data["sections"])

page = f'''<title>AI 日報 · {data["date"]}</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
:root{{--paper:#F7F8F5;--card:#FFFFFF;--ink:#1B2A2F;--muted:#5E6E6A;--jade:#0E7C66;--jade-d:#0A5C4C;--line:#DCE3DA}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font-family:"PingFang HK","PingFang TC","Microsoft JhengHei","Noto Sans TC",sans-serif;line-height:1.6}}
.serif{{font-family:"Songti TC","STSong","Noto Serif TC","PMingLiU",serif}}
.wrap{{max-width:1080px;margin:0 auto;padding:0 20px}}
/* hero */
header{{border-top:4px solid var(--jade);background:var(--card);border-bottom:1px solid var(--line)}}
.mast{{display:flex;align-items:baseline;justify-content:space-between;flex-wrap:wrap;gap:8px;padding:26px 0 6px}}
.mast h1{{font-family:"Songti TC","STSong","Noto Serif TC","PMingLiU",serif;font-size:clamp(30px,5vw,42px);margin:0;letter-spacing:.06em}}
.mast h1 span{{color:var(--jade)}}
.tag{{font-size:12px;letter-spacing:.28em;color:var(--muted);text-transform:uppercase}}
.dateline{{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:10px;padding:0 0 18px;color:var(--muted);font-size:14px}}
.dateline b{{color:var(--ink);font-weight:600}}
#share{{border:1px solid var(--jade);background:var(--jade);color:#fff;font:inherit;font-size:13px;padding:7px 18px;border-radius:4px;cursor:pointer}}
#share:hover{{background:var(--jade-d)}}
#share:focus-visible{{outline:2px solid var(--ink);outline-offset:2px}}
.stats{{display:grid;grid-template-columns:repeat(5,1fr);gap:1px;background:var(--line);border:1px solid var(--line);margin-bottom:26px}}
.stat{{background:var(--card);text-align:center;padding:14px 4px;text-decoration:none;color:var(--ink)}}
.stat b{{display:block;font-size:26px;color:var(--jade);font-variant-numeric:tabular-nums;font-family:"Songti TC","Noto Serif TC",serif}}
.stat span{{font-size:12px;color:var(--muted)}}
.stat:hover{{background:#EFF4EF}}
/* nav */
nav{{position:sticky;top:0;z-index:5;background:rgba(247,248,245,.95);backdrop-filter:blur(4px);border-bottom:1px solid var(--line)}}
nav .wrap{{display:flex;gap:6px;overflow-x:auto;padding:10px 20px}}
nav a{{white-space:nowrap;font-size:13px;color:var(--ink);text-decoration:none;border:1px solid var(--line);background:var(--card);padding:5px 12px;border-radius:99px}}
nav a i{{font-style:normal;color:var(--jade);margin-left:5px;font-variant-numeric:tabular-nums}}
nav a:hover{{border-color:var(--jade);color:var(--jade-d)}}
/* sections */
section{{scroll-margin-top:64px;margin:34px 0}}
h2{{font-family:"Songti TC","STSong","Noto Serif TC","PMingLiU",serif;font-size:22px;margin:0 0 14px;padding-bottom:8px;border-bottom:2px solid var(--ink);display:flex;align-items:baseline;gap:10px}}
h2 em{{font-style:normal;font-size:13px;color:var(--muted);font-family:"PingFang HK","Microsoft JhengHei",sans-serif;font-weight:400}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:14px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:6px;padding:16px 18px;display:flex;flex-direction:column;gap:8px}}
.ctop{{display:flex;justify-content:space-between;align-items:center;gap:8px}}
.no{{font-family:"Songti TC","Noto Serif TC",serif;font-size:20px;color:var(--jade);font-variant-numeric:tabular-nums}}
.chips{{display:flex;gap:6px;flex-wrap:wrap;justify-content:flex-end}}
.chip{{font-size:11px;padding:2px 9px;border-radius:99px;white-space:nowrap}}
.chip.src{{border:1px solid var(--line);color:var(--muted)}}
.chip.mkt{{color:#fff}}
.mkt.intl{{background:#2F5FA8}}.mkt.hk{{background:#8A2E4E}}.mkt.cn{{background:#B04A2F}}.mkt.tw{{background:#6E6428}}
.card h3{{margin:0;font-size:16.5px;line-height:1.45;text-wrap:balance}}
.card h3 a{{color:var(--ink);text-decoration:none}}
.card h3 a:hover{{color:var(--jade-d);text-decoration:underline}}
.card h3 a:focus-visible{{outline:2px solid var(--jade);outline-offset:2px}}
.sum{{margin:0;font-size:14px;color:#38484C;flex:1}}
.why{{margin:0;font-size:13px;line-height:1.55;color:var(--jade-d);background:#EDF4F0;border-left:3px solid var(--jade);padding:6px 10px;border-radius:0 4px 4px 0}}
.why b{{display:inline-block;font-size:11px;font-weight:600;color:#fff;background:var(--jade);border-radius:3px;padding:0 6px;margin-right:7px;vertical-align:1px}}
.cfoot{{display:flex;justify-content:space-between;align-items:center;font-size:12.5px;color:var(--muted);border-top:1px dashed var(--line);padding-top:8px}}
.more{{color:var(--jade);text-decoration:none;font-weight:500}}
.more:hover{{color:var(--jade-d);text-decoration:underline}}
/* footer */
footer{{border-top:1px solid var(--line);margin-top:44px;padding:22px 0 40px;font-size:13px;color:var(--muted)}}
footer b{{color:var(--ink)}}
#toast{{position:fixed;left:50%;bottom:28px;transform:translateX(-50%) translateY(20px);background:var(--ink);color:#fff;padding:9px 20px;border-radius:6px;font-size:13px;opacity:0;pointer-events:none;transition:opacity .25s,transform .25s}}
#toast.on{{opacity:1;transform:translateX(-50%) translateY(0)}}
#sharebox{{display:none;gap:8px;align-items:center;padding:0 0 16px}}
#sharebox.on{{display:flex}}
#sharebox input{{flex:1;font:inherit;font-size:13px;padding:7px 10px;border:1px solid var(--jade);border-radius:4px;color:var(--ink);background:#fff;min-width:0}}
#sharebox span{{font-size:12px;color:var(--muted);white-space:nowrap}}
@media (max-width:640px){{.stats{{grid-template-columns:repeat(2,1fr)}}.stats .stat:first-child{{grid-column:1/-1}}}}
@media (prefers-reduced-motion:reduce){{*{{transition:none!important}}}}
</style>
<header><div class="wrap">
<div class="mast"><h1>AI<span>・</span>日報</h1><span class="tag">AI Daily Briefing</span></div>
<div class="dateline"><span><b>{data["date_display"]}</b>　·　今日精選 <b>{total}</b> 條　·　國際／香港／中國／台灣</span><button id="share">分享俾朋友</button></div>
<div id="sharebox"><span>長按/全選複製：</span><input type="text" readonly value="https://carriehw.github.io/ai-daily/"></div>
<div class="stats">{stats}</div>
</div></header>
<nav><div class="wrap">{nav}</div></nav>
<main class="wrap">
{sections_html}
</main>
<footer><div class="wrap">
<p>今日共 <b>{total}</b> 條精選　·　時間為香港時間　·　每日更新</p>
<p>數據源：{html.escape(data["sources_note"])}</p>
<p>內容僅供資訊參考，不構成投資建議。</p>
</div></footer>
<div id="toast">連結已複製，可以直接 send 俾朋友</div>
<script>
const SHARE_URL="https://carriehw.github.io/ai-daily/";
function toast(msg){{const el=document.getElementById('toast');el.textContent=msg;el.classList.add('on');setTimeout(()=>el.classList.remove('on'),2200)}}
function legacyCopy(){{const ta=document.createElement('textarea');ta.value=SHARE_URL;ta.style.cssText='position:fixed;opacity:0';document.body.appendChild(ta);ta.select();let ok=false;try{{ok=document.execCommand('copy')}}catch(e){{}}ta.remove();return ok}}
function showBox(){{const b=document.getElementById('sharebox');b.classList.add('on');const inp=b.querySelector('input');inp.focus();inp.select()}}
document.getElementById('share').addEventListener('click',async()=>{{
  if(navigator.share){{try{{await navigator.share({{title:document.title,url:SHARE_URL}});return}}catch(e){{if(e.name==='AbortError')return}}}}
  try{{await navigator.clipboard.writeText(SHARE_URL);toast('連結已複製，可以直接 send 俾朋友');return}}catch(e){{}}
  if(legacyCopy()){{toast('連結已複製，可以直接 send 俾朋友');return}}
  showBox();
}});
</script>
'''

(ROOT / "index.html").write_text(page, encoding="utf-8")
print(f"OK index.html total={total} sections=" + ",".join(f"{s}:{len(groups[s])}" for s in data["sections"]))
