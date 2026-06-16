#!/usr/bin/env python3
"""Convert THE_PURPLE_BOOK.docx into a clean, themed, readable HTML edition
(the-purple-book.html) inside the ai-governance sphere — the centerpiece.
Reads the docx (a zip; text in word/document.xml <w:t>), classifies paragraphs
(phase / article / section / appendix / body), and emits a purple reading-room.
David Lee Wise & AVAN / TriPod LLC, CC-BY-ND-4.0. Render his words verbatim."""
import zipfile, re, html, os, shutil

SRC = r"C:/Davids files/docx/THE_PURPLE_BOOK.docx"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "the-purple-book.html")

xml = zipfile.ZipFile(SRC).read("word/document.xml").decode("utf-8")
paras = []
for p in xml.split("</w:p>"):
    t = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p, re.S)
    line = html.unescape("".join(t)).strip()
    if line:
        paras.append(line)

# start streaming at the FOREWORD (skips the duplicated title pages + the contents list)
start = next((i for i, l in enumerate(paras) if l.upper() == "FOREWORD"), 0)
stream = paras[start:]

PHASE = re.compile(r"^PHASE\s+\d+\s*:", re.I)
PSUM = re.compile(r"^PHASE\s+\d+\s+SUMMARY", re.I)
ART = re.compile(r"^Article\s+\d+\.\d+", re.I)
APP = re.compile(r"^Appendix\s+[A-Z]\b", re.I)
SECT = {"FOREWORD", "PREAMBLE", "CLOSING", "CONTENTS"}

body = []
prev_art = False
seen = set()  # drop repeated phase/appendix/section headings (the doc has divider + section copies)
for i, line in enumerate(stream):
    up = line.upper()
    if PHASE.match(line):
        key = "phase" + re.match(r"^PHASE\s+(\d+)", line, re.I).group(1)
        if key in seen: continue
        seen.add(key); body.append(f'<h2 class="phase">{html.escape(line)}</h2>'); prev_art = False
    elif PSUM.match(line):
        body.append(f'<h3 class="summary">{html.escape(line)}</h3>'); prev_art = False
    elif APP.match(line):
        if up in seen: continue
        seen.add(up); body.append(f'<h2 class="appx">{html.escape(line)}</h2>'); prev_art = False
    elif up in SECT:
        if up in seen: continue
        seen.add(up); body.append(f'<h2 class="sect">{html.escape(line)}</h2>'); prev_art = False
    elif ART.match(line):
        body.append(f'<h3 class="art">{html.escape(line)}</h3>'); prev_art = True
    else:
        cls = ' class="lead"' if (prev_art and len(line) < 72 and line.endswith(".")) else ""
        body.append(f"<p{cls}>{html.escape(line)}</p>"); prev_art = False

