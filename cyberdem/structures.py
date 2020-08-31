"""CyberDEM Structures Module"""

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

from enumerations import RelationshipType


class Relationship():
    """[summary]

    :raises TypeError: [description]
    :raises TypeError: [description]
    :raises TypeError: [description]
    :return: [description]
    :rtype: [type]
    """

    def __init__(self, related_object_id=None, relationship_type=None,
            priviledges=None):
        self.related_object_id = related_object_id
        if relationship_type:
            self.relationship_type = relationship_type
        if priviledges:
            self.priviledges = priviledges

    @property
    def related_object_id(self):
        return self._related_object_id

    @related_object_id.setter
    def related_object_id(self, value):
        if value is None:
            raise TypeError(
                f'Relationship object must have a related_object_id.')
        self._related_object_id = value

    @property
    def relationship_type(self):
        return self._relationship_type

    @relationship_type.setter
    def relationship_type(self, value):
        RelationshipType()._check_prop(value)
        self._relationship_type = value
    
    @property
    def priviledges(self):
        return self._priviledges

    @priviledges.setter
    def priviledges(self, value):
        if not isinstance(value, list):
            raise TypeError(
                f'{type(value)} is not a valid type for priviledges. Must '
                f'be list of strings.')
        for v in value:
            if not isinstance(v, str):
                raise TypeError(
                    f'RelatedObject privilege list takes only string types')
        self._priviledges = value
