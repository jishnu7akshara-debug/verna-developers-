with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update state object
html = html.replace('testimonials: [],\n        enquiries: []', 'testimonials: [],\n        clients: [],\n        enquiries: []')

# 2. Update login form handler to password-only + toggle
old_login_js = """      // Login form handler
      document.getElementById('admin-login-form').addEventListener('submit', function (e) {
        e.preventDefault();
        var u = document.getElementById('l-user').value.trim();
        var p = document.getElementById('l-pass').value.trim();
        var errEl = document.getElementById('login-error');

        fetch('/api/admin/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username: u, password: p })
        })"""

new_login_js = """      // Toggle password visibility
      var togglePassBtn = document.getElementById('toggle-pass-btn');
      if (togglePassBtn) {
        togglePassBtn.addEventListener('click', function () {
          var pInput = document.getElementById('l-pass');
          if (pInput.type === 'password') {
            pInput.type = 'text';
            togglePassBtn.textContent = '🙈';
          } else {
            pInput.type = 'password';
            togglePassBtn.textContent = '👁';
          }
        });
      }

      // Login form handler (Password-Only)
      document.getElementById('admin-login-form').addEventListener('submit', function (e) {
        e.preventDefault();
        var p = document.getElementById('l-pass').value.trim();
        var errEl = document.getElementById('login-error');

        fetch('/api/admin/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ password: p })
        })"""

if old_login_js in html:
    html = html.replace(old_login_js, new_login_js)
    print("Replaced login JS with password-only handler!")

# 3. Update loadAllData()
old_load_all = """      // Load all data
      function loadAllData() {
        loadTestimonials();
        loadEnquiries();
      }"""

new_load_all = """      // Load all data
      function loadAllData() {
        loadTestimonials();
        loadClients();
        loadEnquiries();
      }"""

if old_load_all in html:
    html = html.replace(old_load_all, new_load_all)
    print("Updated loadAllData to include loadClients()!")

