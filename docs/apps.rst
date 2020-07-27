********
The Apps
********

The project is composed of five apps- ``core``, ``home``, ``graphs``,
``interactions`` and ``users``. Each of the apps is briefly described below.

Core
----
Contains the core functionalities of the app, like some commonly
required *middlewares* etc.

Home
----
Contains the code logic for the homepages and other related pages.
These pages do not have any special logic handling and don't hit
the database as well. Contains the landing/homepage.

Graphs
------
A lot of the heavy lifting is done here. This contains the actual
functions that create the graphs and render it to the page in HTML
format. Mostly retrieves data from the database rather than writing
to it.

Interactions
------------
This app contains the code logic that enables the users to view and
consequently answer the questions. Once the user has filled in the
answers, this writes them to the database in the correct format.
Mostly writes to the database rather than retrieving to it.

Users
-----
It contains the code logic that handles the user authentication
and other such important functionalities. It also contains the
code logic for *Login*, *Register*, *sending password reset emails*,
and handling the *User Profiles*.
