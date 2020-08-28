"""Object/Event classes for CyberDEM"""

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

from collections import OrderedDict
from datetime import datetime, timedelta
from .enumerations import * 
from .structures import *
import sys
import uuid


class _CyberDEMBase():
    """Base class for all CyberDEM objects

    Will create an appropriate ``id`` if one is not given.

    :param id: string formatted UUIDv4
    :type id: string, optional

    :raises ValueError: if a given ``id`` is not a valid string representation
        of a UUIDv4
    """

    _type = None
    
    def __init__(self, id=None, **kwargs):
        if id is None:
            id = str(uuid.uuid4())
        self.id = id
        
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValueError(
                f'"{value}"" is not a valid value for id. Must be a UUIDv4.')
        self._id = value

    def __str__(self):
        string = self._type + "("
        for attr in self.__dict__:
            if attr.startswith('_'):
                string += '\n    ' + attr[1:] + ': ' + str(self.__dict__[attr])
            else:
                string += '\n    ' + attr + ': ' + str(self.__dict__[attr])
        string += "\n)"
        return string

    def __repr__(self):

        return str(self.__dict__)


## Second level CyberDEM objects
class _CyberObject(_CyberDEMBase):
    """Class for all CyberDEM CyberObjects

    Inherits :_CyberDEMBase:

    
    :param name: The name of the object
    :type name: string, optional
    :param description: A description of the object
    :type description: string
    :param related_objects: A list of relationship object IDs
    :type related_objects: list of relationship object IDs, optional
    """

    def __init__(self, name=None, description=None, related_objects=None,
            **kwargs):
        super().__init__(**kwargs)
        if name:
            self.name = name
        if description:
            self.description = description
        if related_objects:
            self.related_objects = related_objects

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for name. Must be '
                f'string.')
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for description. Must be '
                f'string.')
        self._description = value

    @property
    def related_objects(self):
        return self._related_objects

    @related_objects.setter
    def related_objects(self, value):
        if not isinstance(value, list):
            raise TypeError(
                f'{type(value)} is not a valid type for related_objects. Must be '
                f'list of IDs.')
        # @TODO: implement check for each item in value is a relationship object
        self._related_objects = value

    
class _CyberEvent(_CyberDEMBase):
    """Class for all CyberDEM CyberEvents
    
    Attributes
    ----------
    event_time : 
    target :
    ....
    """

    def __init__(self, event_time=None, target_ids=None, target_modifiers=None,
            phase=None, duration=None, actor_ids=None, source_ids=None,
            **kwargs):
        super().__init__(**kwargs)
        if event_time:
            self.event_time = event_time
        if target_ids:
            self.target_ids = target_ids
        if target_modifiers:
            self.target_modifiers = target_modifiers
        if phase:
            self.phase = phase
        if duration:
            self.duration = duration
        if actor_ids:
            self.actor_ids = actor_ids
        if source_ids:
            self.source_ids = source_ids

    @property
    def event_time(self):
        return self._event_time

    @event_time.setter
    def event_time(self, value):
        if not isinstance(value, datetime):
            raise TypeError(
                f'{type(value)} is not a valid type for event_time. Must be '
                f'datetime.')
        self._event_time = value

    @property
    def target_ids(self):
        return self._target_ids

    @target_ids.setter
    def target_ids(self, value):
        if not isinstance(value, list):
            raise TypeError(
                f'{type(value)} is not a valid type for target_ids. Must be '
                f'list.')
        self._target_ids = value

    @property
    def target_modifiers(self):
        return self._target_modifiers

    @target_modifiers.setter
    def target_modifiers(self, value):
        if not isinstance(value, dict):
            raise TypeError(
                f'{type(value)} is not a valid type for target_modifiers. Must'
                f'be dictionary.')
        self._target_modifiers = value

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        CyberEventPhaseType()._check_prop(value)
        self._phase = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        if not isinstance(value, timedelta):
            raise TypeError(
                f'{type(value)} is not a valid type for duration. Must be '
                f'timedelta.')
        self._duration = value

    @property
    def actor_ids(self):
        return self._actor_ids

    @actor_ids.setter
    def actor_ids(self, value):
        if not isinstance(value, list):
            raise TypeError(
                f'{type(value)} is not a valid type for actor_ids. Must be '
                f'list of IDs.')
        self._actor_ids = value

    @property
    def source_ids(self):
        return self._source_ids

    @source_ids.setter
    def source_ids(self, value):
        if not isinstance(value, list):
            raise TypeError(
                f'{type(value)} is not a valid type for source_ids. Must be '
                f'list of IDs.')
        self._source_ids = value


