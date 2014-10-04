import logging

# Create logger
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
# Create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# Create formatter
formatter = logging.Formatter('%(levelname)s: %(message)s')
# Add formatter to console handler
ch.setFormatter(formatter)
# Add console handler to logger
log.addHandler(ch)
