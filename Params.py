from GlobalParams import *
from Constants import *
from Utils import *
import sys
from datetime import datetime, timedelta
import netCDF4

class Params(object):
    RUNPATH=None
    KEYWORDFILE=None
    ROMSINFILE=None
    FELT_CLMFILE=None
    KEYWORDLIST=None
    XCPU=None
    YCPU=None
    TSTEPS=None
    NRREC=None
    
    def __init__(self,app,xcpu,ycpu,start_date,end_date,nrrec=-1,cicecpu=0,restart=False):
        self.KEYWORDFILE=GlobalParams.METROMSAPPDIR+"/"+app+"/origfiles/roms_keyword.in_roms-trunk"
        self.XCPU=xcpu
        self.YCPU=ycpu
        self.CICECPU=cicecpu
        self.START_DATE=start_date
        self.END_DATE=end_date
        self.FCLEN=(self.END_DATE-self.START_DATE).total_seconds()
        self.NRREC=nrrec
        self.TIMEREF=datetime(1970,01,01,00)
        self.RESTART=restart
        if app=='fjordos_dramsfjord':
            ########################################################################
            # Name of roms.in keyword-file:
            ########################################################################
            self.RUNPATH=GlobalParams.RUNDIR+"/"+app
#            self.ATMFILE=self.RUNPATH+"/ocean_force.nc"
            self.ATMFILE=""
            self.ROMSINFILE=self.RUNPATH+"/roms.in"
            self.CICERUNDIR=self.RUNPATH+'/cice/rundir'
            self.CICEINFILE=self.RUNPATH + "/ice_in"
            self.CICEKEYWORDFILE=self.CICERUNDIR + "/ice_in"
            self.DELTAT=5
            self.CICEDELTAT=600
            self.COUPLINGTIME_I2O=600
            # Find restart-time of CICE:
            if self.CICECPU > 0:
                cice_start_step = (start_date-datetime(start_date.year,01,01,00)).total_seconds()/self.CICEDELTAT
                if restart == True:
                    f = open(self.CICERUNDIR+'/restart/ice.restart_file', 'r')
                    cice_restartfile = f.readline().strip()
                    cice_rst_time = netCDF4.Dataset(cice_restartfile).istep1
                    cicerst_truefalse = ".true."
                else:
                    cice_rst_time = cice_start_step
                    cicerst_truefalse = ".false."
            ########################################################################
            # List of keywords:
            ########################################################################
            self.KEYWORDLIST=[
            ['APPTITLE',"NorKyst-800m - ROMS"],
            ['MYAPPCPPNAME',"FJORDOS"],
            ['VARFILE',GlobalParams.METROMSAPPDIR+"/"+app+"/include/varinfo.dat"],
            ['XPOINTS',"114"],  #Could read from grd-file?
            ['YPOINTS',"174"],  #Could read from grd-file?
            ['NLEVELS',"42"],  #Could read from grd-file?
            ['GRDTHETAS',"3.0d0"],
            ['GRDTHETAB',"0.5d0"],
            ['GRDTCLINE',"15.0d0"],            
            ['_TNU2_',"2*0.0d0"],
            ['_TNU4_',"2*0.5d5"],
            ['_VISC2_',"10.0d0"],
            ['_VISC4_',"0.5d5"],
            ['XCPU',str(self.XCPU)],
            ['YCPU',str(self.YCPU)],
            ['TSTEPS',str(self.FCLEN/self.DELTAT)],
            ['DELTAT',str(self.DELTAT)],
            ['RATIO',"10"],
            ['IRESTART',str(self.NRREC)],
            ['RSTSTEP',str(5*24*3600/int(self.DELTAT))],
            ['STASTEP',str(1*3600/int(self.DELTAT))],
            ['INFOSTEP',str(1*3600/int(self.DELTAT))],
            #['INFOSTEP',str(1)],
            ['HISSTEPP',str(1*60*60/int(self.DELTAT))],
            ['DEFHISSTEP',str(30*24*3600/int(self.DELTAT))],
            ['AVGSTEPP',str(24*3600/int(self.DELTAT))],
            ['STARTAVG',"0"],
            ['DEFAVGSTEP',str(30*24*3600/int(self.DELTAT))],  #if 0; all output in one avg-file
            ['STARTTIME',str((self.START_DATE-self.TIMEREF).total_seconds()/86400)],
            ['TIDEREF',"0.0"],
            ['TIMEREF',self.TIMEREF.strftime("%Y%m%d.00")],
            ['V_TRANS',"2"],
            ['V_STRETCH',"4"],
            ['_TNUDG_',"5.0d0 5.0d0"],
            ['OBCFAKTOR',"1.0"],
            ['NUDGZONEWIDTH',"15"],
            ['GRDFILE',GlobalParams.METROMSAPPDIR+"/"+app+"/grid/FjordOs_grd_v9_dramsfjord.nc"],
            ['RUNDIR',self.RUNPATH],
            ['_CLMNAME_',self.RUNPATH+"/ocean_clm.nc"],
            ['_BRYNAME_',self.RUNPATH+'/ocean_bry.nc'],
            ['_NUDNAME_',self.RUNPATH+'/ocean_nud_dramsfjord.nc'],
            ['TIDEDIR',GlobalParams.METROMSAPPDIR+"/"+app+"/tide/FjordOs_tide_CL_v3_dramsfjord.nc"],
            ['ATMDIR',self.RUNPATH+"/fjordos_atmos.nc"],
            ['RIVERFILE',GlobalParams.METROMSAPPDIR+"/"+app+"/rivers/FjordOs_river_2013_2017_2018avg_dramsfjord_42.nc"],
            ['FORCEFILES',"2"], 
            ['COUPLINGTIMEI2O',str(self.COUPLINGTIME_I2O)],
            ['ROMSINFILE', self.ROMSINFILE ],
            ['CICEINFILE', self.CICEINFILE ],
            ['_SPOSNAM_',GlobalParams.METROMSAPPDIR+"/"+app+"/stations.in"],
            ['NUMROMSCORES',str(int(self.XCPU)*int(self.YCPU))],
            ['NUMCICECORES',str(int(self.CICECPU))]
            ]
            ########################################################################
            # List of CICE keywords:
            ########################################################################
            if self.CICECPU > 0:
                self.CICEKEYWORDLIST=[
                    ['CICEYEARSTART',start_date.strftime("%Y")],
                    ['CICESTARTSTEP',str(int(cice_start_step))],  #number of hours after 00:00 Jan 1st
                    ['CICEDELTAT',str(self.CICEDELTAT)],
                    ['CICENPT',str(int((self.FCLEN/self.CICEDELTAT)-(cice_rst_time - cice_start_step)))],   # minus diff restart og start_date
                    ['CICERUNTYPE',"'continue'"],
                    ['CICEIC',"'default'"],
                    ['CICEREST',".true."],
                    ['CICERSTTIME',cicerst_truefalse],
                    ]
            ########################################################################
        else:
            print 'Unknown application, will exit now'
            sys.exit()


    def change_run_param(self,keyword,value):
        for keyvalue in self.KEYWORDLIST:
            if keyvalue[0]==keyword:
                keyvalue[1]=str(value)
