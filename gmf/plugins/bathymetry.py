from gmf.tools.logger import setup_logger
from gmf.internal import InternalModule

import numpy as np
import xarray as xr

log = setup_logger()

class BathymetryProcess(InternalModule):

    def __init__(self, tag=None, **options):
        
        # Initialize the parent class to handle the tag and options
        super().__init__(tag=tag, **options)

        # Define the outputs as attributes
        self.arr = None
    
    def run(self, arr, **options):

        if arr is None:
            raise ValueError("A valid xarray.DataArray must be provided.")

        log.info(f"Running Bathymetry Process on {str(type(arr).__name__)}")

        band1 = arr.sel(band=['Band_1']).values

        normalized_arr = ((band1 - band1.min()) / (band1.max() - band1.min())) * 20
        # Create a new DataArray for the normalized values with the same coordinates as 'arr'
        normalized_da = xr.DataArray(normalized_arr, coords={'band': ['Z'], 'x': arr.coords['x'], 'y': arr.coords['y']}, dims=['band', 'y', 'x'])

        # Add the normalized array as a new band 'Z' to the original arr
        self.arr = xr.concat([arr, normalized_da], dim='band')