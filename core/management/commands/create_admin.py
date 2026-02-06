from django.core.management.base import BaseCommand
from core.models import User

class Command(BaseCommand):
    help = 'Create default admin user (root/root)'

    def handle(self, *args, **options):
        if not User.objects.filter(username='root').exists():
            User.objects.create_superuser(
                username='root',
                email='admin@agentcontrol.local',
                password='root'
            )
            self.stdout.write(self.style.SUCCESS('Created admin user: root/root'))
        else:
            self.stdout.write(self.style.WARNING('Admin user "root" already exists'))
