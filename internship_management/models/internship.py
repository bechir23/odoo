from odoo import models, fields, api
from .sms_utils import send_sms
from collections import defaultdict
from datetime import datetime, timedelta

class Internship(models.Model):
    _name = 'internship.internship'
    _description = 'Internship'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Internship Name', required=True)
    company_id = fields.Many2one('res.partner', string='Company', domain=[('is_company', '=', True)])
    student_id = fields.Many2one('res.partner', string='Student', domain=[('is_company', '=', False)])
    academic_tutor = fields.Char(string='Academic Tutor')
    professional_tutor = fields.Char(string='Professional Tutor')
    status = fields.Selection([
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled') # Ajout du statut Annulé
    ], string='Status', default='pending')
    student_signature = fields.Binary(string="Signature Étudiant")
    academic_tutor_signature = fields.Binary(string="Signature Tuteur Académique")
    professional_tutor_signature = fields.Binary(string="Signature Tuteur Professionnel")
    start_date = fields.Date(string="Date de Début")
    end_date = fields.Date(string="Date de Fin")
    subject = fields.Char(string="Sujet du Stage")
    description = fields.Text(string="Description")

    def generate_convention_pdf(self):
        """Generate convention PDF"""
        return self.env.ref('internship_management.report_internship_convention').report_action(self)

    def action_send_convention_email(self):
        """Send convention by email"""
        self.ensure_one()
        template = self.env.ref('internship_management.email_template_internship_convention')
        return template.send_mail(self.id, force_send=True)

    @api.model_create_multi
    def create(self, vals_list):
        return super().create(vals_list)

    def notify_student_sms(self):
        if self.student_id and self.student_id.phone:
            send_sms(
                to_number=self.student_id.phone,
                message="Votre convention de stage est disponible.",
                twilio_sid="TON_TWILIO_SID",
                twilio_token="TON_TWILIO_TOKEN",
                twilio_number="TON_NUMERO_TWILIO"
            )

    @api.model
    def get_dashboard_data(self, filters=None):
        """Get comprehensive dashboard data with support for filters"""
        filters = filters or {}
        domain = []
        
        # Apply filters to domain
        if filters.get('status'):
            domain.append(('status', '=', filters.get('status')))
        if filters.get('company_id'):
            domain.append(('company_id', '=', filters.get('company_id')))
        if filters.get('date_from'):
            domain.append(('start_date', '>=', filters.get('date_from')))
        if filters.get('date_to'):
            domain.append(('end_date', '<=', filters.get('date_to')))
        if filters.get('field_of_study'):
            domain.append(('student_id.field_of_study', '=', filters.get('field_of_study')))
        
        # Get all internships matching the domain
        internships = self.search(domain)
        
        # KPIs - Basic statistics
        total_internships = len(internships)
        ongoing_internships = len(internships.filtered(lambda i: i.status == 'ongoing'))
        completed_internships = len(internships.filtered(lambda i: i.status == 'completed'))
        pending_internships = len(internships.filtered(lambda i: i.status == 'pending'))
        cancelled_internships = len(internships.filtered(lambda i: i.status == 'cancelled'))
        
        # Status distribution
        status_data = self._prepare_status_chart_data(internships)
        
        # Company distribution
        company_data = self._prepare_company_chart_data(internships)
        
        # Evolution over time (last 12 months)
        evolution_data = self._prepare_evolution_chart_data(domain)
        
        # Field of study distribution
        field_data = self._prepare_field_chart_data(internships)
        
        # Pivot data - Academic Tutors by Status
        pivot_data = self._prepare_pivot_data(internships)
        
        # Recent internships
        recent_internships = self._get_recent_internships(domain)
        
        # Get available companies and fields for filters
        companies = self.env['res.partner'].search([('is_company', '=', True)]).mapped(lambda c: {'id': c.id, 'name': c.name})
        fields_of_study = self.env['internship.student'].search([]).mapped('field_of_study')
        fields_of_study = list(set(filter(None, fields_of_study)))
        
        # Map status codes to display names
        status_map = dict(self._fields['status'].selection)
        
        return {
            'kpis': {
                'total_internships': total_internships,
                'ongoing_internships': ongoing_internships,
                'completed_internships': completed_internships,
                'pending_internships': pending_internships,
                'cancelled_internships': cancelled_internships,
            },
            'charts': {
                'by_status': status_data,
                'by_company': company_data,
                'evolution': evolution_data,
                'by_field': field_data,
            },
            'pivot_table': pivot_data,
            'recent_internships': recent_internships,
            'filter_options': {
                'companies': companies,
                'fields_of_study': fields_of_study,
            },
            'status_map': status_map,
        }

    def _prepare_status_chart_data(self, internships):
        """Prepare data for status distribution chart"""
        status_count = {'pending': 0, 'ongoing': 0, 'completed': 0, 'cancelled': 0}
        
        for internship in internships:
            if internship.status in status_count:
                status_count[internship.status] += 1
        
        # Filter out status with 0 count
        filtered_status = {k: v for k, v in status_count.items() if v > 0}
        
        return {
            'labels': list(filtered_status.keys()),
            'data': list(filtered_status.values()),
        }

    def _prepare_company_chart_data(self, internships):
        """Prepare data for company distribution chart"""
        company_data = {}
        
        for internship in internships:
            if internship.company_id:
                company_name = internship.company_id.name
                company_data[company_name] = company_data.get(company_name, 0) + 1
        
        # Sort by count and take top 10
        sorted_data = sorted(company_data.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'labels': [item[0] for item in sorted_data],
            'data': [item[1] for item in sorted_data],
        }

    def _prepare_evolution_chart_data(self, domain):
        """Prepare data for evolution over time chart - last 12 months"""
        from datetime import datetime, timedelta
        
        labels = []
        data = []
        
        # Prepare dates for the last 12 months
        end_date = datetime.now()
        
        for i in range(11, -1, -1):
            # Calculate first day of the month
            current_month = end_date.replace(day=1) - timedelta(days=i*30)
            month_start = current_month.replace(day=1)
            
            # Calculate last day of the month
            if month_start.month == 12:
                next_month = month_start.replace(year=month_start.year+1, month=1)
            else:
                next_month = month_start.replace(month=month_start.month+1)
            month_end = next_month - timedelta(days=1)
            
            # Add month to labels
            month_label = month_start.strftime('%b %Y')
            labels.append(month_label)
            
            # Count internships created in this month
            month_domain = domain + [
                ('create_date', '>=', month_start.strftime('%Y-%m-%d')),
                ('create_date', '<=', month_end.strftime('%Y-%m-%d')),
            ]
            count = self.search_count(month_domain)
            data.append(count)
        
        return {
            'labels': labels,
            'data': data,
        }

    def _prepare_field_chart_data(self, internships):
        """Prepare data for field of study distribution chart"""
        field_data = {}
        
        for internship in internships:
            if internship.student_id and internship.student_id.field_of_study:
                field = internship.student_id.field_of_study
                field_data[field] = field_data.get(field, 0) + 1
        
        # Sort by count and take top 8
        sorted_data = sorted(field_data.items(), key=lambda x: x[1], reverse=True)[:8]
        
        return {
            'labels': [item[0] for item in sorted_data],
            'data': [item[1] for item in sorted_data],
        }

    def _prepare_pivot_data(self, internships):
        """Prepare data for pivot table - Academic Tutors by Status"""
        tutors = {}
        status_list = ['pending', 'ongoing', 'completed', 'cancelled']
        
        # Initialize tutors dictionary with zeros for each status
        for internship in internships:
            if internship.academic_tutor:
                if internship.academic_tutor not in tutors:
                    tutors[internship.academic_tutor] = {status: 0 for status in status_list}
        
        # Count internships by tutor and status
        for internship in internships:
            if internship.academic_tutor and internship.status in status_list:
                tutors[internship.academic_tutor][internship.status] += 1
        
        # Extract tutors with at least one internship
        tutor_names = list(tutors.keys())
        
        # Prepare values matrix
        values = []
        for tutor in tutor_names:
            row_values = [tutors[tutor][status] for status in status_list]
            values.append(row_values)
        
        return {
            'rows': tutor_names,
            'cols': status_list,
            'values': values,
        }

    def _get_recent_internships(self, domain):
        """Get list of recent internships"""
        # Find recently created or modified internships
        recent_domain = domain + ['|', 
            ('create_date', '>=', fields.Date.to_string(fields.Date.today() - timedelta(days=30))),
            ('write_date', '>=', fields.Date.to_string(fields.Date.today() - timedelta(days=30)))
        ]
        
        recent = self.search(recent_domain, order='write_date desc, create_date desc', limit=10)
        
        result = []
        for r in recent:
            result.append({
                'id': r.id,
                'name': r.name,
                'status': r.status,
                'student_name': r.student_id.name if r.student_id else '',
                'company_name': r.company_id.name if r.company_id else '',
                'start_date': fields.Date.to_string(r.start_date) if r.start_date else '',
                'end_date': fields.Date.to_string(r.end_date) if r.end_date else '',
            })
        
        return result