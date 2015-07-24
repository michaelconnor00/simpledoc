# SimpleDoc

Simpledoc is tool to create markdown (.md) files from your projects docstrings. The only requirments are to have a config file and and simpledoc installed. Then running the command will traverse your project modules and pull all the docstrings.

##Typical Usage

```config
[controllers.api]
document_name = README.md
;black_list = controllers.factories

[services]
include_classes = False
include_functions = False
document_name = README.md
```

  $ simpledoc.py --config=my_config.ini

The output will
