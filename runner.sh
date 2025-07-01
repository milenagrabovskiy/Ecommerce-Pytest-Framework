
set -x
#set -e


location=$1
options=$2


timestamp=`date "+%Y%m%d%H%M%S"`
output_dir=$(pwd)/output/${timestamp}
log_file=${output_dir}/pytest_log.log
html_report=${output_dir}/report.html
export RESULTS_DIR=${output_dir}
export RESULTS_DIR=${RESULTS_DIR}
export DATA_DIRECTORY=$(pwd)/ssqatest/src/data

#. variables_local.sh

python3 -m pytest \
${location} \
--log-file=${log_file} \
--log-file-level=info \
--log-level=info \
--log-cli-level=info \
--log-level=info \
--html=${html_report} \
--junitxml=$RESULTS_DIR/myjunit.xml \
-o junit_suite_name=$JUNIT_SUITE_NAME \
${options}



echo  "Log File = ${log_file}"
echo  "HTML Report = ${html_report}"

