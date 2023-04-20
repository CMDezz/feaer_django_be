# fields.py
from djongo.models import JSONField  # type: ignore

class MyJSONField(JSONField):
    """ do eval beforce save to mongo """
    def to_python(self, value):
        try:
            value = eval(value)
        except Exception as e:
            raise ValueError(
                f'Value: {value} invalid, make sure before submit?'
            )
        return super().to_python(value)