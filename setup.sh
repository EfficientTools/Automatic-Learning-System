#!/bin/bash

# Script de configuration pour le Système d'Apprentissage

echo "🧠 Configuration du Système d'Apprentissage Automatique..."

# Créer l'environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement virtuel
echo "🔄 Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "⬇️ Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Créer les répertoires nécessaires
echo "📁 Création des répertoires..."
mkdir -p output
mkdir -p logs

# Créer le template des variables d'environnement
echo "📝 Création du template de configuration..."
cat > .env.template << 'EOF'
# Clé API OpenAI pour les résumés de vidéos
OPENAI_API_KEY=votre_cle_openai_ici

# Configuration Kindle
KINDLE_EMAIL=votrenom@kindle.com
SENDER_EMAIL=votre.email@gmail.com
SMTP_PASSWORD=votre_mot_de_passe_app_ici
EOF

# Créer le fichier .env si il n'existe pas
if [ ! -f .env ]; then
    cp .env.template .env
    echo "📄 Fichier .env créé à partir du template"
fi

# Créer le script de test
cat > test_system.py << 'EOF'
#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration du système
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent / "src"))

from src.config import Config
from src.rss_aggregator import RSSAggregator

def test_configuration():
    print("🧪 Test de la configuration...")
    
    try:
        config = Config()
        print("✅ Configuration chargée avec succès")
        
        print(f"📰 Flux RSS configurés: {len(config.rss_feeds)}")
        print(f"🎥 Chaînes YouTube configurées: {len(config.youtube_channels)}")
        print(f"🤖 Clé OpenAI configurée: {'Oui' if config.openai_api_key else 'Non'}")
        print(f"📧 Email Kindle configuré: {'Oui' if config.kindle_email else 'Non'}")
        
        # Test d'un flux RSS
        if config.rss_feeds:
            print("\n📡 Test d'un flux RSS...")
            aggregator = RSSAggregator(config)
            articles = aggregator.process_feed(config.rss_feeds[0])
            print(f"✅ {len(articles)} articles récupérés du premier flux")
        
        print("\n🎉 Système prêt à fonctionner!")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")

if __name__ == "__main__":
    test_configuration()
EOF

chmod +x test_system.py

echo "✅ Configuration terminée!"
echo ""
echo "📋 Prochaines étapes:"
echo "1. Copiez .env.template vers .env et remplissez vos identifiants"
echo "2. Modifiez config.yaml avec vos flux RSS et chaînes YouTube"
echo "3. Testez avec: python test_system.py"
echo "4. Lancez le système avec: python main.py"
echo ""
echo "🔧 Configuration Kindle:"
echo "1. Allez sur https://www.amazon.com/myk"
echo "2. Ajoutez votre email expéditeur à la liste approuvée"
echo "3. Notez votre adresse @kindle.com"
echo ""
echo "🔑 Pour Gmail:"
echo "1. Activez l'authentification à 2 facteurs"
echo "2. Générez un mot de passe d'application"
echo "3. Utilisez ce mot de passe dans .env"
