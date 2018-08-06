from __future__ import unicode_literals
import frappe
from frappe.data_migration.doctype.data_migration_connector.connectors.base import BaseConnection
import requests

class PipedriveConnector(BaseConnection):
	def __init__(self, connector):
		self.connector = connector
		settings = frappe.get_doc("Pipedrive Settings", None)

		self.pipedrive_domain = settings.domain
		self.token = settings.get_password(fieldname='token',raise_exception=False)

		self.name_field = 'id'

	def get(self, remote_objectname, fields=None, filters=None, start=0, page_length=10):
		search = filters.get('search')

		if remote_objectname == 'Person': 
			try:
				return self.get_persons(search, start, page_length)
			except Exception as e:
				frappe.log_error(e, 'Pipedrive Persons Get Error')

		if remote_objectname == 'Organization': 
			try:
				return self.get_organizations(search, start, page_length)
			except Exception as e:
				frappe.log_error(e, 'Pipedrive Organizations Get Error')

	def insert(self, doctype, doc):
		pass

	def update(self, doctype, doc, migration_id):
		pass

	def delete(self, doctype, migration_id):
		pass


	def get_persons(self, search, start=0, page_length=10):
		request_url = "{0}/v1/persons?api_token={1}".format(self.pipedrive_domain, self.token)
		r = requests.get(request_url).json()

		return list(r['data'])

	def get_organizations(self, search, start=0, page_length=10):
		request_url = "{0}/v1/organizations?api_token={1}".format(self.pipedrive_domain, self.token)
		r = requests.get(request_url).json()

		return list(r['data'])