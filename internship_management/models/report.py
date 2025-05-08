from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging
import base64
import os
import tempfile

_logger = logging.getLogger(__name__)

class InternshipReport(models.Model):
    _name = 'internship.report'
    _description = 'Internship Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Title', required=True)
    internship_id = fields.Many2one('internship.internship', string='Internship', required=True)
    submission_date = fields.Date(string='Submission Date', default=fields.Date.context_today)
    report_file = fields.Binary(string='Report File', attachment=True)
    report_filename = fields.Char(string='Report Filename')
    type = fields.Selection([
        ('weekly', 'Weekly Report'),
        ('monthly', 'Monthly Report'),
        ('final', 'Final Report'),
    ], string='Report Type', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected')
    ], default='draft', tracking=True, required=True)
    
    student_id = fields.Many2one(related='internship_id.student_id', string='Student')
    company_id = fields.Many2one(related='internship_id.company_id', string='Company')
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    review_date = fields.Date(string='Review Date')
    feedback = fields.Text(string='Feedback', help='Feedback or comments from the reviewer about the report')
    is_validated = fields.Boolean(string='Validated', default=False)
    ocr_text = fields.Text(string="Texte extrait (OCR)")
    ocr_keywords_found = fields.Char(string="Sections détectées")
    ocr_keywords_missing = fields.Char(string="Sections manquantes")
    ocr_checked = fields.Boolean(string="Analyse OCR effectuée", default=False)

    @api.model_create_multi
    def create(self, vals_list):
        """When creating a report, ensure it starts in draft state"""
        for vals in vals_list:
            if 'state' not in vals:
                vals['state'] = 'draft'
        result = super(InternshipReport, self).create(vals_list)
        return result

    def write(self, vals):
        """Track changes to report status"""
        # Track status changes with a message
        if 'state' in vals and vals['state'] != self.state:
            new_state = vals['state']
            if new_state == 'submitted':
                self.message_post(body=_("Report has been submitted"))
            elif new_state == 'validated':
                self.message_post(body=_("Report has been validated"))
        
        return super(InternshipReport, self).write(vals)
    
    # Simple method implementations
    def action_process_ocr(self):
        """Process file with OCR only if it's an image, handle PDFs separately"""
        self.ensure_one()
        
        if not self.report_file:
            self.message_post(body=_("Please upload a file before processing."))
            return False
        
        # Determine file type based on filename
        file_type = 'other'
        if self.report_filename:
            if self.report_filename.lower().endswith('.pdf'):
                file_type = 'pdf'
            elif any(self.report_filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']):
                file_type = 'image'
        
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(base64.b64decode(self.report_file))
                temp_file_path = temp_file.name
            
            extracted_text = ""
            
            # Process based on file type
            if file_type == 'pdf':
                # For PDFs, we'll directly extract text without OCR
                try:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(temp_file_path)
                    
                    for page in reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            extracted_text += page_text + "\n"
                    
                    if not extracted_text.strip():
                        extracted_text = "PDF contient des images uniquement. Traitement OCR non effectué pour les PDFs."
                except Exception as e:
                    _logger.error(f"Error processing PDF: {str(e)}")
                    extracted_text = "PDF non lisible. Vérifiez que le fichier est valide."
                    
            elif file_type == 'image':
                # Only use OCR for image files
                try:
                    import pytesseract
                    from PIL import Image
                    with Image.open(temp_file_path) as image:
                        extracted_text = pytesseract.image_to_string(image, lang='fra')
                except Exception as e:
                    _logger.error(f"Error processing image: {str(e)}")
                    extracted_text = f"Erreur de traitement d'image: {str(e)}"
            else:
                extracted_text = "Format de fichier non supporté. Veuillez télécharger un PDF ou une image."
            
            # Clean up temporary file
            os.unlink(temp_file_path)
            
            # Check for required sections only if we have extracted text
            if extracted_text and extracted_text != "PDF contient des images uniquement. Traitement OCR non effectué pour les PDFs.":
                expected_keywords = ['introduction', 'remerciements', 'conclusion', 'objectifs', 'résultats']
                found_keywords = []
                missing_keywords = []
                
                for keyword in expected_keywords:
                    if keyword.lower() in extracted_text.lower():
                        found_keywords.append(keyword)
                    else:
                        missing_keywords.append(keyword)
                
                result = {
                    'ocr_checked': True,
                    'ocr_text': extracted_text,
                    'ocr_keywords_found': ', '.join(found_keywords) if found_keywords else 'Aucune section détectée',
                    'ocr_keywords_missing': ', '.join(missing_keywords) if missing_keywords else 'Toutes les sections requises sont présentes'
                }
            else:
                # For PDFs with only images, don't analyze sections
                result = {
                    'ocr_checked': True,
                    'ocr_text': extracted_text,
                    'ocr_keywords_found': 'Non analysé',
                    'ocr_keywords_missing': 'Non analysé'
                }
            
            # Update report with OCR results
            self.write(result)
            
            # Add log message
            msg = _("File processing completed")
            if file_type == 'pdf':
                msg += _(" (PDF document - text extraction only)")
            elif file_type == 'image':
                msg += _(" (Image file with OCR)")
            
            self.message_post(body=msg)
            return True
            
        except Exception as e:
            self.message_post(body=_("Error during file processing: %s") % str(e))
            return False
    
    def action_submit(self):
        """Submit the report"""
        self.ensure_one()
        
        # Check if we have a file before submission
        if not self.report_file:
            raise ValidationError(_("Please upload a report file before submitting."))
        
        # Update status
        self.write({
            'state': 'submitted',
            'submission_date': fields.Date.today(),
        })
        
        return True
    
    def action_validate(self):
        """Validate the report"""
        self.ensure_one()
        
        # Update status
        self.write({
            'state': 'validated',
            'is_validated': True,
            'reviewer_id': self.env.user.id,
            'review_date': fields.Date.today()
        })
        
        return True