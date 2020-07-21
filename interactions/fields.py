from django.db import models


class SeparatedValuesField(models.TextField):

    def __init__(self, seperator=',', *args, **kwargs):
        self.seperator = seperator
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Only include kwarg if it's not the default
        if self.separator != ",":
            kwargs['separator'] = self.separator
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        pass

    def to_python(self, value):
        if not value:
            return
        if isinstance(value, list):
            return value
        return value.split(self.seperator)

    def value_to_string(self, obj):
        value = self.val_from_obj(obj)
        return self.get_db_prep_value(value)
