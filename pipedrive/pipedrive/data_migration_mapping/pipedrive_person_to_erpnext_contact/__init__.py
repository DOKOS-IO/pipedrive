import frappe
def pre_process(doc):
	frappe.log_error(doc)
	phone = ""
	mobile = ""
	email = ""

	for p in doc['phone']:
		if p['label'] == 'mobile':
			mobile = p['value']
		if p['label'] in ['home', 'work', 'other']:
			phone = p['value']

	for e in doc['email']:
		if e['label'] == 'work':
			email = e['value']

	returned_doc = {
		'id': doc['id'],
		'first_name': doc['first_name'],
		'last_name': doc['last_name'],
		'email': email,
		'phone': phone,
		'mobile_no': mobile
	}

	return returned_doc

def post_process(remote_doc=None, local_doc=None, **kwargs):
	if not local_doc:
		return

	if remote_doc:
		organization = remote_doc['org_name']

		if organization is not None:
			if frappe.db.exists("Lead", dict(company_name=organization)):
				leadorg = frappe.db.get_value("Lead", dict(company_name=organization), "name")
				local_doc.append("links",{"link_doctype": "Lead", "link_name": leadorg})
				local_doc.save()
				frappe.db.commit()
			else:
				return
		else:
			return

	else:
		return