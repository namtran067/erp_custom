# ERP Custom

Custom app for ERPNext (Jemmia). All ERPNext customizations live here — **do not**
edit frappe/erpnext directly (see Golden Rule #1 in the meta-repo's `AGENTS.md`).

## Module
- Module name: **ERP Custom** (DocTypes created in this module sync into `erp_custom/erp_custom/`).

## Directory structure

```
erp_custom/
├── hooks.py            # required_apps + hooks (doc_events, doctype_js, fixtures...)
├── overrides/          # server-side business logic (invoked via doc_events)
├── fixtures/           # JSON exported via `bench export-fixtures` (Custom Field, ...)
├── public/js/          # client-side form scripts (invoked via doctype_js)
├── public/css/
└── erp_custom/         # module dir — new DocTypes sync here
```

## 3 customization patterns

### Pattern A — Custom Field (data, version-controlled via fixtures)
1. Desk → Customize Form → select the DocType (e.g. Customer) → add a Custom Field.
2. In `hooks.py`: `fixtures = ["Custom Field:Customer"]`
3. Run: `bench --site development.localhost export-fixtures`
4. Commit the JSON under `fixtures/` → it auto-syncs on every app install.

### Pattern B — Business logic (`doc_events`)
1. Create `erp_custom/overrides/sales_invoice.py`:
   ```python
   import frappe
   def validate(doc, method=None):
       if doc.is_return and not doc.reason_for_return:
           frappe.throw("Reason for return is mandatory")
   ```
2. In `hooks.py`:
   ```python
   doc_events = {"Sales Invoice": {"validate": "erp_custom.overrides.sales_invoice.validate"}}
   ```
3. Restart bench.

### Pattern C — Client-side (`doctype_js`)
1. Create `erp_custom/public/js/customer.js`:
   ```javascript
   frappe.ui.form.on("Customer", {
       refresh(frm) { frm.add_custom_button("Ping", () => frappe.msgprint("hi")); }
   });
   ```
2. In `hooks.py`:
   ```python
   doctype_js = {"Customer": "public/js/customer.js"}
   ```
3. Run: `bench build --app erp_custom`

## Daily workflow
Edit → (JS/CSS: `make dev-build-app APP_NAME=erp_custom` | Python: restart bench) → test on Desk → commit.

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/namtran067/erp_custom.git --branch main
bench install-app erp_custom
```

## License
mit
