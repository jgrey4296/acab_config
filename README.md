# acab_config : A config parser with load time guarantees #

## Overview ##


## Examples ##

Specify a config file as you would for [python's config parser](https://docs.python.org/3/library/configparser.html "config parser"):

``` ini
[List.Section]
bob
bill
jill

[Dict.Section]
bob  = aweg
bill = True
jill = False

[Enum.Test]
bob
bill
jill

[Sub.Action.Test]
"blah"
"bloo"
"blee"

[Float.Test]
a_val = 2.353

```


Then in your program:

``` python
from acab_config.config import AcabConfig
from acab_config.utils.log_formatter import AcabLogRecord
from acab_config.error.config_error import AcabConfigException

# Add {} style formatting for log messages
AcabLogRecord.install()

logging.info("Like {}", "this")
logging.info("This still %s", "works")

# Build the singleton:
config = AcabConfig("path/to/file.config", build=True)

config_2 = AcabConfig()
assert(config is config_2)

# Get Values by the section's structure:
value = config.attr.List.Section.bob
assert(value == bob)

value = config.attr.Dict.Section.bob
assert(value == "aweg")

# Bools are recognized: 
assert(isinstance(config.Dict.Section.bill, bool))

# Make sections enums:
the_enum = config.prepare("Enum.Test", _type=Enum)
assert(isinstance(the_enum, Enum))
assert(the_enum.bob == config.prepare("Enum.Test", "bob"))

# Complain if you try to get a value that doesn't exist:
try:
    config.attr.List.Section.jane
except AcabConfigException:
    pass
    



```
