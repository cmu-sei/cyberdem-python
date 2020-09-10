'''
CyberDEM Example Script

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
from cyberdem.structures import Relationship
from datetime import datetime, timedelta


def main():

    # Set up the FileSystem for storage and retrieval of CyberDEM objects
    fs = FileSystem('./test-fs')

    # Instantiate a known set of CyberObjects
    ap = Device(
        name="Access Point", description="Main access point", is_virtua=False,
        network_interfaces=[("eth0", "10.10.30.40"),("eth1", "192.168.10.2")])
    fs.save(ap)

    firewall = Device(
        name="Firewall", description="Firewall", is_virtual=False,
        network_interfaces=[("eth0", "192.168.10.3"), ("eth1", "192.168.10.4"),
        ("eth2", "192.168.10.5")])
    fs.save(firewall)

    mtu = Device(
        name="MTU", description="Master Terminal Unit", is_virtual=False,
        network_interfaces=[("eth0", "192.168.10.6")])
    fs.save(mtu)

    hmi = Device(
        name="HMI", description="HMI Workstation", is_virtual=False,
        network_interfaces=[("eth0", "192.168.10.7")])
    fs.save(hmi)

    wan_ap = NetworkLink(
        name='WAN-AP', description='WAN to AP link', physical_layer='Wired',
        is_logical=False, data_link_protocol='Ethernet')
    fs.save(wan_ap)

    ap_fw = NetworkLink(
        name='AP-FW', description='AP to FW link', physical_layer='Wired',
        is_logical=False, data_link_protocol='Ethernet')
    fs.save(ap_fw)

    fw_mtu = NetworkLink(
        name='FW-MTU', description='FW to MTU link', physical_layer='Wired',
        is_logical=False, data_link_protocol='Ethernet')
    fs.save(fw_mtu)

    fw_hmi = NetworkLink(
        name='FW-HMI', description='FW to HMI link', physical_layer='Wired',
        is_logical=False, data_link_protocol='Ethernet')
    fs.save(fw_hmi)

    cisco_ios = OperatingSystem(
        name='Cisco IOS', description='AP OS is Cisco IOS', version='15.4(3)M',
        os_type='CiscoIOS')
    fs.save(cisco_ios)

    redhat = OperatingSystem(
        nam='RedHat', description='RedHat OS', version='8', os_type='LinuxRedHat')
    fs.save(redhat)

    win_10 = OperatingSystem(
        name='Windows 10', description='HMI OS is Win10',
        version='Win 10, 2004', os_type='MicrosoftWindows')
    fs.save(win_10)

    pfsense = Application(
        name='PfSense', description='PfSense Firewall', version='2.4.2')
    fs.save(pfsense)

    firefox = Application(
        name='Firefox', description='Firefox browser', version='60')
    fs.save(firefox)

    rapid_scada = Application(
        name='Rapid SCADA', description='Rapid SCADA software', version='5')
    fs.save(rapid_scada)

    httpd_service = Service(
        name='httpd', description='Apache web server', version='2.4.20',
        service_type='WebService', address='192.168.100.40')
    fs.save(httpd_service)

    # Save a bunch of random objects
    obj_types = [
        Application, Data, Device, Network, NetworkLink, Persona,
        System, OperatingSystem, Service, Deny, Detect, Manipulate,
        DataExfiltration, Destroy, Degrade, Disrupt, PacketManipulationEffect,
        ManipulationAttack, PhishingAttack, BlockTrafficEffect,
        HardwareDamageEffect, LoadRateEffect, DelayEffect, JitterEffect,
        CPULoadEffect, MemoryUseEffect, DropEffect, HardwareDegradeEffect,
        OtherDegradeEffect]
    for ot in obj_types:
        for _ in range(0, 4):
            fs.save(ot())

    # @TODO Build relationships between the known objects
    fs.save(Relationship((ap.id, 'ConnectedTo', wan_ap.id)))

    # @TODO Instantiate events of a specific attack

    # @TODO Query the file system
    headers, resp = fs.query("SELECT * FROM Application")
    print(f'QUERY 1\n--------\n{headers}')
    for line in resp:
        print(line)

    query2 = "SELECT description,name FROM * WHERE (name='My application' AND version='2.4') OR system_type='C3'"
    headers, resp = fs.query(query2)
    print(f'QUERY 2\n--------\n{headers}')
    for line in resp:
        print(line)

    #query3 = "SELECT id FROM Application WHERE (name='My application' AND version='2.4') OR system_type='C3'"
    headers, resp = fs.query(query3)
    print(f'QUERY 3\n--------\n{headers}')
    for line in resp:
        print(line)

    # @TODO Load instances of objects and events from the file system
    # change some property and re-save the instance
    for line in resp:
        obj_instance = fs.get(line[0])


if __name__ == "__main__":
    main()
