from django.core.management.base import BaseCommand
from django_parser.parser_mapper import ObjectMapping, FieldMapping, ParserMapper


class Command(BaseCommand):
    help = 'Parse habr feeds'

    def handle(self, *args, **options):
        source = 'https://habrahabr.ru/rss/hubs/all/'

        mapping = ObjectMapping(
            None, 'demo.Post',
            (
                FieldMapping('title', 'title'),
                FieldMapping('summary', 'description'),
                FieldMapping('tags',
                    ObjectMapping(
                        'tags', 'demo.Tag',
                        (FieldMapping('title', 'term'),)
                    )
                ),
                FieldMapping('author',
                    ObjectMapping(
                        None, 'demo.User',
                        (FieldMapping('nick_name', 'author'),)
                    )
                ),
                FieldMapping('updated', 'published')
            )
        )
        parser_mapper = ParserMapper(source, mapping)
        parser_mapper.put_to_models()

        self.stdout.write(
            self.style.SUCCESS("successfully parsed all habr feeds"))
