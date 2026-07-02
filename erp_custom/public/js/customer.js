// erp_custom — client-side override for Customer (loaded via doctype_js hook)
// Smoke test: adds a button on Customer form to verify the hook works end-to-end.
frappe.ui.form.on("Customer", {
	refresh(frm) {
		frm.add_custom_button(__("ERP Custom Ping"), () =>
			frappe.show_alert({
				message: __("erp_custom hook hoạt động!"),
				indicator: "green",
			})
		);
	},
});
