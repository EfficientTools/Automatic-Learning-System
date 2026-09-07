# 🚀 Guide de Démarrage Rapide

## Étape 1 : Installation
```bash
# Cloner le projet (si nécessaire)
git clone https://github.com/EfficientTools/Automatic-Learning-System.git learning-system
cd learning-system

# Installer automatiquement
chmod +x setup.sh
./setup.sh
```

## Étape 2 : Configuration Minimale

### 2.1 Configuration des flux RSS
Éditez `config.yaml` et ajoutez vos flux favoris :
```yaml
rss_feeds:
  - "https://votreblog.com/feed"
  - "https://autresite.com/rss"
```

### 2.2 (Optionnel) Configuration OpenAI pour YouTube
1. Obtenez une clé API sur https://platform.openai.com/api-keys
2. Créez le fichier `.env` :
```bash
test -f .env || cp .env.template .env
# Éditez .env et ajoutez votre clé
```

### 2.3 (Optionnel) Configuration Kindle
1. Allez sur https://www.amazon.com/myk
2. Notez votre adresse `@kindle.com`
3. Autorisez votre email expéditeur
4. Ajoutez vos identifiants dans `.env`

## Étape 3 : Premier Test
```bash
# Tester la configuration
venv/bin/python test_system.py

# Générer votre premier journal
venv/bin/python main.py
```

## Étape 4 : Automatisation (Optionnel)
```bash
# Planifier l'exécution quotidienne à 7h
crontab -e

# Ajouter cette ligne :
0 7 * * * /chemin/vers/learning-system/run_daily.sh
```

## 🎯 Résultat
Vous obtiendrez un PDF formaté avec :
- ✅ Articles RSS récents
- ✅ QR codes pour les sources
- ✅ Résumés AI des vidéos (si configuré)
- ✅ Envoi automatique Kindle (si configuré)

Le fichier sera sauvegardé dans `output/journal_apprentissage_YYYY-MM-DD.pdf`
