import unittest
from unittest import mock
import loguru

loguru.logger = mock.Mock()
import tempfile
import torosgcn
import smtplib

smtplib.SMTP = mock.Mock()


class TestConfig(unittest.TestCase):
    @mock.patch("torosgcn.config._yaml")
    def test_load_config(self, mock_yaml):
        "Test that config.load_config loads the file with the correct text"
        torosgcn.config._CONFIG_IS_LOADED = False
        fp = tempfile.NamedTemporaryFile("w+")
        torosgcn.config.CONFIG_PATH = fp.name
        test_text = "Test"
        fp.write(test_text)
        fp.seek(0)
        torosgcn.config.load_config()
        self.assertTrue(mock_yaml.full_load.called)
        (text,), kwargs = mock_yaml.full_load.call_args
        self.assertEqual(text, test_text)
        fp.close()

    def test_get_config(self):
        "Test that config.get_config returns the correct dictionary"
        torosgcn.config._CONFIG_IS_LOADED = False
        fp = tempfile.NamedTemporaryFile("w+")
        torosgcn.config.CONFIG_PATH = fp.name
        fp.write("Test: Param01")
        fp.seek(0)
        config_dict = torosgcn.config.get_config()
        self.assertEqual({"Test": "Param01"}, config_dict)
        fp.close()

    def test_get_config_for_key(self):
        "Test config.get_config_for_key"
        torosgcn.config._CONFIG_IS_LOADED = False
        fp = tempfile.NamedTemporaryFile("w+")
        torosgcn.config.CONFIG_PATH = fp.name
        fp.write("One: Param01\nTwo: Param02")
        fp.seek(0)
        first_val = torosgcn.config.get_config_for_key("One")
        second_val = torosgcn.config.get_config_for_key("Two")
        self.assertEqual(first_val, "Param01")
        self.assertEqual(second_val, "Param02")
        fp.close()

    @mock.patch("torosgcn.config._logging")
    def test_init_logger(self, mock_logging):
        torosgcn.config._CONFIG_IS_LOADED = False
        fp = tempfile.NamedTemporaryFile("w+")
        torosgcn.config.CONFIG_PATH = fp.name
        mock_conf = """Logging: {
  File: logfilename,
  Log Level: INFO
}
Email Configuration: {
  SMTP Domain: smtp.gmail.com,
  SMTP Port: 587,
  Sender Address: example@gmail.com,
  Login Required: false,
  Username: null,
  Password: null
}"""
        fp.write(mock_conf)
        fp.seek(0)
        torosgcn.config.init_logger()
        self.assertTrue(loguru.logger.add.called)


