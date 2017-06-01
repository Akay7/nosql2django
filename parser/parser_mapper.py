from collections import namedtuple
from functools import reduce
import feedparser
from django.apps import apps

ObjectMapping = namedtuple('RelatedField', ('base_path', 'model', 'fields'))
FieldMapping = namedtuple('Field', ('name', 'mapping'))


def deep_get(deep_dict, path):
    if isinstance(path, str):
        path = (path,)

    return reduce(
        lambda d, key: d.get(key) if isinstance(d, dict) else None,
        path, deep_dict
    )


class ParserMapper:
    def __init__(self, source, mapping):
        self.source = source
        self.mapping = mapping

    @staticmethod
    def save_to_db(model_text_id, parsed_values):
        """save to db and return saved object"""
        Model = apps.get_model(model_text_id)
        model, created = Model.objects.get_or_create(**parsed_values)
        return model

    @staticmethod
    def parse_obj(mapping, obj):
        parsed_values = {}
        for field in mapping.fields:
            parsed_values[field.name] = deep_get(obj, field.mapping)

        ParserMapper.save_to_db(mapping.model, parsed_values)

    def put_to_models(self):
        feed = feedparser.parse(self.source)

        for e in feed['entries']:
            ParserMapper.parse_obj(self.mapping, e)