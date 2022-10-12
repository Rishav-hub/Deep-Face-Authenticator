import os
import sys
from datetime import datetime

import yaml
from dateutil.parser import parse
from dotenv import dotenv_values

from face_auth.exception import AppException


class CommonUtils:
    def read_yaml_file(self, file_path: str) -> dict:
        """
        Reads a YAML file and returns the contents as a dictionary.
        file_path: str
        """
        try:
            with open(file_path, "rb") as yaml_file:
                return yaml.safe_load(yaml_file)
        except Exception as e:
            raise AppException(e, sys) from e

    def get_time(self):
        """
        :return current time:
        """
        return datetime.now().strftime("%H:%M:%S").__str__()

    def get_date(self):
        """
        :return current date:
        """
        return datetime.now().date().__str__()

    def get_difference_in_second(self, future_date_time: str, past_date_time: str):
        """
        :param future_date_time:
        :param past_date_time:
        :return difference in second:
        """
        future_date = parse(future_date_time)
        past_date = parse(past_date_time)
        difference = future_date - past_date
        total_seconds = difference.total_seconds()
        return total_seconds

    def get_difference_in_milisecond(self, future_date_time: str, past_date_time: str):
        """
        :param future_date_time:
        :param past_date_time:
        :return difference in milisecond:
        """
        total_seconds = self.get_difference_in_second(future_date_time, past_date_time)
        total_milisecond = total_seconds * 1000
        return total_milisecond

    def get_environment_variable(self, variable_name: str):
        """
        :param variable_name:
        :return environment variable:
        """
        if os.environ.get(variable_name) is None:
            enironment_variable = dotenv_values(".env")
            return enironment_variable[variable_name]
        else:
            return os.environ.get(variable_name)
