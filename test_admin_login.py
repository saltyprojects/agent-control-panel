#!/usr/bin/env python3
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from core.models import User

# Check if root user exists and can login
users = User.objects.all()
print(f"Total users: {users.count()}")

root_user = User.objects.filter(username='root').first()
if root_user:
    print(f"Root user exists: {root_user.username}")
    print(f"Root is superuser: {root_user.is_superuser}")
    print(f"Root is staff: {root_user.is_staff}")
    print(f"Root is active: {root_user.is_active}")
    print(f"Password check 'root': {root_user.check_password('root')}")
else:
    print("Root user does NOT exist!")
    print("Creating root user now...")
    User.objects.create_superuser(
        username='root',
        email='admin@agentcontrol.local',
        password='root'
    )
    print("Root user created!")
