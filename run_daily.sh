#!/bin/bash

# Script d'exécution quotidienne - ajouter au crontab pour l'automatisation
# Exemple d'entrée crontab: 0 7 * * * /Users/pierre-henrysoria/Code/learning-system/run_daily.sh

# Aller dans le répertoire du script
cd "$(dirname "$0")"

# Activer l'environnement virtuel
source venv/bin/activate

# Créer le répertoire de logs s'il n'existe pas
mkdir -p logs

# Exécuter le système et logger la sortie
echo "$(date): Début de la génération du journal quotidien" >> logs/daily.log
python main.py >> logs/daily.log 2>&1
exit_code=$?

if [ $exit_code -eq 0 ]; then
    echo "$(date): Journal quotidien généré avec succès" >> logs/daily.log
else
    echo "$(date): Erreur lors de la génération du journal (code: $exit_code)" >> logs/daily.log
fi

# Nettoyer les anciens logs (garder 30 jours)
find logs -name "*.log" -mtime +30 -delete

echo "$(date): Fin de l'exécution quotidienne" >> logs/daily.log
