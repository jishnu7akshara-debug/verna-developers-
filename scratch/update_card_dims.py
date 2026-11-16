import re

for filename in ['index.html', 'departments.html']:
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Replace width="233" height="145" or width="228" height="143" with width="800" height="500"
    c_new = re.sub(r'width="\d+" height="\d+"', 'width="800" height="500"', c)
    if c_new != c:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(c_new)
        print(f"Updated image dimensions in {filename}")

