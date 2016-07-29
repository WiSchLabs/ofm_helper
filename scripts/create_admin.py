from users.models import OFMUser

if not OFMUser.objects.get(username='admin'):
    OFMUser.objects.create_user(username='admin', password='admin', is_staff=True, is_superuser=True)