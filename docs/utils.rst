.. _utils:

Command-line Utilities
======================

Manual GCN Processing
^^^^^^^^^^^^^^^^^^^^^

The processing of VOEvents can also be triggered manually on the command line.
If for some reason a VOEvent is missed or it needs to be reprocessed, we can
download it from GraceDB and save it locally.

For example, if we want to reprocess the Preliminary GCN for the event ``S200129m``,
we would download it first (assuming we haven't done so already)::

    $ wget https://gracedb.ligo.org/apiweb/superevents/S200129m/files/S200129m-1-Preliminary.xml,0

and then trigger the processing with the following command::

    $ sudo process_gcn S200129m-1-Preliminary.xml

This last command must be done with ``sudo`` privilege.

If working in a virtualenv, we can invoke it with the full path::

    (myenv) $ which process_gcn
    /path/to/process_gcn
    (myenv) $ sudo /path/to/process_gcn S200129m-1-Preliminary.xml
