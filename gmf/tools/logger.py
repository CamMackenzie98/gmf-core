import logging 

def setup_logger(logger_name="gmf-main", level=logging.DEBUG, log_file=None, to_console=True):
    """
    Setup and configure a logger with the given parameters.

    Parameters:
    - logger_name (str): Name of the logger.
    - level (int): Logging level (default: NOTSET).
    - log_file (str or None): Path to a log file (default: None, logs to console).
    - log_to_console (bool): Whether to log to the console (default: True).
    
    Returns:
    - logger (logging.Logger): Configured logger instance.
    """
    # Create or get the logger
    logger = logging.getLogger(logger_name)

    # Check if the logger is already configured to avoid duplicate handlers
    if not logger.handlers:
        # Set the logger's level
        logger.setLevel(level)

        # Create a formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # If log_to_console is True, create a console handler
        if to_console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # If a log file is provided, create a file handler
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger