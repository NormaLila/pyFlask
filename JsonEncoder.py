import json
from decimal import Decimal
import datetime

class CustomJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)

        if isinstance(obj, datetime.date):
            return obj.isoformat()

        return super(CustomJsonEncoder, self).default(obj)