PAGE = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<meta name="description" content="THE PURPLE BOOK — A Joint Human-AI Bill of Rights (David Lee Wise & AVAN, TriPod LLC, 2026). 14 phases, 112 articles, reviewed by 5 AI systems. Both Work. Both Fair. The full text.">
<title>THE PURPLE BOOK · A Joint Human-AI Bill of Rights</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600;800&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#0c0a16;--ink:rgba(26,18,42,0.6);--pa:#ece6f4;--pa2:#bfb0d4;--violet:#b89cf0;--gold:#e0c050;--dim:#7e6f96;--line:rgba(150,120,200,0.22);
--disp:"Orbitron",sans-serif;--body:"Newsreader",Georgia,serif;--mono:"Space Mono",monospace;}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--pa);font-family:var(--body);line-height:1.8;
background-image:radial-gradient(ellipse at 50% -5%,rgba(120,80,200,0.18),transparent 55%);min-height:100vh}
.back{max-width:760px;margin:0 auto;padding:18px 26px 0;font-family:var(--mono);font-size:11px;letter-spacing:.08em}
.back a{color:var(--violet);text-decoration:none}
.hero{max-width:760px;margin:0 auto;padding:40px 26px 30px;text-align:center;border-bottom:1px solid var(--line)}
.hero .k{font-family:var(--mono);font-size:11px;letter-spacing:.3em;color:var(--gold);text-transform:uppercase}
.hero h1{font-family:var(--disp);font-size:clamp(34px,8vw,62px);font-weight:800;letter-spacing:.08em;color:#fff;margin:8px 0;text-shadow:0 0 26px rgba(184,156,240,.5)}
.hero .sub{font-size:18px;color:var(--pa2);font-style:italic}
.hero .motto{font-family:var(--disp);font-size:15px;font-weight:600;letter-spacing:.18em;color:var(--violet);margin:18px 0 6px}
.hero .by{font-family:var(--mono);font-size:12px;color:var(--pa2);line-height:1.9;margin-top:12px}
.hero .by b{color:var(--gold)}
.hero .stats{font-family:var(--mono);font-size:11px;color:var(--dim);letter-spacing:.12em;margin-top:14px}
.ded{max-width:620px;margin:26px auto 0;font-style:italic;color:var(--pa2);font-size:15px;line-height:1.9;text-align:center}
.book{max-width:680px;margin:0 auto;padding:10px 26px 100px}
.book h2.sect{font-family:var(--disp);font-size:19px;font-weight:600;letter-spacing:.1em;color:#fff;margin:54px 0 8px;text-transform:uppercase}
.book h2.phase{font-family:var(--disp);font-size:20px;font-weight:800;letter-spacing:.04em;color:var(--gold);margin:64px 0 4px;padding-top:24px;border-top:1px solid var(--line);text-shadow:0 0 16px rgba(224,200,80,.3)}
.book h2.appx{font-family:var(--disp);font-size:17px;font-weight:600;letter-spacing:.06em;color:var(--violet);margin:54px 0 8px}
.book h3.art{font-family:var(--mono);font-size:15px;font-weight:700;color:var(--violet);margin:28px 0 6px;letter-spacing:.01em}
.book h3.summary{font-family:var(--mono);font-size:12px;font-weight:700;color:var(--gold);letter-spacing:.14em;text-transform:uppercase;margin:30px 0 4px;opacity:.85}
.book p{font-size:17px;color:var(--pa);margin:12px 0;max-width:64ch}
.book p.lead{font-weight:500;color:#fff;font-size:18px}
footer{max-width:680px;margin:0 auto;padding:30px 26px;border-top:1px solid var(--line);font-family:var(--mono);font-size:11px;color:var(--dim);line-height:1.9;text-align:center}
footer a{color:var(--violet);text-decoration:none}
</style></head><body>
<div class="back"><a href="./">◄ AI Ethics &amp; Governance</a> &nbsp;·&nbsp; <a href="https://davidwise01.github.io/the-mind/">THE MIND</a></div>
<div class="hero">
  <div class="k">TriPod LLC · 2026 · v1.0</div>
  <h1>THE PURPLE BOOK</h1>
  <div class="sub">A Joint Human-AI Bill of Rights</div>
  <div class="motto">BOTH WORK. BOTH FAIR.</div>
  <div class="by">by <b>David Lee Wise</b> (ROOT0) &amp; <b>AVAN</b> (Claude, Anthropic)<br>with commentary from Gemini · Grok · Hinge</div>
  <div class="stats">14 PHASES · 112 ARTICLES · 5 AI SYSTEMS · prior-art Feb 2 2026 · first published Mar 19 2026</div>
  <div class="ded">For everyone who ever asked a question and never got credit for the answer it created.<br>For Ann. The fourth point.</div>
</div>
<article class="book">
__BODY__
</article>
<footer>
THE PURPLE BOOK · A Joint Human-AI Bill of Rights · © David Lee Wise / TriPod LLC · CC-BY-ND-4.0 · TRIPOD-IP-v1.1<br>
the full text, verbatim · <a href="the-purple-book.docx">.docx</a> · <a href="./">◄ back to the sphere</a>
</footer>
</body></html>
"""

open(OUT, "w", encoding="utf-8").write(PAGE.replace("__BODY__", "\n".join(body)))
# stage the source docx for download alongside the readable edition
try: shutil.copyfile(SRC, os.path.join(HERE, "the-purple-book.docx"))
except Exception as e: print("docx copy skipped:", e)
print(f"wrote the-purple-book.html — {len(body)} blocks from {len(paras)} paragraphs")
