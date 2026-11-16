with open('admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'login-overlay' in line.lower() or 'admin username' in line.lower() or 'default access' in line.lower():
        print(f"{i+1}: {line.strip()}")

