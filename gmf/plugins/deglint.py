from gmf.tools.logger import setup_logger
import numpy as np
from gmf.internal import InternalModule

log = setup_logger()

class DeglintProcess(InternalModule):

    def __init__(self, tag=None, **options):
        
        # Initialize the parent class to handle the tag and options
        super().__init__(tag=tag, **options)

        # Define the outputs as attributes
        self.arr = None

    def run(self, arr, **options):

        log.info(f"     Running Deglint Process on {str(type(arr).__name__)}")
        
        new_arr = np.clip(arr, 0.0, 0.6)
        
        self.arr = new_arr