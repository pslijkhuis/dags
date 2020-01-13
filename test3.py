"""
This is an example dag for using the KubernetesPodOperator.
"""
from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin

log = LoggingMixin().log

try:
    # Kubernetes is optional, so not available in vanilla Airflow
    # pip install 'apache-airflow[kubernetes]'
    from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator

    default_args = {"owner": "airflow", "start_date": days_ago(2)}

    with DAG(
        dag_id="example_kubernetes_operator",
        default_args=default_args,
        schedule_interval=None,
    ) as dag:

        tolerations = [{"key": "key", "operator": "Equal", "value": "value"}]

        k = KubernetesPodOperator(
            namespace="default",
            image="ubuntu:16.04",
            cmds=["bash", "-cx"],
            arguments=["echo", "10"],
            labels={"foo": "bar"},
            name="airflow-test-pod",
            in_cluster=False,
            task_id="task",
            get_logs=True,
            is_delete_operator_pod=False,
            tolerations=tolerations,
        )

except ImportError as e:
    log.warning("Could not import KubernetesPodOperator: " + str(e))
    log.warning(
        "Install kubernetes dependencies with: "
        "    pip install 'apache-airflow[kubernetes]'"
    )
