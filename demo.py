#!/usr/bin/env python3
"""
🎬 Démonstration du Système d'Apprentissage
Génère un journal de test avec des données fictives pour montrer les fonctionnalités
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from dataclasses import dataclass

# Ajouter src au path
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import Config
from src.pdf_generator import PDFGenerator

@dataclass
class DemoArticle:
    """Article de démonstration"""
    title: str
    content: str
    url: str
    published: datetime
    source: str
    summary: str = ""

@dataclass
class DemoVideoSummary:
    """Résumé de vidéo de démonstration"""
    title: str
    summary: str
    url: str
    published: datetime
    source: str = "YouTube"
    channel_name: str = ""

def create_demo_content():
    """Créer du contenu de démonstration"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)

    # Articles de démonstration
    demo_articles = [
        DemoArticle(
            title="Les Tendances Technologiques de 2025",
            content="Cette année marque un tournant dans l'adoption de l'intelligence artificielle. "
                   "Les entreprises intègrent massivement des solutions d'IA générative pour améliorer "
                   "leur productivité. L'automatisation intelligente transforme les workflows traditionnels "
                   "et crée de nouvelles opportunités d'innovation. Les développeurs adoptent des outils "
                   "comme GitHub Copilot et ChatGPT pour accélérer le développement.",
            url="https://techblog.example.com/tendances-2025",
            published=today,
            source="TechBlog Pro",
            summary="Analyse des principales tendances technologiques et de l'impact de l'IA générative sur les entreprises."
        ),
        DemoArticle(
            title="Méthodes d'Apprentissage Efficaces",
            content="L'apprentissage espacé et la technique Feynman restent les méthodes les plus efficaces "
                   "pour retenir l'information à long terme. La recherche montre que combiner la lecture active, "
                   "la prise de notes manuscrites et la révision programmée améliore significativement la rétention. "
                   "Les applications de répétition espacée comme Anki revolutionnent l'éducation personnalisée.",
            url="https://learninghub.example.com/methodes-efficaces",
            published=yesterday,
            source="Learning Hub",
            summary="Guide pratique des techniques d'apprentissage basées sur la science cognitive."
        ),
        DemoArticle(
            title="L'Avenir du Travail à Distance",
            content="Le travail hybride s'impose comme la nouvelle norme dans 73% des entreprises technologiques. "
                   "Les outils de collaboration asynchrone se perfectionnent et permettent une coordination efficace "
                   "des équipes distribuées. La productivité augmente de 25% quand les employés choisissent leur "
                   "environnement de travail optimal. Les défis restent la cohésion d'équipe et la formation.",
            url="https://businessinsight.example.com/travail-remote",
            published=today,
            source="Business Insight",
            summary="Analyse de l'évolution du travail à distance et de son impact sur la productivité."
        )
    ]

    # Résumés de vidéos de démonstration
    demo_videos = [
        DemoVideoSummary(
            title="Comment Optimiser Votre Cerveau pour l'Apprentissage",
            summary="Cette vidéo explore les mécanismes neurologiques de l'apprentissage et propose des stratégies "
                   "concrètes pour améliorer la mémorisation. L'auteur explique l'importance du sommeil, de l'exercice "
                   "et de la nutrition sur les fonctions cognitives. Il présente également des techniques de "
                   "méditation et de respiration qui favorisent la concentration et la créativité.",
            url="https://youtube.com/watch?v=demo123",
            published=today,
            channel_name="NeuroScience Channel"
        ),
        DemoVideoSummary(
            title="Productivité : 5 Habitudes des Experts",
            summary="Analyse des habitudes communes aux personnes hautement productives. La vidéo révèle que "
                   "la planification matinale, la technique Pomodoro, et la priorisation selon la matrice d'Eisenhower "
                   "sont des facteurs clés. L'importance de dire 'non' aux distractions et de créer des rituels "
                   "de travail est également soulignée avec des exemples concrets d'application.",
            url="https://youtube.com/watch?v=demo456",
            published=yesterday,
            channel_name="Productivity Masters"
        )
    ]

    return demo_articles + demo_videos

def main():
    """Générer un journal de démonstration"""
    print("🎬 Génération d'un journal de démonstration...")

    # Créer le contenu de démonstration
    demo_content = create_demo_content()

    # Initialiser la configuration
    config = Config()

    # Générer le PDF
    pdf_generator = PDFGenerator(config)

    print(f"📄 Génération du PDF de démonstration...")

    # Utiliser la méthode standard pour générer le PDF
    demo_path = pdf_generator.create_journal(demo_content, demo=True)

    print(f"✅ Journal de démonstration généré: {demo_path}")
    print(f"📊 Contenu inclus:")
    print(f"   📰 {len([x for x in demo_content if hasattr(x, 'source') and x.source != 'YouTube'])} articles")
    print(f"   🎥 {len([x for x in demo_content if hasattr(x, 'source') and x.source == 'YouTube'])} résumés vidéos")
    print(f"📄 Taille du fichier: {demo_path.stat().st_size / 1024:.1f} KB")

    print("\n🎯 Le journal de démonstration montre :")
    print("   ✅ Formatage professionnel avec QR codes")
    print("   ✅ Articles RSS avec métadonnées")
    print("   ✅ Résumés de vidéos YouTube")
    print("   ✅ Navigation par QR codes vers les sources")
    print("   ✅ Mise en page optimisée pour Kindle")

if __name__ == "__main__":
    main()
