"""Check the actual docs-root deployment boundary, not just repository paths."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT=Path(__file__).resolve().parents[1]/"docs"

class Links(HTMLParser):
    def __init__(self):super().__init__();self.targets=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ("href","src") and value:self.targets.append(value)

def main():
    errors=[];count=0
    for page in ROOT.glob("*.html"):
        parser=Links();parser.feed(page.read_text())
        for target in parser.targets:
            u=urlsplit(target)
            if u.scheme or u.netloc or not u.path:continue
            count+=1;p=(page.parent/unquote(u.path)).resolve()
            if not p.is_relative_to(ROOT.resolve()) or not p.exists():
                errors.append(f"{page.name}: outside published docs root or missing: {target}")
    if errors:raise SystemExit("\n".join(errors))
    print(f"site: {count} local assets/routes stay within the published docs root")

if __name__=="__main__":main()
