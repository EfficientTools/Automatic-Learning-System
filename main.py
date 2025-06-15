#!/usr/bin/env python3
"""
🧠 Système d'Apprentissage Automatique
Génère un journal personnalisé quotidien avec flux RSS, résumés YouTube et QR codes
Envoi automatique vers Kindle
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Ajouter src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.rss_aggregator import RSSAggregator
from src.youtube_summarizer import YouTubeSummarizer
from src.pdf_generator import PDFGenerator
from src.kindle_sender import KindleSender
from src.config import Config

def main():
    """Fonction principale pour orchestrer le système d'apprentissage"""
    print("🧠 Démarrage du Système d'Apprentissage Automatique...")
    
    # Initialiser la configuration
    config = Config()
    
    # Initialiser les composants
    rss_aggregator = RSSAggregator(config)
    youtube_summarizer = YouTubeSummarizer(config)
    pdf_generator = PDFGenerator(config)
    kindle_sender = KindleSender(config)
    
    try:
        # Étape 1: Collecter les articles RSS
        print("📰 Collecte des articles RSS...")
        articles = rss_aggregator.collect_articles()
        print(f"✅ {len(articles)} articles collectés")
        
        # Étape 2: Traiter les vidéos YouTube
        print("🎥 Traitement des vidéos YouTube...")
        video_summaries = youtube_summarizer.process_videos()
        print(f"✅ {len(video_summaries)} résumés de vidéos générés")
        
        # Étape 3: Combiner tout le contenu
        all_content = articles + video_summaries
        
        if not all_content:
            print("⚠️ Aucun contenu trouvé pour aujourd'hui")
            return 0
        
        # Étape 4: Générer le PDF avec QR codes
        print("📄 Génération du journal PDF...")
        pdf_path = pdf_generator.create_journal(all_content)
        
        # Étape 5: Envoyer vers Kindle
        print("📧 Envoi vers Kindle...")
        success = kindle_sender.send_to_kindle(pdf_path)
        
        if success:
            print("✅ Journal quotidien envoyé avec succès vers Kindle!")
        else:
            print("⚠️ Erreur lors de l'envoi vers Kindle, mais le PDF est disponible localement")
            print(f"📁 Fichier généré: {pdf_path}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
