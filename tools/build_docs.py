#!/usr/bin/env python3
"""Builds the 5 read pages (*.html) and 5 PDFs (pdf/*.pdf) from src/*.md + documents.json.
Run by CC only (no workflow). Needs: python3, `pip install markdown`, Node + Playwright (Chromium), a Thai font (Loma / Noto Sans Thai).
Usage: python3 tools/build_docs.py [--no-pdf]
"""
import json, re, subprocess, sys, html, tempfile, os
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, 'documents.json'), encoding='utf-8'))
BASE = 'https://docs.janishammer.com'

# SEO text per page (measured: title 50-60, description 140-160 characters)
SEO = {
 'studio-rules': ('Studio Rules — I-Flex Pilates | Janishammer Documents',
  'Studio Rules for renting the I-Flex Pilates studio: booking, registration, payment and deposit, who may use it, teachers, guests and safety. English and Thai.'),
 'safety-consent': ('Safety Consent — I-Flex Pilates | Janishammer Documents',
  'Safety Consent for renting the I-Flex Pilates studio: health, never training alone, age, own risk, emergency and consent. English and Thai, with PDF download.'),
 'equipment-care-damage': ('Equipment Care and Damage — I-Flex | Janishammer Docs',
  'Equipment Care and Damage for renting the I-Flex Pilates studio: care before and after each session, damage charges, refundable deposit. English and Thai.'),
 'privacy-notice': ('Privacy Notice — I-Flex Pilates | Janishammer Documents',
  'Privacy Notice of Janishammer, operating I-Flex Pilates: what we collect, why, who sees it, how long we keep it and your rights. English and Thai, with PDF.'),
 'trainer-pool-agreement': ('Trainer Pool Basic Agreement — I-Flex | Janishammer Docs',
  'Basic agreement for the I-Flex freelance trainer list and the free-class pool: verification, commitment, cancellation and no-show policy. English and Thai.'),
}

def esc(s): return html.escape(s, quote=True)

def parse(path):
    t = open(path, encoding='utf-8').read()
    m = re.match(r'---\n(.*?)\n---\n(.*)', t, re.S)
    fm = dict(l.split(': ', 1) for l in m.group(1).splitlines())
    body = m.group(2)
    en, th = re.split(r'^## ภาษาไทย\s*$', body, flags=re.M)
    en = re.sub(r'^## English\s*$', '', en, flags=re.M)
    return fm, en.strip(), th.strip()

def md2html(s):
    h = markdown.markdown(s, extensions=['sane_lists'])
    h = h.replace('<li>[ ] ', '<li class="check">')
    return h

def head(title, desc, url, css_font=True):
    assert 50 <= len(title) <= 60, (title, len(title))
    assert 140 <= len(desc) <= 160, (desc, len(desc))
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:type" content="website">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap">
<link rel="stylesheet" href="/assets/style.css">
</head>'''

def banner_html():
    b = D['banner']
    return f'<div class="banner" role="note"><p lang="en">{esc(b["en"])}</p><p lang="th">{esc(b["th"])}</p></div>'

LANG_JS = '''<script>
(function () {
  document.documentElement.className += ' js';
  var en = document.getElementById('en'), th = document.getElementById('th');
  var bE = document.getElementById('b-en'), bT = document.getElementById('b-th');
  function show(l) {
    en.hidden = l !== 'en'; th.hidden = l !== 'th';
    bE.setAttribute('aria-pressed', l === 'en'); bT.setAttribute('aria-pressed', l === 'th');
  }
  bE.onclick = function () { show('en'); window.scrollTo(0, 0); };
  bT.onclick = function () { show('th'); window.scrollTo(0, 0); };
  show('en');
})();
</script>'''

def read_page(doc, fm, en, th):
    title, desc = SEO[doc['id']]
    ent = D['entity']
    return head(title, desc, f'{BASE}{doc["page"]}') + f'''
