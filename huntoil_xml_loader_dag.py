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
    'huntoil_xml',
    default_args=default_args,
    description='Datavedik Data Pipeline',
    schedule_interval='@yearly',
    start_date=datetime(2017, 3, 20), catchup=False,
)

# t1, t2 and t3 are examples of tasks created by instantiating operators

t1 = BashOperator(
    task_id='csv_loader',
    bash_command="  export SQLCONFIGFILE=/home/kevinpeng/.config/config.ini  && \
                    cd /media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/Packaging/New_WITSML_Loader/  && \
                    ./bin/witsml_loader \
                    -c UBUNTU  \
                    -s '/media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/Packaging/New_WITSML_Loader/new_witsml_loader/sample_data/csv_huntoil.csv' \
                    -d csv \
                   ",

    dag=dag,
)

t2 = BashOperator(
    task_id='xml_loader',
    bash_command="  export SQLCONFIGFILE=/home/kevinpeng/.config/config.ini  && \
                    cd /media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/Packaging/New_WITSML_Loader/new_witsml_loader && \
                    ./witsml_loader.py \
                    -c UBUNTU  \
                    -d xml -t well\
                    -f '/media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/Packaging/New_WITSML_Loader/new_witsml_loader/sample_data/' \
                    -m '/media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/Packaging/New_WITSML_Loader/new_witsml_loader/mapping/WITSML_PPDM_Mappings.xlsx' \
                   ",

    dag=dag,
)
# t1 = BashOperator(
#     task_id='csv_loader',
#     bash_command="cd :/media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/Packaging/New_WITSML_Loader/new_witsml_loader && \
#                     ./witsml_loader.py \
#                     -c UBUNTU  \
#                     -s '/media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/Packaging/New_WITSML_Loader/new_witsml_loader/sample_data/csv_huntoil.csv' \
#                     -d csv \
#                     -f '/media/kevinpeng/cdrive/Users/kevin.peng/code/HuntOil/Packaging/New_WITSML_Loader/new_witsml_loader/sample_data/' \
#                    ",
#
#     dag=dag,
# )
# def print_hello():
#     return 'Hello world!'

# dummy_operator = DummyOperator(task_id='dummy_task', retries=1, dag=dag)

# hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello, dag=dag)
t1 >> t2
