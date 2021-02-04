import datetime

class Signals():
    def __init__(self,*args,**kwargs):
        self.model = kwargs.get("model")
        self.instance = kwargs.get("instance")
    def save_created_date(self):
        self.instance.created = datetime.datetime.now()
        self.instance.save()
    def save_updated_date(self):
        self.model.objects.filter(pk=self.instance.id).update(updated=datetime.datetime.now())