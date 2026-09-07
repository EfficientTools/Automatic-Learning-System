# Système d'Apprentissage Automatique 🧠

Un système intelligent qui génère automatiquement un journal d'apprentissage personnalisé quotidien et l'envoie directement sur votre Kindle.


## État vérifié

Python **3.12** est l'environnement testé. `setup.sh` installe `requirements.lock`,
préserve `.env` et les scripts existants, puis propose des commandes explicites.
Les variables exportées sont prioritaires sur `.env`, puis sur YAML. Les secrets
restent dans l'environnement; les valeurs par défaut sauvegardées ne les copient
pas dans `config.yaml`.

```bash
venv/bin/python test_system.py  # 12 régressions hors ligne
venv/bin/python verify.py       # présence des fichiers et imports uniquement
venv/bin/python demo.py         # PDF fictif séparé du vrai journal quotidien
```

La commande réelle `venv/bin/python main.py` contacte les flux configurés et peut
utiliser OpenAI puis envoyer un email si les identifiants sont renseignés. Ne
l'utilisez pas comme simple test. Aucun envoi ni automatisation n'est installé
par `setup.sh`. Un message accepté par SMTP ne prouve pas sa réception sur Kindle.

Les notes YouTube utilisent seulement le **titre et la description RSS**, pas la
transcription ou le contenu vidéo. Vérifiez les faits avant utilisation. Les
articles RSS sont des extraits, pas une analyse complète des sources.

Validation locale : 12 tests, contrôle des dépendances, scripts shell et démo
PDF de six pages inspectée. Aucun appel réel OpenAI/SMTP ni livraison Kindle
vérifié. La mise en page reste A4 avec une page par élément; elle n'est pas validée
sur Kindle. Helvetica couvre le texte français de la démo, mais pas tous les
caractères Unicode possibles dans des flux tiers. Aucun workflow CI n'est encore
configuré.

[Capture historique de la démo (juin 2025)](demo/screenshots/daily-learning-plan-script-generation.png)

## 🎯 Fonctionnalités

- **📰 Agrégation RSS** - Collecte les articles de vos flux préférés
- **🎥 Résumés YouTube** - Résumés IA des vidéos récentes
- **📄 PDF avec QR Codes** - Document formaté avec codes QR pour accéder aux sources
- **📧 Envoi automatique Kindle** - Livraison directe chaque matin
- **⚙️ Configuration flexible** - Personnalisation facile via YAML

## 🚀 Installation Rapide

```bash
# Cloner et configurer
git clone https://github.com/EfficientTools/Automatic-Learning-System.git learning-system
cd learning-system

# Exécuter la configuration automatique
chmod +x setup.sh
./setup.sh

# Configurer vos identifiants
test -f .env || cp .env.template .env
# Éditer .env avec vos clés API et emails

# Tester le système
venv/bin/python test_system.py

# Lancer la génération
venv/bin/python main.py
```

## 🔧 Configuration

### 1. Variables d'environnement (.env)
```bash
OPENAI_API_KEY=votre_cle_openai
KINDLE_EMAIL=votrenom@kindle.com
SENDER_EMAIL=votre.email@gmail.com
SMTP_PASSWORD=mot_de_passe_app_gmail
```

### 2. Flux RSS et chaînes YouTube (config.yaml)
```yaml
rss_feeds:
  - "https://blog.exemple.com/rss"
  - "https://autre-site.com/feed"

youtube_channels:
  - "UCxxxxxxx"  # ID de chaîne YouTube
```

### 3. Configuration Kindle
1. Allez sur https://www.amazon.com/myk
2. Ajoutez votre email expéditeur à la liste approuvée
3. Notez votre adresse @kindle.com

## 🤖 Automatisation

Pour recevoir votre journal chaque matin à 7h:

```bash
# Rendre le script exécutable
chmod +x run_daily.sh

# Ajouter au crontab
crontab -e

# Ajouter cette ligne:
0 7 * * * /chemin/vers/learning-system/run_daily.sh
```

## 📱 Exemples historiques de lecteurs RSS

Pour lire vos flux sur macOS et iPad:

### **Reeder 5**
- App native macOS/iPad
- Interface élégante sans distraction
- Conditions commerciales à vérifier auprès de l’éditeur
- Synchronisation via iCloud/Feedbin

