from odoo import models, fields, api

class InternshipQuestion(models.Model):
    _name = 'internship.question'
    _description = 'Internship Question'

    internship_id = fields.Many2one('internship.internship', string='Internship', required=True)
    name = fields.Char(string='Question', required=True)
    question_type = fields.Selection([
        ('text', 'Text'),
        ('textarea', 'Text Area'),
        ('multiple_choice', 'Multiple Choice'),
        ('checkboxes', 'Checkboxes'),
        ('date', 'Date')
    ], string='Question Type', default='text', required=True)
    options = fields.Char(string='Options (comma-separated)', help="For multiple choice or checkboxes, list options separated by commas.")
    is_required = fields.Boolean(string='Is Required?', default=False)
    sequence = fields.Integer(string='Sequence', default=10)