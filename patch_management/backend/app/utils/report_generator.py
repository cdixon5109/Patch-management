from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
from typing import List, Dict, Any
import os
from datetime import datetime
from app.core.config import settings

class ReportGenerator:
    def __init__(self, output_dir: str = None):
        self.output_dir = output_dir or settings.UPLOAD_DIR
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_pdf_report(self, title: str, data: List[Dict[str, Any]], columns: List[str]) -> str:
        filename = f"{title.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        doc = SimpleDocTemplate(filepath, pagesize=letter)
        elements = []

        # Add title
        styles = getSampleStyleSheet()
        elements.append(Paragraph(title, styles["Title"]))

        # Convert data to table format
        table_data = [columns]
        for row in data:
            table_data.append([row.get(col, "") for col in columns])

        # Create table
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        elements.append(table)
        doc.build(elements)
        return filepath

    def generate_csv_report(self, title: str, data: List[Dict[str, Any]], columns: List[str]) -> str:
        filename = f"{title.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = os.path.join(self.output_dir, filename)

        df = pd.DataFrame(data)
        df = df[columns]  # Reorder columns
        df.to_csv(filepath, index=False)
        return filepath

    def generate_compliance_report(self, servers: List[Dict[str, Any]]) -> str:
        columns = ["hostname", "os_type", "os_version", "last_patch_check", 
                  "pending_updates", "security_updates", "compliance_status"]
        return self.generate_pdf_report("Patch Compliance Report", servers, columns)

    def generate_patch_status_report(self, patches: List[Dict[str, Any]]) -> str:
        columns = ["patch_name", "patch_version", "patch_type", "affected_servers",
                  "status", "install_date"]
        return self.generate_pdf_report("Patch Status Report", patches, columns)

    def generate_analytics_report(self, analytics: Dict[str, Any]) -> str:
        columns = ["metric_name", "metric_type", "value", "time_period"]
        data = []
        for metric_name, metric_data in analytics.items():
            data.append({
                "metric_name": metric_name,
                "metric_type": metric_data.get("type", ""),
                "value": metric_data.get("value", ""),
                "time_period": metric_data.get("period", "")
            })
        return self.generate_pdf_report("Analytics Report", data, columns) 