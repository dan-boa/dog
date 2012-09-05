Django's Settings Control
=========================

Django settings file changes through a web interface and corresponding server restart.
Its called a dog pointing to the fact that changing configuration on a testing server is tedios and monotonous job.

Features
================
 
1. Key value pairs are changed.

2. `Server restart` occurs by default.

3. Changes `roll back` if the server restart failed.

3. Server restart is monitored by a timeout thread to prevent extraneous errors creating a log in the process.

Drawbacks
================

Changes will be productive only when the key value pair are mentioned in the file without a line break.

Setup
================

Run the command to start the pico server in super user if the server restart requires super user privileges.

    sudo python pico -m server

File index.html has the following entry. The client.js has been utilized from the pico server checkout.

    <script type="text/javascript" src="client.js"></script>

Settings in home.py.

    CMD : The command required to restart the server.
    PATH: The path of the django project directory.


Requirement
================

1. `Pico`_: An amazing light python server.

.. _Pico: https://github.com/fergalwalsh/pico/

