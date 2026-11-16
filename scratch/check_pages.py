import glob

for f in sorted(glob.glob('*.html')):
    with open(f, encoding='utf-8') as fp:
        c = fp.read()
    has_form = 'data-enquiry' in c
    has_consent = 'name="consent"' in c
    has_preloader = 'site-preloader' in c
    has_sitejs = 'assets/js/site.js' in c
    print(f'{f:40} form={has_form} consent={has_consent} preloader={has_preloader} sitejs={has_sitejs}')
