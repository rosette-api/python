## Generating documentation with Sphinx

The best tutorial for generating documentation can be found [here](http://gisellezeno.com/tutorials/sphinx-for-python-documentation.html)

Files in the source directory are generally static and should not need to be updated.  If another python module is created in `../rosette`, then the source may need to be regenerated using

`sphinx-apidoc -f -o source/ ../rosette/`

This will overwrite the *.rst files, which may then require some editing to provide the desired look.  Edits to date:
1. index.rst: Changed the `Welcome ...` title to `Python Binding`
1. index.rst: Added minor summary, "This is the API documentation for the Rosette API Python Binding.  For examples and usage, please refer to our `API Guide <http://developer.rosette.com/api-guide>`_."

To change the logo, edit conf.py, `html_logo`

To generate the html run `make html`.  The output will be written to `build/html`.  This is the step that is run by the `publish.sh` script when publishing the Python binding.  Note that the version, which is noted in `conf.py` is not displayed anywhere, but is updated during the publish phase.

You can view the generated html locally, by navigating to `docs/build/html` and opening `index.html`