# ERP Custom

Custom app for ERPNext (Jemmia). Mọi customization ERPNext nằm ở đây — **KHÔNG** sửa
frappe/erpnext trực tiếp (xem Golden Rule #1 trong `AGENTS.md` của meta-repo).

## Module
- Tên module: **ERP Custom** (DocType tạo trong module này sync vào `erp_custom/erp_custom/`).

## Cấu trúc thư mục

```
erp_custom/
├── hooks.py            # required_apps + các hook (doc_events, doctype_js, fixtures...)
├── overrides/          # business logic server-side (gọi qua doc_events)
├── fixtures/           # JSON exported qua `bench export-fixtures` (Custom Field, ...)
├── public/js/          # client-side form scripts (gọi qua doctype_js)
├── public/css/
└── erp_custom/         # module dir — DocType mới sync vào đây
```

## 3 pattern customize

### Pattern A — Custom Field (data, version-control qua fixtures)
1. Desk → Customize Form → chọn DocType (vd Customer) → thêm Custom Field.
2. Trong `hooks.py`: `fixtures = ["Custom Field:Customer"]`
3. Chạy: `bench --site development.localhost export-fixtures`
4. Commit JSON trong `fixtures/` → tự sync mỗi khi install app.

### Pattern B — Business logic (`doc_events`)
1. Tạo `erp_custom/overrides/sales_invoice.py`:
   ```python
   import frappe
   def validate(doc, method=None):
       if doc.is_return and not doc.reason_for_return:
           frappe.throw("Lý do trả hàng là bắt buộc")
   ```
2. Trong `hooks.py`:
   ```python
   doc_events = {"Sales Invoice": {"validate": "erp_custom.overrides.sales_invoice.validate"}}
   ```
3. Restart bench.

### Pattern C — Client-side (`doctype_js`)
1. Tạo `erp_custom/public/js/customer.js`:
   ```javascript
   frappe.ui.form.on("Customer", {
       refresh(frm) { frm.add_custom_button("Ping", () => frappe.msgprint("hi")); }
   });
   ```
2. Trong `hooks.py`:
   ```python
   doctype_js = {"Customer": "public/js/customer.js"}
   ```
3. Chạy: `bench build --app erp_custom`

## Workflow hằng ngày
Edit → (JS/CSS: `make dev-build-app APP_NAME=erp_custom` | Python: restart bench) → test trên Desk → commit.

## Installation

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app https://github.com/namtran067/erp_custom.git --branch main
bench install-app erp_custom
```

## License
mit
