/** @odoo-module **/
import { registry } from '@web/core/registry';
import { Component } from '@odoo/owl';

class InternshipDashboard extends Component {}

InternshipDashboard.template = 'internship_management.internship_dashboard';

registry.category('actions').add('internship_dashboard', InternshipDashboard);
