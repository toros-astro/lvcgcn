#!/usr/bin/python
# -*- coding: utf-8 -*-
import gcn
import gcn.handlers
import gcn.notice_types
import os
from . import config
from . import scheduler
from loguru import logger


def sendemail(msg_text, subject, recipients=None, attachments=[]):
    """Will send out email with the message text in msg_text (string), subject (string)
    and a list of attachment file paths.
    If recipients is not provided as a list of email addresses (None),
    it will use email_alert_recipients from conf.py or the Admin Emails."""
    import smtplib
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import formatdate

    msg = MIMEMultipart()
    msg["Subject"] = subject

    email_conf = config.get_config_for_key("Email Configuration")
    if recipients is None:
        recipients = email_conf.get("Alert Recipients")
        if recipients is None:
            logger.warning("No email recipients found. Using admin's.")
            recipients = config.get_config_for_key("Admin Emails")
            msg_text = "WARNING: This email was only sent to Admin's email. "
            "No list of recipients found.\n{}".format(msg_text)

    email_sender_address = email_conf.get("Sender Address")
    msg["From"] = email_sender_address
    msg["To"] = ", ".join(recipients)
    msg["Date"] = formatdate(localtime=True)
    msg.attach(MIMEText(msg_text))

    for attachdata, fname in attachments:
        msg.attach(
            MIMEApplication(
                attachdata,
                Content_Disposition='attachment; filename="{}"'.format(fname),
                Name=fname,
            )
        )

    # The actual mail send
    try:
        email_smtp_domain = email_conf.get("SMTP Domain")
        server = smtplib.SMTP(email_smtp_domain)
        server.starttls()
        email_login_required = email_conf.get("Login Required")
        if email_login_required:
            email_username = email_conf.get("Username")
            email_sender_password = email_conf.get("Password")
            server.login(email_username, email_password)
        server.sendmail(email_sender_address, recipients, msg.as_string())
        server.quit()
    except:
        logger.error("SMTP Service not configured. Unable to send email.")


def sendalertemail(payload, info):
    pre_subject, pre_warning = "", ""
    if info["role"] == "test":
        pre_subject = "[TEST: Mock Alert] "
        pre_warning = "WARNING: The following is a Mock Alert.\n"
    if info["role"] == "drill":
        pre_subject = "[DRILL: Mock Alert] "
        pre_warning = "WARNING: The following is a Drill.\n"
    subject = "{}{} GCN for {}".format(pre_subject, info["alert_type"], info["graceid"])
    msg_text = """{}VOEvent from the LV-EM GCN system.

Alert info:
Grace ID: {}
TOROS Broker Page: https://toros.utrgv.edu/broker/alert/{}
GraceDB Event Page: {}
Sky map URL: {}

Classification Probabilities:
BNS: {}
NS-BH: {}
BBH: {}
NS Probability: {}
Remnants Probability: {}""".format(
        pre_warning,
        info["graceid"],
        info["graceid"],
        info["eventpage"],
        info["skymap_url"],
        info["bnsprob"],
        info["nsbhprob"],
        info["bbhprob"],
        info["nsprob"],
        info["remnprob"],
    )

    if info["alert_type"] == "Retraction":
        msg_text = """{0}VOEvent from the LV-EM GCN system.

This is a RETRACTION for SuperEvent with GraceID: {1}
For more info visit the TOROS Broker Page: https://toros.utrgv.edu/broker/alert/{1}
or the GraceDB Event Page: {2}
""".format(
            pre_warning, info["graceid"], info["eventpage"]
        )
    ADMIN_EMAILS = config.get_config_for_key("Admin Emails")
    recipients = ADMIN_EMAILS if info["role"] == "test" else None
    sendemail(
        msg_text, subject, recipients=recipients, attachments=[(payload, "VOEvent.xml")]
    )


def send_upload_confirmation_email(obs, info, error_message=None):
    if obs is not None:
        broker_uploadstring = (
            "Broker upload-string to manually " "upload targets:\n\n{}"
        ).format(scheduler.broker_uploadstring(obs))
    else:
        broker_uploadstring = "There were no targets to upload."

    pre_subject, pre_warning = "", ""
    if info["role"] == "test":
        pre_subject = "[TEST: Mock Alert] "
        pre_warning = "WARNING: The following is a Mock Alert.\n"
    elif info["role"] == "drill":
        pre_subject = "[DRILL: Mock Alert] "
        pre_warning = "WARNING: The following is a Drill.\n"

    if error_message is None:
        msg_text = (
            "{0}\n\n{1} GCN for LVC super event {2} "
            "was successfully uploaded to broker.\n"
            "For more info, check the broker alert page: https://toros.utrgv.edu/broker/alert/{2}\n"
            "and the LVC event page: {3}\n\n{4}"
        ).format(
            pre_warning,
            info.get("alert_type"),
            info.get("graceid"),
            info.get("eventpage"),
            broker_uploadstring,
        )
    else:
        msg_text = (
            "{0}\n\nError uploading {1} GCN for LVC super event {2}.\n"
            "For more info, check the broker alert page: https://toros.utrgv.edu/broker/alert/{2}\n"
            "and the LVC event page: {3}\n\n{4}\n"
            "Error Trace:\n{5}\n"
        ).format(
            pre_warning,
            info.get("alert_type"),
            info.get("graceid"),
            info.get("eventpage"),
            broker_uploadstring,
            error_message,
        )
    email_subject = "{}{} GCN for {}".format(
        pre_subject, info.get("alert_type"), info.get("graceid")
    )
    ADMIN_EMAILS = config.get_config_for_key("Admin Emails")
    sendemail(msg_text, email_subject, recipients=ADMIN_EMAILS)