### Third level CyberDEM CyberEvents
class _CyberEffect(_CyberEvent):
    """Class for all CyberDEM CyberEffects"""
    
    pass


class _CyberAction(_CyberEvent):
    """Class for all CyberDEM CyberActions"""

    pass


### Third level CyberDEM CyberObjects
class Application(_CyberObject):
    """Class for Application object

    Attributes
    ----------
    version : string
        Version of the application
    """

    _type = "Application"

    def __init__(self, version=None, **kwargs):
        super().__init__(**kwargs)
        if version:
            self.version = version

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for version. Must be '
                f'string.')
        self._version = value


class Data(_CyberObject):
    """Class for Data object

    Attributes
    ----------
    sensitivity : SensitivityType
        Sensitivity level of the data, from the enumerated list of 
            SensitivityType
    data_type : DataType

    encrypted : EncryptionType

    status : DataStatus

    confidetiality : float
    """

    _type = "Data"

    def __init__(self, sensitivity=None, data_type=None, encrypted=None,
            status=None, confidentiality=None, **kwargs):
        super().__init__(**kwargs)
        if sensitivity:
            self.sensitivity = sensitivity
        if data_type:
            self.data_type = data_type

    @property
    def sensitivity(self):
        return self._sensitivity

    @sensitivity.setter
    def sensitivity(self, value):
        SensitivityType()._check_prop(value)
        self._sensitivity = value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        DataType()._check_prop(value)
        self._data_type = value

    @property
    def encrypted(self):
        return self._encrypted

    @encrypted.setter
    def encrypted(self, value):
        EncryptionType()._check_prop(value)
        self._encrypted = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        DataStatus()._check_prop(value)
        self._status = value

    @property
    def confidentiality(self):
        return self._confidentiality

    @confidentiality.setter
    def confidentiality(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for confidentiality. Must be '
                f'float.')
        self._confidentiality = value


class Device(_CyberObject):
    """Class for Device object

    Attributes
    ----------

    """

    _type = "Device"

    def __init__(self, device_types=None, is_virtual=None, role=None,
            device_identifier=None, network_interfaces=None, **kwargs):
        super().__init__(**kwargs)
        if device_types:
            self.device_types = device_types
        if is_virtual:
            self.is_virtual = is_virtual
        if role:
            self.role = role
        if device_identifier:
            self.device_identifier = device_identifier
        if network_interfaces:
            self.network_interfaces = network_interfaces

    @property
    def device_types(self):
        return self._device_types

    @device_types.setter
    def device_types(self, value):
        DeviceType()._check_prop(value)
        self._device_types = value

    @property
    def is_virtual(self):
        return self._is_virtual

    @is_virtual.setter
    def is_virtual(self, value):
        if not isinstance(value, bool):
            raise TypeError(
                f'{type(value)} is not a valid type for is_virtual. Must be '
                f'boolean.')
        self._is_virtual = value

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for role. Must be '
                f'string.')
        self._role = value

    @property
    def device_identifier(self):
        return self._device_identifier

    @device_identifier.setter
    def device_identifier(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for device_identifier. Must be '
                f'string.')
        self._device_identifier = value

    @property
    def network_interfaces(self):
        return self._network_interfaces

    @network_interfaces.setter
    def network_interfaces(self, value):
        NetworkInterface()._check_prop(value)
        self._network_interfaces = value


