from odoo import models, fields


class Company(models.Model):
    _name = 'internship.company'
    _description = 'Company'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    address = fields.Char(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    website = fields.Char(string='Website')
    contact_person = fields.Char(string='Contact Person')
    contact_email = fields.Char(string='Contact Email')
    contact_phone = fields.Char(string='Contact Phone')
    industry = fields.Char(string='Industry')
    internship_ids = fields.One2many('internship.internship', 'company_id', string='Internships')
    active = fields.Boolean(default=True, string='Active')