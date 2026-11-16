import urllib.request
import urllib.parse
import json

def search_commons_files(query, limit=5):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&list=search&srsearch={urllib.parse.quote(query)}&srnamespace=6&format=json&srlimit={limit}"
    req = urllib.request.Request(url, headers={'User-Agent': 'VernaDevelopersBot/1.0 (contact@vernadevelopers.com)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            results = data.get('query', {}).get('search', [])
            return [r['title'] for r in results]
    except Exception as e:
        print(f"Error searching {query}: {e}")
        return []

def get_image_url(file_title, width=1200):
    url = f"https://commons.wikimedia.org/w/api.php?action=query&titles={urllib.parse.quote(file_title)}&prop=imageinfo&iiprop=url&iiurlwidth={width}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'VernaDevelopersBot/1.0 (contact@vernadevelopers.com)'})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            pages = data.get('query', {}).get('pages', {})
            for pid, pdata in pages.items():
                imageinfo = pdata.get('imageinfo', [])
                if imageinfo:
                    return imageinfo[0].get('thumburl') or imageinfo[0].get('url')
    except Exception as e:
        print(f"Error getting url for {file_title}: {e}")
    return None

queries = [
    ("BBMP", "BBMP Corporation building Bangalore"),
    ("BDA", "Bangalore layout OR Indiranagar Bangalore OR Bangalore street"),
    ("BMRDA", "Bangalore highway aerial OR Nelamangala expressway"),
    ("BMICAPA", "NICE Road Bangalore OR Bangalore Mysore expressway"),
    ("BMRCL", "Namma Metro train elevated viaduct"),
    ("KIADB", "Electronic City Bangalore OR ITPL Bangalore OR Bangalore industrial"),
    ("CITB", "Malleswaram tree Bangalore OR Bangalore road avenue"),
    ("RERA", "Bangalore high rise apartment construction"),
    ("Seal_Karnataka", "Seal of Karnataka"),
    ("Logo_Metro", "Namma metro logo")
]

found = {}
for key, q in queries:
    files = search_commons_files(q, limit=3)
    print(f"=== {key} ({q}) ===")
    for f in files:
        img_url = get_image_url(f, width=1000)
        print(f"  {f} -> {img_url}")
        if key not in found and img_url:
            found[key] = (f, img_url)

print("\nFound map:", json.dumps(found, indent=2))

