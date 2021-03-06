import getpass
import sys

from django.contrib.auth import get_user_model
from django.core.exceptions import (
    ObjectDoesNotExist, ValidationError)
from django.core.management.base import (
    BaseCommand, CommandError)
from django.utils.encoding import force_str
from django.utils.text import capfirst, slugify

from profiles.models import Profile


class Command(BaseCommand):
    help = 'Create new User with Profile.'

    required_error = (
        'You must use --{} with --noinput.')

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.User = get_user_model()
        self.first_name_field = (
            get_user_model()._meta.get_field('first_name'))
        self.second_name_field = (
            get_user_model()._meta.get_field('last_name'))
        self.username_field = (
            self.User._meta.get_field(
                self.User.USERNAME_FIELD))

    def execute(self, *args, **options):

        # this method is not changed
        # the stdin kwarg is used later to check
        # if interactive mode is activated

        self.stdin = options.get(
            'stdin', sys.stdin)
        return super().execute(*args, **options)

    def add_arguments(self, parser):

        # django takes arguments defined here and passes to handle()

        parser.add_argument(
            '--{}'.format(self.first_name_field.name),
            dest=self.first_name_field.name,
            default=None,
            help='User profile name.')
        parser.add_argument(
            '--{}'.format(self.second_name_field.name),
            dest=self.second_name_field.name,
            default=None,
            help='User profile name.')
        parser.add_argument(
            '--{}'.format(
                self.User.USERNAME_FIELD),
            dest=self.User.USERNAME_FIELD,
            default=None,
            help='User login.')
        parser.add_argument(
            '--noinput',
            action='store_false',
            dest='interactive',
            default=True,
            help=(
                'Do NOT prompt the user for '
                'input of any kind. You must use '
                '--{} with --noinput, along with '
                'an option for any other '
                'required field. Users created '
                'with --noinput will not be able '
                'to log in until they\'re given '
                'a valid password.'.format(
                    self.User.USERNAME_FIELD)))

    def clean_value(
            self, field, value, halt=True):
        try:
            value = field.clean(value, None)
        except ValidationError as e:
            if halt:
                raise CommandError(
                    '; '.join(e.messages))
            else:
                self.stderr.write(
                    "Error: {}".format(
                        '; '.join(e.messages)))
            return None
        else:
            return value

    def check_unique(
            self, model, field, value, halt=True):
        try:
            q = '{}__iexact'.format(field.name)
            filter_dict = {q: value}
            model.objects.get(**filter_dict)
        except ObjectDoesNotExist:
            return value
        else:
            if halt:
                raise CommandError(
                    "That {} is already takenn."
                    .format(
                        capfirst(
                            field.verbose_name)))
            else:
                self.stderr.write(
                    'Error: That {} is '
                    'already taken.'.format(
                        field.verbose_name))
        return None

    def handle_non_interactive(
            self, first_name, second_name, username, **options):
        if not username:
            raise CommandError(
                self.required_error.format(
                    self.User.USERNAME_FIELD))
        if not first_name or not second_name:
            raise CommandError(
                self.required_error.format(
                    self.first_name_field))
        username = self.clean_value(
            self.username_field, username)
        first_name = self.clean_value(
            self.first_name_field, first_name)
        second_name = self.clean_value(
            self.second_name_field, second_name)
        username = self.check_unique(
            self.User,
            self.username_field,
            username)
        first_name = self.check_unique(
            get_user_model(), self.first_name_field, first_name)
        second_name = self.check_unique(
            get_user_model(), self.second_name_field, second_name)
        return (first_name, second_name, username)

    def get_field_interactive(self, model, field):
        value = None
        input_msg = '{}: '.format(
            capfirst(field.verbose_name))
        while value is None:
            value = input(input_msg)
            value = self.clean_value(
                field, value, halt=False)
            if not value:
                continue
            value = self.check_unique(
                model, field, value, halt=False)
            if not value:
                continue
            return value

    def handle_interactive(
            self, first_name, second_name, username, **options):

        password = None

        if (hasattr(self.stdin, 'isatty')
                and not self.stdin.isatty()):
            self.stdout.write(
                'User creation skipped due '
                'to not running in a TTY. '
                'You can run `manage.py '
                'createuser` in your project '
                'to create one manually.')
            sys.exit(1)

        if username is not None:
            username = self.clean_value(
                self.username_field,
                username,
                halt=False)
            if username is not None:
                username = self.check_unique(
                    self.User,
                    self.username_field,
                    username,
                    halt=False)
        if first_name is not None:
            first_name = self.clean_value(
                self.first_name_field, first_name, halt=False)
            if first_name is not None:
                first_name = self.check_unique(
                    get_user_model(),
                    self.first_name_field,
                    first_name,
                    halt=False)
        if second_name is not None:
            second_name = self.clean_value(
                self.name_field, second_name, halt=False)
            if second_name is not None:
                second_name = self.check_unique(
                    get_user_model(),
                    self.second_name_field,
                    second_name,
                    halt=False)

        try:
            if not username:
                username = (
                    self.get_field_interactive(
                        self.User,
                        self.username_field))
            if not first_name:
                first_name = self.get_field_interactive(
                    get_user_model(),
                    self.first_name_field)

            if not second_name:
                second_name = self.get_field_interactive(
                    get_user_model(),
                    self.second_name_field)

            while password is None:
                password = getpass.getpass()
                password2 = getpass.getpass(
                    force_str(
                        'Password (again): '))
                if password != password2:
                    self.stderr.write(
                        "Error: Your "
                        "passwords didn't "
                        "match.")
                    password = None
                    continue
                if password.strip() == '':
                    self.stderr.write(
                        "Error: Blank passwords "
                        "aren't allowed.")
                    password = None
                    continue

            return (first_name, second_name, username, password)

        except KeyboardInterrupt:
            self.stderr.write(
                "\nOperation cancelled.")
            sys.exit(1)

    def create_user(
            self, first_name, second_name, username, password):
        try:
            new_user = self.User.objects.create_user(
                email=username, first_name=first_name,
                last_name=second_name, password=password)
            self.stdout.write('*** user created ***')
        except Exception as e:
            self.stdout.write(Exception)

    def handle(self, **options):
        first_name = options.pop(
            self.first_name_field.name, None)
        second_name = options.pop(
            self.second_name_field.name, None)
        username = options.pop(
            self.User.USERNAME_FIELD, None)
        password = None

        if not options['interactive']:
            first_name, second_name, username = (
                self.handle_non_interactive(
                    first_name, second_name, username, **options))
        else:
            first_name, second_name, username, password = (
                self.handle_interactive(
                    first_name, second_name, username, **options))

        self.create_user(first_name, second_name, username, password)
