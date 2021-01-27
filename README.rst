********************************************
Pycargo: Excel loading and exporting helper
********************************************

.. image:: https://badgen.net/pypi/v/pycargo
    :target: https://pypi.org/project/pycargo
    :alt: Latest version
   
.. image:: https://badgen.net/badge/code%20style/black/000
    :target: https://github.com/ambv/black
    :alt: code style: black


As a data lover, have you ever wondered working with excel data is as similar to creating models in django ? 
Yes??, No??, confused??, Don't Worry!! you are at the right spot. **pycargo** is a simple to use helper library for exporting and loading data from excel.
Its a usual practice in web applications for bulk loading of data. Pycargo abstracts
all the working and gives you easy to use methods for easy exporting of templates and
loading data.

.. code-block:: python

    from pycargo import fields
    from pycargo import validate
    from pycargo.spreadsheet import SpreadSheet


    class CustomerSpreadSheet(SpreadSheet):
        name = fields.StringField(comment="Customer Name")
        code = fields.IntegerField(data_key="Code", validate=[validate.Required()])
        created_on = fields.DateTimeField()


    cs = CustomerSpreadSheet()

    # Exporting templates
    cs.export_template("customer_template.xlsx", only=["name", "code"])

    # Bulk loading
    cs.load("customer_template.xlsx")
    for row in cs.rows():
        print(row)


So with pycargo you can:

- **Export** template for loading data
- **Load** data from the templates
- **Validate** loaded data.

Export Template gives you a ready-made excel file with customized header styles. 

.. code-block:: python

    cs.export_template("customer_template.xlsx", only=["name", "code"])

Loading data saves your memory by giving you RowIterator Object of each row.

>>> for row in cs.rows():
        print(row)
<Row cells({'name': <Cell Bob>, 'code': <Cell 7>, 'created_on': <Cell None>})>
<Row cells({'name': <Cell Alice>, 'code': <Cell 4>, 'created_on': <Cell None>})>

Validating Data for workbooks! Yes you are reading it right. Tired off making custom methods for validating each and every column based on its values ? **Pycargo** comes with already built-in helper functions which eases your requirements and binds those at one single place. It comes with all the general validators like **Range**, **Equal**, **NoneOf**, and many more.



.. code-block:: python

    code = fields.IntegerField(data_key="Code", validate=[validate.Range(2,10)])
 

Get It Now
==========

Install pycargo with pip. Better to Use Python Virtualenv to shield it from OS system modules.

::

    $ pip install -U pycargo

Requirements
============

- Python >= 3.6


License
=======

MIT licensed. See the bundled LICENSE file for more details.
****