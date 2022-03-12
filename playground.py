#!/usr/bin/env python

"""
Based on example: linuxrouter.py: Example network with Linux IP router
"""


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class LinuxRouter(Node):
    "A Node with IP forwarding enabled."

    # pylint: disable=arguments-differ
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        # Enable forwarding on the router
        self.cmd("sysctl net.ipv4.ip_forward=1")

    def terminate(self):
        self.cmd("sysctl net.ipv4.ip_forward=0")
        super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
    "A LinuxRouter connecting three IP subnets"

    # pylint: disable=arguments-differ
    def build(self, **_opts):

        defaultIP = "192.168.1.1/24"  # IP address for r0-eth1
        router = self.addNode("r0", cls=LinuxRouter, ip=defaultIP)

        s1, s2, s3 = [self.addSwitch(s) for s in ("s1", "s2", "s3")]

        self.addLink(
            s1, router, intfName2="r0-eth1", params2={"ip": defaultIP}
        )  # for clarity
        self.addLink(s2, router, intfName2="r0-eth2", params2={"ip": "172.16.0.1/12"})
        self.addLink(s3, router, intfName2="r0-eth3", params2={"ip": "10.0.0.1/8"})

        client1 = self.addHost("client1", ip="192.168.1.100/24", defaultRoute="via 192.168.1.1")
        client2 = self.addHost("client2", ip="172.16.0.100/12", defaultRoute="via 172.16.0.1")
        server1 = self.addHost("server1", ip="10.0.0.100/8", defaultRoute="via 10.0.0.1")
        server2 = self.addHost("server2", ip="10.0.0.101/8", defaultRoute="via 10.0.0.1")
        server3 = self.addHost("server3", ip="10.0.0.102/8", defaultRoute="via 10.0.0.1")
        proxy = self.addHost("proxy", ip="10.0.0.250/8", defaultRoute="via 10.0.0.1")

        for h, s in [(client1, s1), (client2, s2), (server1, s3),(server2, s3),(server3, s3), (proxy, s3)]:
            self.addLink(h, s)


def run():
    "Test linux router"
    topo = NetworkTopo()
    net = Mininet(topo=topo, waitConnected=True)  # controller is used by s1-s3
    net.start()
    info("*** Routing Table on Router:\n")
    info(net["r0"].cmd("route"))

    # info(net["client1"].cmd("ping -c 2 172.16.0.100"))
    # info(net["client2"].cmd("ping -c 2 10.0.0.100"))
    # info(net["h3"].cmd("ping -c 2 192.168.1.100"))

    net["proxy"].cmd(
        "envoy -c /vagrant/envoy-demo.yaml > output/envoy-stdout.txt 2> output/envoy-stderr.txt &"
    )
    net["server1"].cmd(
        "go-server > output/go-server-stdout.txt 2> output/go-server-stderr.txt &"
    )
    net["server2"].cmd(
        "go-server > output/go-server-stdout.txt 2> output/go-server-stderr.txt &"
    )
    net["server3"].cmd(
        "go-server > output/go-server-stdout.txt 2> output/go-server-stderr.txt &"
    )

    info(net["client1"].cmd("k6 run --vus 10 --duration 30s /vagrant/k6-client.js"))
    info(net["client2"].cmd("k6 run --vus 10 --duration 30s /vagrant/k6-client.js"))

    CLI(net)
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    run()
