# Système d'Apprentissage Automatique 🧠

Un système intelligent qui génère automatiquement un journal d'apprentissage personnalisé quotidien et l'envoie directement sur votre Kindle.

## 🎯 Fonctionnalités

- **📰 Agrégation RSS** - Collecte les articles de vos flux préférés
- **🎥 Résumés YouTube** - Résumés IA des vidéos récentes
- **📄 PDF avec QR Codes** - Document formaté avec codes QR pour accéder aux sources
- **📧 Envoi automatique Kindle** - Livraison directe chaque matin
- **⚙️ Configuration flexible** - Personnalisation facile via YAML

## 🚀 Installation Rapide

```bash
# Cloner et configurer
git clone <votre-repo> learning-system
cd learning-system

# Exécuter la configuration automatique
chmod +x setup.sh
./setup.sh

# Configurer vos identifiants
cp .env.template .env
# Éditer .env avec vos clés API et emails

# Tester le système
python test_system.py

# Lancer la génération
python main.py
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
0 7 * * * /Users/pierre-henrysoria/Code/learning-system/run_daily.sh
```

## 📱 Applications RSS Recommandées

Pour lire vos flux sur macOS et iPad:

### 🏆 **Reeder 5** (Recommandé)
- App native macOS/iPad
- Interface élégante sans distraction
- Achat unique, pas d'abonnement
- Synchronisation via iCloud/Feedbin

### 🆓 **NetNewsWire**
- Gratuit et open source
- Rapide et léger
- Parfait pour un usage minimaliste

### ✨ **Readwise Reader**
- Résumés IA intégrés
- Gestion newsletters + RSS + PDF
- Envoi automatique vers Kindle
- Abonnement ~10€/mois

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
- **Mise en page optimisée** pour Kindle

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