class Network(_CyberObject):
    """Class for Network object
    
    Attributes
    ----------

    """

    _type = "Network"

    def __init__(self, protocol=None, mask=None, **kwargs):
        super().__init__(**kwargs)
        if protocol:
            self.protocol = protocol

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        NetworkProtocolType()._check_prop(value)
        self._protocol = value

    @property
    def mask(self):
        return self._mask

    @mask.setter
    def mask(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for mask. Must be '
                f'string.')
        self._mask = value


class NetworkInterface(_CyberObject):
    _type = "NetworkInterface"

    def __init__(self, name=None, address=None, **kwargs):
        super().__init__(**kwargs)
        if name:
            self.name = name
        if address:
            self.address = address

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for name. Must be '
                f'string.')
        self._name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for address. Must be '
                f'string.')
        self._address = value


class NetworkLink(_CyberObject):
    """Class for NetworkLink object"""

    _type = "NetworkLink"

    def __init__(self, is_logical=None, physical_layer=None, 
            data_link_protocol=None, bandwidth=None, latency=None, jitter=None,
            network_interfaces=None, **kwargs):
        super().__init__(**kwargs)
        if is_logical:
            self.is_logical = is_logical
        if physical_layer:
            self.physical_layer = physical_layer
        if data_link_protocol:
            self.data_link_protocol = data_link_protocol
        if bandwidth:
            self.bandwidth = bandwidth
        if latency:
            self.latency = latency
        if jitter:
            self.jitter = jitter
        if network_interfaces:
            self.network_interfaces = network_interfaces

    @property
    def is_logical(self):
        return self._is_logical

    @is_logical.setter
    def is_logical(self, value):
        if not isinstance(value, bool):
            raise TypeError(
                f'{type(value)} is not a valid type for is_logical. Must be '
                f'boolean.')
        self._is_logical = value

    @property
    def physical_layer(self):
        return self._physical_layer

    @physical_layer.setter
    def physical_layer(self, value):
        PhysicalLayerType()._check_prop(value)
        self._physical_layer = value

    @property
    def data_link_protocol(self):
        return self._data_link_protocol

    @data_link_protocol.setter
    def data_link_protocol(self, value):
        DataLinkProtocolType()._check_prop(value)
        self._data_link_protocol = value

    @property
    def bandwidth(self):
        return self._bandwidth

    @bandwidth.setter
    def bandwidth(self, value):
        if not isinstance(value, int):
            raise TypeError(
                f'{type(value)} is not a valid type for bandwidth. Must be '
                f'int.')
        self._bandwidth = value

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, value):
        if not isinstance(value, int):
            raise TypeError(
                f'{type(value)} is not a valid type for latency. Must be '
                f'int.')
        self._latency = value
    
    @property
    def jitter(self):
        return self._jitter

    @jitter.setter
    def jitter(self, value):
        if not isinstance(value, int):
            raise TypeError(
                f'{type(value)} is not a valid type for jitter. Must be '
                f'int.')
        self._jitter = value

    @property
    def network_interfaces(self):
        return self._network_interfaces

    @network_interfaces.setter
    def network_interfaces(self, value):
        NetworkInterface()._check_prop(value)
        self._network_interfaces = value


class Persona(_CyberObject):
    """Class for Persona object"""

    _type = "Persona"


class System(_CyberObject):
    """Class for System object
    
    Attributes
    ----------
    system_type : SystemType
        From the enumerated list of SystemType
    """

    _type = "System"

    def __init__(self, system_type=None, **kwargs):
        super().__init__(**kwargs)
        if system_type:
            self.system_type = system_type

    @property
    def system_type(self):
        return self._system_type

    @system_type.setter
    def system_type(self, value):
        SystemType()._check_prop(value)
        self._system_type = value


