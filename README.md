# sdn-lab

Simple mininet topology

       Client10 --- OFs1 --- LinuxRouter --- OFs2 --- Client20
                                  |
                                  |
                               Server00

### Run the topology
```
$ sudo python topology.py
```
### Clean the topology
```
$ sudo mn -c
```