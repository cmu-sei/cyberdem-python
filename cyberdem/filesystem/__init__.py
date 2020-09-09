"""
CyberDEM FileSystem Module

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


from cyberdem import base
import inspect
import json
import os
import re


class FileSystem():
    """Create a directory structure and file storage and retrieval methods.

    Creates file storage, retrieval, and query methods for storing and
    retrieving CyberObjects, CyberEvents, and Relationships.

    :param path: directory path to store CyberDEM json files; can be existing
        directory or non-existing
    :type path: string, required

    :Example:
        >>> from cyberdem import filesystem
        >>> fs = filesystem.FileSystem("./test-fs")
        Using existing FileSystem at ./test-fs
        >>> fs.path
        './test-fs'
    """

    # find the types of objects allowed from the base module and map the "type"
    # attribute to the class method
    obj_types = {}
    for name, test_obj in inspect.getmembers(base, inspect.isclass):
        if test_obj.__module__ == 'cyberdem.base':
            if test_obj._type:
                obj_types[test_obj._type] = test_obj

    def __init__(self, path):
        """Creates a directory for storing CyberDEM objects and Events"""

        if not os.path.isdir(path):
            print(f'Creating new FileSystem path {path}.')
            os.mkdir(path)
        else:
            print(f'Using existing FileSystem at {path}')
        self.path = path
        self._folders = []
        for folder in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, folder)):
                self._folders.append(folder)

    def save(self, objects, overwrite=False):
        """Save CyberDEM objects and events to the FileSystem as json files

        :param objects: CyberDEM object or event instance (or list of
            instances)
        :type objects: CyberDEM class instance from :py:mod:`base`, or a list
            of objects
        :param overwrite: allow object with the same ID as one already in the
            FileSystem to overwrite the existing file, defaults to False
        :type overwrite: bool, optional

        :raises Exception: if object is already in FileSystem and overwrite is
            set to False

        :Example:
            >>> from cyberdem.base import Service
            >>> my_service = Service(
                    name='httpd', description='Apache web server',\
                    version='2.4.20', service_type='WebService',\
                    address='192.168.100.40')
            >>> fs.save(my_service)
            >>>
            $ ls ./test-fs/Service
            82ca4ed1-a053-4fc1-b1cc-f4b58b4dbf8c.json
        """

        if not isinstance(objects, list):
            objects = [objects]
        for obj in objects:
            if obj._type not in self._folders:
                self._create_folder(obj._type)

            filepath = os.path.join(self.path, obj._type, obj.id)

            if os.path.isfile(filepath+'.json') and not overwrite:
                raise Exception(
                    f'Object {obj.id} already exists in '
                    f'{self.path}. Add "overwrite=True" to overwrite.')

            serialized = obj._serialize()
            with open(filepath + '.json', 'w') as outfile:
                json.dump(serialized, outfile, indent=4)
            outfile.close()

    def get(self, ids, obj_type=None):
        """Get an object or list of objects by ID

        :param ids: UUID(s) of object(s) to retrieve
        :type ids: string or list of strings, required
        :param obj_type: CyberDEM type of the id(s). Ex. "Application"
        :type obj_type: string, optional

        :return: instance(s) of the requested object(s)
        :rtype: object or list of objects, or ``None`` if no matching IDs are
            found

        :Example:
            >>> my_object = fs.get("82ca4ed1-a053-4fc1-b1cc-f4b58b4dbf8c",\
                "Application")
            >>> str(my_object)
            Application(
                id: 82ca4ed1-a053-4fc1-b1cc-f4b58b4dbf8c
            )
            >>> my_objects = fs.get(["46545b7a-1840-4e34-a26f-aef5eb954b25",\
                "82ca4ed1-a053-4fc1-b1cc-f4b58b4dbf8c"])
            >>> for obj in my_obects:
            ... print(obj)
            Service(
                name='httpd',
                description='Apache web server',
                version='2.4.20',
                service_type='WebService',
                address='192.168.100.40'
            )
            Application(
                id: 82ca4ed1-a053-4fc1-b1cc-f4b58b4dbf8c
            )
        """

        # ensure the obj_type specified is allowed
        if obj_type:
            if obj_type not in self.obj_types:
                raise Exception(
                    f'obj_type "{obj_type}" is not an allowed '
                    f'CyberDEM base type. must be in {self.obj_types}"')
            filepath = os.path.join(self.path, obj_type)
        else:
            filepath = self.path

        if not isinstance(ids, list):
            ids = [ids]  # if only one id is given, convert to list

        found_objects = []
        for i in ids:
            if obj_type:
                # if the object type was specified the search is quicker
                if os.path.isfile(os.path.join(filepath, i) + '.json'):
                    with open(os.path.join(filepath, i) + '.json') as j_file:
                        obj = json.load(j_file)
                    j_file.close()
            else:
                # otherwise, you have to search through the whole directory
                for root, _, files in os.walk(filepath):
                    if i+'.json' in files:
                        obj_type = os.path.split(root)[1]
                        with open(os.path.join(root, i) + '.json') as j_file:
                            obj = json.load(j_file)
                        j_file.close()
            found_objects.append(self.obj_types[obj_type](**obj))
        if len(found_objects) == 1:
            return found_objects[0]
        elif len(found_objects) == 0:
            return None
        else:
            return found_objects

    def query(self, query_string):
        """Search the FileSystem for a specific object or objects

        :param query_string: SQL formatted query string
        :type query_string: string, required

        :return: attribute names (headers), values of matching objects
        :rtype: 2-tuple of lists

        :Example query strings:
            * ``SELECT * FROM *`` (you probably shouldn't do this one...)
            * ``SELECT attr1,attr2 FROM * WHERE attr3=value``
            * ``SELECT id,name,description FROM Device,System WHERE name='my \
                device'``
            * ``SELECT id FROM * WHERE (name='foo' AND description='bar') OR\
                 version<>'foobar'``

        :Example:
            >>> query = "SELECT id FROM * WHERE name='Rapid SCADA'"
            >>> fs.query(query)
            (['id'], [('9293510b-534b-4dd0-b7c5-78d92e279400',)])
            >>> query = "SELECT id,name FROM Application"
            >>> headers,results = fs.query(query)
            >>> headers
            ['id','name']
            >>> results
            [('9293510b-534b-4dd0-b7c5-78d92e279400',),\
            ('46545b7a-1840-4e34-a26f-aef5eb954b25','My application')]
        """

        # split the query string into the key components
        if not query_string.upper().startswith("SELECT "):
            raise Exception(
                f'query_string must start with "SELECT ". {query_string}')
        if " FROM " not in query_string.upper():
            raise Exception(
                f'query_string must contain "FROM" statement. {query_string}')
        q_select = query_string[7:query_string.find(" FROM ")]
        q_from = query_string[query_string.find(" FROM ")+6:]
        if " WHERE " in query_string.upper():
            q_where = query_string[query_string.find(" WHERE ")+7:]
            q_from = q_from[:q_from.find(" WHERE ")]
            q_where = q_where.replace('AND', 'and').replace('OR', 'or')
            q_where = q_where.replace('<>', '!=').replace('=', '==')
            q_where = q_where.replace(';', '')
        else:
            q_where = None

        # find all of the paths to search on (all of the object types)
        paths = []
        if q_from == "*":
            for obj_type in self.obj_types:
                if os.path.isdir(os.path.join(self.path, obj_type)):
                    paths.append(os.path.join(self.path, obj_type))
        else:
            for obj_type in q_from.split(','):
                if obj_type not in self.obj_types:
                    raise Exception(
                        f'obj_type "{obj_type}" is not an allowed '
                        f'CyberDEM base type. must be in {self.obj_types}"')
                paths.append(os.path.join(self.path, obj_type))

        # if the SELECT is *, find all possible class attributes to include
        if q_select == "*":
            get_attrs = []
            for path in paths:
                type_attrs = [
                    a for a in dir(self.obj_types[os.path.split(path)[1]])
                    if not a.startswith('_') and a not in get_attrs]
                get_attrs.extend(type_attrs)
            get_attrs.append('_type')
        else:
            get_attrs = q_select.split(',')

        # find all of the attribute names in the WHERE clause
        if q_where:
            clauses = re.split('and | or', q_where)
            where_attrs = []
            for c in clauses:
                if '==' in c:
                    operator = '=='
                elif '!=' in c:
                    operator = '!='
                elif '<' in c:
                    operator = '<'
                elif '>' in c:
                    operator = '>'
                elif '<=' in c:
                    operator = '<='
                elif '>=' in c:
                    operator = '>='
                else:
                    raise ValueError(f'Unrecognized operator in "{c}"')
                clause = re.split(operator, c)
                attr = clause[0].strip().lstrip('(')
                where_attrs.append((attr, operator))

        # search each file in each path for the desired attributes
        selected = []
        for path in paths:
            for f in os.listdir(path):
                with open(os.path.join(path, f)) as json_file:
                    obj_dict = json.load(json_file)
                json_file.close()

                # check for filtering criteria
                where_check = q_where
                if q_where is not None:
                    for attr in where_attrs:
                        # change out the attribute name in the WHERE clause
                        #   for their values from the current object
                        try:
                            obj_val = obj_dict[attr[0]]
                            where_check = where_check.replace(
                                ''.join(attr), "'"+obj_val+"'"+attr[1])
                        except KeyError:
                            where_check = where_check.replace(
                                ''.join(attr), "'"+attr[0]+"'"+attr[1])

                    matches = eval(where_check)
                    if not matches:
                        continue

                match = ()
                for attr in get_attrs:
                    try:
                        match += (obj_dict[attr],)
                    except KeyError:
                        match += (None,)
                selected.append(match)

        return get_attrs, selected

    def _create_folder(self, folder_name):
        """Creates a sub-folder in the FileSystem path

        :param folder_name: should match one of the CyberDEM base classes
        :type folder_name: string, required
        """

        # sub-folders should match the public classes in the base module
        if folder_name in self.obj_types:
            os.mkdir(self.path + '/' + folder_name)
            self._folders.append(folder_name)
        else:
            raise Exception(
                f'The folder_name "{folder_name}" does not match '
                f'the base classes for CyberDEM.')