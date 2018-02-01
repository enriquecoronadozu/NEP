import simplejson

def json2dict(s, **kwargs):
    """Convert JSON to python dictionary. See jsonapi.jsonmod.loads for details on kwargs.
     
        Parameters
        ----------
        s: string
            string with the content of the json data

        Returns:
        ----------
        d: dictionary
            dictionary with the content of the json data
    """
    
    if str is unicode and isinstance(s, bytes):
        s = s.decode('utf8')
    
    return simplejson.loads(s, **kwargs)

def dict2json(o, **kwargs ):
    """ Load object from JSON bytes (utf-8). See jsonapi.jsonmod.dumps for details on kwargs.
     
        Parameters
        ----------
        o: dictionary
            dictionary to convert
            

        Returns:
        ----------
        d: string
            string in json format

    """
        
    if 'separators' not in kwargs:
        kwargs['separators'] = (',', ':')
        
    s = simplejson.dumps(o, **kwargs)
        
    if isinstance(s, unicode):
        s = s.encode('utf8')
        
    return s

def read_json(json_file):
    """ Read a json file and return a string 
        
        Parameters
        ----------
        json file:string
            Path +  name + extension of the json file

        Returns:
        ----------
        json_data: string
            string with the content of the json data

    """
    json_data = open (json_file).read()
    return json_data