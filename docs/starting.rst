*******************************
OCEAN-Personality-Visualization
*******************************

.. image:: https://img.shields.io/github/license/IgnisDa/ocean-pv?style=for-the-badge   
	:alt: GitHub

A website that helps you visualize your personality using graphs and compare it 
with others. It asks you a
series of questions and analyzes your inputs to create an easy to understand 
graph. It also provides you an
easy way to share these results with your peers and compare your personalities.
It is based on the 
OCEAN_ personality model which is the most acceptable model to measure 
personality used by researchers. 

.. _OCEAN: https://en.m.wikipedia.org/wiki/Big_Five_personality_traits 

The Website
===========
.. todo::
	
	This is incomplete 

Prerequisites
=============
This website has been built using the Django_ framework, using Python_ 
(version: 3.8), HTML_ (version: 5), 
and other web-dev components. 

.. _Django: https://www.djangoproject.com 
.. _Python: https://www.python.org
.. _HTML: https://en.wikipedia.org/wiki/HTML

Installing
==========
First, clone this project from Github_:
	
.. _Github: https://github.com/IgnisDa/ocean-pv/

.. code:: console 

	$ git clone https://github.com/IgnisDa/OCEAN-personality-visualization.git

The root directory contains a ``requirements.txt`` which can you can use to whip
up a working environment. 

.. code:: console

	$ cd ocean-pv/
	$ python -m venv env
	$ source ./env/bin/activate
	$ pip install -r requirements.txt

If you use Poetry_ package manager to manage your dependencies, you can run the 
following command in the project root. 

.. code:: console 

	$ poetry install --no-dev

To get the website up and running, you need to run the following:
	
.. code:: console

	$ python manage.py makemigrations
	$ python manage.py migrate
	$ python manage.py createsuperuser # enter your superuser name which can be used to access admin
	$ python manage.py createdata <superuser> # replace <superuser> with the name you entered above
	$ python manage.py calculateglobals
	$ python manage.py runserver 

You can then visit ``http://127.0.0.1:8000/`` in your browser to access the website.

.. note::
	
	The project uses ``ocean_website/settings/development.py`` as the default.
	If you want to use ``ocean_website/settings/production.py`` as 
	the settings module, then rename ``.env.example`` to ``.env``
	and fill it with correct information. Then add an environment variable 
	using ``export $OCEAN_PV 1`` or change ``manage.py`` instead to point to 
	the required settings. Alternatively, you can run ```OCEAN_PV=1 python manage.py runserver``.
	
Project Structure
=================
The project was created using the command ``django-admin startproject
ocean_website`` and that is also the main directory where important files like
``settings.py`` and ``wsgi.py`` live. 

This project uses the default django project structure_ with a few 
modifications. The apps that are part of the website are ``core``, ``graphs``, ``home``, 
``interactions``, ``users`` and are present in their corresponding directories. 

Major modifications include changing the location of 
``ocean_website/settings.py`` to ``ocean_website/settings/base.py``. 
This was done because this project uses 4 different settings files for 
*development*, *testing*, *production* and *heroku*. The ``manage.py`` and 
``wsgi.py`` files have been changed accordingly. 

.. note:: 
	 
	When starting a development server, the project will look for an 
	environment variable ``$OCEAN_PV``, and use that to decide which settings 
	file to use. 
	If ``$OCEAN_PV == "1"``, ``ocean_website/settings/production_settings.py`` 
	will be used. Otherwise, ``ocean_website/settings/development_settings.py`` 
	is used by default. 

.. _structure: https://django-project-skeleton.readthedocs.io/en/latest/structure.html

Testing
=======
The project uses pytest_ and a plugin pytest-django_ as its standard test-runner.
Read the full documentation on `testing the project`_

.. _Poetry: https://python-poetry.org/
.. _pytest-django: https://github.com/pytest-dev/pytest-django 
.. _pytest: https://docs.pytest.org/en/latest/
	
Contributing
============
Contributions are welcome! Read more at `contributing to the project`_

Authors
=======
This project is maintained by the community. Read more at 
`authors of this project`_.

License
=======
This project is licensed under the MIT License. Read more at 
`licensing and legal`_.

.. _licensing and legal: https://ocean-personality-visualization.readthedocs.io/en/latest/license.html
.. _authors of this project: https://ocean-personality-visualization.readthedocs.io/en/latest/authors.html
.. _contributing to the project: https://ocean-personality-visualization.readthedocs.io/en/latest/contributing.html
.. _testing the project: https://ocean-personality-visualization.readthedocs.io/en/latest/testing.html
