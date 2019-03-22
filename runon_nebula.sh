#!/bin/sh
#
#SBATCH --job-name=dramsfjord
#SBATCH --time=48:00:00
####SBATCH --ntasks-per-node=10
#SBATCH --mem=30G
#SBATCH --nodes=2
#SBATCH -o /nobackup/forsk/sm_nilkr/metroms_run/fjordos_dramsfjord/tmp/o.log
#SBATCH -e /nobackup/forsk/sm_nilkr/metroms_run/fjordos_dramsfjord/tmp/e.log
#SBATCH --exclusive
set -x
app=fjordos_dramsfjord
source $HOME/metroms/apps/myenv.bash nebula
datstamp=`date +%Y_%m_%d_%H_%M`
exec 1>${METROMS_TMPDIR}/${app}/run.log_${datstamp} 2>&1
ln -sf ${METROMS_TMPDIR}/${app}/run.log_${datstamp} ${METROMS_TMPDIR}/${app}/run.log
# Load modules needed
source ${METROMS_BASEDIR}/apps/modules.sh
module list
#
cd ${METROMS_APPDIR}/${app}
source activate nils_nebula
python my_fjordos.py
source deactivate
#
#
set +x
exit
