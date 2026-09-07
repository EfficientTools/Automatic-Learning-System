"""
Résumeur de vidéos YouTube
Traite les flux RSS YouTube et génère des résumés IA
"""

import feedparser
import requests
from openai import OpenAI
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from dataclasses import dataclass
import re
import time
import html

@dataclass
class VideoSummary:
    """Structure de données pour un résumé de vidéo"""
    title: str
    summary: str
    url: str
    published: datetime
    source: str
    channel_name: str

class YouTubeSummarizer:
    """Résumeur de vidéos YouTube utilisant l'IA"""
    
    def __init__(self, config):
        self.config = config
        self.client = OpenAI(api_key=config.openai_api_key) if config.openai_api_key else None
    
    def process_videos(self) -> List[VideoSummary]:
        """Traiter les vidéos des chaînes YouTube"""
        if not self.client:
            print("⚠️ Clé API OpenAI non configurée, résumés de vidéos ignorés")
            return []
        
        if not self.config.youtube_channels:
            print("ℹ️ Aucune chaîne YouTube configurée")
            return []
        
        all_summaries = []
        
        for channel_id in self.config.youtube_channels:
            try:
                print(f"🎥 Traitement de la chaîne YouTube: {channel_id}")
                summaries = self.process_channel(channel_id)
                all_summaries.extend(summaries)
                time.sleep(2)  # Limitation du taux
            except Exception as e:
                print(f"⚠️ Erreur lors du traitement de la chaîne {channel_id}: {e}")
                continue
        
        # Trier par date de publication (plus récent en premier)
        all_summaries.sort(key=lambda x: x.published, reverse=True)
        
        return all_summaries[:self.config.max_video_summaries]
    
    def process_channel(self, channel_id: str) -> List[VideoSummary]:
        """Traiter une seule chaîne YouTube"""
        # URL du flux RSS YouTube
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            response = requests.get(rss_url, headers=headers, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except Exception as e:
            print(f"⚠️ Échec du parsing du RSS YouTube pour la chaîne {channel_id}: {e}")
            return []
        
        if not feed.entries:
            print(f"⚠️ Aucune vidéo trouvée pour la chaîne: {channel_id}")
            return []
        
        channel_name = feed.feed.get('title', f'Chaîne {channel_id}')
        summaries = []
        
        # Date limite (vidéos récentes uniquement)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.config.days_lookback)
        
        for entry in feed.entries[:2]:  # Max 2 vidéos par chaîne
            try:
                # Parser la date de publication
                published = datetime.now(timezone.utc)
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                
                # Ignorer les vidéos trop anciennes
                if published < cutoff_date:
                    continue
                
                # Obtenir les métadonnées de la vidéo
                video_url = entry.link
                video_title = self.clean_text(entry.title)
                video_description = self.clean_text(entry.get('summary', ''))
                
                # Générer le résumé avec l'IA
                summary = self.generate_video_summary(video_title, video_description)
                
                if summary:
                    video_summary = VideoSummary(
                        title=video_title,
                        summary=summary,
                        url=video_url,
                        published=published,
                        source="YouTube",
                        channel_name=channel_name
                    )
                    summaries.append(video_summary)
                
            except Exception as e:
                print(f"⚠️ Erreur lors du traitement de la vidéo: {e}")
                continue
        
        return summaries
    
    def generate_video_summary(self, title: str, description: str) -> str:
        """Générer un résumé IA du contenu vidéo"""
        try:
            prompt = f"""
            Créez un résumé concis (2-3 paragraphes) de cette vidéo YouTube basé sur son titre et sa description.
            Concentrez-vous sur les points clés et les enseignements principaux qui seraient précieux pour l'apprentissage.
            Répondez en français et soyez informatif mais concis.
            
            Titre de la vidéo: {title}
            
            Description: {description[:800]}...
            
            Résumé:
            """
            
            response = self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=[
                    {"role": "system", "content": "Vous êtes un assistant qui crée des résumés concis et informatifs de contenu éducatif en français."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=250,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la génération du résumé: {e}")
            return f"Résumé non disponible. Vidéo: {title}"
    
    def clean_text(self, text: str) -> str:
        """Nettoyer un texte"""
        if not text:
            return ""
        
        text = html.unescape(text)
        text = re.sub(r'<[^>]+>', '', text)  # Supprimer les balises HTML
        text = re.sub(r'\s+', ' ', text)     # Nettoyer les espaces
        return text.strip()
