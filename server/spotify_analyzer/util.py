"""_summary_
"""
import logging

def log_error(logger: logging.Logger, entity: str, identifier: str):
    """_summary_

    Args:
        logger (logging.Logger): _description_
        entity (str): _description_
        identifier (str): _description_
    """
    logger.warning(
        "%s", entity, "record doesn't exist. Check for race conditions or re-validate")
    logger.warning("%s", entity, "identified by %s",
                   identifier, " does not exist in db.")
def log_error_dependency(logger: logging.Logger, caller: str, entity:str):
    """_summary_

    Args:
        logger (logging.Logger): _description_
        caller (str): _description_
        entity (str): _description_
    """
    logger.warning("%s",caller," tried to get an instance from %s",entity," but it did not exist")