import logging


def create_logger():

    logging.basicConfig(

        level=logging.INFO,

        format="%(asctime)s | %(levelname)-8s | %(message)s"

    )

    return logging.getLogger("F1ReplayStudio")