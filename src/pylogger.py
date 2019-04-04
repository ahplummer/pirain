import logging, os

log = logging.getLogger()
def projectLogger():
    loglevel = logging.INFO
    ch = logging.StreamHandler()
    if 'PY_LOGLEVEL' in os.environ:
        loglevel = os.environ['PY_LOGLEVEL']
    try:
        log.setLevel(loglevel)
        ch.setLevel(loglevel)
    except:
        log.setLevel(logging.INFO)
        ch.setLevel(logging.INFO)

    logging.basicConfig(
        format='[%(asctime)s] %(levelname)s {%(filename)s:%(lineno)d} - %(message)s',
    )

    return log