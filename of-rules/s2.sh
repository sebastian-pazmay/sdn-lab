#Open Flow rules!
#Deleting old rules
ovs-ofctl del-flows s2
#s2 rules
ovs-ofctl add-flow s2 'in_port=1,idle_timeout=0,actions=output:2'
ovs-ofctl add-flow s2 'in_port=2,idle_timeout=0,actions=output:1'
#Print configuration
# ovs-ofctl dump-flows s2