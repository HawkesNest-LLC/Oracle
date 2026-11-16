import json, pathlib, unittest
from jsonschema import Draft202012Validator
from esp_contract import validate, EnvelopeError
ROOT=pathlib.Path(__file__).resolve().parent
class SchemaTests(unittest.TestCase):
    def test_schema_is_valid(self):
        schema=json.loads((ROOT/'esp_v01.schema.json').read_text())
        Draft202012Validator.check_schema(schema)
    def test_schema_matches_core_cases(self):
        schema=json.loads((ROOT/'esp_v01.schema.json').read_text())
        validator=Draft202012Validator(schema)
        good={'claimId':'id','status':'PROPOSED','authority':'AI','confidence':0.2,'sources':['source']}
        cases=[good,{**good,'status':'ESTABLISHED','sources':[]},{**good,'status':'UNKNOWN','sources':[]},{**good,'confidence':True},{**good,'claimId':' '},{**good,'status':'CANONICAL'},{**good,'extra':True}]
        for case in cases:
            schema_ok=validator.is_valid(case)
            try:validate(case);python_ok=True
            except (EnvelopeError,TypeError):python_ok=False
            self.assertEqual(schema_ok,python_ok,case)
if __name__=='__main__':unittest.main()
