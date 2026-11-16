import re

def check_file(filename):
    print(f"Checking {filename}...")
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()
    cards = re.findall(r'<article class="govt-auth-card">[\s\S]*?<img src="([^"]+)"[\s\S]*?<h3 class="govt-auth-title">([^<]+)</h3>', c)
    for i, (img, title) in enumerate(cards, 1):
        print(f"  {i}. {img} -> {title.strip()}")

check_file("index.html")
check_file("departments.html")

