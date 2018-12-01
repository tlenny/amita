import json

class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o,Decimal):
			return str(o)
		return json.JSONEncoder.default(self,o)