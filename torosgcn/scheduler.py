# -*- coding: utf-8 -*-

import numpy as np
import astropy
from astropy import units as u
from astropy.io import ascii
from astropy.table import Column
from astropy.time import Time
from . import config


def alpha_cuts(observation_time, horizon=-15 * u.degree, min_height=30 * u.degree):
    "Helper function to calculate alpha limits to visibility away from the sun"
    sun = astropy.coordinates.get_sun(observation_time)
    horiz = horizon.to(u.degree)
    h = min_height.to(u.degree)
    lowest_alpha = (sun.ra - horiz + h).to(u.hourangle).value
    highest_alpha = (sun.ra + horiz - h).to(u.hourangle).value
    return lowest_alpha, highest_alpha


def broker_uploadstring(observatories):
    "OBSOLETE: Manual upload of targets in case json upload fails"
    obs_uploadstring = []
    for obs in observatories:
        t_strings = [
            "{} {:e}".format(atarget["Name"], atarget["Likelihood"])
            for atarget in obs["targets"]
        ]
        obs_uploadstring.append(obs["name"] + ": " + ", ".join(t_strings))
    uploadstring = "; ".join(obs_uploadstring)
    return uploadstring


def broker_json(info, observatories):
    "Generate JSON file to upload targets and GCN Notice information"
    import json

    setype = "S"
    if info.get("role") == "test":
        setype = "T"
    elif info.get("role") == "drill":
        setype = "D"
    data = {
        "alert": {
            "ligo_run": config.get_config_for_key("LIGO Run"),
            "graceid": info.get("graceid"),
            "SEtype": setype,
            "datetime": info.get("datetime"),
        },
        "gcnnotice": {
            "gcntype": info.get("alerttype"),
            "gcnserial": info.get("pkt_ser_num"),
            "datetime": info.get("gcndatetime"),
        },
    }
    if observatories:
        asgndata = {}
        for anobs in observatories:
            odata = {}
            oname = anobs["name"]
            otarg = anobs["targets"]
            for tname, tprob in zip(otarg["Name"], otarg["Likelihood"]):
                odata[tname] = float(tprob)
            asgndata[oname] = odata
        data["assignments"] = asgndata
    return json.dumps(data, indent=2)


def generate_targets(skymap, detection_time=None):
    """Generate targets of observation visible at detection_time for each
    observatory in the configuration file"""
    observatories = config.get_config_for_key("Observatories")
    catalog_path = config.get_config_for_key("Catalog Path")
    catfilters = config.get_config_for_key("Catalog Filters")
    timeofthenow = detection_time or Time.now()

    glade_table = ascii.read(catalog_path, format="csv", guess=False)
    import healpy as hp
    from scipy.stats import norm

    contains_dist_estimation = True
    try:
        aligo_banana, distmu, distsigma, distnorm = hp.read_map(
            skymap, verbose=False, field=range(4)
        )
    except:
        aligo_banana = hp.read_map(skymap, verbose=False)
        contains_dist_estimation = False

    npix = len(aligo_banana)
    nside = hp.npix2nside(npix)

    for obs in observatories:
        if obs["location"].lat > 0:  # northern hemisphere
            lim_dec = glade_table["Dec"] * u.deg > (
                -90 * u.degree + obs["location"].lat
            )
        else:  # southern hemisphere
            lim_dec = glade_table["Dec"] * u.deg < abs(
                90 * u.degree - abs(obs["location"].lat)
            )
        glade_visible = glade_table[lim_dec]

        circum = 90.0 * u.degree - abs(glade_visible["Dec"] * u.degree) < abs(
            obs["location"].lat
        )

        alpha_obs_min, alpha_obs_max = alpha_cuts(Time(timeofthenow))

        # Alpha cut
        alfa_min = glade_visible["RA"] > float(alpha_obs_min)
        alfa_max = glade_visible["RA"] <= float(alpha_obs_max)

        if alpha_obs_max > alpha_obs_min:
            sample = glade_visible[((alfa_min & alfa_max) | circum)]
        else:
            sample = glade_visible[((alfa_min | alfa_max) | circum)]

        deg2rad = np.pi / 180.0
        phis = sample["RA"] * deg2rad
        thetas = np.pi / 2.0 - sample["Dec"] * deg2rad
        dists = sample["Dist"]
        ipix = hp.ang2pix(nside, thetas, phis)
        if contains_dist_estimation:
            probs = (
                aligo_banana[ipix]
                * distnorm[ipix]
                * norm(distmu[ipix], distsigma[ipix]).pdf(dists)
                * dists ** 2
            )
        else:
            probs = aligo_banana[ipix]
        sample.add_column(Column(name="Likelihood", data=probs))
        sample.sort("Likelihood")
        sample.reverse()
        obs["targets"] = sample[: catfilters.get("NUM_TARGETS")]
        # obs['targets'].sort('Abs_Mag')
    return observatories


def graphtargets(info, targets, skymap):
    "Generate a graph with the targets generated over the sky map"
    import healpy as hp
    from io import BytesIO

    aligo_banana = hp.read_map(skymap)
    numfig = 1
    fig = plt.figure(numfig, figsize=(10, 5))
    graph_title = "{} -{}-{}\nBayestar Prob. Sky Map with Targets".format(
        info["graceid"], info["pkt_ser_num"], info["alerttype"]
    )
    hp.mollview(
        aligo_banana,
        title=graph_title,
        flip="astro",
        unit="$\Delta$",
        fig=numfig,
        cmap=plt.cm.gist_heat_r,
    )
    fig.axes[1].texts[0].set_fontsize(8)

    for obs in targets:
        ra_pointings = np.array(obs["targets"]["RA"])
        dec_pointings = np.array(obs["targets"]["Dec"])
        hp.projscatter(
            ra_pointings, dec_pointings, lonlat=True, color="green", marker="."
        )
    hp.graticule()

    graphIO = BytesIO()
    plt.savefig(graphIO)
    return graphIO.getvalue()
