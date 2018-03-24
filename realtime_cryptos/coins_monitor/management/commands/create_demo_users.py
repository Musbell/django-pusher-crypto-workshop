import random
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from . import names


class Command(BaseCommand):
    help = 'Generate demo users'

    def add_arguments(self, parser):
        parser.add_argument('-q', '--quantity', type=int, required=False, default=50)

    def handle(self, *args, **options):
        # print(names.LAST_NAMES)
        if User.objects.exists():
            largest_user_id = User.objects.latest('id').id
        else:
            largest_user_id = 0
        user_id = largest_user_id + 1

        for idx in range(options['quantity']):
            username = 'user{}'.format(user_id)
            email = "{}@example.com".format(username)
            password = 'pusher-rmotr'
            first_name = random.choice(names.FIRST_NAMES)
            last_name = random.choice(names.LAST_NAMES)
            # user = User.objects.create_user(username, email, password

            user = User.objects.create(
                id=user_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                email=email,
            )
            user.set_password(password)
            user_id = user_id + 1
