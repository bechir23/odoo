from odoo import models, fields, api

class InternshipApplication(models.Model):
    _name = 'internship.application'
    _description = 'Internship Application'

    student_id = fields.Many2one('internship.student', string='Student', required=True)
    internship_id = fields.Many2one('internship.internship', string='Internship', required=True)
    application_date = fields.Date(string='Application Date', default=fields.Date.context_today, required=True)
    status = fields.Selection([
        ('new', 'New'),
        ('under_review', 'Under Review'),
        ('interview', 'Interview Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ], string='Status', default='new', required=True)
    cover_letter = fields.Text(string='Cover Letter')
    cv = fields.Binary(string="CV/Resume", attachment=True)
    answer_ids = fields.One2many('internship.application.answer', 'application_id', string='Answers')

    @api.depends('student_id', 'internship_id')
    def _compute_display_name(self):
        for app in self:
            name = f"{app.student_id.name if app.student_id else 'N/A'} - {app.internship_id.name if app.internship_id else 'N/A'}"
            app.display_name = name

    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True)
