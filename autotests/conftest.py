import logging
import os
import shutil

import allure
import pytest

import api


pytest_plugins = (
    "pytest_customizations.api.plugin")

LOGS_DIR = 'logs'


@pytest.fixture(autouse=True, scope="session")
def logs():
        api.BASE_URL = os.environ.get("BASE_URL", "https://dev.coolrocket.com/test")
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logging.getLogger("urllib3").setLevel(logging.WARNING)

        if not os.path.exists(LOGS_DIR):
            os.makedirs(LOGS_DIR)
        else:
            shutil.rmtree(LOGS_DIR)
            os.makedirs(LOGS_DIR)
        return logger


@pytest.fixture(autouse=True, scope="function")
def setup_method(logs, request):
        file_handler = logging.FileHandler(os.path.join(LOGS_DIR, '{}.log'.format(request.node.name)))
        file_handler.setFormatter(logging.Formatter('%(asctime)s | %(levelname)s | %(message)s', '%H:%M:%S'))
        log_file_handler = file_handler
        logs.addHandler(file_handler)

        def teardown_method(log_file_handler, logger):
                allure.attach.file(log_file_handler.baseFilename, 'logs')
                log_file_handler.close()
                logger.removeHandler(log_file_handler)
        yield
        teardown_method(log_file_handler, logs)
