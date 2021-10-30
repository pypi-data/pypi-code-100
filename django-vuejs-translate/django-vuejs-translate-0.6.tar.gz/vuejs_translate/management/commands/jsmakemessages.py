import io
import os

from django.conf import settings
from django.utils.jslex import prepare_js_for_gettext
from django.utils.functional import cached_property
from django.utils.translation import templatize
from django.core.management.commands.makemessages import BuildFile
from django.core.management.utils import handle_extensions
from django_jinja.management.commands.makemessages import (
    Command as JinjaMakemessagesCommand
)


class JSBuildFile(BuildFile):
    def __init__(self, command, domain, translatable):
        self.command = command
        self.domain = domain
        self.translatable = translatable

    @cached_property
    def is_js(self):
        filename, ext = os.path.splitext(self.path)

        return ext in self.command.options['jsextensions']

    @cached_property
    def is_templatized(self):
        if self.is_js:
            return self.command.gettext_version < (0, 19, 9)
        else:
            file_ext = os.path.splitext(self.translatable.file)[1]

            return file_ext != '.py'

    def preprocess(self):
        """
        Preprocess (if necessary) a translatable file before passing it to
        xgettext GNU gettext utility.
        """
        if not self.is_templatized:
            return

        encoding = settings.FILE_CHARSET if self.command.settings_available else 'utf-8'
        path = self.path

        with io.open(path, 'r', encoding=encoding) as fp:
            src_data = fp.read()

        if self.is_js:
            content = prepare_js_for_gettext(src_data)
        else:
            content = templatize(
                src_data, origin=path[2:],
                # charset=encoding
            )

        with io.open(self.work_path, 'w', encoding='utf-8') as fp:
            fp.write(content)


class Command(JinjaMakemessagesCommand):
    build_file_class = JSBuildFile

    def add_arguments(self, parser):
        parser.add_argument(
            '--jsextension',
            '-jse',
            default=[],
            dest='jsextensions',
            action='append',
            help=(
                'The file extension(s) to use to tdetermine whether file is '
                'a Javascript file if the domain is "djangojs"). Separate '
                'multiple extensions with commas, or use -e multiple times.'
            )
        )

        return super().add_arguments(parser)

    def handle(self, *args, **options):
        self.options = options

        options['jsextensions'] = (
            handle_extensions(options['jsextensions']) or set(['js'])
        )

        return super().handle(*args, **options)
