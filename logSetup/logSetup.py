import logging

# # write logs to console
def consoleLogger(log_level=logging.DEBUG):
    # create logger
    logger = logging.getLogger(consoleLogger.__name__)
    logger.setLevel(logging.DEBUG)

    # Create console handler and set level to info
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s %(levelname)s: %(message)s',datefmt='%I:%M:%S %p')

    # Add formatter to conlsole handler
    console_handler.setFormatter(formatter)

    # add console handler to logger
    logger.addHandler(console_handler)

    return logger