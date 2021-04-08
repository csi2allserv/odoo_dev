# Copyright 2017 Tecnativa - Vicent Cubells
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "mail request maintenance",
    "summary": "maintenance report by email",
    "version": "13.0.1.0.0",
    "author": "Rafael Amaris",
    "depends": ["mail_request_report"],
    "data": ["views/maintenance_task_views.xml", "data/maintenance_template.xml"],
    "installable": True,
}