import os
import re

preloader_html = '''  <!-- Page Preloader Animation with Verna Developers Logo -->
  <div id="site-preloader" class="site-preloader" aria-hidden="true">
    <div class="preloader-content">
      <div class="preloader-logo-wrapper">
        <img src="assets/img/verna-logo-dark.png" class="preloader-logo" alt="Verna Developers" width="180" height="97">
      </div>
      <div class="preloader-bar-wrap">
        <div class="preloader-bar"></div>
      </div>
      <div class="preloader-subtext">VERNA DEVELOPERS • BENGALURU</div>
    </div>
  </div>
'''

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # 1. Add preloader if not present
    if 'id="site-preloader"' not in content:
        # insert after <body>
        body_match = re.search(r'<body[^>]*>', content, re.I)
        if body_match:
            idx = body_match.end()
            content = content[:idx] + '\n' + preloader_html + content[idx:]
            modified = True

    # 2. Remove Properties from nav
    # <li><a href="properties.html"[^>]*>Properties</a></li>
    new_content = re.sub(r'<li><a href="properties\.html"[^>]*>Properties</a></li>\s*', '', content)
    if new_content != content:
        content = new_content
        modified = True

    # 3. Remove Properties for sale from footer
    new_content = re.sub(r'<li><a href="properties\.html"[^>]*>Properties for sale</a></li>\s*', '', content)
    if new_content != content:
        content = new_content
        modified = True

    if modified:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {fname}")

print("All HTML files processed.")

