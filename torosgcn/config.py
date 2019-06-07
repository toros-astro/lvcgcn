# -*- coding: utf-8 -*-
from astropy.coordinates import EarthLocation
from astropy import units as u
import yaml as _yaml

CONFIG_PATH = '/etc/toros/lvcgcn-conf.yaml'
_CONFIG_IS_LOADED = False
_config = {}

obs = None

def load_config():
    global _config
    with open(CONFIG_PATH) as f:
        iread = f.read()
        _config = _yaml.full_load(iread)

def get_config():
    global _CONFIG_IS_LOADED
    global _config
    if not _CONFIG_IS_LOADED:
        load_config()
        _CONFIG_IS_LOADED = True
    return _config

def get_config_for_key(key):
    config = get_config()
    cval = config.get(key)
    if key == 'Observatories' and config.get('obs_fixed') is None:
        for obs in cval:
            obs['location'] = EarthLocation.from_geodetic(**obs['location'])
        config['obs_fixed'] = True
    return cval

def init_logger():
    from loguru import logger
    logger.remove()
    log_config = get_config_for_key('Logging') or {}
    log_file = log_config.get('File')
    if log_file is not None:
        log_level = log_config.get('Log Level') or 'INFO'
        logger.add(log_file,
                   format="{time} {level} {name}: {message}",
                   level=log_level,
                   rotation="1 day",
                   retention=20,
                   backtrace=True,
                   )
    logger.info("LVC-GCN service started.")
    logger.info("Logger level set to {}".format(log_level))

    # Intercept stdlib logging and redirect to loguru
    import logging
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            logger_opt = logger.opt(depth=6, exception=record.exc_info)
            logger_opt.log(record.levelno, record.getMessage())
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.NOTSET)

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
catalog_path = os.path.join(BASE_DIR, 'aux_files', 'GWGCCatalog.txt')
