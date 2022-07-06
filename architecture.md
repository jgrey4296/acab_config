# acab_config Architecture #

`interface.py` defines the two main units of the module:
- ConfigSpec_d: packages details of what to get and what to do with it
- Config_i: Describes the public interface of a config object

`config_meta.py` provides the singleton logic as a metaclass.

`config.py` implements the ConfigSpec_d and Config_i api.

`log_formatter.py` provides functionality to use {} formatting in logging calls, 
instead of the old style % formatting.
It does this with a custom LogRecord implementation, where `getMessage` tries {} formatting
if % formatting produces an error.

`attr_gen.py` provides the attribute generation logic for `config.attr`.
