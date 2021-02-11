#!/usr/bin/python

"""SDN Lab Topology

       Client10 --- OFs1 --- LinuxRouter --- OFs2 --- Client20
                                  |
                                  |
                               Server00
"""
from mininet.cli import CLI
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink, Link
from mininet.log import setLogLevel, info
from mininet.node import Node
from time import sleep

class LinuxRouter( Node ):

    "A Node with IP forwarding enabled."
    # pylint: disable=arguments-differ
    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()

class sdnLab(Topo):

    def build(self):

        info( '*** Adding hosts\n' )
        ## Client10
        c10 = self.addHost('c10',ip='10.0.10.10/24', mac='00:00:00:00:00:10')
        ## Client20
        c20 = self.addHost('c20',ip='10.0.20.20/24', mac='00:00:00:00:00:20')
        ## Server00
        s00 = self.addHost('s00',ip='192.168.0.100/24', mac='00:00:00:00:00:20')

        info( '*** Adding router\n' )
        defaultIP = '192.168.0.1/24'
        ## LinuxRouter
        lr0 = self.addNode('lr0', cls=LinuxRouter, ip=defaultIP)

        info( '*** Adding switches\n' )
        ## OpenFlow Switch 1 && OpenFlow Switch 2
        ofs1, ofs2 = [self.addSwitch(s) for s in ('ofs1', 'ofs2')]
        
        info( '*** Creating links\n' )
        for c, s, ci, si in [ (c10, ofs1, 0, 1), (ofs2, c20, 1, 0) ]:
            self.addLink( c, s, ci, si )
        self.addLink( s00, lr0, 0, 1 )
        self.addLink( ofs1, lr0, 2, 2 )
        self.addLink( ofs2, lr0, 2, 3 )

def run():

    ## Import nodes
    net = Mininet(topo=sdnLab(), link=TCLink, controller=None)
    net.start()
    c10 = net.get('c10')
    c20 = net.get('c20')
    ofs1 = net.get('ofs1')
    ofs2 = net.get('ofs2')
    lr0 = net.get('lr0')
    s00 = net.get('s00')
    sleep(5)

    ## Configure c10/c20
    c10.cmd('sudo arp -s 10.0.0.20 00:00:00:00:00:20')
    c10.cmd('sudo ip route add default via 10.0.10.1')
    c20.cmd('sudo arp -s 10.0.0.10 00:00:00:00:00:10')
    c20.cmd('sudo ip route add default via 10.0.20.1')
    
    ## Configure OF switches
    ofs1.cmd('of-rules/ofs1.sh')
    ofs2.cmd('of-rules/ofs2.sh')
   
    ## Configure lr0
    lr0.cmd('sudo ifconfig lr0-eth2 10.0.10.1 netmask 255.255.255.0')
    lr0.cmd('sudo ifconfig lr0-eth3 10.0.20.1 netmask 255.255.255.0')
    lr0.cmd('sudo ip link set dev lr0-eth1 up')
    lr0.cmd('sudo ip link set dev lr0-eth2 up')
    lr0.cmd('sudo ip link set dev lr0-eth3 up')

    ## Configure s00
    s00.cmd('sudo ip route add default via 192.168.0.1')

    ## Connectivity test
    net.pingAll()
    print('Topology is connected && running!')
    CLI(net)

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
