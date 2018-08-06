# -*- coding: utf-8 -*-
# Copyright (c) 2018, Dokos and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class PipedriveSettings(Document):
	def sync(self):
		"""Create and execute Data Migration Run for Pipedrive Sync plan"""
		frappe.has_permission('Pipedrive Settings', throw=True)

		exists = frappe.db.exists('Data Migration Run', dict(status=('in', ['Fail', 'Error']),	name=('!=', self.name)))
		if exists:
			failed_run = frappe.get_doc("Data Migration Run", dict(status=('in', ['Fail', 'Error'])))
			failed_run.delete()

		started = frappe.db.exists('Data Migration Run', dict(status=('in', ['Started']),	name=('!=', self.name)))
		if started:
			print("Break")
			return

		try:
			doc = frappe.get_doc({
				'doctype': 'Data Migration Run',
				'data_migration_plan': 'Pipedrive Sync',
				'data_migration_connector': 'Pipedrive Connector'
			}).insert()

			try:
				doc.run()
			except Exception:
					frappe.log_error(frappe.get_traceback())
		except Exception as e:
			frappe.logger().debug({"Pipedrive Error: "}, e)

	def create_pipedrive_connector(self):
		if frappe.db.exists('Data Migration Connector', 'Pipedrive Connector'):
			pipedrive_connector = frappe.get_doc('Data Migration Connector', 'Pipedrive Connector')
			pipedrive_connector.connector_type = 'Custom'
			pipedrive_connector.python_module = 'pipedrive.pipedrive.connectors.pipedrive_connector'
			pipedrive_connector.save()
			return

		frappe.get_doc({
			'doctype': 'Data Migration Connector',
			'connector_type': 'Custom',
			'connector_name': 'Pipedrive Connector',
			'python_module': 'pipedrive.pipedrive.connectors.pipedrive_connector',
		}).insert()

	def create_pipedrive_plan(self):
		if frappe.db.exists('Data Migration Plan', 'Pipedrive Sync'):
			pipedrive_sync = frappe.get_doc('Data Migration Plan', 'Pipedrive Sync')
			pipedrive_sync.module = "Pipedrive"
			pipedrive_sync.update({"mappings":[]})

			mappings = ["Pipedrive Organization to ERPNext Lead", "Pipedrive Person to ERPNext Contact"]

			for mapping in mappings:
				pipedrive_sync.append("mappings", {
					"mapping": mapping,
					"enabled": 1
				})
			pipedrive_sync.save()
			frappe.db.commit()
			return

		else:
			pipedrive_sync = frappe.get_doc('Data Migration Plan', 'Pipedrive Sync')
			pipedrive_sync.module = "Pipedrive"

			mappings = ["Pipedrive Organization to ERPNext Lead", "Pipedrive Person to ERPNext Contact"]

			for mapping in mappings:
				pipedrive_sync.append("mappings", {
					"mapping": mapping,
					"enabled": 1
				})
			pipedrive_sync.insert()


@frappe.whitelist()
def sync():
	pipedrive_settings = frappe.get_doc('Pipedrive Settings')
	if pipedrive_settings.enable == 1:
		if not frappe.db.exists('Data Migration Connector', 'Pipedrive Connector'):
			self.create_pipedrive_connector()
		if not frappe.db.exists('Data Migration Plan', 'Pipedrive Sync'):
			self.create_pipedrive_plan()
		try:
			pipedrive_settings.sync()
		except Exception:
			frappe.log_error(frappe.get_traceback())