"""
Render the Marp-style Markdown slide decks to self-contained HTML.

Dependency-free (Python stdlib only). Splits each slides.md on '---' slide
breaks, does lightweight Markdown-to-HTML, and emits a keyboard-navigable deck
(arrow keys / space to move between slides).

Usage:
    python3 render_slides.py          # renders all six decks into slides-rendered/
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "slides-rendered"
OUT.mkdir(exist_ok=True)

MODULES = [
    "01-foundations", "02-how-ml-works", "03-llms-for-developers",
    "04-your-own-data", "05-agents-and-tools", "06-responsible-ai-apps",
    "07-decision-models", "08-rl-games",
]


def md_inline(text):
    """Minimal inline markdown: bold, italic, inline code, links."""
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def md_block_to_html(block):
    """Convert one slide's markdown body to HTML (headings, lists, code, tables, quotes)."""
    lines = block.split("\n")
    out, i = [], 0
    in_code = in_list = in_table = in_raw = False
    while i < len(lines):
        line = lines[i]
        # raw passthrough block: ```svg ... ``` emits contents verbatim (for inline SVG diagrams)
        if line.strip() == "```svg":
            in_raw = True; i += 1; continue
        if in_raw:
            if line.strip() == "```":
                in_raw = False
            else:
                out.append(line)  # NOT escaped — raw SVG/HTML
            i += 1; continue
        # fenced code
        if line.strip().startswith("```"):
            if not in_code:
                out.append("<pre><code>"); in_code = True
            else:
                out.append("</code></pre>"); in_code = False
            i += 1; continue
        if in_code:
            out.append(html.escape(line)); i += 1; continue
        # tables
        if "|" in line and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if re.match(r"^\s*[-: ]+\s*$", line.replace("|", "")):
                i += 1; continue  # separator row
            if not in_table:
                out.append("<table>"); in_table = True
            tag = "th" if (i + 1 < len(lines) and set(lines[i+1].replace("|","").strip()) <= set("-: ")) else "td"
            out.append("<tr>" + "".join(f"<{tag}>{md_inline(c)}</{tag}>" for c in cells) + "</tr>")
            i += 1; continue
        elif in_table:
            out.append("</table>"); in_table = False
        # headings
        m = re.match(r"^(#{1,6})\s+(.*)", line)
        if m:
            lvl = len(m.group(1)); out.append(f"<h{lvl}>{md_inline(m.group(2))}</h{lvl}>")
            i += 1; continue
        # blockquote
        if line.strip().startswith(">"):
            out.append(f"<blockquote>{md_inline(line.strip()[1:].strip())}</blockquote>")
            i += 1; continue
        # lists
        m = re.match(r"^\s*[-*]\s+(.*)", line)
        if m:
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{md_inline(m.group(1))}</li>")
            i += 1; continue
        m = re.match(r"^\s*\d+\.\s+(.*)", line)
        if m:
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{md_inline(m.group(1))}</li>")
            i += 1; continue
        if in_list and line.strip() == "":
            out.append("</ul>"); in_list = False
        # paragraph
        if line.strip():
            out.append(f"<p>{md_inline(line)}</p>")
        i += 1
    if in_list: out.append("</ul>")
    if in_table: out.append("</table>")
    if in_code: out.append("</code></pre>")
    return "\n".join(out)


def render(module):
    src = (ROOT / "lessons" / module / "slides.md").read_text(encoding="utf-8")
    # strip the marp front-matter (between leading --- ... ---)
    src = re.sub(r"^---\n.*?\n---\n", "", src, count=1, flags=re.DOTALL)
    # split on slide breaks (--- on its own line)
    raw_slides = re.split(r"\n---\n", src)
    slides_html = []
    for s in raw_slides:
        if s.strip():
            slides_html.append(f'<section class="slide">{md_block_to_html(s.strip())}</section>')
    body = "\n".join(slides_html)
    title = module.replace("-", " ").title()
    page = f"""<!doctype html><html><head><meta charset="utf-8">
<title>AI for Developers — {title}</title>
<style>
 body{{margin:0;background:#1f2a44;font-family:-apple-system,Segoe UI,Roboto,sans-serif}}
 .slide{{display:none;width:100vw;height:100vh;box-sizing:border-box;padding:6vh 8vw;
   background:#fff;color:#1a1a1a;overflow:auto}}
 .slide.active{{display:block}}
 h1{{color:#1f2a44;font-size:2.4em;margin:.2em 0}} h2{{color:#1f2a44;font-size:1.8em}}
 h3{{color:#2a3a5c}} p,li{{font-size:1.25em;line-height:1.5}}
 code{{background:#eef1f6;padding:1px 5px;border-radius:4px;font-size:.9em}}
 pre{{background:#0f1626;color:#d8e0f0;padding:16px;border-radius:8px;overflow:auto;font-size:1em}}
 pre code{{background:none;color:inherit}}
 blockquote{{border-left:4px solid #1f2a44;margin:.6em 0;padding:.3em 1em;color:#333;background:#f6f8fc}}
 table{{border-collapse:collapse;font-size:1.05em}} th,td{{border:1px solid #cbd2e0;padding:6px 12px;text-align:left}} th{{background:#eef1f6}}
 .nav{{position:fixed;bottom:12px;right:16px;color:#1f2a44;background:#fff;
   padding:4px 10px;border-radius:6px;font-size:.9em;opacity:.8}}
 svg{{display:block;margin:1em auto;max-width:92%;height:auto}}
 .diagram-caption{{text-align:center;color:#555;font-size:.95em;margin-top:.2em}}
</style></head><body>
{body}
<div class="nav"><span id="n">1</span> / {len(slides_html)} &nbsp;(← →)</div>
<script>
 let i=0; const s=document.querySelectorAll('.slide');
 function show(x){{s[i].classList.remove('active');i=(x+s.length)%s.length;s[i].classList.add('active');document.getElementById('n').textContent=i+1;}}
 show(0);
 document.addEventListener('keydown',e=>{{if(e.key==='ArrowRight'||e.key===' ')show(i+1);if(e.key==='ArrowLeft')show(i-1);}});
 document.addEventListener('click',()=>show(i+1));
</script></body></html>"""
    out_file = OUT / f"{module}.html"
    out_file.write_text(page, encoding="utf-8")
    return out_file, len(slides_html)


if __name__ == "__main__":
    for m in MODULES:
        f, n = render(m)
        print(f"  {m}: {n} slides -> {f.name}")
    print(f"\nRendered {len(MODULES)} decks into {OUT}/ (open any .html in a browser; arrow keys to navigate)")
