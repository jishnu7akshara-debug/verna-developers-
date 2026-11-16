with open('departments.html', 'r', encoding='utf-8') as f:
    html = f.read()

depts = [
    ('dept-bbmp.html', 'Bruhat Bengaluru Mahanagara Palike', 'dept-bbmp.webp', 'dept-bbmp-2x.webp'),
    ('dept-bda.html', 'Bangalore Development Authority', 'dept-bda.webp', 'dept-bda-2x.webp'),
    ('dept-bmrda.html', 'Bangalore Metropolitan Region Development Authority', 'dept-bmrda.webp', 'dept-bmrda-2x.webp'),
    ('dept-bmicapa.html', 'Bangalore Mysore Infrastructure Corridor Area Planning Authority', 'dept-bmicapa.webp', 'dept-bmicapa-2x.webp'),
    ('dept-bmrcl.html', 'Bengaluru Metro Rail Corporation Limited', 'dept-bmrcl.webp', 'dept-bmrcl-2x.webp'),
    ('dept-kiadb.html', 'Karnataka Industrial Areas Development Board', 'dept-kiadb.webp', 'dept-kiadb-2x.webp'),
    ('dept-citb.html', 'City Improvement Trust Board', 'dept-citb.webp', 'dept-citb-2x.webp'),
    ('dept-rera.html', 'Real Estate Regulatory Authority (Karnataka RERA)', 'dept-rera.webp', 'dept-rera-2x.webp')
]

for url, name, img1, img2 in depts:
    old_thumb = f'<div class="govt-auth-thumb">\n              <img src="assets/img/dept/{img1}" srcset="assets/img/dept/{img2} 2x" alt="{name}" loading="lazy" width="800" height="500">\n            </div>'
    new_thumb = f'<a href="{url}" class="govt-auth-thumb-link" aria-label="{name}">\n              <div class="govt-auth-thumb">\n                <img src="assets/img/dept/{img1}" srcset="assets/img/dept/{img2} 2x" alt="{name}" loading="lazy" width="800" height="500">\n              </div>\n            </a>'
    if old_thumb in html:
        html = html.replace(old_thumb, new_thumb)

    old_title = f'<h3 class="govt-auth-title">{name}</h3>'
    new_title = f'<h3 class="govt-auth-title"><a href="{url}" style="color: inherit; text-decoration: none;">{name}</a></h3>'
    if old_title in html:
        html = html.replace(old_title, new_title)

with open('departments.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated departments.html card links successfully!")

