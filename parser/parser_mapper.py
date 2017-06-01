from collections import namedtuple
from functools import reduce
import feedparser
from dateutil import parser as time_parser
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

        # normalise values and separate to m2m, simple
        simple_fields = {}
        many2many_fields = {}
        for field, value in parsed_values.items():
            if (Model._meta.get_field(
                    field).get_internal_type() == 'ManyToManyField'):
                many2many_fields[field] = value
            elif (Model._meta.get_field(
                    field).get_internal_type() == 'DateTimeField'):
                simple_fields[field] = time_parser.parse(value)

            else:
                simple_fields[field] = value

        # ToDo: add unique identify parameter to field
        # ToDo: allow unique identify m2m field
        model, created = Model.objects.get_or_create(**simple_fields)

        for field, value in many2many_fields.items():
            setattr(model, field, value)
        model.save()

        return model

    @staticmethod
    def parse_obj(mapping, obj):
        def _parse_single_obj(mapping, obj):
            parsed_values = {}
            for field in mapping.fields:
                if isinstance(field.mapping, ObjectMapping):
                    value = ParserMapper.parse_obj(
                        field.mapping, obj[field.mapping.base_path] if field.mapping.base_path else obj
                    )
                else:
                    value = deep_get(obj, field.mapping)
                parsed_values[field.name] = value

            return ParserMapper.save_to_db(mapping.model, parsed_values)

        if isinstance(obj, list):
            return [_parse_single_obj(mapping, i) for i in obj]
        return _parse_single_obj(mapping, obj)

    def put_to_models(self):
        feed = feedparser.parse(self.source)

        for e in feed['entries']:
            ParserMapper.parse_obj(
                self.mapping,
                e[self.mapping.base_path] if self.mapping.base_path else e
            )