class TestListen(unittest.TestCase):
    def setUp(self):
        self.info = {
            "role": "drill",
            "graceid": "D190422ab",
            "alerttype": "Initial",
            "eventpage": "http://someurl.com/view",
            "skymap_fits": "http://download/skymap",
            "sourceprobs": {
                "BNS": 0.7,
                "NSBH": 0.1,
                "BBH": 0.05,
                "MassGap": 0.02,
                "Terrestrial": 0.0,
                },
            "nsprobs": {
                "HasNS": 0.5,
                "HasRemnant": 0.99,
                },
            "gcndatetime": "2019-04-22T00:00:00",
            "datetime": "2019-04-22T03:12:23",
        }
        from astropy.coordinates import EarthLocation

        self.obs = [
            {
                "name": "EABA",
                "location": EarthLocation.from_geodetic(-64.5467, -31.5983, 1350),
            },
            {
                "name": "CTMO",
                "location": EarthLocation.from_geodetic(-97.568956, 25.995789, 12),
            },
        ]
        from astropy.io import ascii
        import numpy as np
        from . import sample_data

        self.ntarg = 10
        t_targets = ascii.read(sample_data.minicat)[: 2 * self.ntarg]
        t_targets["Likelihood"] = np.random.random(2 * self.ntarg)
        self.obs_trg = self.obs.copy()
        self.obs_trg[0]["targets"] = t_targets[: self.ntarg]
        self.obs_trg[1]["targets"] = t_targets[self.ntarg :]

    @mock.patch("torosgcn.listen.config.get_config_for_key")
    def test_sendemail(self, mock_conf):
        def get_config(arg):
            if arg == "Email Configuration":
                return {
                    "SMTP Domain": "smtp.example.com:25",
                    "Sender Address": "sender@example.com",
                    "Login Required": True,
                    "Username": "sender",
                    "Password": "$ecretP4ssw0rd",
                }
            elif arg == "Admin Emails":
                return ["admin@example.com"]
            elif arg == "Alert Recipients":
                return ["person01@example.com", "person02@example.com"]
            else:
                return None

        mock_conf.side_effect = get_config
        subject = "To whom it may concern"
        msg_text = "I hope this finds you well.\n"
        recipient = ["user@example.com"]
        torosgcn.listen.sendemail(msg_text, subject, recipients=recipient)
        self.assertTrue(smtplib.SMTP.called)
        torosgcn.listen.sendemail(msg_text, subject, recipients=None)
        self.assertTrue(smtplib.SMTP.called)
        smtplib.SMTP.side_effect = ValueError
        torosgcn.listen.sendemail(msg_text, subject, recipients=recipient)
        self.assertTrue(loguru.logger.error.called)
        smtplib.SMTP.side_effect = None

    @mock.patch("torosgcn.listen.config")
    @mock.patch("torosgcn.listen.sendemail")
    def test_sendalertemail(self, mock_sendemail, mock_config):
        mock_config.get_config_for_key.return_value(["admin@example.com"])
        torosgcn.listen.sendalertemail("some payload", self.info)
        self.assertTrue(mock_sendemail.called)
        self.assertTrue(mock_config.get_config_for_key.called)
        (msg_text, subject), kwargs = mock_sendemail.call_args
        self.assertTrue("DRILL" in subject)
        self.assertTrue("Initial" in subject)
        self.assertTrue("D190422ab" in subject)
        self.assertTrue("D190422ab" in msg_text)
        self.assertTrue("http://someurl.com/view" in msg_text)
        self.assertTrue("http://download/skymap" in msg_text)
        self.assertTrue("0.7" in msg_text)
        self.assertTrue("0.1" in msg_text)
        self.assertTrue("0.0" in msg_text)
        self.assertTrue("0.5" in msg_text)
        self.assertTrue("0.99" in msg_text)
        self.assertTrue(kwargs.get("recipients") is None)
        self.assertTrue(isinstance(kwargs.get("attachments"), list))
        self.assertTrue(isinstance(kwargs.get("attachments")[0], tuple))
        self.assertEqual(kwargs.get("attachments")[0][0], "some payload")

    def test_getinfo(self):
        from . import sample_data
        from lxml.etree import fromstring

        for voe, at_string in zip(
            (
                sample_data.preliminary_voe,
                sample_data.initial_voe,
                sample_data.update_voe,
            ),
            ("Preliminary", "Initial", "Update"),
        ):
            root = fromstring(voe)
            info_ret = torosgcn.listen.getinfo(root)
            self.assertTrue(isinstance(info_ret, dict))
            self.assertEqual(info_ret.get("role"), "test")
            self.assertTrue("graceid" in info_ret)
            self.assertEqual(info_ret.get("alerttype"), at_string)
            self.assertTrue("eventpage" in info_ret)
            self.assertTrue("skymap_fits" in info_ret)
            self.assertTrue("sourceprobs" in info_ret)
            sourceprobs = info_ret["sourceprobs"]
            self.assertTrue("BNS" in sourceprobs)
            self.assertTrue("NSBH" in sourceprobs)
            self.assertTrue("BBH" in sourceprobs)
            self.assertTrue("MassGap" in sourceprobs)
            self.assertTrue("Terrestrial" in sourceprobs)
            self.assertTrue("nsprobs" in info_ret)
            nsprobs = info_ret["nsprobs"]
            self.assertTrue("HasNS" in nsprobs)
            self.assertTrue("HasRemnant" in nsprobs)
            self.assertTrue("gcndatetime" in info_ret)
            self.assertTrue("datetime" in info_ret)

        # Retractions are special
        root = fromstring(sample_data.retraction_voe)
        info_ret = torosgcn.listen.getinfo(root)
        self.assertTrue(isinstance(info_ret, dict))
        self.assertEqual(info_ret.get("role"), "test")
        self.assertTrue("graceid" in info_ret)
        self.assertEqual(info_ret.get("alerttype"), "Retraction")
        self.assertTrue("eventpage" in info_ret)
        self.assertTrue(info_ret.get("skymap_url") is None)
        self.assertTrue(info_ret.get("bnsprob") is None)
        self.assertTrue(info_ret.get("nsbhprob") is None)
        self.assertTrue(info_ret.get("bbhprob") is None)
        self.assertTrue(info_ret.get("nsprob") is None)
        self.assertTrue(info_ret.get("remnprob") is None)
        self.assertTrue("gcndatetime" in info_ret)
        self.assertTrue("datetime" in info_ret)

    @mock.patch("requests.session")
    @mock.patch("torosgcn.listen.config.get_config_for_key")
    def test_upload_gcnnotice(self, mock_get_conf, mock_session):
        def get_conf(arg):
            if arg == "Broker Upload":
                return {
                    "site url": "https://toros.utrgv.edu/",
                    "login url": "https://toros.utrgv.edu/account/login/",
                    "uploadjson url": "https://toros.utrgv.edu/broker/uploadjson/",
                    "logout url": "https://toros.utrgv.edu/account/logout/",
                    "username": "admin",
                    "password": "yourpassword",
                }
            else:
                return None

        mock_get_conf.side_effect = get_conf
        torosgcn.listen.upload_gcnnotice(self.info, self.obs_trg)
        self.assertTrue(mock_session.called)

    @mock.patch("torosgcn.listen.config.get_config_for_key")
    @mock.patch("requests.post")
    def test_slack(self, mock_post, mock_config):
        def slackwebhook(arg):
            if arg == "Slack Webhook":
                return "https://slack.com/STRING"
            return None

        mock_config.side_effect = slackwebhook
        info = self.info.copy()
        info["alerttype"] = "Preliminary"
        torosgcn.listen.sendslack(info)
        self.assertTrue(mock_config.called)
        self.assertTrue(mock_post.called)
        args, kw_args = mock_post.call_args
        self.assertTrue("BNS" in kw_args["data"])
        self.assertTrue("D190422ab" in kw_args["data"])
        self.assertTrue("https://slack.com/STRING" in kw_args["url"])

        # Test that nothing is sent with Updates or Initial
        for altype in ["Initial", "Update"]:
            info["alerttype"] = altype
            mock_post.reset_mock()
            mock_config.reset_mock()
            torosgcn.listen.sendslack(info)
            self.assertTrue(mock_config.called)
            self.assertFalse(mock_post.called)

        # Test that retractions are sent
        info["alerttype"] = "Retraction"
        torosgcn.listen.sendslack(info)
        self.assertTrue(mock_config.called)
        self.assertTrue(mock_post.called)
        args, kw_args = mock_post.call_args
        self.assertFalse("BNS" in kw_args["data"])
        self.assertTrue("D190422ab" in kw_args["data"])
        self.assertTrue("https://slack.com/STRING" in kw_args["url"])

    @mock.patch("torosgcn.listen.sendslack")
    @mock.patch("torosgcn.listen.upload_gcnnotice")
    @mock.patch("torosgcn.listen.sendalertemail")
    @mock.patch("torosgcn.listen.retrieve_skymap")
    @mock.patch("torosgcn.scheduler.generate_targets")
    @mock.patch("torosgcn.listen.backup_skymap")
    @mock.patch("torosgcn.listen.backup_voe")
    @mock.patch("torosgcn.listen.getinfo")
    @mock.patch("torosgcn.listen.config.get_config_for_key")
    def test_process_gcn(
        self,
        mock_config,
        mock_info,
        mock_backup_voe,
        mock_backup_map,
        mock_targets,
        mock_retrieve,
        mock_email,
        mock_upload,
        mock_slack,
    ):

        all_mocks = [
            mock_config,
            mock_info,
            mock_backup_voe,
            mock_email,
            mock_upload,
            mock_slack,
        ]

        def assert_mocks_called(*mocks, truth=True):
            "Helper function to assert that all mocks were called"
            if truth:
                for amock in mocks:
                    self.assertTrue(amock.called)
            else:
                for amock in mocks:
                    self.assertFalse(amock.called)

        def reset_mocks(*mocks):
            "Helper function to reset all mocks"
            for amock in mocks:
                amock.reset_mock()

        def get_conf(arg):
            if arg == "DEBUG_TEST":
                return True
            return None

        mock_config.side_effect = get_conf
        mock_info.return_value = self.info

        from . import sample_data
        from lxml.etree import fromstring

        root = fromstring(sample_data.preliminary_voe)
        payload = bytes(sample_data.preliminary_voe, encoding="utf8")
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(mock_backup_map, mock_targets, mock_retrieve, *all_mocks)
        reset_mocks(mock_backup_map, mock_targets, mock_retrieve, *all_mocks)

        mock_info.side_effect = ValueError
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(loguru.logger.exception, *all_mocks)
        reset_mocks(*all_mocks)
        mock_info.side_effect = None

        ### Test now when not test debugging ###
        def get_conf_prod(arg):
            if arg == "DEBUG_TEST":
                return False
            return None

        # A test GCN arrives and debug is set to False.
        # It should log that it got a test and return
        info_test = self.info.copy()
        info_test["role"] = "test"
        mock_info.return_value = info_test
        mock_config.side_effect = get_conf_prod
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(mock_config, mock_info, loguru.logger.debug)
        assert_mocks_called(
            mock_backup_voe, mock_email, mock_upload, mock_slack, truth=False
        )
        reset_mocks(*all_mocks, loguru.logger.debug)

        # The next tests will be for Observation GCN type
        mock_info.return_value = self.info

        # Test when backup_voe throws error
        # It should log it and continue as usual
        mock_backup_voe.side_effect = ValueError
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(loguru.logger.exception, *all_mocks)
        reset_mocks(loguru.logger.exception, *all_mocks)
        mock_backup_voe.side_effect = None

        # Test when backup_map throws error
        # It should log it and continue as usual
        mock_backup_map.side_effect = ValueError
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(loguru.logger.exception, *all_mocks)
        reset_mocks(loguru.logger.exception, *all_mocks)
        mock_backup_map.side_effect = None

        # Test when sendemail throws an exception
        # It should log it and continue as usual
        mock_email.side_effect = ValueError
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(loguru.logger.exception, *all_mocks)
        reset_mocks(loguru.logger.exception, *all_mocks)
        mock_email.side_effect = None

        # Test when retrieve_skymap throws an exception
        # It should log it and continue as usual
        mock_retrieve.side_effect = ValueError
        reset_mocks(mock_backup_map, mock_targets)
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(loguru.logger.exception, *all_mocks)
        assert_mocks_called(mock_backup_map, mock_targets, truth=False)
        reset_mocks(loguru.logger, *all_mocks)
        mock_retrieve.side_effect = None

        # Test when upload_gcnnotice throws an error
        # It should log it and continue as usual
        mock_upload.side_effect = ValueError
        reset_mocks(loguru.logger, *all_mocks)
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(loguru.logger.exception, *all_mocks)
        reset_mocks(loguru.logger.exception, *all_mocks)
        mock_upload.side_effect = None

        # Test when upload_gcnnotice throws an error
        # It should log it and continue as usual
        mock_slack.side_effect = ValueError
        torosgcn.listen.process_gcn(payload, root)
        assert_mocks_called(loguru.logger.exception, *all_mocks)
        reset_mocks(loguru.logger.exception, *all_mocks)
        mock_slack.side_effect = None

    @mock.patch("builtins.open")
    @mock.patch("torosgcn.listen.config.get_config_for_key")
    @mock.patch("torosgcn.listen.os")
    def test_backup_voe(self, mock_os, mock_config, mock_open):
        def get_conf(arg):
            if arg == "Backup":
                bkp = {"VOEvent Backup Dir": "some/path", "Backup VOEvent": True}
                return bkp
            return None

        mock_os.path.exists.return_value = True
        mock_os.path.join.return_value = "some/path/file.xml"
        torosgcn.listen.backup_voe(b"Testing", self.info)
        (bkpfile_path, __), cp_kwarg = mock_open.call_args
        self.assertTrue(mock_open.called)
        self.assertEqual(bkpfile_path, "some/path/file.xml")
        self.assertTrue(loguru.logger.info.called)

        mock_os.path.exists.return_value = False
        torosgcn.listen.backup_voe(b"Testing", self.info)
        self.assertTrue(mock_os.makedirs.called)


