with open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

client_modal = """
  <!-- ==================== CLIENT MODAL: ADD / EDIT ==================== -->
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
          <input type="text" id="c-name" class="admin-input" placeholder="e.g. Hotel Paraag, Raja Capital, Peel Plywood" required>
        </div>

        <div class="admin-form-group">
          <label for="c-cat">Industry / Sector *</label>
          <input type="text" id="c-cat" class="admin-input" placeholder="e.g. Hospitality, Real Estate, Enterprise Tech, Manufacturing" required>
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

target = '<!-- ==================== MODAL: EDIT LEAD ENQUIRY ==================== -->'
if target in html and 'id="client-modal"' not in html:
    html = html.replace(target, client_modal + '\n  ' + target)
    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('client-modal successfully inserted!')
else:
    print('Already present or target not found')

