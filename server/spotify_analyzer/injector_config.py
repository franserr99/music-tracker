from injector import inject, Module, provider, singleton
import logging

class Config(Module):
    @singleton
    @provider
    def provide_logger(self) -> logging.Logger:
        logger = logging.getLogger('spotify_analyzer')
        logger.setLevel(logging.INFO)
        return logger
