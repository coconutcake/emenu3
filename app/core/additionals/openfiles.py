import json
import os

class File():
    def __init__(self,filepath):
        """Klasa operacji na każdych plikach"""
        # self.absolutepath=os.path.dirname(os.path.abspath(__file__))
        self.filepath = filepath
        if not filepath:
            raise ValueError("Wymagana sćieżka do pliku")
    def content(self):
        self.f = open(self.filepath, "r")
        return self.f
    def content_read(self):
        self.r = self.content()
        return self.r.read()
    def close(self):
        self.f.close()

class JsonFile(File):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def returnJsonFile(self):
        self.js = json.loads(self.content_read())
        self.close()
        return self.js

class Requirements(File):
    """Klasa operacji na pliku requirements.txt"""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def requirements_to_dict(self):
        return {i.strip().split('~=')[0]:i.strip().split('~=')[1] for i in self.content()}
    def requirements_to_json(self):
        return json.loads(json.dumps(self.requirements_to_dict()))
    def requirements_to_list(self):
        return [x+"=="+y for x,y in self.requirements_to_dict().items()]
    def requirements_install(self):
        for x in self.requirements_to_list():
            os.system("%s %s" % ("pip3 install",x))