#### Fourth level CyberDEM CyberObjects
class OperatingSystem(_CyberObject):
    """Class for OperatingSystem object 

    Attributes
    ----------
    os_type : OperatingSystemType
        From the enumerated list of OperatingSystemType
    """

    _type = "OperatingSystem"

    def __init__(self, os_type=None, **kwargs):
        super().__init__(**kwargs)
        if os_type:
            self.os_type = os_type

    @property
    def os_type(self):
        return self._os_type

    @os_type.setter
    def os_type(self, value):
        OperatingSystemType()._check_prop(value)
        self._os_type = value


class Service(Application):
    """Class for Service object 

    Attributes
    ----------
    service_type : ServiceType
        From the enumerated list of ServiceType
    address : string
        ??
    """

    _type = "Service"

    def __init__(self, service_type=None, address=None, **kwargs):
        super().__init__(**kwargs)
        if service_type:
            self.service_type = service_type
        if address:
            self.address = address

    @property
    def service_type(self):
        return self._service_type

    @service_type.setter
    def service_type(self, value):
        ServiceType()._check_prop(value)
        self._service_type = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for address. Must be '
                f'string.')
        self._address = value


#### Fourth level CyberDEM CyberEvents
class CyberAttack(_CyberAction):
    """Class for CyberAttack object 

    Attributes
    ----------
    none
    """

    _type = "CyberAttack"

    
class CyberDefend(_CyberAction):
    """Class for CyberDefend object 

    Attributes
    ----------
    none
    """

    _type = "CyberDefend"

    
class CyberRecon(_CyberAction):
    """Class for CyberRecon object 

    Attributes
    ----------
    recon_type : ReconType
        From the enumerated list of ReconType
    """

    _type = "CyberRecon"

    def __init__(self, recon_type=None, **kwargs):
        super().__init__(**kwargs)
        if recon_type:
            self.recon_type = recon_type

    @property
    def recon_type(self):
        return self._recon_type

    @recon_type.setter
    def recon_type(self, value):
        ReconType()._check_prop(value)
        self._recon_type = value


class Deny(_CyberEffect):
    """Class for Deny object 

    Attributes
    ----------
    none
    """

    _type = "Deny"


class Detect(_CyberEffect):
    """Class for Detect object 

    Attributes
    ----------
    acquired_information : dict
        ??
    """

    _type = "Detect"

    def __init__(self, acquired_information=None, **kwargs):
        super().__init__(**kwargs)
        if acquired_information:
            self.acquired_information = acquired_information

    @property
    def acquired_information(self):
        return self._acquired_information

    @acquired_information.setter
    def acquired_information(self, value):
        if not isinstance(value, dict):
            raise TypeError(
                f'{type(value)} is not a valid type for acquired_information. Must be '
                f'dict.')
        self._acquired_information = value
    

class Manipulate(_CyberEffect):
    """Class for Manipulate object 

    Attributes
    ----------
    description : string
        ?? desc ??
    """

    _type = "Manipulate"

    def __init__(self, description=None, **kwargs):
        super().__init__(**kwargs)
        if description:
            self.description = description

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for description. Must be '
                f'string.')
        self._description = value

    
#### Fifth level CyberDEM CyberEvents
class DataExfiltration(CyberAttack):
    """Class for DataExfiltration object 

    Attributes
    ----------
    none
    """

    _type = "DataExfiltration"


class Destroy(Deny):
    """Class for Destroy object 

    Attributes
    ----------
    none
    """

    _type = "Destroy"


class Degrade(Deny):
    """Class for Degrade object 

    Attributes
    ----------
    none
    """

    _type = "Degrade"


