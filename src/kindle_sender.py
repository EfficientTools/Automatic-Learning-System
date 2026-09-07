"""
Expéditeur Kindle par Email
Envoie les PDFs générés vers Kindle via email
"""

import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path
from datetime import datetime

class KindleSender:
    """Envoie du contenu vers Kindle via email"""
    
    def __init__(self, config):
        self.config = config
    
    def send_to_kindle(self, pdf_path: Path) -> bool:
        """Envoyer le PDF à l'adresse email Kindle"""
        if not self.config.kindle_email or not self.config.sender_email:
            print("⚠️ Email Kindle ou email expéditeur non configuré")
            print("ℹ️ Pour configurer:")
            print("   1. Allez sur https://www.amazon.com/myk")
            print("   2. Ajoutez votre email expéditeur à la liste approuvée")
            print("   3. Notez votre adresse @kindle.com")
            return False
        
        smtp_config = self.config.smtp_config
        if not smtp_config.get('smtp_password'):
            print("⚠️ Mot de passe SMTP non configuré")
            print("ℹ️ Pour Gmail, utilisez un mot de passe d'application:")
            print("   1. Activez la 2FA sur votre compte Google")
            print("   2. Générez un mot de passe d'application")
            print("   3. Utilisez ce mot de passe dans la configuration")
            return False
        
        try:
            # Créer le message
            msg = MIMEMultipart()
            msg['From'] = self.config.sender_email
            msg['To'] = self.config.kindle_email
            msg['Subject'] = f"Journal d'Apprentissage - {datetime.now().strftime('%d/%m/%Y')}"
            
            # Corps de l'email
            body = f"""
📚 Votre journal d'apprentissage quotidien est en pièce jointe !

Ce PDF contient :
• Les derniers articles de vos flux RSS
• Des résumés IA des vidéos récentes
• Des QR codes pour accéder aux sources originales

Date : {datetime.now().strftime('%d %B %Y')}
Taille du fichier : {pdf_path.stat().st_size / 1024:.1f} KB

Bonne lecture ! 🧠✨

---
Généré automatiquement par votre Système d'Apprentissage
            """
            
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            # Attacher le PDF
            with open(pdf_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename= {pdf_path.name}'
                )
                msg.attach(part)
            
            # Envoyer l'email
            print(f"📧 Connexion au serveur SMTP...")
            server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'], timeout=30)
            server.starttls(context=ssl.create_default_context())
            server.login(smtp_config['sender_email'], smtp_config['smtp_password'])
            
            print(f"📤 Envoi vers {self.config.kindle_email}...")
            server.send_message(msg)
            server.quit()
            
            print(f"✅ Message accepté par le serveur SMTP pour: {self.config.kindle_email}")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("❌ Erreur d'authentification SMTP")
            print("ℹ️ Vérifiez vos identifiants et utilisez un mot de passe d'application pour Gmail")
            return False
        except smtplib.SMTPRecipientsRefused:
            print("❌ Adresse email Kindle refusée")
            print("ℹ️ Vérifiez que votre email expéditeur est autorisé sur Amazon")
            return False
        except Exception as e:
            print(f"❌ Échec de l'envoi vers Kindle: {e}")
            return False
