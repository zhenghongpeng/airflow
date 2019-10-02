# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
### Tutorial Documentation
Documentation that goes along with the Airflow tutorial located
[here](https://airflow.apache.org/tutorial.html)
"""
from datetime import timedelta
from datetime import datetime
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator

# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(2),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'trigger_rule': u'all_success'
}

dag = DAG(
    'huntoil',
    default_args=default_args,
    description='Datavedik Data Pipeline',
    schedule_interval='@yearly',
    start_date=datetime(2017, 3, 20), catchup=False,
)

# t1, t2 and t3 are examples of tasks created by instantiating operators
t1 = BashOperator(
    task_id='one_sec_log_para',
    bash_command="/media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/DataConditioning/TIMELOG_RIG-ACTIVITY_KPI/oneseclog/bin/oneseclog   \
                     -i  /media/kevinpeng/cdrive/Users/kevin.peng/code/Depthshift_Depthjump_corrected/newdata/input     \
                     -b /media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/DataConditioning/TIMELOG_RIG-ACTIVITY_KPI/oneseclog/data/bha_master.csv \
                     -o /media/kevinpeng/cdrive/Users/kevin.peng/code/Depthshift_Depthjump_corrected/newdata/result/",
    dag=dag,
)

t2 = BashOperator(
    task_id='depth_log',
    bash_command="cd /media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/DataConditioning/TIMELOG_RIG-ACTIVITY_KPI/depthlog/ && \
                    ./bin/depthlog   \
                     -i /media/kevinpeng/cdrive/Users/kevin.peng/code/Depthshift_Depthjump_corrected/newdata/result/results/time_log/ \
                     -o  /media/kevinpeng/cdrive/Users/kevin.peng/code/Depthshift_Depthjump_corrected/newdata/parquet \
                     -b /media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/DataConditioning/TIMELOG_RIG-ACTIVITY_KPI/depthlog/data/",
    dag=dag,
)

t3 = BashOperator(
    task_id='analytics_ml',
    bash_command="/media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/DataConditioning/TIMELOG_RIG-ACTIVITY_KPI/analyticsml/bin/analyticsml   \
                     -i /home/kevinpeng/workdir/Depthshift_Depthjump_corrected/newdata/parquet/parquet \
                     -o /home/kevinpeng/workdir/Depthshift_Depthjump_corrected/newdata/result/",
    dag=dag,
)
def print_hello():
    return 'Hello world!'

# dummy_operator = DummyOperator(task_id='dummy_task', retries=1, dag=dag)

# hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)

# dummy_operator >> hello_operator >> t1 >> t2

t1 >> t2 >> t3