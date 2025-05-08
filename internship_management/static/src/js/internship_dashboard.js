odoo.define('internship_management.internship_dashboard', function (require) {
    "use strict";
    var registry = require('web.core').registry || require('@web/core/registry').registry;
    var Component = require('@odoo/owl').Component;
    var loadTemplates = require('@web/core/assets').loadTemplates;

    loadTemplates("internship_management.internship_dashboard");

    class InternshipDashboard extends Component {}
    InternshipDashboard.template = 'internship_management.internship_dashboard';
    registry.category('actions').add('internship_dashboard', InternshipDashboard);
});
