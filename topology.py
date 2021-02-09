#!/usr/bin/python

"""SDN Lab Topology

   Client --- OFs1 --- OFs2 --- Server

"""
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink, Link
from mininet.log import setLogLevel, info
#from mininet.node import Controller

from time import sleep

class sdnLab(Topo):

    def build(self):

        info( '*** Adding hosts\n' )
        h10 = self.addHost('h10',ip='10.0.0.10', mac='00:00:00:00:00:10')
        h20 = self.addHost('h20',ip='10.0.0.20', mac='00:00:00:00:00:20')

        info( '*** Adding switches\n' )
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')

        info( '*** Creating links\n' )
        self.addLink(h10, s1, 0, 1)
        self.addLink(s1, s2, 2, 2)
        self.addLink(s2, h20, 1, 0)

if __name__ == '__main__':
    #Import nodes
    net = Mininet(topo=sdnLab(), link=TCLink, controller=None)
    net.start()
    h10 = net.get('h10')
    h20 = net.get('h20')
    s1 = net.get('s1')
    s2 = net.get('s2')
    sleep(5)
    
    #Configure OF switches
    s1.cmd('of-rules/s1.sh')
    s2.cmd('of-rules/s2.sh')
    
    #Configure h10/h20
    h10.cmd('sudo arp -s 10.0.0.20 00:00:00:00:00:20')
    h20.cmd('sudo arp -s 10.0.0.10 00:00:00:00:00:10')

    print('The topology is running!')

    CLI(net)
