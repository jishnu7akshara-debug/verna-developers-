import json

with open('index.html', encoding='utf-8') as f:
    idx = f.read()
with open('team.html', encoding='utf-8') as f:
    team = f.read()
with open('admin.html', encoding='utf-8') as f:
    admin = f.read()
with open('assets/css/site.css', encoding='utf-8') as f:
    css = f.read()

checks = {
    'Hero consultant image in index.html': 'hero-a-1100.webp' in idx and 'consultant reviewing' in idx,
    'Consistent Enquire buttons in index.html': 'Inquire on Advisory' not in idx,
    'Team card photo with headroom in team.html': 'team-card-photo' in team and 'object-position: center top' in team,
    'Admin client modal backdrop': 'id="client-modal" class="modal-backdrop"' in admin,
    'Admin client modal head': 'client-modal-title' in admin and 'modal-head' in admin,
    'Admin client modal body & foot': 'modal-body' in admin and 'modal-foot' in admin,
    'Reduced hero top gap in site.css': 'padding-top: clamp(0.75rem' in css,
    'Service actions whitespace nowrap in site.css': '.service-card-actions .text-link' in css
}

for k, v in checks.items():
    print(f'{"[OK]" if v else "[FAIL]"} {k}: {v}')
