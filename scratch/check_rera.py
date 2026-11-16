import urllib.request
import re
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
try:
    req = urllib.request.Request('https://rera.karnataka.gov.in', headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        html = r.read().decode('utf-8', errors='ignore')
    logos = re.findall(r'<img[^>]*src=[\'"]([^\'"]*(?:logo|emblem|rera|header)[^\'"]*)[\'"]', html, re.I)
    print('Found logos on rera.karnataka.gov.in:', logos)
    for l in logos:
        if not l.startswith('http'):
            l_url = 'https://rera.karnataka.gov.in/' + l.lstrip('/')
        else:
            l_url = l
        print('Testing', l_url)
        try:
            req_l = urllib.request.Request(l_url, headers=headers)
            with urllib.request.urlopen(req_l, timeout=5) as resp:
                fn = os.path.basename(l.split('?')[0])
                with open(f'scratch/downloads/{fn}', 'wb') as fp:
                    fp.write(resp.read())
            print(f'Saved scratch/downloads/{fn}: {os.path.getsize(f"scratch/downloads/{fn}")}')
        except Exception as err:
            print('Download err:', err)
except Exception as e:
    print('Error accessing rera:', e)

