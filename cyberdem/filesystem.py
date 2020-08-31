"""CyberDEM FileSystem Module"""

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


import base
import inspect
import json
import os


class FileSystem():
    
    # find the types of objects allowed from the base module and map the "type"
    # attribute to the class method 
    obj_types = {}
    for name, obj in inspect.getmembers(base):
        if inspect.isclass(obj) and obj.__module__ == 'base':
            if obj._type:
                obj_types[obj._type] = obj

    def __init__(self, path):
        if not os.path.isdir(path):
            print(f'Creating new FileSystem path {path}.')
            os.mkdir(path)
        else:
            print(f'Using existing FileSystem at {path}')
        self.path = path
        self.folders = []
        for folder in os.listdir(self.path):
            if os.path.isdir(os.path.join(self.path, folder)):
                self.folders.append(folder)


    def save(self, objects):
        if not isinstance(objects, list):
            objects = [objects]
        for obj in objects:
            if obj._type not in self.folders:
                self._create_folder(obj._type)

            # @TODO - check before overwriting existing file

            filepath = os.path.join(self.path, obj._type, obj.id)
            serialized = obj._serialize()
            with open(filepath + '.json', 'w') as outfile: 
                json.dump(serialized, outfile, indent=4)
            outfile.close()


    def get(self, ids, obj_type=None):
        """Get an object or list of objects by ID

        :param ids: UUIDs to search for
        :type ids: string or list of strings, required
        :param obj_type: CyberDEM type of the id(s). Ex. "Application"
        :type obj_type: string, optional

        :return: instance(s) of the requested object(s) 
        :rtype: object or list of objects, or None if no matching IDs are found
        """

        # ensure the obj_type specified is allowed
        if obj_type:
            if obj_type not in self.obj_types:
                raise Exception(f'obj_type "{obj_type}" is not an allowed '
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
                if os.path.isfile(os.path.join(filepath, i) +'.json'):
                    with open(os.path.join(filepath, i) +'.json') as json_file:
                        obj = json.load(json_file)
                    json_file.close()
            else:
                # otherwise, you have to search through the whole directory
                for root, dirs, files in os.walk(filepath):
                    if i+'.json' in files:
                        obj_type = os.path.split(root)[1]
                        print(os.path.join(root, i) +'.json')
                        with open(os.path.join(root, i) +'.json') as json_file:
                            obj = json.load(json_file)
                        json_file.close()
            found_objects.append(self.obj_types[obj_type](**obj))
        if len(found_objects) == 1:
            return found_objects[0]
        elif len(found_objects) == 0:
            return None
        else:
            return found_objects

    # @TODO
    def query(self, query_string):
        pass

    def _create_folder(self, folder_name):
        """Creates a sub-folder in the FileSystem path

        :param folder_name: should match one of the CyberDEM base classes
        :type folder_name: string, required
        """

        # sub-folders should match the public classes in the base module
        if folder_name in self.obj_types:
            os.mkdir(self.path + '/' + folder_name)
            self.folders.append(folder_name)
        else:
            raise Exception(f'The folder_name "{folder_name}" does not match '
                f'the base classes for CyberDEM.')
        