def getinfo(root):
    info = {}
    try:
        info["role"] = root.attrib["role"]
    except KeyError:
        logger.exception("Could not find tag `role` in XML.")
        info["role"] = None

    tag_graceid = root.find("./What//Param[@name='GraceID']")
    if tag_graceid is not None:
        info["graceid"] = tag_graceid.attrib["value"]
    else:
        logger.error("Could not find tag `GraceID` in XML.")
        info["graceid"] = None

    tag_type = root.find("./What//Param[@name='Packet_Type']")
    number_to_type = {
        "150": "Preliminary",
        "151": "Initial",
        "152": "Update",
        "164": "Retraction",
    }
    if tag_type is not None:
        info["alert_type"] = number_to_type.get(tag_type.attrib["value"])
    else:
        logger.error("Could not process tag `Packet_Type` in XML.")
        info["alert_type"] = None

    tag_eventpage = root.find("./What//Param[@name='EventPage']")
    if tag_eventpage is not None:
        info["eventpage"] = tag_eventpage.attrib["value"]
    else:
        logger.error("Could not find tag `EventPage` in XML.")
        info["eventpage"] = None

    tag_url = root.find("./What//Param[@name='skymap_fits']")
    if tag_url is not None:
        info["skymap_url"] = tag_url.attrib["value"]
    else:
        logger.debug("Could not find tag `skymap_fits` in XML.")
        info["skymap_url"] = None

    tag_bnsprob = root.find("./What//Param[@name='BNS']")
    if tag_bnsprob is not None:
        info["bnsprob"] = tag_bnsprob.attrib["value"]
    else:
        logger.debug("Could not find tag `BNS` in XML.")
        info["bnsprob"] = None

    tag_nsbhprob = root.find("./What//Param[@name='NSBH']")
    if tag_nsbhprob is not None:
        info["nsbhprob"] = tag_nsbhprob.attrib["value"]
    else:
        logger.debug("Could not find tag `NSBH` in XML.")
        info["nsbhprob"] = None

    tag_bbhprob = root.find("./What//Param[@name='BBH']")
    if tag_bbhprob is not None:
        info["bbhprob"] = tag_bbhprob.attrib["value"]
    else:
        logger.debug("Could not find tag `BBH` in XML.")
        info["bbhprob"] = None

    tag_nsprob = root.find("./What//Param[@name='HasNS']")
    if tag_nsprob is not None:
        info["nsprob"] = tag_nsprob.attrib["value"]
    else:
        logger.debug("Could not find tag `HasNS` in XML.")
        info["nsprob"] = None

    tag_remnprob = root.find("./What//Param[@name='HasRemnant']")
    if tag_remnprob is not None:
        info["remnprob"] = tag_remnprob.attrib["value"]
    else:
        logger.debug("Could not find tag `HasRemnant` in XML.")
        info["remnprob"] = None

    tag_gcndatetime = root.find("./Who//Date")
    if tag_gcndatetime is not None:
        info["gcndatetime"] = tag_gcndatetime.text
    else:
        logger.error("Could not find tag `Date` in XML.")
        info["gcndatetime"] = None

    tag_datetime = root.find("./WhereWhen//ISOTime")
    if tag_datetime is not None:
        info["datetime"] = tag_datetime.text
    else:
        logger.error("Could not find tag `ISOTime` in XML.")
        info["datetime"] = None
    return info


def retrieve_skymap(info):
    import requests
    import tempfile

    fits_response = requests.get(info["skymap_url"], stream=False)
    fits_response.raise_for_status()
    fp = tempfile.NamedTemporaryFile()
    for block in fits_response.iter_content(1024):
        fp.write(block)
    fp.seek(0)
    skymap_data = fp.read()
    fp.close()

    try:
        bkp_config = config.get_config_for_key("Backup")
        if bkp_config.get("Backup Skymap"):
            backup_skymap(skymap_data, info)
    except:
        logger.exception("Skymap backup failed.")
    return skymap_data


