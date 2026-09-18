#!/usr/bin/env python3
"""Offline regressions: synthetic data, temporary files and mocked providers."""
import io
import os
import ssl
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from reportlab.platypus import Paragraph

from src.config import Config
from src.pdf_generator import PDFGenerator
from src.rss_aggregator import Article, RSSAggregator
from src.youtube_summarizer import VideoSummary, YouTubeSummarizer
from src.kindle_sender import KindleSender
import main as application


class LearningSystemTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.config_path = self.root / 'config.yaml'
        self.network = patch('socket.socket.connect', side_effect=AssertionError('Network disabled in tests'))
        self.network.start()
        self.addCleanup(self.network.stop)
        self.environment = patch.dict(os.environ, dict.fromkeys(
            ['OPENAI_API_KEY', 'KINDLE_EMAIL', 'SENDER_EMAIL', 'SMTP_PASSWORD'], ''))
        self.environment.start()
        self.addCleanup(self.environment.stop)

    def config(self):
        return Config(str(self.config_path))

    def test_default_config_never_copies_environment_credentials_to_disk(self):
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-value', 'SMTP_PASSWORD': 'test-password'}):
            config = self.config()
            self.assertFalse(self.config_path.exists())
            config.save_config()
            self.assertNotIn('test-value', self.config_path.read_text())
            self.assertNotIn('test-password', self.config_path.read_text())
            self.assertEqual(config.openai_api_key, 'test-value')

    def test_env_file_loads_without_replacing_exported_values(self):
        (self.root / '.env').write_text('OPENAI_API_KEY=from-file\nSMTP_PASSWORD=file-password\n')
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'exported'}):
            # Remove only this test's empty SMTP variable to allow dotenv fallback.
            os.environ.pop('SMTP_PASSWORD', None)
            config = self.config()
            self.assertEqual(config.openai_api_key, 'exported')
            self.assertEqual(config.smtp_config['smtp_password'], 'file-password')

    def test_empty_yaml_and_invalid_yaml_shape(self):
        self.config_path.write_text('')
        self.assertEqual(self.config().rss_feeds, [])
        self.config_path.write_text('- unexpected-list\n')
        with self.assertRaises(ValueError):
            self.config()

    def test_output_is_relative_to_config_not_process_directory(self):
        self.config_path.write_text('output:\n  output_dir: nested/output\n')
        self.assertEqual(self.config().output_dir, self.root / 'nested/output')

    def test_pdf_treats_feed_markup_as_literal_text(self):
        article = Article('Titre <b> & exemple', 'Une balise <img src="https://example.invalid/x"> et x < 3.',
                          'https://example.invalid/?a=1&b=2', datetime.now(), 'Source <i>')
        with redirect_stdout(io.StringIO()):
            path = PDFGenerator(self.config()).create_journal([article])
        self.assertTrue(path.read_bytes().startswith(b'%PDF-'))
        self.assertGreater(path.stat().st_size, 1000)

    def test_demo_cannot_overwrite_the_daily_journal(self):
        generator = PDFGenerator(self.config())
        daily = generator.output_dir / f'journal_apprentissage_{datetime.now():%Y-%m-%d}.pdf'
        daily.write_bytes(b'existing journal')
        with redirect_stdout(io.StringIO()):
            demo = generator.create_journal([], demo=True)
        self.assertEqual(daily.read_bytes(), b'existing journal')
        self.assertTrue(demo.name.startswith('demo_journal_'))

    def test_openai_client_constructs_without_a_request(self):
        summarizer = YouTubeSummarizer(SimpleNamespace(openai_api_key='test-value'))
        summarizer.client.close()

    def test_rss_http_failure_is_not_parsed_as_content(self):
        response = MagicMock()
        response.raise_for_status.side_effect = RuntimeError('offline HTTP failure')
        with patch('src.rss_aggregator.requests.get', return_value=response), redirect_stdout(io.StringIO()):
            self.assertEqual(RSSAggregator(self.config()).process_feed('https://example.invalid/rss'), [])

    def test_rss_dates_are_utc(self):
        date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        response = MagicMock(content=f'<rss version="2.0"><channel><title>Test</title><item><title>Recent</title><link>https://example.invalid/a</link><pubDate>{date}</pubDate><description>Text</description></item></channel></rss>'.encode())
        with patch('src.rss_aggregator.requests.get', return_value=response):
            articles = RSSAggregator(self.config()).process_feed('https://example.invalid/rss')
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0].published.tzinfo, timezone.utc)

    def test_duplicate_links_across_feeds_appear_once(self):
        self.config_path.write_text(
            'rss_feeds:\n  - https://example.invalid/a\n  - https://example.invalid/b\n')
        date = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        feed = ('<rss version="2.0"><channel><title>Test</title><item><title>Shared</title>'
                '<link>https://example.invalid/post?utm_source=feed</link>'
                f'<pubDate>{date}</pubDate><description>Text</description></item>'
                '</channel></rss>').encode()
        with patch('src.rss_aggregator.requests.get', return_value=MagicMock(content=feed)), \
             patch('src.rss_aggregator.time.sleep'), redirect_stdout(io.StringIO()):
            articles = RSSAggregator(self.config()).collect_articles()
        self.assertEqual(len(articles), 1)

    def test_recent_entries_survive_a_pinned_older_entry(self):
        old = (datetime.now(timezone.utc) - timedelta(days=400)).strftime('%a, %d %b %Y %H:%M:%S GMT')
        new = datetime.now(timezone.utc).strftime('%a, %d %b %Y %H:%M:%S GMT')
        items = ''.join(
            f'<item><title>Pinned {index}</title><link>https://example.invalid/old{index}</link>'
            f'<pubDate>{old}</pubDate><description>Old</description></item>' for index in range(3))
        feed = ('<rss version="2.0"><channel><title>Test</title>' + items +
                '<item><title>Recent</title><link>https://example.invalid/new</link>'
                f'<pubDate>{new}</pubDate><description>Fresh</description></item>'
                '</channel></rss>').encode()
        with patch('src.rss_aggregator.requests.get', return_value=MagicMock(content=feed)):
            articles = RSSAggregator(self.config()).process_feed('https://example.invalid/rss')
        self.assertEqual([article.title for article in articles], ['Recent'])

    def test_pdf_renders_article_content_rather_than_its_truncation(self):
        body = 'Phrase unique. ' + 'corps ' * 200
        article = Article('Titre', body, 'https://example.invalid/a',
                          datetime.now(), 'Source', summary=body[:200] + '...')
        generator = PDFGenerator(self.config())
        story, styles = [], generator.create_custom_styles()
        generator.add_content_item(story, article, 1, styles)
        rendered = ' '.join(item.text for item in story if isinstance(item, Paragraph))
        self.assertIn(body.strip(), rendered)

    def test_pdf_still_uses_the_ai_summary_for_videos(self):
        video = VideoSummary('Titre', 'Résumé rédigé par le modèle.', 'https://example.invalid/v',
                             datetime.now(), 'YouTube', 'Chaîne')
        generator = PDFGenerator(self.config())
        story, styles = [], generator.create_custom_styles()
        generator.add_content_item(story, video, 1, styles)
        rendered = ' '.join(item.text for item in story if isinstance(item, Paragraph))
        self.assertIn('Résumé rédigé par le modèle.', rendered)

    def test_smtp_uses_verified_tls_with_a_timeout(self):
        pdf = self.root / 'test.pdf'; pdf.write_bytes(b'%PDF-test')
        config = SimpleNamespace(kindle_email='reader@example.invalid', sender_email='sender@example.invalid',
            smtp_config={'smtp_server':'smtp.example.invalid', 'smtp_port':587,
                         'sender_email':'sender@example.invalid','smtp_password':'test-value'})
        with patch('src.kindle_sender.smtplib.SMTP') as smtp, redirect_stdout(io.StringIO()):
            self.assertTrue(KindleSender(config).send_to_kindle(pdf))
            self.assertEqual(smtp.call_args.kwargs['timeout'], 30)
            context = smtp.return_value.starttls.call_args.kwargs['context']
            self.assertTrue(context.check_hostname)
            self.assertEqual(context.verify_mode, ssl.CERT_REQUIRED)

    def test_initialisation_failure_returns_nonzero(self):
        with patch.object(application, 'Config', side_effect=ValueError('invalid config')), redirect_stdout(io.StringIO()):
            self.assertEqual(application.main(), 1)

    def test_configured_delivery_failure_returns_nonzero(self):
        config = SimpleNamespace(kindle_email='reader@example.invalid',sender_email='sender@example.invalid')
        with patch.object(application,'Config',return_value=config), \
             patch.object(application,'RSSAggregator') as rss, \
             patch.object(application,'YouTubeSummarizer') as youtube, \
             patch.object(application,'PDFGenerator'), \
             patch.object(application,'KindleSender') as sender, redirect_stdout(io.StringIO()):
            rss.return_value.collect_articles.return_value = [object()]
            youtube.return_value.process_videos.return_value = []
            sender.return_value.send_to_kindle.return_value = False
            self.assertEqual(application.main(), 1)


if __name__ == '__main__':
    unittest.main(verbosity=2)
