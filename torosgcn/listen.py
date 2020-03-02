# -*- coding: utf-8 -*-
import gcn
import gcn.handlers
import gcn.notice_types
import os
from . import config
from . import scheduler
from loguru import logger


def sendslack(info):
    import requests

    if info.get("role") == "test":
        return
    webhook = config.get_config_for_key("Slack Webhook")
    if webhook is None:
        logger.info("No Slack webhook found.")
        return
    alerttype = info.get("alerttype")
    if alerttype == "Preliminary":
        obj, prob = max(info["sourceprobs"].items(), key=(lambda x: float(x[1])))
        msg_text = (
            "New Event: {}.\nObject is most likely {} ({:.2f}%).\nDistance: {:.0f} Mpc."
        ).format(info.get("graceid"), obj, float(prob) * 100, info.get("dist") or -1.0)
    elif alerttype == "Retraction":
        msg_text = "Event {} was retracted.".format(info.get("graceid"))
    else:
        logger.debug("Alert not Preliminary or Retraction.")
        return
    msg_json = '{{"text": "{}"}}'.format(msg_text)
    response = requests.post(data=msg_json, url=webhook)
    if not response.ok:
        logger.error("Slack response not OK.")
        logger.debug(response)


def sendemail(msg_text, subject, recipients=None, attachments=[]):
    """Will send out email with the message text in msg_text (string), subject (string)
    and a list of attachment tuples (bytes, filename).
    If recipients is not provided as a list of email addresses (None),
    it will get the list of recipients from the configuration file."""
    import smtplib
    from email.mime.application import MIMEApplication
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.utils import formatdate

    msg = MIMEMultipart()
    msg["Subject"] = subject

    email_conf = config.get_config_for_key("Email Configuration")
    if recipients is None:
        recipients = config.get_config_for_key("Alert Recipients")
        if not recipients:
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


def sendalertemail(payload, info, targets_graph=None):
    "Prepare and send the notification email of a new alert"
    pre_subject, pre_warning = "", ""
    if info.get("role") == "test":
        pre_subject = "[TEST: Mock Alert] "
        pre_warning = "WARNING: The following is a Mock Alert.\n"
    if info.get("role") == "drill":
        pre_subject = "[DRILL: Mock Alert] "
        pre_warning = "WARNING: The following is a Drill.\n"
    subject = "{}{} GCN for {}".format(
        pre_subject, info.get("alerttype"), info.get("graceid")
    )
    msg_text = """{}VOEvent from the LV-EM GCN system.

Alert info:
Grace ID: {}
TOROS Broker Page: https://toros.utrgv.edu/broker/alert/{}
GraceDB Event Page: {}
Sky map URL: {}
Distance Estimation: {:.2f} Mpc.

Classification Probabilities:
BNS: {}
NSBH: {}
BBH: {}
Mass Gap: {}
Terrestrial: {}
-------------------

Has NS Probability: {}
Has Remnant Probability: {}""".format(
        pre_warning,
        info.get("graceid"),
        info.get("graceid"),
        info.get("eventpage"),
        info.get("skymap_fits"),
        info.get("dist") or 0.0,
        info["sourceprobs"].get("BNS"),
        info["sourceprobs"].get("NSBH"),
        info["sourceprobs"].get("BBH"),
        info["sourceprobs"].get("MassGap"),
        info["sourceprobs"].get("Terrestrial"),
        info["nsprobs"].get("HasNS"),
        info["nsprobs"].get("HasRemnant"),
    )
    if info.get("alerttype") == "Retraction":
        msg_text = """{0}VOEvent from the LV-EM GCN system.

This is a RETRACTION for SuperEvent with GraceID: {1}
For more info visit the TOROS Broker Page: https://toros.utrgv.edu/broker/alert/{1}
or the GraceDB Event Page: {2}
""".format(
            pre_warning, info.get("graceid"), info.get("eventpage")
        )
    ADMIN_EMAILS = config.get_config_for_key("Admin Emails")
    recipients = ADMIN_EMAILS if info.get("role") == "test" else None
    attachments = [(payload, "VOEvent.xml")]
    if targets_graph is not None:
        attachments.append((targets_graph, "skymap.png"))
    sendemail(msg_text, subject, recipients=recipients, attachments=attachments)


def getinfo(root):
    "Parse VOEvent XML tree and create an info dictionary with relevant information"
    info = {}
    try:
        info["role"] = root.attrib["role"]
    except KeyError:
        logger.exception("Could not find tag `role` in XML.")
        info["role"] = None

    for key in ["GraceID", "AlertType", "Pkt_Ser_Num", "EventPage", "skymap_fits"]:
        tag = root.find("./What//Param[@name='{}']".format(key))
        if tag is not None:
            info[key.lower()] = tag.attrib["value"]
        else:
            if key != "skymap_fits":
                logger.error("Could not find tag `{}` in XML.".format(key))
            info[key.lower()] = None

    # Time of the event
    tag_datetime = root.find("./WhereWhen//ISOTime")
    if tag_datetime is not None:
        info["datetime"] = tag_datetime.text
    else:
        logger.error("Could not find tag `ISOTime` in XML.")
        info["datetime"] = None

    # Time of the GCN Notice
    tag_gcndatetime = root.find("./Who//Date")
    if tag_gcndatetime is not None:
        info["gcndatetime"] = tag_gcndatetime.text
    else:
        logger.error("Could not find tag `Date` in XML.")
        info["gcndatetime"] = None

    # Group source probabilities together
    info["sourceprobs"] = {}
    for probname in ["BNS", "NSBH", "BBH", "MassGap", "Terrestrial"]:
        tag = root.find("./What//Param[@name='{}']".format(probname))
        if tag is not None:
            info["sourceprobs"][probname] = tag.attrib["value"]
        else:
            logger.debug("Could not find tag `{}` in XML.".format(probname))
            info["sourceprobs"][probname] = None

    # Group NS merger probabilities together
    info["nsprobs"] = {}
    for probname in ["HasNS", "HasRemnant"]:
        tag = root.find("./What//Param[@name='{}']".format(probname))
        if tag is not None:
            info["nsprobs"][probname] = tag.attrib["value"]
        else:
            logger.debug("Could not find tag `{}` in XML.".format(probname))
            info["nsprobs"][probname] = None

    return info