def upload_gcnnotice(info):
    error_msg = None
    if info.get("skymap_url") is not None:
        try:
            skymap_data = retrieve_skymap(info)
            try:
                import tempfile

                with tempfile.NamedTemporaryFile("wb") as fp:
                    fp.write(skymap_data)
                    fp.seek(0)
                    obs = scheduler.generate_targets(fp.name)
            except Exception as e:
                logger.exception("Error generating targets")
                obs = None
                error_msg = str(e)
        except Exception as e:
            logger.exception(
                "Error downloading FITS skymap for Grace ID: {} from URL: {}".format(
                    info.get("graceid"), info.get("skymap_url")
                )
            )
            obs = None
            error_msg = str(e)
    else:
        obs = None

    # Get Broker website config
    broker_conf = config.get_config_for_key("Broker Upload")
    site_url = broker_conf.get("site url")
    url_login = broker_conf.get("login url")
    url_uploadjson = broker_conf.get("uploadjson url")
    url_logout = broker_conf.get("logout url")
    broker_user_name = broker_conf.get("username")
    broker_user_password = broker_conf.get("password")
    try:
        import requests

        # Log into a session with our user
        client = requests.session()
        client.get(url_login)
        csrftoken = client.cookies["csrftoken"]
        login_data = {
            "username": broker_user_name,
            "password": broker_user_password,
            "csrfmiddlewaretoken": csrftoken,
        }
        r1 = client.post(url_login, data=login_data, headers={"Referer": url_login})

        # Upload targets in json format
        targetsjson = scheduler.broker_json(obs, info)
        sessionid = client.cookies["sessionid"]
        loadjson_data = {
            "targets.json": targetsjson,
            "csrfmiddlewaretoken": csrftoken,
            "sessionid": sessionid,
        }
        r2 = client.post(url_uploadjson, data=loadjson_data)

        # Log out
        r3 = client.get(url_logout, data={"sessionid": sessionid})

    except Exception as e:
        logger.exception("Could not upload target list using HTTP post method.")
        logger.debug(targetsjson)
        error_msg = str(e)

    send_upload_confirmation_email(obs, info, error_message=error_msg)


def backup_skymap(skymap_data, info):
    bkp_config = config.get_config_for_key("Backup")
    skymap_bkpdir = bkp_config.get("Skymap Backup Dir")
    if not os.path.exists(skymap_bkpdir):
        os.makedirs(skymap_bkpdir)

    skymap_bkpname = "skymap_basic_{}_{}.fits".format(
        info.get("graceid"), info.get("alert_type")
    )

    skymap_path = os.path.join(skymap_bkpdir, skymap_bkpname)
    with open(skymap_path, "wb") as fp:
        fp.write(skymap_data)
    logger.info("Skymap file {} copied to {}".format(skymap_bkpname, skymap_bkpdir))


def backup_voe(payload, info):
    bkp_config = config.get_config_for_key("Backup")
    if not bkp_config.get("Backup VOEvent"):
        return
    voevent_bkpdir = bkp_config.get("VOEvent Backup Dir")
    if not os.path.exists(voevent_bkpdir):
        os.makedirs(voevent_bkpdir)

    voevent_bkpname = "VOE_{}_{}.xml".format(
        info.get("graceid"), info.get("alert_type")
    )

    voevent_path = os.path.join(voevent_bkpdir, voevent_bkpname)
    with open(voevent_path, "w") as fp:
        fp.write(str(payload, encoding="utf-8"))
    logger.info("VOE file {} copied to {}".format(voevent_bkpname, voevent_bkpdir))


@gcn.handlers.include_notice_types(
    gcn.notice_types.LVC_PRELIMINARY,
    gcn.notice_types.LVC_INITIAL,
    gcn.notice_types.LVC_UPDATE,
    gcn.notice_types.LVC_RETRACTION,
)
def process_gcn(payload, root):
    "The callback function when a GCN is received."
    DEBUG_TEST = config.get_config_for_key("DEBUG_TEST") or False

    # Get relevant info from VOEvent
    try:
        info = getinfo(root)
    except:
        logger.exception("Error getting info from VOEvent payload.")
        info = {}

    if not DEBUG_TEST:
        if info.get("role") == "test":
            logger.debug("Received Mock VOEvent.")
            return

    # Back up VOE file
    try:
        backup_voe(payload, info)
    except:
        logger.exception("Error backing up VOE file.")

    # Send Alert by email
    try:
        sendalertemail(payload, info)
    except:
        logger.exception("Error sending alert email.")
    # Create and upload targets
    try:
        upload_gcnnotice(info)
    except:
        logger.exception("Error uploading targets.")


def main():
    # Set up logging
    config.init_logger()

    # Listen for GCNs until the program is interrupted
    # (killed or interrupted with control-C).
    gcn.listen(handler=process_gcn)


if __name__ == "__main__":
    main()
