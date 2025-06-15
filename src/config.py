"""
Gestion de la configuration pour le système d'apprentissage
"""

import os
from pathlib import Path
from typing import List, Dict, Any
import yaml

class Config:
    """Classe de configuration pour le système d'apprentissage"""
    
    def __init__(self, config_file: str = "config.yaml"):
        self.config_file = Path(config_file)
        self.load_config()
    
    def load_config(self):
        """Charger la configuration depuis le fichier YAML"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self._config = yaml.safe_load(f)
        else:
            self._config = self.get_default_config()
            self.save_config()
    
    def save_config(self):
        """Sauvegarder la configuration actuelle dans le fichier"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
    
    def get_default_config(self) -> Dict[str, Any]:
        """Obtenir la configuration par défaut"""
        return {
            'rss_feeds': [
                'https://feeds.feedburner.com/oreilly',
                'https://blog.pragmaticengineer.com/rss/',
                'https://martinfowler.com/feed.atom',
                'https://hbr.org/feed',
                'https://feeds.harvard.edu/blog/gazette'
            ],
            'youtube_channels': [
                # Remplacer par de vrais IDs de chaînes YouTube
                # Pour trouver l'ID: aller sur la chaîne > voir le code source > chercher "channelId"
            ],
            'openai': {
                'api_key': os.getenv('OPENAI_API_KEY', ''),
                'model': 'gpt-4o-mini'  # Modèle plus économique
            },
            'kindle': {
                'email': os.getenv('KINDLE_EMAIL', ''),
                'sender_email': os.getenv('SENDER_EMAIL', ''),
                'smtp_server': 'smtp.gmail.com',
                'smtp_port': 587,
                'smtp_password': os.getenv('SMTP_PASSWORD', '')
            },
            'output': {
                'output_dir': 'output',
                'max_articles_per_feed': 3,
                'max_video_summaries': 2,
                'days_lookback': 2  # Nombre de jours à regarder en arrière
            }
        }
    
    @property
    def rss_feeds(self) -> List[str]:
        return self._config.get('rss_feeds', [])
    
    @property
    def youtube_channels(self) -> List[str]:
        return self._config.get('youtube_channels', [])
    
    @property
    def openai_api_key(self) -> str:
        return self._config.get('openai', {}).get('api_key', '')
    
    @property
    def openai_model(self) -> str:
        return self._config.get('openai', {}).get('model', 'gpt-4o-mini')
    
    @property
    def kindle_email(self) -> str:
        return self._config.get('kindle', {}).get('email', '')
    
    @property
    def sender_email(self) -> str:
        return self._config.get('kindle', {}).get('sender_email', '')
    
    @property
    def smtp_config(self) -> Dict[str, Any]:
        return self._config.get('kindle', {})
    
    @property
    def output_dir(self) -> Path:
        return Path(self._config.get('output', {}).get('output_dir', 'output'))
    
    @property
    def max_articles_per_feed(self) -> int:
        return self._config.get('output', {}).get('max_articles_per_feed', 3)
    
    @property
    def max_video_summaries(self) -> int:
        return self._config.get('output', {}).get('max_video_summaries', 2)
    
    @property
    def days_lookback(self) -> int:
        return self._config.get('output', {}).get('days_lookback', 2)
