import os
from django.test import TestCase
from .models import User, Tag
from parser_mapper import ParserMapper, ObjectMapping, FieldMapping

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


class TestParser(TestCase):
    def test_can_get_model_without_any_nested_models(self):
        self.assertEqual(User.objects.count(), 0)

        mapping = ObjectMapping(
            None, 'tests.User',
            (FieldMapping('nick_name', 'author'),)
        )
        source = os.path.join(TESTS_DIR, 'habr_source.xml')
        parser_mapper = ParserMapper(source, mapping)

        parser_mapper.put_to_models()
        self.assertEqual(User.objects.count(), 20)

        # after restart not add duplicates to db
        parser_mapper.put_to_models()
        self.assertEqual(User.objects.count(), 20)

    def test_can_get_many_nested_models(self):
        self.assertEqual(Tag.objects.count(), 0)

        mapping = ObjectMapping(
            'tags', 'tests.Tag',
            (FieldMapping('title', 'term'),)
        )
        source = os.path.join(TESTS_DIR, 'habr_source.xml')
        parser_mapper = ParserMapper(source, mapping)
        parser_mapper.put_to_models()

        self.assertEqual(Tag.objects.count(), 129)
        self.assertTrue(Tag.objects.filter(title="positive technologies").exists())