class Disrupt(Deny):
    """Class for Disrupt object 

    Attributes
    ----------
    is_random : boolean
        ?? desc ??
    percentage : float
        ?? desc ??
    """

    _type = "Disrupt"

    def __init__(self, is_random=None, percentage=None, **kwargs):
        super().__init__(**kwargs)
        if is_random:
            self.is_random = is_random
        if percentage:
            self.percentage = percentage

    @property
    def is_random(self):
        return self._is_random

    @is_random.setter
    def is_random(self, value):
        if not isinstance(value, bool):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'boolean.')
        self._is_random = value

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'float.')
        self._percentage = value


class PacketManipulationEffect(Manipulate):
    """Class for PacketManipulationEffect object 

    Attributes
    ----------
    manipulation_type : PacketManipulationType
        ?? desc ??
    percentage : float
        ?? desc ??
    """

    _type = "PacketManipulationEffect"

    def __init__(self, manipulation_type=None, attack_content=None, **kwargs):
        super().__init__(**kwargs)
        if manipulation_type:
            self.manipulation_type = manipulation_type
        if attack_content:
            self.attack_content = attack_content

    @property
    def manipulation_type(self):
        return self._manipulation_type

    @manipulation_type.setter
    def manipulation_type(self, value):
        PacketManipulationType()._check_prop(value)
        self._manipulation_type = value

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'float.')
        self._percentage = value


class ManipulationAttack(CyberAttack):
    """Class for ManipulationAttack object 

    Attributes
    ----------
    description : string
        Describes the "what and how" of the manipulation attack
    attack_content : string
        Could contain the details of the manipulation attack itself OR the 
            manipulated message after the attack
    """

    _type = "ManipulationAttack"

    def __init__(self, description=None, attack_content=None, **kwargs):
        super().__init__(**kwargs)
        if description:
            self.description = description
        if attack_content:
            self.attack_content = attack_content

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for description. Must be '
                f'string.')
        self._description = value

    @property
    def attack_content(self):
        return self._attack_content

    @attack_content.setter
    def attack_content(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for attack_content. Must be '
                f'string.')
        self._attack_content = value


class PhishingAttack(CyberAttack):
    """Class for PhishingAttack object 

    Attributes
    ----------
    type : MessageType
        From the MessageType enumeration
    header : string
        Header of the message
    body : string
        Message body
    """

    _type = "PhishingAttack"

    def __init__(self, message_type=None, header=None, body=None, **kwargs):
        super().__init__(**kwargs)
        if message_type:
            self.message_type = message_type
        if header:
            self.header = header
        if body:
            self.body = body

    @property
    def message_type(self):
        return self._message_type

    @message_type.setter
    def message_type(self, value):
        MessageType()._check_prop(value)
        self._message_type = value

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for header. Must be '
                f'string.')
        self._header = value

    @property
    def body(self):
        return self._body

    @body.setter
    def body(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for body. Must be '
                f'string.')
        self._body = value


###### Sixth level CyberDEM CyberEvents --> CyberEffects
class BlockTrafficEffect(Disrupt):
    """Class for BlockTrafficEffect object 

    Attributes
    ----------
    none
    """

    _type = "BlockTrafficEffect"


class HardwareDamageEffect(Destroy):
    """Class for HardwareDamageEffect object 

    Attributes
    ----------
    damage_type : HardwareDamageType
        From the HardwareDamageType enumeration
    """

    _type = "HardwareDamageEffect"

    def __init__(self, damage_type=None, **kwargs):
        super().__init__(**kwargs)
        if damage_type:
            self.damage_type = damage_type

    @property
    def damage_type(self):
        return self._damage_type

    @damage_type.setter
    def damage_type(self, value):
        HardwareDamageType()._check_prop(value)
        self._damage_type = value


