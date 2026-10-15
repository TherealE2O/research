import glob, re

for f in sorted(glob.glob('*.html')):
    txt = open(f, encoding='utf-8').read()
    gh_links = re.findall(r'href=[\'"](https://github\.com/[^\'"]+)[\'"]', txt)
    if gh_links:
        print(f"{f}:")
        for link in set(gh_links):
            print(f"   {link}")
