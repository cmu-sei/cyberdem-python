"""CyberDEM Enumerations"""

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

class _CyberDEMEnumeration():
    """Super class for all CyberDEM enumerations"""

    _opts = []

    def _check_prop(self, value):
        if value.lower() not in [o.lower() for o in self._opts]:
            raise ValueError(
                f'"{value}" is not an acceptable {self.__class__.__name__}. '
                f'Options are {", ".join(self._opts)}.')
        if value not in self._opts:
            print(
                f'Warning: "{value}" is not the same capitalization as '
                f'{self.__class__.__name__} option.')


class CyberEventPhaseType(_CyberDEMEnumeration):
    """CyberDEM CyberEventPhaseType enumeration"""

    _opts = [
        'Start',
        'Suspend',
        'Continue',
        'ContinueWithChanges',
        'End'
    ]


class DataLinkProtocolType(_CyberDEMEnumeration):
    """CyberDEM DataLinkProtocolType enumeration"""

    _opts = [
        'Ethernet',
        'WiFi',
        'ATM',
        'LocalTalk',
        'PPP',
        'TokenRing',
        'VLAN',
        'Bluetooth',
        '1553Bus'
    ]


class DataStatus(_CyberDEMEnumeration):
    """CyberDEM DataStatus enumeration"""

    _opts = [
        'Uncompromised',
        'Corrupted',
        'Manipulated',
        'NonDecryptable',
        'Erased'
    ]


class DataType(_CyberDEMEnumeration):
    """CyberDEM DataType enumeration"""

    _opts = [
        'File',
        'Code',
        'Credentials'
    ]


class DeviceType(_CyberDEMEnumeration):
    """CyberDEM DeviceType enumeration"""

    _opts = [
        'Generic',
        'Networking',
        'ComputerNode',
        'PortableComputer',
        'Controller',
        'StorageDevice',
        'Sensor',
        'Printer',
        'Scanner',
        'Communications',
        'HMI',
        'Monitoring',
        'IoT'
    ]

    def _check_prop(self, value):
        if not isinstance(value, list):
            raise ValueError(f'"types" should be a list of DeviceTypes')
        for t in value:
            if t.lower() not in [o.lower() for o in self._opts]:
                raise ValueError(f'"{t}" is not a valid value for DeviceType')
            if t not in self._opts:
                print(f'Warning: "{t}" is not the same capitalization as '
                    f'{self.__class__.__name__} option.')


class EncryptionType(_CyberDEMEnumeration):
    """CyberDEM EncryptionType enumeration"""

    _opts = [
        'DES',
        'TripleDES',
        'RSA',
        'AES',
        'TwoFish',
        'SHA'
    ]


class HardwareDamageType(_CyberDEMEnumeration):
    """CyberDEM HardwareDamageType enumeration"""

    _opts = [
        'BootLoop',
        'PhysicalDestruction',
        'HardDriveErased'
    ]


class HardwareDegradeType(_CyberDEMEnumeration):
    """CyberDEM HardwareDegradeType enumeration"""

    _opts = [
        'Keyboard',
        'Mouse',
        'Display',
        'Sound',
        'BlueScreen',
        'RandomText',
        'Reboot'
    ]


class LoadRateType(_CyberDEMEnumeration):
    """CyberDEM LoadRateType enumeration"""

    _opts = [
        'Upload',
        'Download'
    ]


class MessageType(_CyberDEMEnumeration):
    """CyberDEM MessageType enumeration"""

    _opts = [
        'Email',
        'Chat',
        'Text',
        'SocialMedia'
    ]


class NetworkProtocolType(_CyberDEMEnumeration):
    """CyberDEM NetworkProtocolType enumeration"""

    _opts = [
        'InternetProtocol',
        'NAT',
        'ICMP',
        'ARP',
        'RIP',
        'OSPF',
        'IPsec'
    ]


class OperatingSystemType(_CyberDEMEnumeration):
    """CyberDEM OperatingSystemType enumeration"""

    _opts = [
        'MicrosoftDOS',
        'MicrosoftWindows',
        'AppleMacOS',
        'BellLabsUnix',
        'BSDUnix',
        'GNUUnix',
        'LinuxRedHat',
        'Ubuntu',
        'OpenSolaris',
        'DECHP_UX',
        'DECVMS',
        'IBMOS_2',
        'Android',
        'AppleiOS',
        'CiscoIOS',
        'Firmware'                       
    ]


class PacketManipulationType(_CyberDEMEnumeration):
    """CyberDEM PacketManipulationType enumeration"""

    _opts = [
        'Duplication',
        'Corruption',
        'Redordering',
        'Dropped'
    ]


class PhysicalLayerType(_CyberDEMEnumeration):
    """CyberDEM PhysicalLayerType enumeration"""

    _opts = [
        'Wired',
        'Wireless'
    ]


class ReconType(_CyberDEMEnumeration):
    """CyberDEM ReconType enumeration"""

    _opts = [
        'Ping',
        'PingScan',
        'PortScan',
        'PortSweep',
        'TraceRoute',
        'NetworkMap',
        'VulnerabilityEnumeration',
        'DeviceEnumeration',
        'OSScan',
        'ServiceEnumeration',
        'DomainEnumeration',
        'AccountEnumeration',
        'NetBiosScan',
        'SNMPSweep',
        'LDAPScan',
        'NTPEnumeration',
        'SMTPEnumeration',
        'DNSEnumeration',
        'WindowsEnumeration',
        'UNIX-LinuxEnumeration',
        'ARPScan'
    ]


class RelationshipType(_CyberDEMEnumeration):
    """CyberDEM RelationshipType enumeration"""

    _opts = [
        'Administers',
        'ComponentOf',
        'ContainedIn',
        'ProvidedBy',
        'ResidesOn'
    ]


class SensitivityType(_CyberDEMEnumeration):
    """CyberDEM SensitivityType enumeration"""

    _opts = [
        'Unclassified',
        'Confidential',
        'FOUO',
        'Secret',
        'SecretNoForn',
        'TS',
        'TS_SCI',
        'NATORestricted',
        'NATOConfidential',
        'NATOSecret',
        'CosmicTopSecret',
        'FVEY',
        'Proprietary',
        'PII',
        'HIPPA',
        'GDPR',
        'Public'
    ]


class ServiceType(_CyberDEMEnumeration):
    """CyberDEM ServiceType enumeration"""

    _opts = [
        'DomainNameServer',
        'EmailServer',
        'WebService',
        'DatabaseServer',
        'FileShare',
        'ChatServer',
        'Forum',
        'SocialMediaServer'
    ]


class SystemType(_CyberDEMEnumeration):
    """CyberDEM SystemType enumeration"""

    _opts = [
        'Generic',
        'SCADA',
        'C2',
        'ICS'
    ]