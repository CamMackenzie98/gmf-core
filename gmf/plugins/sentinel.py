from gmf.input import InputModule
from gmf.tools.logger import setup_logger


import xarray as xr
import numpy as np
import pandas as pd
import rioxarray as rio

log = setup_logger()

class Sentinel2ProductReader(InputModule):
    
    def __init__(self, tag=None, **options):
        
        # Initialize the parent class to handle the tag and options
        super().__init__(tag=tag, **options)

        # Define the outputs as attributes
        self.arr = None
        self.meta = None


    def run(self, path, **options):
        """ WIP - Simulates reading in a Sentinel 2 SAFE file from disk and exposes 
                  the DataArray at self.arr, as well dumb metadata at self.meta
        """
        log.info(f"     Reading Sentinel 2 product from {path}")        
        x, y, bands = 2500, 2500, 4
        data = np.random.random((bands, x, y))
        x_coords = np.linspace(-180, 180, x)  # Longitude range
        y_coords = np.linspace(-90, 90, y)    # Latitude range
        band_coords = [f"Band_{i+1}" for i in range(bands)]
        timestamp = pd.Timestamp("2025-01-22")
        data_array = xr.DataArray(data,dims=["band", "y", "x"],coords={"band": band_coords,"x": x_coords,"y": y_coords,"time": timestamp},name="example_data")
        data_array = data_array.rio.write_crs("EPSG:4326")  # Assign WGS 84 (latitude/longitude)
        
        # Expose results (could do a Results class to handle this)
        self.arr  = data_array
        self.meta = {'key' : 'value'}
