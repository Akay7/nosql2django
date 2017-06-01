from django.core.management.base import BaseCommand
from django_parser.parser_mapper import ObjectMapping, FieldMapping, ParserMapper


class Command(BaseCommand):
    help = 'Parse reddit feeds'

    def handle(self, *args, **options):
        source = 'https://www.reddit.com/r/news/.rss'

        mapping = ObjectMapping(
            None, 'demo.Post',
            (
                FieldMapping('title', 'title'),
                FieldMapping('author',
                    ObjectMapping(
                        None, 'demo.User',
                        (FieldMapping('nick_name', 'author'),)
                    )
                ),
                FieldMapping('updated', 'updated')
            )
        )

        parser_mapper = ParserMapper(source, mapping)
        parser_mapper.put_to_models()

        self.stdout.write(
            self.style.SUCCESS("successfully parsed all reddit feeds"))
