# erp_custom — code-controlled branding (placeholder: "Jemmia ERP").
#
# Why a script instead of the Desk UI: Website Settings' favicon/app_logo are
# "Attach Image" fields — the Desk UI forces a file upload and won't accept a
# plain `/assets/...` path. Setting the value via `set_single_value` bypasses
# that restriction, so we can point at app-bundled assets.
#
# Logo priority (verified in frappe's `navbar_settings.get_app_logo`):
#   1. Website Settings.app_logo   <-  highest priority, shadows everything
#   2. Navbar Settings.app_logo
#   3. hook `app_logo_url`
# We set BOTH singletons (#1 and #2) so the hook is never shadowed by a stale
# value a user may have uploaded earlier.

import frappe

LOGO = "/assets/erp_custom/images/logo.svg"
FAVICON = "/assets/erp_custom/images/favicon.svg"
TITLE_PREFIX = "Jemmia ERP"
BRAND_HTML = (
	f'<img src="{LOGO}" style="height:28px;vertical-align:middle"> {TITLE_PREFIX}'
)

WEBSITE_SETTINGS = {
	"title_prefix": TITLE_PREFIX,
	"favicon": FAVICON,
	"brand_html": BRAND_HTML,
	"app_logo": LOGO,
}

NAVBAR_SETTINGS = {
	"app_logo": LOGO,
}


def apply():
	"""Apply Jemmia branding. Idempotent — safe to run repeatedly."""
	frappe.db.set_single_value("Website Settings", WEBSITE_SETTINGS)
	frappe.db.set_single_value("Navbar Settings", NAVBAR_SETTINGS)
	frappe.db.commit()
	frappe.clear_cache()
	frappe.msgprint(f"Branding {TITLE_PREFIX} đã áp dụng.")
