#PBS -N fjordos
#PBS -A mifa02hi
#PBS -l walltime=240:00:00
#PBS -l select=45:ncpus=32:mpiprocs=16:ompthreads=16:mem=27gb
##PBS -l select=1:ncpus=32:mpiprocs=10:ompthreads=16:mem=25gb
#PBS -j oe
#PBS -o /work/nilsmk/tmproms/run/fjordos_cl1/o.log
#PBS -r n
###PBS -V
set -x
#
source /home/metno/nilsmk/metroms/apps/myenv.bash vilje
# Load modules needed
source /etc/profile.d/modules.sh
source ${METROMS_BASEDIR}/apps/modules.sh
datstamp=`date +%Y_%m_%d_%H_%M`
exec 1>${METROMS_TMPDIR}/fjordos_cl1/run.log_${datstamp} 2>&1
module list
#
cd ${METROMS_APPDIR}/fjordos_cl1
export MPI_BUFS_PER_PROC=256
export MPI_BUFS_PER_HOST=1024
python my_fjordos.py
#
set +x
exit
