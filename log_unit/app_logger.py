import yaml
import logging.config
import os
"""
Load config file by YAML, and config the logging module by logging.dictConfig.
"""


def setup_logging(default_path="../appconfig/logging.yaml", default_level=logging.INFO, env_key="LOG_CFG"):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "r") as f:
            config = yaml.load(f)
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


def func():
    import subModule
    logging.info("start func")
    a = subModule.SubModuleClass()
    logging.info("exec func")
    a.doSomething()
    logging.info("end func")
    subModule.som_function()


if __name__ == "__main__":
    setup_logging(default_path="../appconfig/logging.yaml")
    func()