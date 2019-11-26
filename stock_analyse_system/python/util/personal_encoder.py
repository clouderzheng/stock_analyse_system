import json
import decimal
import datetime
class personal_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')

        if isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        return super(personal_encoder, self).default(obj)