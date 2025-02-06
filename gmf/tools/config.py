import os
import configparser

def read_config(filepath=None):
    """
    Reads a configuration file and returns its content as a dictionary.
    Defaults to searching for `config.ini` in the current working directory.
    
    Parameters:
        filepath (str, optional): The path to the configuration file. Defaults to None.
    
    Returns:
        dict: A dictionary containing the configuration data.
    
    Raises:
        FileNotFoundError: If the configuration file is not found.
    """
    if filepath is None:
        # Default to 'config.ini' in the current directory
        filepath = os.path.join(os.getcwd(), "config.ini")
    
    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"Configuration file not found: {filepath}")
    
    config = configparser.ConfigParser()
    config.read(filepath)
    
    # Convert the configparser object to a dictionary
    config_dict = {section: dict(config.items(section)) for section in config.sections()}
    return config_dict