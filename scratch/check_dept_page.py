with open('departments.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = re.findall(r'<img[^>]*src=[\'"]([^\'"]*dept-[^\'"]*)[\'"]', c)
print("Dept images in departments.html:", matches)
titles = re.findall(r'<h[23][^>]*>([^<]*(?:Bengaluru|Authority|Board|Palike|RERA|Trust)[^<]*)</h[23]>', c)
print("Titles in departments.html:", titles)

