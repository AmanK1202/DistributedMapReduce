# DistributedMapReduce
Distributed MapReduce (devevloped from scratch) on Google Cloud Platform

Public cloud platform utilized- Google Cloud Platform
GCP overview:
GCP consists of a set of physical assets, such as computers and hard disk drives, and virtual resources, such as virtual machines (VMs), that are contained in Google's data centers around the globe.  [cited from GCP official docs]
A project was created in GCP under which the instances were created. A total of three VMs are created for to handle a maximum of 3 mappers and 3 reducers. For each instance I have used 2 CPU configurations.

Bird’s eye view of the system
Goal- To host the distributed MapReduce system on Google Cloud Platform.
Implementation and design - 
	Assumptions-
1.	Variables such as file path, host_name and port_numbers and operations are provided in the configuration file. Hence these parameters can be tweaked easily by the user from the configuration file.
2.	For testing purposes, a file from guttenberg project was downloaded. The input file will also be provided along with the submission.
3.	The output file is merged and written in mapperreducer1 instance.
4.	Cost increases with increase in number of VMs utilized, hence I have implemented reusability of VMs. Mapper and reducers are utilized in the same VM.
5.	Three VMs for mapper and reducers have been initially created along with kv-store instance.
6.	The master node VM is already running which starts rest of the VMs.

•	In this implementation I have designed a distributed Map Reduce system which can support applications of word count and inverted index. 
•	There is a master node that is responsible for coordination and synchronizing the whole process. 
•	The Master Node is assigned a VM instance which is already running. The user has to just run the ‘master_node3.py’ file by ‘sshing’ into the VM instance. The in built SSH console given in the instance on the GCP console can be used.





Contents of master-node instance-
 
    

As it can be observed I have uploaded the master_node3.py file, the input file, configuration file and the json file consisting of ssh keys.

•	The master-node contains code snippets for starting the VMs and terminating them once process is done.
•	List of VMs used-
•	Mapperreducer1, Mapperreducer2, Mapperreducer3 and kv-store.
•	Memcahed-lite server is running in the kv-store VM, again initiated by the master node.
•	After starting all the instances, the master sends the input file into the Mapper VMs. The mapper VMs do the mapping tasks send it to KV store.
•	These mapper VMs are stopped and restarted by the master node for the reducers to function.
•	Reducers receive the data and do the reducing task and output the merged file at mapperreducer1 instance. 
•	The operation that needs to be performed (‘WordCount’ or ‘InvertedIndex’) can be mentioned in the configuration file.
•	After the operation is completed the master node stops all the VM instances except mapperreducer1 for the user to observe the output in this instance.







Logs obtained at master-node instance-

 



How to observe the output?

•	2 test cases are provided. One for word count and other for inverted index.
•	For observing the output file the user has to ssh into the mapperreducer1 instance. The outputted file can be seen there.
•	One can access the output file in the instance’s prompt itself using the vim editor.
Command- vim filename.txt

Output for Word count application-
 

Output for Word count application-

 

Performance numbers- Cpu utilization

 





Data Partitioning
•	The master handles data partitioning. Number of mappers are initiated as per the number of splits made into the data file.
•	In this case the master splits the data into 3 chunks (since number of mapper=3) and hence each chunk is sent to each of the three mappers.

Code snippets-
	The code for starting and stopping the VMs were obtained from GCP official library or python. 
Following is the code snippet used for starting the VMs.

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    project = 'aman-kumar-257316'
    zone = 'us-central1-a'
    instance = ['mapperreducer-1','mapperreducer-2', 'mapperreducer-3','kv-store']
    print("Starting all instances")
    for i in range(num_map):
        request = service.instances().start(project=project, zone=zone, instance=instance[i])
        response = request.execute()

Following is the code snippet used for stopping the VMs.
Everything is same just ‘.stop’ method is used instead of ‘.start’

    credentials = GoogleCredentials.get_application_default()
    service = discovery.build('compute', 'v1', credentials=credentials)
    # Project ID for this request.
    project = 'aman-kumar-257316'  # TODO: Update placeholder value
    # The name of the zone for this request.
    zone = 'us-central1-a'  # TODO: Update placeholder value.
    # Name of the instance resource to stop.
    instance = ['mapperreducer-2', 'mapperreducer-3','kv-store']  # TODO: Update placeholder value.
    print("stopping instances")
    for i in range(len(instance)):
        request = service.instances().stop(project=project, zone=zone, instance=instance[i])
        response = request.execute()

