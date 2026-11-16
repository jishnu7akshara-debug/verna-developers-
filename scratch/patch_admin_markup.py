with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update CSS: Add client grid and card styles
client_css = """
    /* Corporate Clients Grid */
    .clients-admin-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
      gap: 1.5rem;
    }
    .client-admin-card {
      background: #FFFFFF;
      border: 1px solid var(--admin-border);
      border-radius: 10px;
      padding: 1.25rem;
      display: flex;
      flex-direction: column;
      box-shadow: 0 1px 3px rgba(0,0,0,0.05);
      transition: all 0.2s ease;
    }
    .client-admin-card:hover {
      box-shadow: 0 6px 16px rgba(0,0,0,0.08);
      transform: translateY(-2px);
    }
    .client-logo-box {
      background: #F8FAFC;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      height: 90px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0.75rem;
      margin-bottom: 1rem;
    }
    .client-logo-box img {
      max-height: 100%;
      max-width: 100%;
      object-fit: contain;
    }
    .client-admin-card h4 {
      font-size: 1rem;
      color: var(--admin-navy);
      margin: 0 0 0.35rem;
      font-weight: 700;
    }
    .client-admin-card .client-sector {
      font-size: 0.8rem;
      color: var(--admin-muted);
      margin-bottom: 1rem;
      flex-grow: 1;
    }
"""

if '.clients-admin-grid' not in html:
    html = html.replace('/* Testimonials Admin Grid */', client_css + '\n    /* Testimonials Admin Grid */')

# 2. Update Login Box to Password-Only
old_login_form = """      <div class="login-demo-pill">
        Default Access: <b>admin</b> &bull; Password: <b>verna2026</b>
      </div>

      <form id="admin-login-form">
        <div class="admin-form-group">
          <label for="l-user">Admin Username</label>
          <input type="text" id="l-user" class="admin-input" placeholder="admin" value="admin" required>
        </div>
        <div class="admin-form-group">
          <label for="l-pass">Password</label>
          <input type="password" id="l-pass" class="admin-input" placeholder="••••••••" value="verna2026" required>
        </div>
        <p id="login-error" style="color: #DC2626; font-size: 0.85rem; margin-bottom: 1rem; display: none;">Invalid credentials. Please verify your login.</p>
        <button type="submit" class="admin-btn" style="width: 100%;">Authenticate & Enter Portal →</button>
      </form>"""

new_login_form = """      <form id="admin-login-form">
        <div class="admin-form-group">
          <label for="l-pass" style="display: flex; justify-content: space-between; font-weight: 600; color: var(--admin-navy);">
            <span>Master Password</span>
            <span style="font-size: 0.78rem; font-weight: 400; color: var(--admin-muted);">Default: verna2026</span>
          </label>
          <div style="position: relative;">
            <input type="password" id="l-pass" class="admin-input" placeholder="Enter master password..." required autofocus style="padding-right: 2.75rem;">
            <button type="button" id="toggle-pass-btn" style="position: absolute; right: 0.75rem; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; color: #64748B; font-size: 1.1rem; padding: 0.2rem;" title="Toggle password visibility">👁</button>
          </div>
        </div>
        <p id="login-error" style="color: #DC2626; font-size: 0.85rem; margin-bottom: 1rem; display: none;">Incorrect master password. Access denied.</p>
        <button type="submit" class="admin-btn" style="width: 100%;">Unlock Admin Portal →</button>
      </form>"""

if old_login_form in html:
    html = html.replace(old_login_form, new_login_form)
    print("Replaced login form with password-only login!")

# 3. Add Clients Tab to nav
old_tabs = """      <button class="tab-btn active" data-tab="testimonials">
        💬 Client Testimonials <span class="badge-count" id="count-testi">0</span>
      </button>
      <button class="tab-btn" data-tab="enquiries">"""

new_tabs = """      <button class="tab-btn active" data-tab="testimonials">
        💬 Client Testimonials <span class="badge-count" id="count-testi">0</span>
      </button>
      <button class="tab-btn" data-tab="clients">
        🏢 Corporate Clients <span class="badge-count" id="count-clients">0</span>
      </button>
      <button class="tab-btn" data-tab="enquiries">"""