class TestScheduler(unittest.TestCase):
    def setUp(self):
        from astropy.coordinates import EarthLocation

        self.obs = [
            {
                "name": "EABA",
                "location": EarthLocation.from_geodetic(-64.5467, -31.5983, 1350),
            },
            {
                "name": "CTMO",
                "location": EarthLocation.from_geodetic(-97.568956, 25.995789, 12),
            },
        ]

        from astropy.io import ascii
        import numpy as np
        from . import sample_data

        self.ntarg = 10
        t_targets = ascii.read(sample_data.minicat)[: 2 * self.ntarg]
        t_targets["Likelihood"] = np.random.random(2 * self.ntarg)
        self.obs_trg = self.obs.copy()
        self.obs_trg[0]["targets"] = t_targets[: self.ntarg]
        self.obs_trg[1]["targets"] = t_targets[self.ntarg :]

    def test_alpha_cuts(self):
        from astropy.time import Time

        observation_time = Time("2019-04-22T00:00:00")
        lo_alpha, hi_alpha = torosgcn.scheduler.alpha_cuts(observation_time)
        self.assertNotEqual(lo_alpha, hi_alpha)
        self.assertFalse(lo_alpha is None)
        self.assertFalse(hi_alpha is None)

    def test_broker_uploadstring(self):
        ret_string = torosgcn.scheduler.broker_uploadstring(self.obs)
        self.assertTrue(isinstance(ret_string, str))
        self.assertTrue("EABA" in ret_string)
        self.assertTrue("CTMO" in ret_string)
        self.assertTrue(len(ret_string.split(";")), 2)
        eaba, ctmo = ret_string.split(";")
        eaba_name, eaba_targets = eaba.split(":")
        ctmo_name, ctmo_targets = ctmo.split(":")
        self.assertEqual(eaba_name.strip(), "EABA")
        self.assertEqual(len(eaba_targets.split(",")), self.ntarg)
        self.assertEqual(ctmo_name.strip(), "CTMO")
        self.assertEqual(len(ctmo_targets.split(",")), self.ntarg)

    @mock.patch("torosgcn.scheduler.config")
    def test_broker_json(self, mock_config):
        import json

        # Patching for get_config_for_key("LIGO Run")
        mock_config.get_config_for_key.return_value = "O3"
        info = {
            "role": "S",
            "graceid": "S190422ab",
            "datetime": "2019-04-22T03:23:12",
            "alerttype": "Preliminary",
            "gcndatetime": "2019-04-22T00:00:00",
        }
        json_str = torosgcn.scheduler.broker_json(info, self.obs_trg)
        self.assertFalse(json_str is None)
        self.assertTrue(isinstance(json.loads(json_str), dict))
        self.assertTrue("S190422ab" in json_str)
        self.assertTrue("2019-04-22T03:23:12" in json_str)
        self.assertTrue("Preliminary" in json_str)
        self.assertTrue("O3" in json_str)

    @mock.patch("torosgcn.scheduler.config")
    def test_generate_targets(self, mock_config):
        cat_filters = {
            "NUM_TARGETS": 5,
            "MAX_DIST": 120,
            "MAX_APP_MAG": 19.0,
            "MAX_ABS_MAG": -17.5,
        }
        fp = tempfile.NamedTemporaryFile("w+")
        miniglade = """Name, RA, Dec, Dist
1831688,166.182,28.29288,159.20118355
SDSSJ105324.63+254607.4,163.353,25.76881,157.53630617
SDSSJ105332.98+254611.7,163.387,25.76992,157.549874929
1751874,163.476379,25.839355,158.979449972
1790410,164.572464,26.856163,157.961488837
NGC0253,11.88806,-25.288799,3.92595099046
NGC5128,201.365646,-43.018711,3.76743399832
03464851+6805459,56.702141,68.096107,8.3557478325
NGC5236,204.253,-29.8655,4.46732076201
NGC4736,192.721451,41.120152,4.24571533533
NGC0055,3.72334,-39.196629,2.18817755456
NGC0300,13.723,-37.68486,1.87855744795
NGC5102,200.490234,-36.630211,3.58100833048
NGC7793,359.457611,-32.59103,3.94486557231
"""
        fp.write(miniglade)
        fp.seek(0)
        mock_config.get_config_for_key.side_effect = [self.obs, fp.name, cat_filters]
        skymap_path = "./tests/test_bayestar.fits.gz"
        from astropy.time import Time

        now = Time("2019-06-01T01:00:00")
        obs_ret = torosgcn.scheduler.generate_targets(skymap_path, detection_time=now)
        self.assertEqual(len(obs_ret), 2)
        eaba = obs_ret[0]
        ctmo = obs_ret[1]
        self.assertTrue("name" in eaba)
        self.assertEqual("EABA", eaba.get("name"))
        self.assertTrue("name" in ctmo)
        self.assertEqual("CTMO", ctmo.get("name"))
        self.assertTrue("targets" in eaba)
        for targets in [eaba.get("targets"), ctmo.get("targets")]:
            self.assertTrue("Name" in targets.colnames)
            self.assertTrue("RA" in targets.colnames)
            self.assertTrue("Dec" in targets.colnames)
            self.assertTrue("Likelihood" in targets.colnames)
            self.assertEqual(len(targets), 5)

        # Test that it works if skymap is an hdulist
        from astropy.io import fits
        hdulist = fits.open(skymap_path)
        fp.seek(0)
        mock_config.get_config_for_key.side_effect = [self.obs, fp.name, cat_filters]
        obs_ret = torosgcn.scheduler.generate_targets(hdulist, detection_time=now)
        fp.close()
        self.assertEqual(len(obs_ret), 2)
        eaba = obs_ret[0]
        ctmo = obs_ret[1]
        self.assertTrue("name" in eaba)
        self.assertEqual("EABA", eaba.get("name"))
        self.assertTrue("name" in ctmo)
        self.assertEqual("CTMO", ctmo.get("name"))
        self.assertTrue("targets" in eaba)
        for targets in [eaba.get("targets"), ctmo.get("targets")]:
            self.assertTrue("Name" in targets.colnames)
            self.assertTrue("RA" in targets.colnames)
            self.assertTrue("Dec" in targets.colnames)
            self.assertTrue("Likelihood" in targets.colnames)
            self.assertEqual(len(targets), 5)


if __name__ == "__main__":
    unittest.main()
