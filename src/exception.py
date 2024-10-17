import sys
import os
from dotenv import load_dotenv
load_dotenv()
project_home_path = os.environ.get('PROJECT_HOME_PATH')
sys.path.append(project_home_path)
from src.logger import logging

def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
     file_name,exc_tb.tb_lineno,str(error))

    return error_message

    

import sys
import logging

class CustomException(Exception):
    def __init__(self, message, error_detail):
        super().__init__(message)
        self.error_detail = error_detail
        logging.error(f"CustomException: {message}")
        logging.error(f"Error Detail: {error_detail}")