import urllib.request
import json
import re

print("=== 1. Checking Established 2000 Image in index.html ===")
with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

assert 'about-1000.webp' in index_html, "about-1000.webp missing"
assert 'Verna Developers executive office' in index_html, "alt text not updated"
print("[PASS] Established 2000 section has the new office image!")

print("\n=== 2. Testing Password-Only Admin Login ===")
login_req = urllib.request.Request(
    'http://localhost:3000/api/admin/login',
    data=json.dumps({'password': 'verna2026'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(login_req) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    assert res.get('ok') is True, "Login failed"
    token = res.get('token')
    print(f"[PASS] Password-only login successful! Token: {token}")

print("\n=== 3. Testing Clients API (CRUD) ===")
# GET
get_req = urllib.request.Request('http://localhost:3000/api/clients')
with urllib.request.urlopen(get_req) as resp:
    clients = json.loads(resp.read().decode('utf-8'))
    assert len(clients) >= 16, f"Expected at least 16 clients, got {len(clients)}"
    print(f"[PASS] GET /api/clients returned {len(clients)} corporate clients!")

# POST (Add client)
post_payload = {
    "name": "Test Partner Ltd",
    "category": "Corporate Consulting",
    "logo": "assets/img/clients/paraag.webp",
    "order": 99
}
post_req = urllib.request.Request(
    'http://localhost:3000/api/clients',
    data=json.dumps(post_payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'}
)
with urllib.request.urlopen(post_req) as resp:
    post_res = json.loads(resp.read().decode('utf-8'))
    assert post_res.get('ok') is True, "POST client failed"
    new_id = post_res['client']['id']
    print(f"[PASS] POST /api/clients created new client: {new_id}")

# PUT (Update client)
put_payload = {
    "name": "Test Partner Ltd (Updated)",
    "category": "Strategic Advisory"
}
put_req = urllib.request.Request(
    f'http://localhost:3000/api/clients/{new_id}',
    data=json.dumps(put_payload).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='PUT'
)
with urllib.request.urlopen(put_req) as resp:
    put_res = json.loads(resp.read().decode('utf-8'))
    assert put_res.get('ok') is True, "PUT client failed"
    assert put_res['client']['name'] == "Test Partner Ltd (Updated)"
    print(f"[PASS] PUT /api/clients/{new_id} updated client successfully!")

# DELETE (Delete client)
del_req = urllib.request.Request(
    f'http://localhost:3000/api/clients/{new_id}',
    method='DELETE'
)
with urllib.request.urlopen(del_req) as resp:
    del_res = json.loads(resp.read().decode('utf-8'))
    assert del_res.get('ok') is True, "DELETE client failed"
    print(f"[PASS] DELETE /api/clients/{new_id} deleted successfully!")

print("\n=== 4. Checking Pause Buttons Removal & Hover-Pause in JS/CSS ===")
with open('assets/js/site.js', 'r', encoding='utf-8') as f:
    site_js = f.read()

assert 'marquee-toggle' not in site_js, "marquee-toggle button generator still in site.js"
assert 'mouseenter' in site_js and 'mouseleave' in site_js, "Hover pause listeners missing"
print("[PASS] Pause buttons removed from JS and mouseenter/mouseleave hover-pause active!")

with open('assets/css/site.css', 'r', encoding='utf-8') as f:
    site_css = f.read()

assert '.marquee-toggle { display: none !important; }' in site_css, "marquee-toggle display none missing"
print("[PASS] .marquee-toggle forced to display none in site.css!")

print("\n=== 5. Checking Admin Portal Features ===")
with open('admin.html', 'r', encoding='utf-8') as f:
    admin_html = f.read()

assert 'data-tab="clients"' in admin_html, "Corporate Clients tab missing in admin.html"
assert 'id="client-modal"' in admin_html, "client-modal missing in admin.html"
assert 'id="l-pass"' in admin_html, "Password input missing in admin.html"
assert 'id="l-user"' not in admin_html, "Username input still present in admin.html"
print("[PASS] Admin portal has password-only login and full corporate clients management!")

print("\nALL 5 AUDIT TESTS PASSED 100%!")

