from kubernetes import client, config
import time
def create_deployment_object():
    container = client.V1Container(
        name="app-local",
        image="khalifaserraye/app-local",
    )

    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"app": "app-local"}),
        spec=client.V1PodSpec(containers=[container]),
    )

    spec = client.V1DeploymentSpec(replicas=3, template=template, selector={"matchLabels":{"app": "app-local"}})

    deployment = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name='app-local'),
        spec=spec,
    )
    return deployment


def create_deployment(api, deployment):
    api.create_namespaced_deployment(body=deployment, namespace="default")


def update_deployment(api, deployment_index, replicas):
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    deployment_body = client.V1Deployment(
        api_version="apps/v1",
        kind="Deployment",
        metadata=client.V1ObjectMeta(name=apps_v1.list_deployment_for_all_namespaces().items[deployment_index].metadata.name),
        spec=apps_v1.list_deployment_for_all_namespaces().items[deployment_index].spec
    )
    deployment_body.spec.replicas = replicas
    api.patch_namespaced_deployment(
        name=apps_v1.list_deployment_for_all_namespaces().items[deployment_index].metadata.name, namespace="default", body=deployment_body
    )



def main():
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    #print(apps_v1.list_deployment_for_all_namespaces().items[0].metadata.name)
   # dep = create_deployment_object()
    #create_deployment(apps_v1, dep)
    index = 0

    while True:
        print("Scalling up:")
        for i in  [2, 3, 4]:
            update_deployment(apps_v1, index,i)
            print("replicas number = ", i)
            time.sleep(10.0)
        time.sleep(1.0)
        print("Scalling down:")
        for i in  [3, 2, 1]:
            update_deployment(apps_v1, index,i)
            print("replicas number = ", i)
            time.sleep(10.0)
        time.sleep(1.0)
        
            

if __name__ == "__main__":
    main()
