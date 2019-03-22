#!/bin/sh
#
#SBATCH --job-name=fjordos
#SBATCH --time=72:00:00
#SBATCH --ntasks-per-node=16
#SBATCH --mem=30G
#SBATCH --nodes=24
#SBATCH -o /nobackup/forsk/sm_nilkr/metroms_run/fjordos_cl1/tmp/o.log
#SBATCH -e /nobackup/forsk/sm_nilkr/metroms_run/fjordos_cl1/tmp/e.log
#SBATCH --exclusive
set -x
source $HOME/metroms/apps/myenv.bash elvis
# Load modules needed
source ${METROMS_BASEDIR}/apps/modules.sh
module list
datstamp=`date +%Y_%m_%d_%H_%M`
exec 1>${METROMS_TMPDIR}/fjordos_cl1/run.log_${datstamp} 2>&1
ln -sf ${METROMS_TMPDIR}/fjordos_cl1/run.log_${datstamp} ${METROMS_TMPDIR}/fjordos_cl1/run.log
#
#
cd ${METROMS_APPDIR}/fjordos_cl1
python my_fjordos.py
#
#
set +x
exit
