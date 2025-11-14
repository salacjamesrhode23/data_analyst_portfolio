# Starting a spark master
$SPARK_HOME/sbin/start-master.sh

# Start one or more workers
$SPARK_HOME/sbin/start-worker.sh spark://vm-instance-nyc-taxi.asia-southeast1-a.c.de-project-nyc-taxi.internal:7077

# Run custom API
python $ecomm/faker_generator/create_custom_api.py