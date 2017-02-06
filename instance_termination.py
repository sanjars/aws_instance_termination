#!/usr/bin/python
import boto3
import sys
#The following reads the file and saves in variable

print "Make sure that the file contains only the instance IDs."
#file_in = raw_input("Please specify the full path for the file:")
servers = open('/home/sanjar/lab_hub/rest_list.txt','r').readlines()
#servers = open(file_in,'r').readlines()
servers = map(lambda servers: servers.strip(), servers) 

ec2 = boto3.resource('ec2')

# Ensure the servers that are in the list are stopped
print ("The following list is stopped instances ONLY and if you do not see the instance listed here, then instance is running and in which case you have to abort the process before turning off the termination protection.")
print ("Stopped instances (Make Sure to Check Carefully The List!:")
stopped_instances = ec2.instances.filter(InstanceIds=servers,
    Filters=[{'Name': 'instance-state-name', 'Values': ['stopped']}])
for instance in stopped_instances:
    print(instance.id, instance.instance_type)

# Disable Termination Protection
_answer_ = raw_input("Do you still want to continue to disable termination protection? (yes/no):")
if _answer_ == "yes":
	print "Turning off termination protection..."
	for inst in stopped_instances.filter(InstanceIds=servers):
       		inst.modify_attribute(DryRun=False, Attribute='disableApiTermination',Value='False')
		#time.sleep(3)
elif _answer_ == 'no':
        print ("Roger that! We will stop and will not turn off termination protection")
        sys.exit()
else:
        print ("Your answer is not valid answer. Type either 'yes' or 'no'.")
	sys.exit()

# 
_termResponse_ = raw_input("Would you like to terminate the instances as well? (yes/no):")
if _termResponse_ == 'yes':
	print ("Terminating...")
	stopped_instances.filter(InstanceIds=servers).terminate()
	print ("All specified instances terminated!")
elif _termResponse_ == 'no':
	print ("Will not terminate! Got it!")
	sys.exit()
else:
	print ("Your answer is not valid again. Type 'yes' or 'no'.")
	sys.exit()
