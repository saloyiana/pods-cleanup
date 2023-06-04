import kubernetes.client, logging
from kubernetes import client, config
from kubernetes.client.rest import ApiException

def main(): 
    config.load_incluster_config()

    v1 = kubernetes.client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False)

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    def delete_failed_pod(name, namespace):
        v1.delete_namespaced_pod(name, namespace)
        logging.info("The failed pod {} in {} has been deleted".format(name, namespace))

    for pod in pods.items:
        name = pod.metadata.name
        namespace = pod.metadata.namespace
        status = pod.status.phase
        if status == "Failed":
            try:
                delete_failed_pod(name, namespace)
            except ApiException as error:
                if error.status == 404:
                    continue
                else:
                    logging.info("Exception when calling CoreV1Api->delete_namespaced_pod: {}".format(error))

if __name__ == '__main__':
    main()