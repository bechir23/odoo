from odoo import models, fields, api

class InternshipReportSection(models.Model):
    _name = 'internship.report.section'
    _description = 'Internship Report Required Sections'
    _order = 'sequence, id'
    
    name = fields.Char(string='Section Name', required=True)
    description = fields.Text(string='Description', help='Explanation of what this section should contain')
    sequence = fields.Integer(string='Sequence', default=10)
    required = fields.Boolean(string='Mandatory', default=True, 
                             help='If checked, this section will be required in reports')
