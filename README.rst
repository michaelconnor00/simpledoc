SimpleDoc
=========
**_This is a Concept Only_**

Simpledoc is tool to create markdown (.md) files from your projects docstrings. The only requirments are to have a config file and and simpledoc installed. Then running the command will traverse your project modules and pull all the docstrings.

Test Installation
-----------------

```bash
sudo pip install -i https://testpypi.python.org/pypi simpledoc
```

Typical Usage
-------------

.. code-block::
    [controllers.api]
    document_name = README.md

    [services]
    include_classes = False
    include_functions = False
    document_name = README.md

Then run the simpledoc command.

.. code-block::
   $ simpledoc.py --config=my_config.ini

The output will be a README.md file with all the docstrings in the modules `controllers.api` and `services`.

Command Line Options
--------------------
The following are the command line options:
- --config="file" : Required. File where the config settings are for this project.

Configuration Options
---------------------
The following are settings that can be used for each section of a config file.
- include_module: Include the docstring for the module.
- include_classes: Include the docstring for each class.
- include_class_methods: Include the docstring for each class method
- include_functions: Include the docstring for each function in the module.
- document_name: the path and file name of where the markdown file should be stored.
- black_list: is a list of packages or modules to be ignored.