
# Core Package
from gmf.workflow import Workflow
from gmf.tools.logger import setup_logger


# Addon Modules (To be seperated from this repo, but serves as a demonstration)
from gmf.plugins.sentinel import Sentinel2ProductReader
from gmf.plugins.deglint import DeglintProcess
from gmf.plugins.bathymetry import BathymetryProcess
from gmf.plugins.export import ExportProcess


# Set the seed to make the outputs repeatable
import numpy as np
np.random.seed(0)


# Setup a new workflow
wf = Workflow()


# Add the Sentinel Reader module
wf.add(Sentinel2ProductReader , tag='sentinelReader')

# Add the Deglinting module
wf.add(DeglintProcess   , tag='deglintProcess', arr='sentinelReader:arr')

# Add the Bathymetry module
wf.add(BathymetryProcess, tag='bathyProcess'  , arr='deglintProcess:arr')

# Add the Exporting module
wf.add(ExportProcess    , tag='exportBathy'    , arr='bathyProcess:arr')

# Compile the workflow by ensuring all modules are successfully linked, and all required user parameters are known
wf.compile()

# Runtime parameters ( Dict or JSON or Config File )
runtime_params = {
    'sentinelReader' : {'path' : 'fake/path/to/sentinel2.SAFE'},
    'exportBathy'    : {'path' : 'output/raw.tif'}
}

# Execute the workflow
wf.execute(**runtime_params)