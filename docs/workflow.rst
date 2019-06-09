Workflow
========

Here we describe the workflow of ``lvcgcnd`` after an alert is received.

``lvcgcnd`` is a systemd wrapper for a Python script (``lvcgcn``) created at install time.
When ``lvcgcnd`` is started it will setup a logger and release control to pygcn
specifying a callback function (``process_gcn``) to be called when an alert is received.

The sequential list of operations after an alert is received is encapsulated in
the method ``torosgcn.listen.process_gcn`` and can be summarized as follows:

- Parse VOEvent and retrieve information for specific keywords.
- If the alert is a mock test and ``DEBUG_TEST`` is on, pass it along, otherwise return.
- Backup VOEvent to an xml file in the filesystem, if required in the configuration.
- Send the alert email to people in the collaboration.
- Retrieve skymap (if any) from GraceDB website and backup a copy if required in the configuration.
- Generate targets for each observatory using the skymap and GLADE catalog.
- Upload targets to broker website.
- Send confirmation email with error messages if any.
