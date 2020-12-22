********************************************
Pycargo: Excel loading and exporting helper
********************************************

.. image:: https://badgen.net/pypi/v/pycargo
    :target: https://pypi.org/project/pycargo
    :alt: Latest version
   
.. image:: https://badgen.net/badge/code%20style/black/000
    :target: https://github.com/ambv/black
    :alt: code style: black


**pycargo** is a simple to use helper library for exporting and loading data from excel.
Its a common requirement in web applications for bulk loading of data. Pycargo hides
all the working and gives you easy to use methods for easy exporting of templates and
loading data.

.. code-block:: python

    from pycargo import fields
    from pycargo.spreadsheet import SpreadSheet


    class CustomerSpreadSheet(SpreadSheet):
        name = fields.StringField(comment="Customer Name")
        code = fields.IntegerField(required=True, data_key="Code")
        created_on = fields.DateTimeField()


    cs = CustomerSpreadSheet()

    # Exporting templates
    cs.export_template("customer_template.xlsx", only=["name", "code"])

    # Bulk loading
    dataset = cs.load("customer_template.xlsx")


So with pycargo you can:

- **Export** template for loading data
- **Load** data from the templates
- **Validate** loaded data.

Get It Now
==========

::

    $ pip install -U pycargo

Requirements
============

- Python >= 3.6


License
=======

MIT licensed. See the bundled LICENSE file for more details.
****