class LoadRateEffect(Degrade):
    """Class for LoadRateEffect object 

    Attributes
    ----------
    percentage : float
        ?? desc ??
    rate_type : LoadRateType
        From the LoadRateType enumeration
    """

    _type = "LoadRateEffect"

    def __init__(self, percentage=None, rate_type=None, **kwargs):
        super().__init__(**kwargs)
        if percentage:
            self.percentage = percentage
        if rate_type:
            self.rate_type = rate_type

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'float.')
        self._percentage = value

    @property
    def rate_type(self):
        return self._rate_type

    @rate_type.setter
    def rate_type(self, value):
        LoadRateType()._check_prop(value)
        self._rate_type = value


class DelayEffect(Degrade):
    """Class for DelayEffect object 

    Attributes
    ----------
    seconds : float
        ?? desc ??
    """

    _type = "DelayEffect"

    def __init__(self, seconds=None, **kwargs):
        super().__init__(**kwargs)
        if seconds:
            self.seconds = seconds

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for seconds. Must be '
                f'float.')
        self._seconds = value


class JitterEffect(Degrade):
    """Class for JitterEffect object 

    Attributes
    ----------
    milliseconds : float
        ?? desc ??
    """

    _type = "JitterEffect"

    def __init__(self, milliseconds=None, **kwargs):
        super().__init__(**kwargs)
        if milliseconds:
            self.milliseconds = milliseconds

    @property
    def milliseconds(self):
        return self._milliseconds

    @milliseconds.setter
    def milliseconds(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for milliseconds. Must be '
                f'float.')
        self._milliseconds = value


class CPULoadEffect(Degrade):
    """Class for CPULoadEffect object 

    Attributes
    ----------
    percentage : float
        ?? desc ??
    """

    _type = "CPULoadEffect"

    def __init__(self, percentage=None, **kwargs):
        super().__init__(**kwargs)
        if percentage:
            self.percentage = percentage

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'float.')
        self._percentage = value


class MemoryUseEffect(Degrade):
    """Class for MemoryUseEffect object 

    Attributes
    ----------
    percentage : float
        ?? desc ??
    """

    _type = "MemoryUseEffect"

    def __init__(self, percentage=None, **kwargs):
        super().__init__(**kwargs)
        if percentage:
            self.percentage = percentage

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'float.')
        self._percentage = value


class DropEffect(Degrade):
    """Class for DropEffect object 

    Attributes
    ----------
    percentage : float
        ?? desc ??
    """

    _type = "DropEffect"

    def __init__(self, percentage=None, **kwargs):
        super().__init__(**kwargs)
        if percentage:
            self.percentage = percentage

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'float.')
        self._percentage = value


class HardwareDegradeEffect(Degrade):
    """Class for HardwareDegradeEffect object 

    Attributes
    ----------
    degrade_type : HardwareDegradeType
        From the HardwareDegradeType enumeration
    percentage : float
        ?? desc ??
    """

    _type = "HardwareDegradeEffect"

    def __init__(self, degrade_type=None, percentage=None, **kwargs):
        super().__init__(**kwargs)
        if degrade_type:
            self.degrade_type = degrade_type
        if percentage:
            self.percentage = percentage

    @property
    def degrade_type(self):
        return self._degrade_type

    @degrade_type.setter
    def degrade_type(self, value):
        HardwareDegradeType()._check_prop(value)
        self._degrade_type = value

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'float.')
        self._percentage = value


class OtherDegradeEffect(Degrade):
    """Class for OtherDegradeEffect object 

    Attributes
    ----------
    percentage : float
        ?? desc ??
    description : string
        ?? desc ??
    """

    _type = "OtherDegradeEffect"

    def __init__(self, percentage=None, description=None, **kwargs):
        super().__init__(**kwargs)
        if percentage:
            self.percentage = percentage
        if description:
            self.description = description

    @property
    def percentage(self):
        return self._percentage

    @percentage.setter
    def percentage(self, value):
        if not isinstance(value, float):
            raise TypeError(
                f'{type(value)} is not a valid type for percentage. Must be '
                f'float.')
        self._percentage = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError(
                f'{type(value)} is not a valid type for description. Must be '
                f'string.')
        self._description = value