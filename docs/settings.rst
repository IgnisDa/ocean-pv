.. _settings-label:

####################
The Project Settings
####################

Due to the project's complexity, it contains 4 different settings
modules. They are all present in ``ocean_website/settings/*``.

*******
base.py
*******

This module contains all the settings that are common to the
project. All other settings modules import this into their
global namespace.

**************
development.py
**************

This module should *ideally* be the one that that should be
used during development. This uses **postgresql** as the
database backend and needs postgresql to be installed on the
your machine. It also loads sensitive information from a
separate file, ``.env`` (which shouldn't be committed to
version control) using a library called python-decouple_. A
starting ``.env.example`` is present in the root directory,
rename it to ``.env`` and fill in the correct information.
Remember to change the ``SECRET_KEY`` variable too. It uses
GMAIL as it's email backend but to set it to console based,
change ``EMAIL_BACKEND`` to ``'django.core.mail.backends.console.EmailBackend'``

.. _python-decouple: https://github.com/henriquebastos/python-decouple

******************
development_alt.py
******************

`_hecc_`
