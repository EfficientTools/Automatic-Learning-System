"""
Générateur de PDF avec QR Codes
Génère un journal PDF formaté avec des QR codes pour chaque article
"""

import qrcode
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import black, blue, grey
from io import BytesIO
from datetime import datetime
from pathlib import Path
from typing import List
import textwrap

class PDFGenerator:
    """Générateur de PDF avec QR codes"""
    
    def __init__(self, config):
        self.config = config
        self.output_dir = config.output_dir
        self.output_dir.mkdir(exist_ok=True)
    
    def create_journal(self, content_items: List) -> Path:
        """Créer un journal PDF avec tous les éléments de contenu"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"journal_apprentissage_{today}.pdf"
        filepath = self.output_dir / filename
        
        doc = SimpleDocTemplate(
            str(filepath), 
            pagesize=A4, 
            leftMargin=1*cm, 
            rightMargin=1*cm,
            topMargin=1*cm, 
            bottomMargin=1*cm
        )
        
        story = []
        styles = self.create_custom_styles()
        
        # Titre du journal
        story.append(Paragraph(f"📚 Journal d'Apprentissage", styles['JournalTitle']))
        story.append(Paragraph(f"{datetime.now().strftime('%d %B %Y')}", styles['DateStyle']))
        story.append(Spacer(1, 20))
        
        # Résumé du contenu
        story.append(Paragraph("📋 Contenu d'aujourd'hui", styles['SectionHeader']))
        
        # Compter les types de contenu
        articles_count = len([item for item in content_items if hasattr(item, 'source') and item.source != 'YouTube'])
        videos_count = len([item for item in content_items if hasattr(item, 'source') and item.source == 'YouTube'])
        
        summary_data = [
            ['📰 Articles RSS', f'{articles_count} articles'],
            ['🎥 Résumés vidéos', f'{videos_count} vidéos'],
            ['📖 Total', f'{len(content_items)} éléments']
        ]
        
        summary_table = Table(summary_data, colWidths=[4*cm, 3*cm])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), 'white'),
            ('GRID', (0, 0), (-1, -1), 1, black)
        ]))
        
        story.append(summary_table)
        story.append(PageBreak())
        
        # Ajouter chaque élément de contenu
        for i, item in enumerate(content_items, 1):
            self.add_content_item(story, item, i, styles)
            if i < len(content_items):
                story.append(PageBreak())
        
        # Footer avec informations
        story.append(Spacer(1, 30))
        story.append(Paragraph(
            "🤖 Généré automatiquement par le Système d'Apprentissage Automatique", 
            styles['Footer']
        ))
        
        # Construire le PDF
        doc.build(story)
        print(f"📄 PDF généré: {filepath}")
        return filepath
    
    def create_custom_styles(self):
        """Créer des styles personnalisés pour le PDF"""
        styles = getSampleStyleSheet()
        
        # Style pour le titre principal
        styles.add(ParagraphStyle(
            name='JournalTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=10,
            alignment=TA_CENTER,
            textColor=blue
        ))
        
        # Style pour la date
        styles.add(ParagraphStyle(
            name='DateStyle',
            parent=styles['Normal'],
            fontSize=12,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=grey
        ))
        
        # Style pour les en-têtes de section
        styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=blue
        ))
        
        # Style pour les titres d'articles
        styles.add(ParagraphStyle(
            name='ArticleTitle',
            parent=styles['Heading3'],
            fontSize=14,
            spaceAfter=8,
            spaceBefore=15,
            textColor=black
        ))
        
        # Style pour les métadonnées
        styles.add(ParagraphStyle(
            name='Metadata',
            parent=styles['Normal'],
            fontSize=9,
            spaceAfter=10,
            textColor=grey
        ))
        
        # Style pour le contenu principal
        styles.add(ParagraphStyle(
            name='MainContent',
            parent=styles['Normal'],
            fontSize=11,
            spaceAfter=15,
            alignment=TA_LEFT,
            leading=14
        ))
        
        # Style pour le footer
        styles.add(ParagraphStyle(
            name='Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=grey
        ))
        
        return styles
    
    def add_content_item(self, story: List, item, index: int, styles):
        """Ajouter un élément de contenu à l'histoire"""
        # Titre avec index
        story.append(Paragraph(f"{index}. {item.title}", styles['ArticleTitle']))
        
        # Informations sur la source et la date
        if hasattr(item, 'source') and item.source == 'YouTube':
            source_info = f"🎥 {item.channel_name} | 📅 {item.published.strftime('%d/%m/%Y')}"
        else:
            source_info = f"📰 {item.source} | 📅 {item.published.strftime('%d/%m/%Y')}"
        
        story.append(Paragraph(source_info, styles['Metadata']))
        
        # Contenu principal
        content_text = ""
        if hasattr(item, 'summary') and item.summary:
            content_text = item.summary
        elif hasattr(item, 'content') and item.content:
            content_text = item.content
        
        if content_text:
            # Diviser le contenu en paragraphes si nécessaire
            paragraphs = content_text.split('\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), styles['MainContent']))
        
        story.append(Spacer(1, 15))
        
        # QR Code et lien
        if hasattr(item, 'url') and item.url:
            # Créer une table pour aligner le QR code et le texte
            qr_image = self.generate_qr_code(item.url)
            url_text = f"🔗 Scanner pour visiter:<br/><font size=8>{item.url}</font>"
            
            qr_table = Table(
                [[qr_image, Paragraph(url_text, styles['Metadata'])]],
                colWidths=[2.5*cm, 12*cm]
            )
            qr_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            
            story.append(qr_table)
        
        story.append(Spacer(1, 20))
    
    def generate_qr_code(self, url: str) -> Image:
        """Générer un QR code pour l'URL"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=2,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir en BytesIO
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Créer une Image ReportLab
        return Image(buffer, width=2*cm, height=2*cm)