# 4. Add Clients Management JS logic right before ENQUIRIES LOGIC
clients_js = """
      // ==================== CORPORATE CLIENTS LOGIC ====================
      function loadClients() {
        fetch('/api/clients')
          .then(function (r) { return r.json(); })
          .then(function (list) {
            state.clients = list;
            var countEl = document.getElementById('count-clients');
            if (countEl) countEl.textContent = list.length;
            renderClientsGrid();
          })
          .catch(function (err) {
            console.error('Failed to load clients:', err);
          });
      }

      function renderClientsGrid() {
        var grid = document.getElementById('clients-grid');
        var loading = document.getElementById('clients-loading');
        if (loading) loading.style.display = 'none';
        if (!grid) return;
        grid.innerHTML = '';

        if (!state.clients || !state.clients.length) {
          grid.innerHTML = '<p style="color: var(--admin-muted); grid-column: 1/-1; text-align: center; padding: 2rem;">No client logos found. Add your first client logo!</p>';
          return;
        }

        state.clients.forEach(function (c) {
          var card = document.createElement('div');
          card.className = 'client-admin-card';

          card.innerHTML = [
            '<div class="client-logo-box">',
            '  <img src="' + c.logo + '" alt="' + (c.name || 'Client') + '" onerror="this.src=\\'assets/img/clients/paraag.webp\\'">',
            '</div>',
            '<h4>' + (c.name || 'Corporate Partner') + '</h4>',
            '<div class="client-sector">🏷 ' + (c.category || 'Commercial') + '</div>',
            '<div class="card-actions-group" style="margin-top: auto; display: flex; gap: 0.5rem; justify-content: flex-end;">',
            '  <button class="admin-btn admin-btn-outline btn-icon edit-client" data-id="' + c.id + '" style="font-size: 0.8rem; padding: 0.35rem 0.65rem;">✏ Edit</button>',
            '  <button class="admin-btn admin-btn-red btn-icon del-client" data-id="' + c.id + '" style="font-size: 0.8rem; padding: 0.35rem 0.65rem;">🗑 Delete</button>',
            '</div>'
          ].join('');

          grid.appendChild(card);
        });

        // Attach edit handlers
        document.querySelectorAll('.edit-client').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var cid = this.getAttribute('data-id');
            var client = state.clients.find(function (x) { return x.id === cid; });
            if (!client) return;

            document.getElementById('client-modal-title').textContent = 'Edit Client Logo';
            document.getElementById('c-id').value = client.id;
            document.getElementById('c-name').value = client.name || '';
            document.getElementById('c-cat').value = client.category || '';
            document.getElementById('c-logo').value = client.logo || '';
            document.getElementById('c-order').value = client.order || 1;

            var prev = document.getElementById('c-preview');
            prev.src = client.logo || '';
            prev.style.display = client.logo ? 'inline-block' : 'none';

            document.getElementById('client-modal').style.display = 'flex';
          });
        });

        // Attach delete handlers
        document.querySelectorAll('.del-client').forEach(function (btn) {
          btn.addEventListener('click', function () {
            var cid = this.getAttribute('data-id');
            var client = state.clients.find(function (x) { return x.id === cid; });
            var cname = client ? client.name : 'this client';
            if (!confirm('Are you sure you want to delete "' + cname + '"? It will be removed from the scrolling marquee.')) return;

            fetch('/api/clients/' + cid, { method: 'DELETE' })
              .then(function (r) { return r.json(); })
              .then(function () {
                loadClients();
              })
              .catch(function (err) { alert('Delete failed: ' + err.message); });
          });
        });
      }

      // Open Add Client Modal
      var openClientBtn = document.getElementById('open-add-client-btn');
      if (openClientBtn) {
        openClientBtn.addEventListener('click', function () {
          document.getElementById('client-form').reset();
          document.getElementById('c-id').value = '';
          document.getElementById('client-modal-title').textContent = 'Add Corporate Client Logo';
          var prev = document.getElementById('c-preview');
          prev.src = '';
          prev.style.display = 'none';
          document.getElementById('c-upload-status').textContent = '';
          document.getElementById('client-modal').style.display = 'flex';
        });
      }

      // Close Client Modal
      function closeClientModal() {
        document.getElementById('client-modal').style.display = 'none';
      }
      var closeClientBtn = document.getElementById('close-client-modal');
      var cancelClientBtn = document.getElementById('cancel-client-btn');
      if (closeClientBtn) closeClientBtn.addEventListener('click', closeClientModal);
      if (cancelClientBtn) cancelClientBtn.addEventListener('click', closeClientModal);

      // Client Logo File Upload handler
      var cUploadBtn = document.getElementById('c-upload-btn');
      var cFileInput = document.getElementById('c-file');
      if (cUploadBtn && cFileInput) {
        cUploadBtn.addEventListener('click', function () { cFileInput.click(); });
        cFileInput.addEventListener('change', function () {
          var file = this.files[0];
          if (!file) return;

          var statusEl = document.getElementById('c-upload-status');
          statusEl.textContent = 'Uploading...';

          var reader = new FileReader();
          reader.onload = function (e) {
            fetch('/api/upload', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ filename: file.name, base64: e.target.result })
            })
            .then(function (r) { return r.json(); })
            .then(function (data) {
              if (data.ok && data.url) {
                document.getElementById('c-logo').value = data.url;
                var prev = document.getElementById('c-preview');
                prev.src = data.url;
                prev.style.display = 'inline-block';
                statusEl.textContent = '✓ Uploaded';
              } else {
                statusEl.textContent = 'Upload error';
              }
            })
            .catch(function () {
              statusEl.textContent = 'Upload failed';
            });
          };
          reader.readAsDataURL(file);
        });
      }

      // Logo URL input preview update
      var cLogoInput = document.getElementById('c-logo');
      if (cLogoInput) {
        cLogoInput.addEventListener('input', function () {
          var val = this.value.trim();
          var prev = document.getElementById('c-preview');
          if (val) {
            prev.src = val;
            prev.style.display = 'inline-block';
          } else {
            prev.style.display = 'none';
          }
        });
      }

      // Save Client Form Submission
      var clientForm = document.getElementById('client-form');
      if (clientForm) {
        clientForm.addEventListener('submit', function (e) {
          e.preventDefault();
          var cid = document.getElementById('c-id').value;
          var payload = {
            name: document.getElementById('c-name').value.trim(),
            category: document.getElementById('c-cat').value.trim(),
            logo: document.getElementById('c-logo').value.trim(),
            order: parseInt(document.getElementById('c-order').value) || 1,
            featured: true
          };

          var url = cid ? ('/api/clients/' + cid) : '/api/clients';
          var method = cid ? 'PUT' : 'POST';

          fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          })
          .then(function (r) { return r.json(); })
          .then(function () {
            closeClientModal();
            loadClients();
          })
          .catch(function (err) {
            alert('Failed to save client: ' + err.message);
          });
        });
      }
"""

if 'loadClients' not in html:
    html = html.replace('// ==================== ENQUIRIES LOGIC ====================', clients_js + '\n      // ==================== ENQUIRIES LOGIC ====================')
    print("Added Client Management JS!")

with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("admin.html JavaScript successfully updated!")

