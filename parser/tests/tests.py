from django.test import TestCase
from .models import User
from parser_mapper import ParserMapper, ObjectMapping, FieldMapping


class TestParser(TestCase):
    def test_can_get_model_without_any_nested_models(self):
        self.assertEqual(User.objects.count(), 0)

        mapping = ObjectMapping(
            None, 'tests.User',
            (FieldMapping('nick_name', 'author'),)
        )
        parser_mapper = ParserMapper(
            'https://habrahabr.ru/rss/hubs/all/', mapping
        )

        parser_mapper.put_to_models()
        self.assertEqual(User.objects.count(), 20)

        # after restart not add duplicates to db
        parser_mapper.put_to_models()
        self.assertEqual(User.objects.count(), 20)