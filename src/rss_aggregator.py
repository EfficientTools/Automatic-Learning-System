"""
Agrégateur de flux RSS
Collecte et traite les flux RSS
"""

import feedparser
import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from dataclasses import dataclass
import time
import re
import html
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

@dataclass
class Article:
    """Structure de données pour un article"""
    title: str
    content: str
    url: str
    published: datetime
    source: str
    summary: str = ""

class RSSAggregator:
    """Agrégateur de flux RSS"""
    
    def __init__(self, config):
        self.config = config
        self.articles: List[Article] = []
    
    def collect_articles(self) -> List[Article]:
        """Collecter les articles de tous les flux RSS"""
        all_articles = []
        
        if not self.config.rss_feeds:
            print("⚠️ Aucun flux RSS configuré")
            return all_articles
        
        for feed_url in self.config.rss_feeds:
            try:
                print(f"📡 Traitement du flux: {feed_url}")
                articles = self.process_feed(feed_url)
                all_articles.extend(articles)
                time.sleep(1)  # Être respectueux avec les serveurs
            except Exception as e:
                print(f"⚠️ Erreur lors du traitement du flux {feed_url}: {e}")
                continue
        
        # Trier par date de publication (plus récent en premier)
        all_articles.sort(key=lambda x: x.published, reverse=True)
        
        # Écarter les doublons: un même lien revient souvent via plusieurs flux
        # (agrégateurs). Le tri ci-dessus garde la version la plus récente.
        unique_articles = []
        seen_urls = set()
        for article in all_articles:
            key = self.normalise_url(article.url)
            if key in seen_urls:
                print(f"↔️ Doublon ignoré: {article.title}")
                continue
            seen_urls.add(key)
            unique_articles.append(article)
        
        return unique_articles
    
    def process_feed(self, feed_url: str) -> List[Article]:
        """Traiter un seul flux RSS"""
        try:
            # Configuration des headers pour éviter les blocages
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }
            
            # Récupérer le flux avec un timeout
            response = requests.get(feed_url, headers=headers, timeout=10)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
        except Exception as e:
            print(f"⚠️ Erreur lors de la récupération du flux {feed_url}: {e}")
            return []
        
        if not feed.entries:
            print(f"⚠️ Aucune entrée trouvée dans le flux: {feed_url}")
            return []
        
        source_name = feed.feed.get('title', feed_url)
        articles = []
        
        # Date limite (articles récents uniquement)
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=self.config.days_lookback)
        
        # Filtrer sur la date avant de limiter: certains flux ne sont pas triés
        # par date et épinglent d'anciennes entrées en tête.
        recent_entries = []
        for entry in feed.entries:
            published = self.parse_published(entry)
            if published >= cutoff_date:
                recent_entries.append((entry, published))
        
        for entry, published in recent_entries[:self.config.max_articles_per_feed]:
            try:
                # Obtenir le contenu
                content = self.extract_content(entry)
                
                # Nettoyer et limiter le contenu
                content = self.clean_content(content)
                
                article = Article(
                    title=self.clean_text(entry.title),
                    content=content,
                    url=entry.link,
                    published=published,
                    source=source_name,
                    summary=self.create_summary(content)
                )
                
                articles.append(article)
                
            except Exception as e:
                print(f"⚠️ Erreur lors du traitement de l'entrée: {e}")
                continue
        
        return articles
    
    def normalise_url(self, url: str) -> str:
        """Normaliser une URL pour comparer deux liens équivalents"""
        if not url:
            return ""
        
        cleaned = url.strip()
        
        # Ignorer la casse du schéma et du domaine, ainsi qu'un slash final
        parts = urlsplit(cleaned)
        path = parts.path.rstrip('/') or '/'
        
        # Retirer les paramètres de suivi, qui diffèrent d'un flux à l'autre
        query = urlencode([(name, value) for name, value in parse_qsl(parts.query)
                           if not name.lower().startswith('utm_')
                           and name.lower() not in {'fbclid', 'gclid', 'ref', 'source'}])
        
        return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, query, ''))
    
    def parse_published(self, entry) -> datetime:
        """Lire la date de publication d'une entrée, en UTC"""
        for attribute in ('published_parsed', 'updated_parsed'):
            value = getattr(entry, attribute, None)
            if value:
                return datetime(*value[:6], tzinfo=timezone.utc)
        
        # Sans date exploitable, considérer l'entrée comme actuelle
        return datetime.now(timezone.utc)
    
    def extract_content(self, entry) -> str:
        """Extraire le contenu de l'entrée RSS"""
        content = ""
        
        # Essayer différentes sources de contenu
        if hasattr(entry, 'content') and entry.content:
            content = entry.content[0].value
        elif hasattr(entry, 'summary'):
            content = entry.summary
        elif hasattr(entry, 'description'):
            content = entry.description
        
        return content
    
    def clean_content(self, content: str) -> str:
        """Nettoyer le contenu HTML et le limiter"""
        if not content:
            return ""
        
        # Décoder les entités HTML
        content = html.unescape(content)
        
        # Supprimer les balises HTML
        content = re.sub(r'<[^>]+>', '', content)
        
        # Nettoyer les espaces multiples et les retours à la ligne
        content = re.sub(r'\s+', ' ', content)
        content = content.strip()
        
        # Limiter la longueur (pour éviter des PDFs trop longs)
        if len(content) > 1000:
            content = content[:1000] + "..."
        
        return content
    
    def clean_text(self, text: str) -> str:
        """Nettoyer un texte simple"""
        if not text:
            return ""
        
        text = html.unescape(text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def create_summary(self, content: str) -> str:
        """Créer un résumé simple du contenu"""
        if not content:
            return ""
        
        # Prendre les 200 premiers caractères
        summary = content[:200]
        if len(content) > 200:
            summary += "..."
        
        return summary