<body>
<div class="langbar"><div class="inner">
<button type="button" id="b-en" aria-pressed="true">EN</button>
<button type="button" id="b-th" aria-pressed="false">ไทย</button>
</div></div>
<header class="band"><div class="card">
<h1>{esc(fm['title_en'])}</h1>
<p class="sub" lang="th">{esc(fm['title_th'])}</p>
<p class="issuer">{esc(ent['en'])}<br><span lang="th">{esc(ent['th'])}</span></p>
<p class="ver">{esc(fm['version_line_en'])}<br><span lang="th">{esc(fm['version_line_th'])}</span></p>
</div></header>
<main>
{banner_html()}
<a class="back" href="/">← All documents / <span lang="th">กลับไปรายการเอกสาร</span></a>
<section class="lang" id="en" lang="en">
<h2>English</h2>
{md2html(en)}
</section>
<section class="lang" id="th" lang="th">
<h2>ภาษาไทย</h2>
{md2html(th)}
</section>
<p class="dl"><a class="btn pdf" href="{doc['pdf']}" download>Download PDF / ดาวน์โหลด PDF</a></p>
<a class="back" href="/">← All documents / <span lang="th">กลับไปรายการเอกสาร</span></a>
</main>
<footer>Reference documents only · <span lang="th">เอกสารอ้างอิงเท่านั้น</span></footer>
{LANG_JS}
</body>
</html>
'''

PDF_CSS = '''@page { size: A4; margin: 16mm 15mm 20mm 15mm; }
body { font-family: "Loma","Noto Sans Thai","Garuda",sans-serif; font-size: 11pt; line-height: 1.55; color: #1A1A1A; margin: 0; }
.banner { background: #FFD700; border-left: 6px solid #1A1A1A; padding: 8px 10px; margin: 0 0 10px; font-weight: bold; font-size: 10pt; }
.banner p { margin: 0 0 5px; } .banner p:last-child { margin: 0; }
h1 { font-size: 18pt; margin: 6px 0 2px; } .sub { font-size: 13pt; margin: 0 0 6px; }
.issuer, .ver { margin: 2px 0; font-size: 10pt; }
h2 { font-size: 14pt; border-bottom: 2px solid #FFD700; padding-bottom: 3px; margin: 14px 0 8px; }
h3 { font-size: 12pt; margin: 12px 0 4px; break-after: avoid; }
ul { margin: 4px 0 8px; padding-left: 18px; } li { margin: 0 0 4px; }
li.check { list-style: none; margin-left: -18px; padding-left: 20px; position: relative; }
li.check::before { content: ""; position: absolute; left: 0; top: 4px; width: 9px; height: 9px; border: 1.5px solid #1A1A1A; }
blockquote { margin: 8px 0; padding: 4px 10px; border-left: 4px solid #FFD700; }
hr { border: 0; border-top: 1.5px solid #FFD700; }
.pb { break-before: page; }'''

def pdf_html(doc, fm, en, th):
    ent = D['entity']
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>{esc(fm['title_en'])}</title><style>{PDF_CSS}</style></head><body>
{banner_html()}
<h1>{esc(fm['title_en'])}</h1><p class="sub" lang="th">{esc(fm['title_th'])}</p>
<p class="issuer">{esc(ent['en'])}<br><span lang="th">{esc(ent['th'])}</span></p>
<p class="ver">{esc(fm['version_line_en'])}<br><span lang="th">{esc(fm['version_line_th'])}</span></p>
<section lang="en"><h2>English</h2>{md2html(en)}</section>
<section lang="th" class="pb"><h2>ภาษาไทย</h2>{md2html(th)}</section>
</body></html>'''

PDF_JS = '''const {chromium}=require('playwright');
(async()=>{const jobs=JSON.parse(process.argv[2]);const b=await chromium.launch();
for(const j of jobs){const p=await b.newPage();await p.goto('file://'+j.html);
const foot='<div style="width:100%;font-size:8px;font-family:Loma,sans-serif;text-align:center;color:#1A1A1A;">DRAFT · ฉบับร่าง — '+j.title+' — page <span class="pageNumber"></span> / <span class="totalPages"></span></div>';
await p.pdf({path:j.pdf,format:'A4',printBackground:true,displayHeaderFooter:true,headerTemplate:'<div></div>',footerTemplate:foot,margin:{top:'16mm',bottom:'20mm',left:'15mm',right:'15mm'}});await p.close();}
await b.close();})();'''

def main():
    pdf = '--no-pdf' not in sys.argv
    tmp = tempfile.mkdtemp()
    jobs = []
    for doc in D['documents']:
        fm, en, th = parse(os.path.join(ROOT, 'src', doc['id'] + '.md'))
        assert fm['id'] == doc['id']
        open(os.path.join(ROOT, doc['id'] + '.html'), 'w', encoding='utf-8').write(read_page(doc, fm, en, th))
        h = os.path.join(tmp, doc['id'] + '.html')
        open(h, 'w', encoding='utf-8').write(pdf_html(doc, fm, en, th))
        jobs.append({'html': h, 'pdf': os.path.join(ROOT, 'pdf', doc['id'] + '.pdf'), 'title': doc['title_en']})
    if pdf:
        js = os.path.join(tmp, 'pdf.js'); open(js, 'w').write(PDF_JS)
        env = dict(os.environ, NODE_PATH=os.environ.get('NODE_PATH', '/opt/node22/lib/node_modules'))
        subprocess.run(['node', js, json.dumps(jobs)], check=True, env=env)
    print('built', len(jobs), 'pages', '+ PDFs' if pdf else '(no PDFs)')

if __name__ == '__main__':
    main()