if old_tabs in html:
    html = html.replace(old_tabs, new_tabs)
    print("Added Corporate Clients tab to nav!")

# 4. Add Tab Section for Clients
clients_tab_section = """
      <!-- TAB: CORPORATE CLIENTS MANAGER -->
      <section id="tab-clients" class="tab-pane" style="display: none;">
        <div class="section-header-row">
          <div>
            <h1>Corporate Client Logos & Brands</h1>
            <p>Add new client logos, edit company details, delete entries, and control the rolling marquee on the website.</p>
          </div>
          <button class="admin-btn" id="open-add-client-btn">
            + Add New Client Logo
          </button>
        </div>

        <div id="clients-loading" style="text-align: center; padding: 3rem; color: var(--admin-muted);">
          Loading clients...
        </div>

        <div class="clients-admin-grid" id="clients-grid">
          <!-- Rendered dynamically -->
        </div>
      </section>
"""

if 'id="tab-clients"' not in html:
    html = html.replace('<!-- TAB 2: ENQUIRIES / LEADS MANAGER -->', clients_tab_section + '\n      <!-- TAB 2: ENQUIRIES / LEADS MANAGER -->')
    print("Added Clients Tab section!")

# 5. Add Client Modal
client_modal = """
  <!-- ==================== CLIENT MODAL ==================== -->
  <div id="client-modal" class="modal-overlay" style="display: none;">
    <div class="modal-box">
      <div class="modal-header">
        <h3 id="client-modal-title">Add Corporate Client Logo</h3>
        <button class="modal-close" id="close-client-modal">&times;</button>
      </div>
      <form id="client-form">
        <input type="hidden" id="c-id">

        <div class="admin-form-group">
          <label for="c-name">Company / Client Name *</label>
          <input type="text" id="c-name" class="admin-input" placeholder="e.g. Hotel Paraag, Raja Capital" required>
        </div>

        <div class="admin-form-group">
          <label for="c-cat">Industry / Sector *</label>
          <input type="text" id="c-cat" class="admin-input" placeholder="e.g. Hospitality & Commercial, Real Estate, Enterprise Tech" required>
        </div>

        <div class="admin-form-group">
          <label>Client Logo (Upload or URL) *</label>
          <div style="display: flex; gap: 0.75rem; align-items: center; margin-bottom: 0.5rem;">
            <input type="file" id="c-file" accept="image/*" style="display: none;">
            <button type="button" class="admin-btn admin-btn-outline" id="c-upload-btn" style="font-size: 0.85rem; padding: 0.5rem 1rem;">
              📁 Upload Logo Image
            </button>
            <span id="c-upload-status" style="font-size: 0.8rem; color: var(--admin-muted);"></span>
          </div>
          <input type="text" id="c-logo" class="admin-input" placeholder="assets/img/clients/paraag.webp or https://..." required>
          <div id="c-preview-wrap" style="margin-top: 0.75rem; text-align: center; background: #F8FAFC; padding: 1rem; border: 1px dashed var(--admin-border); border-radius: 8px;">
            <p style="font-size: 0.78rem; color: var(--admin-muted); margin: 0 0 0.5rem;">Logo Preview:</p>
            <img id="c-preview" src="" alt="Preview" style="max-height: 60px; max-width: 180px; object-fit: contain; display: none;">
          </div>
        </div>

        <div class="admin-form-group">
          <label for="c-order">Display Sequence Order</label>
          <input type="number" id="c-order" class="admin-input" value="1" min="1">
        </div>

        <div class="modal-footer">
          <button type="button" class="admin-btn admin-btn-outline" id="cancel-client-btn">Cancel</button>
          <button type="submit" class="admin-btn" id="save-client-btn">Save Client Logo</button>
        </div>
      </form>
    </div>
  </div>
"""

if 'id="client-modal"' not in html:
    html = html.replace('<!-- ==================== LEAD DETAILS MODAL ==================== -->', client_modal + '\n  <!-- ==================== LEAD DETAILS MODAL ==================== -->')
    print("Added Client Modal!")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("admin.html markup updated successfully!")

