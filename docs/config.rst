.. _conf:

Configuration
=============

Lvcgcn makes use of a configuration file installed in /etc/toros/lvcgcn-conf.yaml

It uses the `YAML`_ mark-up language.

.. note::
    During installation, a sample ``lvcgcn-conf.yaml`` is installed to help
    with configuration.

Keyword Description
-------------------

Following is a description of the keyworks that you should configure

``LIGO Run``: A string for the LIGO Run name (O1, O2, O3, etc).

``Catalog Path``: The full path to the galaxy catalog file to retrieve sources.
lvcgcnd is set to work with GLADE 2.3. If you want to modify the catalog used, 
see section :ref:`cat`.

``Catalog Filters``: Parameters to filter galaxy selection criteria.
This depends on the particular selection criteria and are used in 
``torosgcn.scheduler.generate_targets``.

``Observatories``: lvcgcnd will generate separate lists of targets for each
observatory based on what each can observe.
This keyword should contain a list and each item should look like the following:

.. code-block:: yaml

    name: OBS01
    location: {
      lon: -64.5467, # degrees
      lat: -31.5983, # degres
      height: 1350   # meters
    }

``DEBUG_TEST``: If ``true`` it will respond to mock alerts (the M-series). It will
only send emails to people specified under ``Admin Emails``, but it will upload the
targets to the broker website and will backup the files if specified.
Settign it to ``false``, will ignore them.

``Email Configuration``: A dictionary with the sender email configuration.
It should look like the following:

.. code-block:: yaml

    SMTP Domain: smtp.gmail.com:587,
    Sender Address: example@gmail.com,
    Login Required: true,
    Username: yourUserName,  # null if not needed
    Password: $ecretPassw0rd,  # null if not needed

``Admin Emails``: A yaml list with the list of the administrators of lvcgcnd.
Admins will be alerted of error when ``DEBUG_TEST`` is set to ``true``.

``Alert Recipients``: A yaml list with the recipient emails that should be
notified when an alert is received.

``Broker Upload``: A dictionary containing URLs and credentials to upload targets
for different observatories. An example is given below.

.. code-block:: yaml

    site url: https://toros.utrgv.edu/,
    login url: https://toros.utrgv.edu/account/login/,
    uploadjson url: https://toros.utrgv.edu/broker/uploadjson/,
    logout url: https://toros.utrgv.edu/account/logout/,
    username: admin,
    password: Adm1nPa$$word

``Logging``: The file path (``File``) and ``Log Level`` 
(``DEBUG``, ``INFO``, ``WARNING``, ``ERROR``, ``CRITICAL``) to be set for logging.

``Backup``: Whether to backup VOEvents and skymap files.

.. _YAML: https://yaml.org
