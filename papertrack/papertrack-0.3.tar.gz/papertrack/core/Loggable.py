
import inspect
import json 
import datetime

class Loggable:
    def __init__(self, obj, journal_location) -> None:
        self.obj = obj
        self.journal_location = journal_location
    
    def __getattr__(self, attr):
        if callable(getattr(self.obj, attr)):
            journal_entry = {
                "operation": attr,
                "component": self.obj.name,
                "data": {}, 
                "timestamp": datetime.datetime.now().strftime(r"%Y-%m-%d-%H-%M-%S"),
                "object_data": {k: str(getattr(self.obj, k)) 
                    for k in dir(self.obj) if not k.startswith("__") and not callable(getattr(self.obj, k))
                }
            } 
            def _callable(*args, **kw):
                for k, v in zip(inspect.getfullargspec(getattr(self.obj, attr))[0], [self.obj] + list(args)):
                    journal_entry["data"][k] = str(v)
                for k,v in kw.items():
                    journal_entry["data"][k] = str(v)
                result = getattr(self.obj, attr)(*args, **kw)
                journal_entry["result"] = str(result)
                journal = [] 
                try:
                    with open(self.journal_location, "r") as f:
                        journal = json.loads(f.read())
                except FileNotFoundError:
                    pass
                with open(self.journal_location, "w") as f:
                    journal.append(journal_entry)
                    f.write(json.dumps(journal, indent=5))
                return result
            return _callable
        else:
            return getattr(self.obj, attr)

            