def retrieve_skymap(info):
    "Fetch skymap FITS file from GraceDB service. Return skymap FITS as HDUList"
    import requests
    import tempfile
    from astropy.io import fits

    fits_response = requests.get(info.get("skymap_fits"), stream=False)
    if not fits_response.ok:
        logger.error("Downloading Skymap response not OK.")
    fp = tempfile.NamedTemporaryFile()
    for block in fits_response.iter_content(1024):
        fp.write(block)
    fp.seek(0)
    skymap_hdulist = fits.open(fp.name)
    fp.close()
    return skymap_hdulist


def upload_gcnnotice(info, targets=None):
    "Upload the JSON file that contains information about GCN Notice to broker"
    import requests

    # Get Broker website config
    broker_conf = config.get_config_for_key("Broker Upload")
    site_url = broker_conf.get("site url")
    url_login = broker_conf.get("login url")
    url_uploadjson = broker_conf.get("uploadjson url")
    url_logout = broker_conf.get("logout url")
    broker_user_name = broker_conf.get("username")
    broker_user_password = broker_conf.get("password")

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
    targetsjson = scheduler.broker_json(info, targets)
    sessionid = client.cookies["sessionid"]
    loadjson_data = {
        "targets.json": targetsjson,
        "csrfmiddlewaretoken": csrftoken,
        "sessionid": sessionid,
    }
    r2 = client.post(url_uploadjson, data=loadjson_data)

    # Log out
    r3 = client.get(url_logout, data={"sessionid": sessionid})
    logger.debug("Target JSON sent to broker:\n{}".format(targetsjson))


def backup_skymap(skymap_hdulist, info):
    "Save to file the skymap FITS file asociated with this GCN Notice"
    bkp_config = config.get_config_for_key("Backup")
    if not bkp_config.get("Backup Skymap"):
        return
    skymap_bkpdir = bkp_config.get("Skymap Backup Dir")
    if not os.path.exists(skymap_bkpdir):
        os.makedirs(skymap_bkpdir)

    skymap_bkpname = "{}_{}_{}.fits".format(
        info.get("graceid"), info.get("pkt_ser_num"), info.get("alerttype")
    )

    skymap_path = os.path.join(skymap_bkpdir, skymap_bkpname)
    skymap_hdulist.writeto(skymap_path)
    logger.info("Skymap file {} copied to {}".format(skymap_bkpname, skymap_bkpdir))


def backup_voe(payload, info):
    "Save to file the VOEvent XML"
    bkp_config = config.get_config_for_key("Backup")
    if not bkp_config.get("Backup VOEvent"):
        return
    voevent_bkpdir = bkp_config.get("VOEvent Backup Dir")
    if not os.path.exists(voevent_bkpdir):
        os.makedirs(voevent_bkpdir)

    voevent_bkpname = "{}_{}_{}.xml".format(
        info.get("graceid"), info.get("pkt_ser_num"), info.get("alerttype")
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

    # Retrieve skymap and generate targets if necessary
    targets = None
    if info.get("skymap_fits") is not None:
        try:
            skymap_hdulist = retrieve_skymap(info)
            try:
                backup_skymap(skymap_hdulist, info)
            except:
                logger.exception("Problem backing-up skymap")
            try:
                targets = scheduler.generate_targets(skymap_hdulist)
            except:
                logger.exception("Error generating targets")
            try:
                graphbytes = scheduler.graphtargets(info, targets, skymap_hdulist)
            except:
                graphbytes = None
                logger.exception("Error sending targets graph")
            try:
                scheduler.get_distance(skymap_hdulist, info)
            except:
                logger.exception("Error getting distance")
        except:
            logger.exception(
                "Error downloading FITS skymap for Grace ID: {} from URL: {}".format(
                    info.get("graceid"), info.get("skymap_fits")
                )
            )

    # Send Alert by email
    try:
        sendalertemail(payload, info, targets_graph=graphbytes)
    except:
        logger.exception("Error sending alert email.")

    # Send Alert to Slack
    try:
        sendslack(info)
        logger.info("Alert message sent to Slack.")
    except:
        logger.exception("Error sending Slack message.")

    # Upload targets to broker site
    try:
        upload_gcnnotice(info, targets)
    except:
        logger.exception("Error uploading targets to broker.")


def main():
    # Set up logging
    config.init_logger()

    # Listen for GCNs until the program is interrupted
    # (killed or interrupted with control-C).
    gcn.listen(handler=process_gcn)


def manual_process():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("filepath", help="The file path for the xml VOEvent.")
    args = parser.parse_args()
    with open(args.filepath, "rb") as f:
        payload = f.read()
    from lxml.etree import fromstring

    root = fromstring(payload)
    process_gcn(payload, root)


if __name__ == "__main__":
    main()
