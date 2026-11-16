with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(120, 290):
    line = lines[i]
    if 'service-' in line:
        print(f"{i+1}: {line.strip()}")

