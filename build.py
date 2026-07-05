"""
hxsgr.github.io — 编译展示脚本

用法:
  python build.py            → 编译 article.json → index.html 并打开浏览器
  python build.py --no-open  → 只编译，不打开浏览器
"""

import json
import os
import re
import sys
import webbrowser

# 强制 UTF-8 输出，避免 Windows GBK 终端编码错误
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'article.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'index.html')


# ─── 渲染函数 ───────────────────────────────────────────

def escape_html(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def escape_attr(s):
    return s.replace('&', '&amp;').replace('"', '&quot;')


URL_RE = re.compile(r'(https?://[^\s<>"{}|\\^`\[\]()]+)')

def auto_link_urls(text):
    """将文本中的 URL 自动转为可点击链接"""
    escaped = escape_html(text)
    return URL_RE.sub(r'<a href="\1" target="_blank" rel="noopener">\1</a>', escaped)


def render_block(block):
    t = block['type']

    if t == 'heading':
        lvl = block.get('level', 2)
        return f'<h{lvl}>{escape_html(block["text"])}</h{lvl}>'

    elif t == 'paragraph':
        return f'<p>{auto_link_urls(block["text"])}</p>'

    elif t == 'image':
        img = f'<img src="{escape_attr(block["src"])}" alt="{escape_attr(block.get("caption") or "")}">'
        if block.get('caption'):
            return f'<figure>{img}<figcaption>{escape_html(block["caption"])}</figcaption></figure>'
        else:
            return f'<figure class="no-caption">{img}</figure>'

    elif t == 'divider':
        return '<hr>'

    else:
        return f'<!-- 未知类型: {t} -->'


# ─── 编译 HTML ──────────────────────────────────────────

def build():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        blocks = json.load(f)

    if blocks:
        body_lines = [render_block(b) for b in blocks]
        body_html = '\n      '.join(body_lines)
    else:
        body_html = '<p class="empty-hint">(empty) 还没有内容。运行 <code>python article.py</code> 添加示例内容。</p>'

    html = f'''<!DOCTYPE html>
<html lang="zh">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>hxsgr's Blog</title>
  <style>
    /* ── Reset & Base ── */
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans SC",
                   "PingFang SC", "Microsoft YaHei", sans-serif;
      line-height: 1.85;
      color: #333;
      background: #fafafa;
    }}

    article {{
      max-width: 720px;
      margin: 0 auto;
      padding: 60px 24px 80px;
    }}

    /* ── Headings ── */
    h1 {{ font-size: 2rem; margin: 48px 0 16px; color: #111; font-weight: 800; }}
    h2 {{ font-size: 1.5rem; margin: 40px 0 12px; color: #222; font-weight: 700; }}
    h3 {{ font-size: 1.2rem; margin: 32px 0 8px; color: #333; font-weight: 600; }}
    h1:first-child {{ margin-top: 0; }}

    /* ── Paragraphs ── */
    p {{ margin: 12px 0; font-size: 1.05rem; }}

    .empty-hint {{
      text-align: center;
      color: #999;
      font-size: 1.1rem;
      margin-top: 80px;
    }}
    .empty-hint code {{
      background: #eee;
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 0.95em;
    }}

    /* ── Divider ── */
    hr {{
      border: none;
      border-top: 2px dashed #ddd;
      margin: 36px 0;
    }}

    /* ── Images ── */
    figure {{
      margin: 28px 0;
      text-align: center;
    }}
    figure img {{
      max-width: 100%;
      height: auto;
      border-radius: 6px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    }}
    figcaption {{
      margin-top: 8px;
      font-size: 0.92rem;
      color: #888;
      font-style: italic;
    }}

    /* ── Footer ── */
    footer {{
      text-align: center;
      padding: 32px 24px;
      color: #bbb;
      font-size: 0.85rem;
      border-top: 1px solid #eee;
      margin-top: 40px;
    }}

    /* ── Responsive ── */
    @media (max-width: 600px) {{
      article {{ padding: 32px 16px 48px; }}
      h1 {{ font-size: 1.5rem; }}
      h2 {{ font-size: 1.25rem; }}
    }}
  </style>
</head>
<body>
  <article>
    {body_html}
  </article>
  <footer>Built with love by hxsgr</footer>
</body>
</html>'''

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'[OK] 编译完成 -> {OUTPUT_FILE}')
    print(f'   共 {len(blocks)} 个内容块')

    # ─── 打开浏览器 ──────────────────────────────────────
    if '--no-open' not in sys.argv:
        url = f'file:///{OUTPUT_FILE.replace(os.sep, "/")}'
        print(f'   [WWW] 打开浏览器: {url}')
        webbrowser.open(OUTPUT_FILE)


if __name__ == '__main__':
    build()
