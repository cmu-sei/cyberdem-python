"""CyberDEM Example Script"""

'''
CyberDEM Python

Copyright 2020 Carnegie Mellon University.

NO WARRANTY. THIS CARNEGIE MELLON UNIVERSITY AND SOFTWARE ENGINEERING INSTITUTE
MATERIAL IS FURNISHED ON AN "AS-IS" BASIS. CARNEGIE MELLON UNIVERSITY MAKES NO 
WARRANTIES OF ANY KIND, EITHER EXPRESSED OR IMPLIED, AS TO ANY MATTER 
INCLUDING, BUT NOT LIMITED TO, WARRANTY OF FITNESS FOR PURPOSE OR 
MERCHANTABILITY, EXCLUSIVITY, OR RESULTS OBTAINED FROM USE OF THE MATERIAL. 
CARNEGIE MELLON UNIVERSITY DOES NOT MAKE ANY WARRANTY OF ANY KIND WITH RESPECT 
TO FREEDOM FROM PATENT, TRADEMARK, OR COPYRIGHT INFRINGEMENT.

Released under a MIT (SEI)-style license, please see license.txt or contact 
permission@sei.cmu.edu for full terms.

[DISTRIBUTION STATEMENT A] This material has been approved for public release 
and unlimited distribution.  Please see Copyright notice for non-US Government 
use and distribution.

DM20-0711
'''


from cyberdem.filesystem import FileSystem
from cyberdem.base import *
from datetime import datetime, timedelta

def main():

    # Set up the FileSystem for storage and retrieval of CyberDEM objects
    fs = FileSystem('./test-fs')

    # Instantiate a known set of CyberObjects
    device_kwargs = [
        {
            'name': "Access Point",
            'description': "Main access point",
            'is_virtual': False,
            'network_interfaces': [
                ("eth0", "10.10.30.40"),
                ("eth1", "192.168.10.2")
            ]
        },
        {
            'name': "Firewall",
            'description': "Firewall",
            'is_virtual': False,
            'network_interfaces': [
                ("eth0", "192.168.10.3"),
                ("eth1", "192.168.10.4"),
                ("eth2", "192.168.10.5")
            ]
        },
                {
            'name': "MTU",
            'description': "Master Terminal Unit",
            'is_virtual': False,
            'network_interfaces': [
                ("eth0", "192.168.10.6")
            ]
        },
                {
            'name': "HMI",
            'description': "HMI Workstation",
            'is_virtual': False,
            'network_interfaces': [
                ("eth0", "192.168.10.7")
            ]
        }
    ]
    for kwargs in device_kwargs:
        fs.save(Device(**kwargs))

    network_link_kwargs = [
        {
            'name': 'WAN-AP',
            'description': 'WAN to AP link',
            'physical_layer': 'Wired',
            'is_logical': False,
            'data_link_protocol': 'Ethernet'
        },
        {
            'name': 'AP-FW',
            'description': 'AP to FW link',
            'physical_layer': 'Wired',
            'is_logical': False,
            'data_link_protocol': 'Ethernet'
        },
        {
            'name': 'FW-MTU',
            'description': 'FW to MTU link',
            'physical_layer': 'Wired',
            'is_logical': False,
            'data_link_protocol': 'Ethernet'
        },
        {
            'name': 'FW-HMI',
            'description': 'FW to HMI link',
            'physical_layer': 'Wired',
            'is_logical': False,
            'data_link_protocol': 'Ethernet'
        }
    ]
    for kwargs in network_link_kwargs:
        fs.save(NetworkLink(**kwargs))

    operating_system_kwargs = [
        {
            'name': 'Cisco IOS',
            'description': 'AP OS is Cisco IOS',
            'version': '15.4(3)M',
            'os_type': 'CiscoIOS'
        },
        {
            'name': 'RedHat',
            'description': 'RedHat OS',
            'version': '8',
            'os_type': 'LinuxRedHat'
        },
        {
            'name': 'Windows 10',
            'description': 'HMI OS is Win10',
            'version': 'Win 10, 2004',
            'os_type': 'MicrosoftWindows'
        }
    ]
    for kwargs in operating_system_kwargs:
        fs.save(OperatingSystem(**kwargs))

    application_kwargs = [
        {
            'name': 'PfSense',
            'description': 'PfSense Firewall',
            'version': '2.4.2'
        },
        {
            'name': 'Firefox',
            'description': 'Firefox browser',
            'version': '60'
        },
        {
            'name': 'Rapid SCADA',
            'description': 'Rapid SCADA software',
            'version': '5'
        }
    ]
    for kwargs in application_kwargs:
        fs.save(Application(**kwargs))

    fs.save(Service(
        name='httpd', description='Apache web server', version='2.4.20',
        service_type='WebService', address='192.168.100.40'))

    # Instantiate and save a bunch of other random objects
    obj_types = [Application, Data, Device, Network, NetworkLink, Persona,
        System, OperatingSystem, Service, Deny, Detect, Manipulate,
        DataExfiltration, Destroy, Degrade, Disrupt, PacketManipulationEffect,
        ManipulationAttack, PhishingAttack, BlockTrafficEffect,
        HardwareDamageEffect, LoadRateEffect, DelayEffect, JitterEffect,
        CPULoadEffect, MemoryUseEffect, DropEffect, HardwareDegradeEffect,
        OtherDegradeEffect]
    for ot in obj_types:
        for _ in range(0,4):
            fs.save(ot())

    # Build relationships between the known objects



    # Instantiate events of a specific attack 




    

    headers,resp = fs.query("SELECT * FROM Application")
    #headers,resp = fs.query("SELECT * FROM Application WHERE (name='My application' AND version='2.4') OR system_type='C3'")
    print(headers)
    for line in resp:
        print(line)


if __name__ == "__main__":
    main()