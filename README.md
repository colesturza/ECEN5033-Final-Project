# ECEN5033-Final-Project

This project presents the concept of Chaos Engineering, as well as provides a tutorial for the popular open-source tool [Chaos Mesh](https://chaos-mesh.org/).

## Chaos Engineering

Chaos Engineering is the discipline of experimenting on a system in order to build confidence in the system’s capability to withstand turbulent conditions in production. In a nutshell, you break your systems on purpose to find their weaknesses and avoid catastrophic failure in production.

This practice was pioneered by Netflix, with the intention to move from a development model that assumed no breakdowns to a model where breakdowns were considered to be inevitable. Developers would then be motivated to consider built-in resilience to be an obligation in development, rather than simply an option.

Chaos Engineering can be more simply understood as a series of steps:

1. Start by defining a ‘steady state’ as some measurable output of a system that indicates normal behavior.
2. Hypothesize that this steady state will continue in both the control group and the experimental group.
3. Introduce variables that reflect real-world events (servers that crash, hard drives that malfunction, network connections that are severed, etc.).
4. Try to disprove the hypothesis by looking for a difference in the steady-state between the control group and the experimental group.

The harder it is to disrupt the steady-state, the more confidence we have in the behavior of the system.

## Chaos Mesh

Chaos Mesh is an open-source cloud-native Chaos Engineering platform. It offers various types of fault simulation and has an enormous capability to orchestrate fault scenarios.

It can be more easily understood as an aggregation of its three parts:
- Chaos Dashboard: The visualization component of Chaos Mesh.
  - Provides a GUI where users manipulate and observe Chaos experiments.
- Chaos Controller Manager: The core logical component of Chaos Mesh.
  - Primarily responsible for the scheduling and management of Chaos experiments.
- Chaos Daemon: The main executive component.
  - Interferes with network devices, file systems, and kernels (“hacks” into target Pods).

![](resources/chaos_mesh_architecture_diagram.png?raw=true)

It offers three overarching types of fault injection, each of which has sub-types, some of which have various fault types.
- Basic resource faults
  - PodChaos (pod failure, pod kill, container kill)
  - NetworkChaos (partition, net emulation, bandwidth)
  - DNSChaos
  - HTTPChaos (abort, delay, replace, patch)
  - StressChaos
  - TimeChaos
  - KernelChaos
- Platform faults
  - AWSChaos (EC2 stop, EC2 restart, detach volume)
  - GCPChaos (node stop, node reset, disk loss)
- Application faults
  - JVMChaos (specify return value, method delay, throw custom exceptions, out of memory, fill JVM code cache, CPU full load in Java, perform customized Groovy or Java script)

Further details about each fault injection type and sub-type can be found [here](https://chaos-mesh.org/docs/).

Desired fault injections can be applied through Chaos Experiments, defined through YAML configuration files. These files can be created from scratch, or automatically generated upon sufficient input to the Chaos Dashboard. As long as the user has a Kubernetes cluster up and running, this process requires only defining the experiment and applying it (this can be done wholly through the Chaos Dashboard, or can be completed using `kubectl apply` command-line statements).

If the user desires to run multiple experiments, either serially or in parallel, they can make use of Chaos Workflows. These essentially function as a method of pipelining Experiments in order to create a comprehensive experimentation plan.

Both Workflows and Experiments allow user analysis both at the end of execution mid-process (pausing is allowed).

While the many fault types have a plethora of unique configuration options, allowing users to customize their plan as desired, the bar to entry is fairly low, as most types share some fairly basic options.

Users can specify what type of injection is desired, which pods are to be attacked (specific pods, all pods, or a specific percentage or number of available pods), which containers are to be attacked (if applicable), what the desired duration of the experiment is, and how much time should pass between the experiment initialization and start time (a pre-start grace period).

After (or during) the experiment, when users would like to view simple statistics about their experiments, such information can be accessed through the Chaos Dashboard. If more complex statistics are desired, it may be helpful to use third-party monitoring and analysis tools such as [Prometheus](https://prometheus.io/) and [Grafana](https://grafana.com/).

## Tutorial

This tutorial utilizes a Kubernetes cluster running on three vagrant machines. There is a server application that comprises two services: a mongo database, and a backend application with various endpoints. There is also a client application used to simulate traffic to the server application. Grafana can be used to visualize the traffic. Chaos mesh is used to run various experiments and the results are visible on Grafana. 

### Prerequisites
- Vagrant should be installed on your machine. Installation binaries can be found [here](https://www.vagrantup.com/downloads).
- Oracle VirtualBox can be used as a Vagrant provider or make use of similar providers as described in Vagrant's official [documentation](https://www.vagrantup.com/docs/providers).
- Ansible should be installed in your machine. Refer to the [Ansible installation guide](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) for platform-specific installation.

### Setup

#### Step 1:

```bash
$ vagrant up
```

Upon completion of the above step you should be able to login to the master or worker nodes using Vagrant as follows:

``` bash
$ ## Accessing master
$ vagrant ssh machine1

$ ## Accessing nodes
$ vagrant ssh machine2
$ vagrant ssh machine3
```

#### Step 1.1:

ssh into machine1 and run the following commands.

``` bash
$ chmod +x *.sh
$ ./part1.sh  
```

Open `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf` in a vi editor with the following command.

``` bash
$ sudo vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf  
```

Modify line (last line):
```
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
```
to
```
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS --node-ip=192.168.33.10
```

Then run the following command.

``` bash
$ ./part2_master.sh  
```

Note at the end of the output there should be a command that looks like the following.

```bash
kubeadm join 192.168.33.10:6443 --token fmjd4k.35gh8kccpx47mliz \
        --discovery-token-ca-cert-hash sha256:34a59dfa77699192fab12e19d38cb7233f786819192d5fe9b57399ded1c47c26
```
Copy that command.

(Optional) You can validate that the above all worked with the following command. If you see a list of things, that's a good sign.

```bash
$ kubectl get pods --all-namespaces
```

#### Step 1.2:

ssh into machine2 and run the following commands.

``` bash
$ chmod +x *.sh
$ ./part1.sh  
```

Open `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf` in a vi editor with the following command.

``` bash
$ sudo vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf  
```

Modify line (last line):
```
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
```
to
```
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS --node-ip=192.168.33.11
```

Paste the command from step 1.1, but do it as super user (sudo at beginning), and append `--node-name machine2` to the end. Note, you can continue the command on a new line by using \. Example below:

```bash
kubeadm join 192.168.33.10:6443 --token fmjd4k.35gh8kccpx47mliz \
        --discovery-token-ca-cert-hash sha256:34a59dfa77699192fab12e19d38cb7233f786819192d5fe9b57399ded1c47c26 \
        --node-name machine2
```

(Optional) To test that it worked - on machine1 run the below command, and you should see machine1 and machine2.

```bash
$ kubectl get nodes
```

#### Step 1.3:

ssh into machine3 and run the following commands.

``` bash
$ chmod +x *.sh
$ ./part1.sh  
```

Open `/etc/systemd/system/kubelet.service.d/10-kubeadm.conf` in a vi editor with the following command.

``` bash
$ sudo vi /etc/systemd/system/kubelet.service.d/10-kubeadm.conf  
```

Modify line (last line):
```
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS
```
to
```
ExecStart=/usr/bin/kubelet $KUBELET_KUBECONFIG_ARGS $KUBELET_CONFIG_ARGS $KUBELET_KUBEADM_ARGS $KUBELET_EXTRA_ARGS --node-ip=192.168.33.12
```

Paste the command from step 1.1, but do it as super user (sudo at beginning), and append `--node-name machine3` to the end. Note, you can continue the command on a new line by using \. Example below:

```bash
kubeadm join 192.168.33.10:6443 --token fmjd4k.35gh8kccpx47mliz \
        --discovery-token-ca-cert-hash sha256:34a59dfa77699192fab12e19d38cb7233f786819192d5fe9b57399ded1c47c26 \
        --node-name machine3
```

(Optional) To test that it worked - on machine1 run the below command, and you should see machine1 and machine2 and machine3.

```bash
$ kubectl get nodes
```

#### Step 1.4:

ssh into machine1 and install Helm with the following command.

``` bash
$ curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

#### Step 1.5:

Run the following commands to create a monitoring namespace and to install the Kube-Prometheus stack.

```bash
$ kubectl create namespace monitoring
$ helm install prometheus kube-prometheus-stack --namespace monitoring
```

(Optional) Run the following command to check that the above commands worked. 

```bash
$ kubectl --namespace monitoring get pods -l "release=prometheus"
```

You should see something that looks like the following.

```bash
NAME                                                  READY   STATUS    RESTARTS   AGE
prometheus-kube-prometheus-operator-bcdfdbc79-kx5ns   1/1     Running   0          21s
prometheus-prometheus-node-exporter-d2vtk             1/1     Running   0          21s
prometheus-prometheus-node-exporter-hll6n             1/1     Running   0          21s
prometheus-prometheus-node-exporter-jhsqn             1/1     Running   0          21s
```

#### Step 1.6:

Run the following command to install Chaos Mesh.

```bash
$ curl -sSL https://mirrors.chaos-mesh.org/v2.1.0/install.sh | bash
```

(Optional) To check the running status of Chaos Mesh, execute the following command:

```bash
$ kubectl get pods --namespace chaos-testing
```

The expected output is as follows:

```
NAME                                        READY   STATUS    RESTARTS   AGE
chaos-controller-manager-7d86885d5f-69hhr   1/1     Running   0          73s
chaos-controller-manager-7d86885d5f-724d8   1/1     Running   0          73s
chaos-controller-manager-7d86885d5f-cdw59   1/1     Running   0          73s
chaos-daemon-v7wdw                          1/1     Running   0          73s
chaos-daemon-xq4cl                          1/1     Running   0          73s
chaos-dashboard-b8c66f994-9g4wl             1/1     Running   0          73s
```

#### Step 1.7

Validate that the last two steps worked by accessing the Grafana and Chaos Mesh dashboards from a web browser. The login for Grafana is 

- user: admin
- pass: prom-operator

Run the following command and take note of the exposed port number for the chaos dashboard and Grafana (the second port number).

```bash
$ kubectl get service --all-namespaces | grep -i nodeport
```

The URLs are

- Grafana: http://192.168.33.10:[grafana port number]
- Chaos Mesh: http://192.168.33.10:[choas dashboard port number]

#### Step 2

On each machine run the following.

```bash
$ sudo docker run -d -p 5000:5000 --restart=always --name registry registry:2
```

Edit `/etc/docker/daemon.json` by adding `"insecure-registries":["192.168.33.10:5000"]`
inside the `{ }` (you’ll need a comma on the current last entry).

```bash
$ sudo vi /etc/docker/daemon.json
```

Then restart the docker service.

```bash
$ sudo service docker restart
```

#### Step 3

Now we need to start the mongo database. Change directories to the `src/` directory and run the following command.

```bash
$ kubectl apply -f mongo_persistent_volume.yml
```

(Optional) Run the following command to check that the previous worked.

```bash
$ kubectl get pv
```

The output should be the following. Notice that the status of the volume is available for claim.

```bash
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM   STORAGECLASS   REASON   AGE
mongo-pv   256Mi      RWO            Retain           Available                                   2s
```

Now claim the volume with the following command.

```bash
$ kubectl apply -f mongo_persistent_volume_claim.yml
```

(Optional) If you run the following command the volume should now be bound.

```bash
$ kubectl get pv
```

The output should be similar to the following.

```bash
NAME       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM               STORAGECLASS   REASON   AGE
mongo-pv   256Mi      RWO            Retain           Bound    default/mongo-pvc                           2m12s
```

Now create a deployment and service for the mongo database. Run the following commands.

```bash
$ kubectl apply -f mongo_deployment.yml
$ kubectl apply -f mongo_service.yml
```

(Optional) To check if both those steps worked run the following command.

```bash
$ kubectl get svc
```

Take note of the cluster ip for the mongo service and run the following command using that ip.

```bash
$ curl 10.99.106.138:27017
```

The output should be the following.

```
It looks like you are trying to access MongoDB over HTTP on the native driver port.
```

#### Step 4

Now we need to get the server app up and running. Change the directory to the `server_app/` directory and run the following commands.

```bash
$ chmod +x *.sh
$ ./build_server.sh
```

Return to the `src/` directory. Run the following commands.

```
$ kubectl apply -f server_app_deployment.yml
$ kubectl apply -f server_app_service.yml
$ kubectl apply -f server_app_service_monitor.yml
```

Run the following and take note of the cluster ip for the server app.

```bash
$ kubectl get svc
```

Populate the database with the following entries.

```bash
$ curl -X POST -d "{\"title\": \"The Sound of Music\", \"year\": 1965}" http://10.99.110.124/movies
$ curl -X POST -d "{\"title\": \"Fast Times at Ridgemont High\", \"year\": 1982}" http://10.99.110.124/movies
$ curl -X POST -d "{\"title\": \"Napoleon Dynamite\", \"year\": 2004}" http://10.99.110.124/movies
```

You should see the following message after each post request.

```
{"message":"Movie saved successfully!"}
```

Validate that you can retrieve the data with the following command.

```bash
$ curl http://10.99.110.124/movies
```

You should see something similar to the following.

```
{"data":[{"id":"61af299a39ce6818c2d6ab4a","title":"The Sound of Music","year":1965},{"id":"61af2a1839ce6818c2d6ab4b","title":"Fast Times at Ridgemont High","year":1982},{"id":"61af2a2039ce6818c2d6ab4c","title":"Napoleon Dynamite","year":2004}]}
```

Also, check that the service monitor has been added to the list of targets in Prometheus. It should be the first entry at http://192.168.33.10:30001/targets.

#### Step 5

Now that the server app is up and running it is time to create the Grafana dashboard so that we can observe our chaos experiments. Go to Crafana (http://192.168.33.10:30000/) and import the dashboard stored at `./grafana/dashboard.json`. You should see something that looks like the following.

![](resources/grafana_dashboard_import.png?raw=true)

#### Step 6 

Now open a new terminal and ssh into machine1. Change directories to the `src/client_app/` directory. Edit the contents of the `app.py` file and change the ip to the cluster ip of the server app service (the same one we used to insert the movie data). The line you need to edit looks like the following. 

```python
requests.get("http://10.104.135.34/%s" % target, timeout=1)
```

Once you are finished that running the python script, it will begin simulating traffic to the server app.

```bash
$ python3 app.py
```

If you go back to Grafana you will see the graphs begin to populate with data. It should look like the following (It does take a couple of minutes to populate).

![](resources/grafana_data_populating.png?raw=true)

### Chaos Testing

#### Step 1

We need to define our steady-state before we can conduct our experiments. Below is a picture of the Grafana dashboard during the steady-state.

![](resources/steady_state.png?raw=true)

As you can see the average response time for the `/movies` endpoint is about 1.85ms, whereas the average response time for the `/message1`, `/message2`, `/message3`, `/` endpoints is about 110μs. There are also no 500 errors. The reason the `/movies` endpoint is a lot slower is that it is accessing the mongo database whereas the other endpoints are returning a message immediately. We are going to conduct 3 types of chaos tests: network delay fault, partition fault, and pod failure fault.

#### Step 2: Network Delay Example

The first fault is a network delay fault. The yaml script is below.

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: network-delay-example
spec:
  action: delay
  mode: one
  selector:
    namespaces:
      - default
    labelSelectors:
      "app": "mongo"
  delay:
    latency: "150ms"
    correlation: "100"
    jitter: "0ms"
  duration: "5m"
```

This configuration causes a latency of 150 milliseconds in the network connections of the mongo pod. Here the mode is set to `one`, which tells Chaos Mesh to only select one server pod. Since there is only one pod all of the server pods will be affected. If we were to increase the replicas on the deployment we would see that only some of the traffic is affected. To execute the above experiment run the following command within machine1 in the `chaos-testing` directory.

```bash
$ kubectl apply -f network-delay-example.yml
```

You should see something like the following within the Grafana dashboard. We can see that the request being made that need to access the database are now experiencing a delay of 150ms. This occurs for the duration of the test, which is 5 minutes. We also see the percentage of requests that take under 100ms goes to zero for the `/movies` endpoint.

![](resources/network_delay_example.png?raw=true)

#### Step 3

Wait for the application to return to a steady-state before carrying out the next step.

#### Step 4: Partition Example

The second fault is a partition fault. The yaml script is below.

```yaml
apiVersion: chaos-mesh.org/v1alpha1
kind: NetworkChaos
metadata:
  name: partition
spec:
  action: partition
  mode: all
  selector:
    namespaces:
      - default
    labelSelectors:
      'app': 'server-app'
  direction: to
  target:
    mode: all
    selector:
      namespaces:
        - default
      labelSelectors:
        'app': 'mongo'
  duration: "1m"
```

This configuration blocks the connection between the mongo database and the server app for 1 minute. The mode `all` tells chaos mesh to apply the experiment to all the mongo and server pods. To execute the above experiment run the following command within machine1 in the `chaos-testing` directory.

```bash
$ kubectl apply -f partition-example.yml
```

You should see something like the following within the Grafana dashboard. The total number of requests being made has dropped, and there is a gap in data being collected for the `/movies` endpoint. The number of errors shoots up and we can see that there was a max of 64 500 responses returned during the test. The response time for the `/movies` endpoint shot up to 600ms once data resumed being collected. 

![](resources/partition_example.png?raw=true)

#### Step 5

Wait for the application to return to a steady-state before carrying out the next step.

#### Step 6: Pod Failure Example

The third fault is a pod failure fault. The yaml script is below.

```yaml
kind: PodChaos
apiVersion: chaos-mesh.org/v1alpha1
metadata:
  namespace: default
  name: pod-failure-example
spec:
  duration: '30s'
  selector:
    namespaces:
      - default
    labelSelectors:
      app: mongo
  mode: all
  action: pod-failure
  gracePeriod: 0

```

This configuration injects a pod failure to all the mongo pods for 30 seconds. To execute the above experiment run the following command within machine1 in the `chaos-testing` directory.

```bash
$ kubectl apply -f pod-failure-example.yml
```

You should see something like the following within the Grafana dashboard. This experiment has noticeably less severe effects on the system (this is because the duration of the experiment is shorter). There is a spike in the number of errors, but this time only a max of 8 500 errors were recorded. Also, there is a small dip in the percent of `/movies` requests under 100ms. We can also see a drop in CPU usage and a spike in memory usage.

![](resources/pod_failure_example.png?raw=true)

## Sources
"Principles of Chaos Engineering". principlesofchaos.org. Retrieved 2017-10-21.

"The Netflix Simian Army". Netflix Tech Blog. Medium. 2011-07-19. Retrieved 2017-10-21.

"Discovering Issues with HTTP/2 via Chaos Testing". https://www.twilio.com/blog/2017/10/http2-issues.html.
