import hcl
import toml
from pprint import pprint
f = open("Schedule.hcl")
try:
    data = hcl.load(f)
finally:
     f.close()
toml_str = toml.dumps(data)
print(toml_str)