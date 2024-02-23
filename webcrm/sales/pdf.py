import os

from django.conf import settings
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


class PDF:
    def __init__(self, file_name):
        self.file_name = f"{file_name}.pdf"

    def create_invoice(self, invoice):
        # Create a PDF document
        c = canvas.Canvas(self.file_name, pagesize=letter)
        width, height = letter

        # Add some custom text for headers
        c.setFont("Helvetica-Bold", 24)
        c.drawString(30, height - 50, "Your Invoice from Django Sales")
        c.setFont("Helvetica", 12)
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'assets', 'logo-crm2.png')
        with Image.open(logo_path) as img:
            original_width, original_height = img.size

            # Calculate the new logo dimensions
        aspect_ratio = original_width / original_height
        new_width = 80
        new_height = new_width / aspect_ratio

        c.drawImage(logo_path, 500, 700, width=new_width, height=new_height)
        c.drawString(60, 710, f"Invoice for {invoice.order.order_id}")
        c.drawString(60, 690, f"Date Created: {invoice.date_created}")
        c.drawString(60, 670, f"Due Date: {invoice.due_date}")
        c.drawString(60, 650, f"Status: {invoice.order.status}")
        c.drawString(60, 620, f"Total: {invoice.total} EUR")
        c.save()
        return self.file_name
