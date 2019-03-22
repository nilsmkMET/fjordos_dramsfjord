#module load nco netcdf
module load netCDF/4.3.2-HDF5-1.8.12-nsc1-intel-2018.u1-bare
module load buildenv-intel/2018.u1-bare
module load NCO/4.6.3-nsc1 

ncrename -O -d ocean_time,clim_time ocean_ini.nc ocean_clm.nc
#ncrename -O -v ocean_time,clim_time ocean_clm.nc ocean_clm.nc

for var in zeta ubar vbar u v salt temp; do 
   ncatted -h -O -a time,${var},c,c,"clim_time" ocean_clm.nc
done

~/models/romstools/bry_from_clim_noice << EOF
ocean_clm.nc
ocean_bry.nc
EOF
