from os import listdir
from os.path import isfile, join
import simplejson

def json2dict(s, **kwargs):
    """Load object from JSON bytes (utf-8).
    
    See jsonapi.jsonmod.loads for details on kwargs.
    """
    
    if str is unicode and isinstance(s, bytes):
        s = s.decode('utf8')
    
    return simplejson.loads(s, **kwargs)

def read_json(json_file):
    """ Read a json file and return a string 
        
        Parameters
        ----------
        json_file:string
            Path +  name + extension of the json file

        Returns:
        ----------
        json_data: string
            string with the content of the json data

    """
    json_data = open (json_file).read()
    return json_data

def getFiles(path):
    """ Get a list of files that are inside a folder
        
        Parameters
        ----------
        path: string
            path of the folder

        Returns:
        ----------
        onlyfiles: list 
            list of strings with the name of the files in the folder

    """
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    print ("Available primitives:" +  str(onlyfiles))
    return onlyfiles