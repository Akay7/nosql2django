import os
from django.test import TestCase
from .models import User, Tag, Post
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

    def test_can_get_model_with_nested_models(self):
        self.assertEqual(Tag.objects.count(), 0)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Post.objects.count(), 0)

        mapping = ObjectMapping(
            None, 'tests.Post',
            (
                FieldMapping('title', 'title'),
                FieldMapping('summary', 'description'),
                FieldMapping('tags',
                    ObjectMapping(
                        'tags', 'tests.Tag',
                        (FieldMapping('title', 'term'),)
                    )
                ),
                FieldMapping('author',
                    ObjectMapping(
                        None, 'tests.User',
                        (FieldMapping('nick_name', 'author'),)
                    )
                ),
                FieldMapping('updated', 'published')
            )
        )

        source = os.path.join(TESTS_DIR, 'habr_source.xml')
        parser_mapper = ParserMapper(source, mapping)
        parser_mapper.put_to_models()

        # verify result
        self.assertEqual(Tag.objects.count(), 129)
        self.assertTrue(Tag.objects.filter(title="positive technologies").exists())

        self.assertEqual(User.objects.count(), 20)

        self.assertEqual(Post.objects.count(), 20)
        self.assertNotEqual(Post.objects.first().title, '')
        self.assertNotEqual(Post.objects.first().author, None)
        tags_in_post_qty = len(
            Post.objects.values_list('tags__title', flat=True).distinct()
        )
        self.assertEqual(tags_in_post_qty, 129)

    def test_correct_parse_reddit(self):
        mapping = ObjectMapping(
            None, 'tests.Post',
            (
                FieldMapping('title', 'title'),
                FieldMapping('author',
                    ObjectMapping(
                        None, 'tests.User',
                        (FieldMapping('nick_name', 'author'),)
                    )
                ),
                FieldMapping('updated', 'updated')
            )
        )
        source = os.path.join(TESTS_DIR, 'reddit_source.xml')
        parser_mapper = ParserMapper(source, mapping)
        parser_mapper.put_to_models()

        self.assertEqual(Post.objects.count(), 25)
        self.assertEqual(User.objects.count(), 21)
        self.assertEqual(Tag.objects.count(), 0)