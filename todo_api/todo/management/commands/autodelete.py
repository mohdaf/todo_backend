from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta

from todo.models import Todo

class Command(BaseCommand):
    help = 'Deletes todos that are older than a week'

    def handle(self, *args, **kwargs):
        time = timezone.now().strftime('%')
        self.stdout.write("Deleting todos that are older than a week")
        Todo.objects.filter(created_on__lte=timezone.now()-timedelta(days=7)).delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted!'))