### 🆓 **NetNewsWire**
- Gratuit et open source
- Rapide et léger
- Parfait pour un usage minimaliste

### ✨ **Readwise Reader**
- Résumés IA intégrés
- Gestion newsletters + RSS + PDF
- Envoi automatique vers Kindle
- Tarifs actuels à vérifier auprès de l’éditeur

## 🛠️ Structure du Projet

```
learning-system/
├── main.py              # Script principal
├── config.yaml          # Configuration
├── requirements.txt     # Dépendances Python
├── setup.sh            # Script de configuration
├── run_daily.sh        # Script d'automatisation
├── src/
│   ├── config.py           # Gestion configuration
│   ├── rss_aggregator.py   # Collecte RSS
│   ├── youtube_summarizer.py # Résumés YouTube
│   ├── pdf_generator.py    # Génération PDF + QR
│   └── kindle_sender.py    # Envoi email Kindle
├── output/             # PDFs générés
└── logs/              # Fichiers de log
```

## 🎨 Exemple de Sortie

Le PDF généré contient:
- **En-tête stylé** avec date du jour
- **Résumé du contenu** (nombre d'articles, vidéos)
- **Articles RSS** avec source et date
- **Résumés vidéos IA** en français
- **QR codes** pour chaque source
- **Mise en page A4** à vérifier sur votre liseuse

## 🔍 Comment Inclure les QR Codes

Les QR codes sont automatiquement générés pour chaque article:

```python
# Dans pdf_generator.py
def generate_qr_code(self, url: str) -> Image:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=2,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    qr_img = qr.make_image(fill_color="black", back_color="white")
    # Conversion en Image ReportLab...
```

## 🚨 Dépannage

### Problème d'authentification Gmail
- Activez l'authentification à 2 facteurs
- Générez un mot de passe d'application
- Utilisez ce mot de passe dans .env

### Kindle ne reçoit pas les emails
- Vérifiez que votre email est autorisé sur Amazon
- Confirmez l'adresse @kindle.com
- Vérifiez les dossiers spam

### Pas de résumés de vidéos
- Vérifiez votre clé OpenAI API
- Ajoutez des IDs de chaînes YouTube valides
- Vérifiez les quotas API

## 📈 Prochaines Améliorations

- [ ] Support EPUB pour un meilleur rendu Kindle
- [ ] Interface web de configuration
- [ ] Filtres intelligents par mots-clés
- [ ] Intégration newsletters automatique
- [ ] Support de plus de sources (Reddit, Hacker News)

## 👨‍💻 Auteur

[![Pierre-Henry Soria](https://s.gravatar.com/avatar/a210fe61253c43c869d71eaed0e90149?s=200)](https://PH7.me "Site personnel de Pierre-Henry Soria")

**Pierre-Henry Soria** — Un ingénieur logiciel super passionné et enthousiaste.
Un véritable amateur de fromage, café et chocolat. 🧀☕🍫
Vous pouvez me contacter sur [PH7.me](https://PH7.me).

Le projet vous plaît ? **[Offrez-moi un café](https://ko-fi.com/phenry)** — ma boisson de choix est un flat white aux amandes. ☕✨

[![@phenrysay][x-icon]](https://x.com/phenrysay "Me suivre sur X") [![Vidéos Tech YouTube][youtube-icon]](https://www.youtube.com/@pH7Programming "Ma chaîne YouTube Tech") [![BlueSky][bsky-icon]](https://bsky.app/profile/pierrehenry.dev "Follow Me on BlueSky") [![pH-7][github-icon]](https://github.com/pH-7 "Me suivre sur GitHub")

## 📄 Licence

Ce projet est distribué sous licence MIT. Voir le fichier [LICENSE.md](license.md) pour plus de détails.

## 🤝 Contribution

Les contributions sont bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.

---

**🧠 Bon apprentissage automatique ! 📚✨**

<!-- GitHub's Markdown reference links -->
[x-icon]: https://img.shields.io/badge/x-000000?style=for-the-badge&logo=x
[bsky-icon]: https://img.shields.io/badge/BlueSky-00A8E8?style=for-the-badge&logo=bluesky&logoColor=white
[youtube-icon]: https://img.shields.io/badge/YouTube-FF0000?style=for-the-badge&logo=youtube&logoColor=white
[github-icon]: https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
