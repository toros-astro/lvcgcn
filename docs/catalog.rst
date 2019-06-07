.. _cat:

Galaxy Catalogs
===============

lvcgcn is designed to work with the GLADE catalog (revision 2.3).

To speed up the reading process ``torosgcn.scheduler.get_targets`` will need
a comma separated value (csv) reduced version of GLADE.

The columns for the reduced version should at least contain
``Name``, ``RA``, ``Dec``, and ``Dist``.

lvcgcnd will open the catalog using the ``Catalog Path`` entry in the
``lvcgcn-conf.yaml`` configuration file.

