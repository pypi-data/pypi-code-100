import re

html = """https://www.google.com"""
html2 = """<a href="https://docs.google.com/document/d/1bGOITC8zoes1RLDj6ybWDtKiszTnBq5jZe1icx6itnI/edit?usp=sharing"> https://www.google.com"""
html3 = """<a href="https://docs.google.com/document/d/1bGOITC8zoes1RLDj6ybWDtKiszTnBq5jZe1icx6itnI/edit?usp=sharing">"""


def testting(html):
    link = re.search("<?(.*)?https?:\/\/.*", html)
    spl = re.split(">", link.group())
    links = [x for x in spl if re.search("https?:\/\/.*", x)]
    print(links)
    line = ""
    if len(links) > 1:
        for f in links:
            print(f)
            if not "<" in f:
                line = html.replace(f.strip(), f"[{f.strip()}]({f.strip()})")
    else:
        f = links[0]
        print(f)
        if not "<" in f:
            line = html.replace(f.strip(), f"[{f.strip()}]({f.strip()})")
        else:
            line = html
    return line


print("1", testting(html))
print("2", testting(html2))
