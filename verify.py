#!/usr/bin/env python3
"""Vérification locale uniquement : aucun appel RSS, OpenAI ou SMTP."""
import importlib.util
from pathlib import Path


def main():
    root = Path(__file__).resolve().parent
    files = ['main.py', 'config.yaml', 'requirements.txt', '.env.template',
             'setup.sh', 'run_daily.sh', 'test_system.py', 'demo.py',
             'src/config.py', 'src/pdf_generator.py', 'src/kindle_sender.py',
             'src/rss_aggregator.py', 'src/youtube_summarizer.py']
    missing = [name for name in files if not (root / name).is_file()]
    modules = ['feedparser', 'requests', 'openai', 'reportlab', 'qrcode', 'yaml', 'PIL', 'dotenv']
    missing += [name for name in modules if importlib.util.find_spec(name) is None]
    if missing:
        print('Éléments manquants : ' + ', '.join(missing))
        return 1
    print('Structure et imports disponibles. Exécutez test_system.py pour les régressions.')
    print('Aucune vérification de contenu réel, de compte OpenAI ou de livraison Kindle.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
