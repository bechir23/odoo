
from odoo import models, fields, api

class InternshipApplicationAnswer(models.Model):
    _name = 'internship.application.answer'
    _description = 'Internship Application Answer'

    application_id = fields.Many2one('internship.application', string='Application', required=True, ondelete='cascade')
    question_id = fields.Many2one('internship.question', string='Question', required=True)
    answer_text = fields.Text(string='Answer (Text)')
    answer_multiple_choice = fields.Char(string='Answer (Multiple Choice)')
    # Add fields for other answer types as needed, e.g., answer_date, answer_boolean for checkboxes

    _sql_constraints = [
        ('application_question_uniq', 'unique (application_id, question_id)',
         'An answer already exists for this question in this application.')
    ]