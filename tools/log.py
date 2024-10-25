import logging
from pathlib import Path
import datetime


def init_logger(logger_obj:logging.Logger, level = logging.DEBUG, level_file = logging.DEBUG, consol_level = logging.INFO):

    logger_obj.setLevel(level)

    now = datetime.datetime.now()
    time_string = now.strftime("%Y%m%d%H%M%S")
    logfile = Path(f'./logs/{time_string}.log')  
    logfile.parent.mkdir(exist_ok=True, parents=True)
    fh = logging.FileHandler(logfile, mode='a')  
    fh.setLevel(level_file)  


    ch = logging.StreamHandler()
    ch.setLevel(consol_level)  

  
    formatter = logging.Formatter('[%(asctime)s - %(filename)s, line:%(lineno)d] - %(levelname)s: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)


    logger_obj.addHandler(fh)
    logger_obj.addHandler(ch)
    
logger = logging.getLogger('UICoder')
init_logger(logger)


