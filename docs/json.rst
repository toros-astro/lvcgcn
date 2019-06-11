JSON Sample File
================

The GCN Notice information and targets for observatories is uploaded to the broker site using
a JSON file through a private API.
Below is a sample JSON file.

The ``assignments`` key is optional ("Retraction" notices do not specify assignments).

.. code-block:: json

  {
    "alert": {
      "ligo_run": "O3",
      "graceid": "S190501a",
      "SEtype": "S",
      "datetime": "2019-06-01T03:53:23"
    },
    "gcnnotice": {
      "gcntype": "Initial",
      "datetime": "2019-06-01T04:21:31"
    },
    "assignments": {
      "OBS01": {
        "NGC3527": 4.579577594439791e-07,
        "SDSSJ111036.33+291631.5": 4.571471198600905e-07,
        "SDSSJ110931.04+290153.1": 4.570529667464678e-07,
        "SDSSJ105717.80+262039.7": 4.565977915949241e-07,
        "UGC06147": 4.5358279508508366e-07
      },
      "OBS02": {
        "1790410": 4.754568836051921e-07,
        "1751874": 4.729037759899382e-07,
        "SDSSJ105332.98+254611.7": 4.727430685333189e-07,
        "SDSSJ105324.63+254607.4": 4.7274177982139006e-07,
        "1831688": 4.674778642517513e-07,
      },
      "OBS03": {
        "SDSSJ105530.54+260442.7": 4.6561621329489456e-07,
        "SDSSJ110509.50+283702.6": 4.629186351956917e-07,
        "SDSSJ110619.55+282301.5": 4.608629463520819e-07,
        "NGC3527": 4.579577594439791e-07,
        "UGC06147": 4.5358279508508366e-07
      }
    }
  }
