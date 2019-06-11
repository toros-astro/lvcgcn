Installation and Usage
======================

Installation
------------

To install the lvcgcnd systemd service type in a terminal::

    $ make
    $ sudo make install

The first command will install the Python package ``torosgcn`` and a script ``lvcgcn``.
It will also create a ``lvcgcnd.service`` file to create the systemctl daemon ``lvcgcnd``.

The second command needs root permissions.
It will copy the ``lvcgcnd.service`` file to ``/etc/systemd/system`` and it will also
copy a sample ``lvcgcn-conf.yaml`` file to ``/etc/toros`` (see section :ref:`conf`). 

It is highly recommended (but not necessary) that you use a virtual environment
when installing.

Usage
-----

Usage of the ``lvcgcnd`` daemon follow all of the rules for ``systemd`` services.

For a full documentation of the systemd service, please refer to the `official documentation <https://www.freedesktop.org/wiki/Software/systemd/>`_.

Most common commands
^^^^^^^^^^^^^^^^^^^^

To start running the daemon::

    $ systemctl start lvcgcnd

If you change the configuration, you can restart the daemon to use the new config::

    $ systemctl restart lvcgcnd

To stop it::

    $ systemctl stop lvcgcnd

If you want to check if ``lvcgcnd`` whether is active and running or not::

    $ systemctl status lvcgcnd

All the previous commands may require ``root`` privilege to execute.
