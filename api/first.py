from api.models import User
import logging

logger = logging.getLogger('api')


def create_first_user():
    if not User.objects.exists():
        username = 'admin'
        password = 'Abcd@1234'
        email = 'admin@gmail.com'
        type = 'admin'

        logger.info('Creating first user...')
        User.objects.create_superuser(username=username, email=email, password=password, type=type)
        logger.info(f'Created user: {username} with password: {password}')
