########################################################################
# Python-modules:
########################################################################
import numpy as np
import os
from datetime import datetime, timedelta
import netCDF4
########################################################################
# METROMS-modules:
########################################################################
import Constants
from GlobalParams import *
from Params import *
from ModelRun import *
########################################################################
########################################################################
# Set cpus for ROMS:
xcpu=8 #32
ycpu=8 #18
# Choose a predefined ROMS-application:
app='fjordos_dramsfjord'

# Find start- and enddate:
start_date  = datetime(2015,1,1,12)
end_date    = datetime(2015,12,31,12)
print start_date, end_date

params=Params(app,xcpu,ycpu,start_date,end_date,nrrec=-1,restart=False)

modelrun=ModelRun(params)

#
#modelrun.preprocess()
modelrun.run_roms(Constants.MPI,Constants.NODEBUG,Constants.NEBULA)
#modelrun.run_roms(Constants.DRY,Constants.NODEBUG,Constants.VILJE)


