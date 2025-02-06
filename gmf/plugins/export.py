from gmf.tools.logger import setup_logger
from gmf.internal import InternalModule
import numpy as np
from pathlib import Path
import rioxarray as rio

log = setup_logger()


class ExportProcess(InternalModule):

    def __init__(self, tag=None, **options):
        
        # Initialize the parent class to handle the tag and options
        super().__init__(tag=tag, **options)


    def run(self, arr, **options):

        log.info(f"     Running Export Process on {str(type(arr).__name__)}")
        
        if "bands" in options:
            arr = arr.sel(band=options['bands'])
        
        dest = Path(options['path'])
        dest.parents[0].mkdir(parents=True, exist_ok=True) 
        arr.rio.to_raster(str(dest))