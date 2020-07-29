.. _testing-label:

####################
Testing this project
####################
There is a ``requirements-dev.txt`` in ``docs/`` which will install all the dependencies required for testing this project. The tests are present in ``tests/*``. 

.. code-block:: console

	$ python -m venv env
	$ source ./env/bin/activate
	$ pip install -r docs/requirements-dev.txt

If you use Poetry_ package manager to manage your dependencies, you can instead run ``poetry install`` in the project root. 

.. _Poetry: https://python-poetry.org/

**********************
How tests are arranged
**********************

Each app_ contains its own tests in the ``tests`` folder. These tests
exclusively test their corresponding app. The ``tests/integration/`` 
directory contains selenium_ tests that test the website itself. 

.. _app: https://docs.djangoproject.com/en/3.0/ref/applications/
.. _selenium: https://pypi.org/project/selenium/
.. _Chromedriver: https://sites.google.com/a/chromium.org/chromedriver/

*****************
Running the tests
*****************
A ``pytest.ini`` present in the root directory takes care of pointing to the correct settings.
It also writes the test coverage in ``htmlcov/``. Simply run ``pytest`` in the root directory
to get the tests underway. 

****************
Integrated tests
****************

Since they take a lot longer to execute than unittests, they are
disabled by default (in the ``pytest.ini`` file). 
These tests are present in ``tests/integration/``. They use Chromedriver_ for testing.
They are all marked with ``pytest.mark.browser``.
The associated webdriver should be present in ``tests/integration/webdrivers/``.
Download the correct binary from here https://chromedriver.chromium.org/downloads
and make it executable to be able to run the tests.

.. code-block:: console

	$ chmod +x tests/integration/webdrivers/chromedriver
	$ pytest -m browser # run only the integrated tests
