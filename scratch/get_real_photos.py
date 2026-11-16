import urllib.request
import urllib.parse
import json

def get_direct_url(file_name, width=1200):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_name)}&prop=imageinfo&iiprop=url&iiurlwidth={width}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    with urllib.request.urlopen(req, timeout=10) as resp:
        d = json.loads(resp.read().decode('utf-8'))
        pages = d.get('query', {}).get('pages', {})
        for pid, p in pages.items():
            info = p.get('imageinfo', [])
            if info:
                return info[0].get('thumburl') or info[0].get('url')
    return None

specific_files = [
    ("BBMP_Building", "File:BBMP Office Building front.jpg"),
    ("BBMP_Alt", "File:BBMP Tower.JPG"),
    ("NICE_Road", "File:NICE Road (Channasandra second bridge (left), 2024) 12.jpg"),
    ("Namma_Metro_Train", "File:Train on Namma Metro viaduct, Bangalore.jpg"),
    ("Namma_Metro_Alt", "File:Bangalore Metro at Trinity.jpg"),
    ("Karnataka_Seal", "File:Seal of Karnataka.svg"),
    ("Metro_Logo", "File:Namma metro icon.svg"),
    ("Electronic_City", "File:Bangalore Electronic City Fly Over (Elevated HighWay) 1356.jpg"),
    ("Indiranagar_BDA", "File:100 Feet Road, Indiranagar, Bengaluru.jpg"),
    ("Bangalore_Skyline", "File:Bangalore Skyline.jpg"),
    ("Malleswaram_Tree", "File:Avenue in Malleswaram, Bangalore.jpg")
]

for key, fname in specific_files:
    try:
        u = get_direct_url(fname, width=1200)
        print(f"{key}: {u}")
    except Exception as e:
        print(f"{key} error: {e}")

