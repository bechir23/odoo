from odoo import models, fields, api, _
import base64
import tempfile
import os
import logging

_logger = logging.getLogger(__name__)

class InternshipStudent(models.Model):
    _name = 'internship.student'
    _description = 'Internship Student'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)
    student_number = fields.Char(string='Student Number')
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    field_of_study = fields.Char(string='Field of Study')
    level = fields.Selection([
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD')
    ], string='Level', default='bachelor')
    internship_ids = fields.One2many('internship.internship', 'student_id', string='Internships')
    resume_file = fields.Binary(string='Resume/CV', attachment=True)
    resume_filename = fields.Char(string='Resume Filename')
    resume_text = fields.Text(string='Extracted Resume Text')

    @api.onchange('resume_file', 'resume_filename')
    def _onchange_resume_file(self):
        for rec in self:
            if not rec.resume_file or not rec.resume_filename:
                rec.resume_text = False
                continue
            file_type = 'other'
            fname = rec.resume_filename.lower()
            if fname.endswith('.pdf'):
                file_type = 'pdf'
            elif any(fname.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.gif']):
                file_type = 'image'
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                    temp_file.write(base64.b64decode(rec.resume_file))
                    temp_file_path = temp_file.name
                extracted_text = ""
                if file_type == 'pdf':
                    try:
                        from PyPDF2 import PdfReader
                        reader = PdfReader(temp_file_path)
                        for page in reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                extracted_text += page_text + "\n"
                        if not extracted_text.strip():
                            extracted_text = rec._ocr_from_pdf(temp_file_path)
                    except Exception as e:
                        _logger.error(f"PDF extraction error: {str(e)}")
                        extracted_text = rec._ocr_from_pdf(temp_file_path)
                elif file_type == 'image':
                    try:
                        import pytesseract
                        from PIL import Image
                        with Image.open(temp_file_path) as image:
                            extracted_text = pytesseract.image_to_string(image, lang='eng')
                    except Exception as e:
                        _logger.error(f"OCR image error: {str(e)}")
                        extracted_text = f"OCR image error: {str(e)}"
                else:
                    extracted_text = "Unsupported file format."
                os.unlink(temp_file_path)
                rec.resume_text = extracted_text
            except Exception as e:
                _logger.error(f"Resume processing error: {str(e)}")
                rec.resume_text = f"Resume processing error: {str(e)}"

    def _ocr_from_pdf(self, pdf_path):
        try:
            from pdf2image import convert_from_path
            import pytesseract
            images = convert_from_path(pdf_path)
            extracted_text = ""
            for image in images:
                extracted_text += pytesseract.image_to_string(image, lang='eng') + "\n"
            return extracted_text
        except Exception as e:
            _logger.error(f"OCR PDF error: {str(e)}")
            return f"OCR PDF error: {str(e)}"