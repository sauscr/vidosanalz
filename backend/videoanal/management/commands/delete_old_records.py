from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from videoanal.models import Event

class Command(BaseCommand):
    help = 'Удаляет старые записи из Events'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            help='Кол-во дней для определения старых записей',
            default=30,
        )
    
    def handle(self, *args, **options):
        days = options['days']
        cutoff_date =timezone.now() - timedelta(days=days)
        old_records = Event.objects.filter(created_at__lt=cutoff_date)
        count, __ = old_records.delete()
        self.stdout.write(f'Удалено {count} старых записей из Events')