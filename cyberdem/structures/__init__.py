"""
CyberDEM Structures Module provides classes for CyberDEM DataTypes

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
"""


import uuid
from cyberdem.enumerations import RelationshipType


class Relationship():
    """Represents a relationship between two CyberObjects.

    Given two CyberObjects A and B, where A administers B, the
    ``related_object_struct`` would be represented as (A_ID, "Administers",
    B_ID).

    :param related_object_struct: defines the relationship between the two
        objects; format: (ObjA_ID_string,
        :class:`~cyberdem.enumerations.RelationshipType` string,
        ObjB_ID_string)
    :type related_object_struct: 3-tuple, required
    :param id: string formatted UUIDv4 prefixed with "relationship--"
    :type id: string, optional
    :param privileges: [desc]
    :type privileges: list of strings, optional

    :raises ValueError: if the provided ``id`` is not a string formatted UUIDv4
        prefixed with "relationship--"

    :Example:
        >>> from cyberdem.base import Application,Device
        >>> my_application = Application()
        >>> my_device = Device()
        >>> rel_struct = (my_application.id, 'Administers', my_device.id)
        >>> my_rel = Relationship(rel_struct, privileges=['priv1', 'priv2'])
    """

    def __init__(self, related_object_struct, id=None, privileges=None):
        if id is None:
            id = 'relationship--' + str(uuid.uuid4())
        self.id = id
        self.related_object_struct = related_object_struct
        if privileges:
            self.privileges = privileges

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        try:
            uuid.UUID(value.replace('relationship--', ''))
        except ValueError:
            raise ValueError(
                f'"{value}" is not a valid value for id. Must be a UUIDv4.')
        self._id = value

    @property
    def related_object_struct(self):
        return self._related_object_struct

    @related_object_struct.setter
    def related_object_struct(self, value):
        if not isinstance(value, tuple):
            raise TypeError(
                f'{type(value)} is not a valid type for related_object_struct.'
                f' Must be a 3-tuple. Ex. "(object_A_ID, RelationshipType, '
                f'object_B_ID)"')
        if len(value) != 3:
            raise ValueError(
                f'related_object_struct should have three items. Ex. '
                f'"(object_A_ID, RelationshipType, object_B_ID)"')
        RelationshipType()._check_prop(value[1])
        self._related_object_struct = value

    @property
    def privileges(self):
        return self._privileges

    @privileges.setter
    def privileges(self, value):
        if not isinstance(value, list):
            raise TypeError(
                f'{type(value)} is not a valid type for privileges. Must '
                f'be list of strings.')
        for v in value:
            if not isinstance(v, str):
                raise TypeError(
                    f'RelatedObject privilege list takes only string types')
        self._privileges = value
