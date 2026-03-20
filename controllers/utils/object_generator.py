# CREATE A CLASS OBJECT THAT RETURNS DATA AFTER BEING MODIFIED
class Generate_Object:
    def __init__(self, obj = {}):
        if obj:
            for key, value in obj.items():
                if isinstance(value,list) and len(value) > 0 and isinstance(value[0],dict):
                    vals = [Generate_Object(v) for v in value]
                    setattr(self, key, vals)
                elif isinstance(value,dict):
                    setattr(self, key, Generate_Object(value))
                else:
                    setattr(self, key, value)


# LETS EXTRACT THE VALUES FROM THE CLASS ABOVE
class Extract_Object:
    def __init__(self, obj):
        self.data = vars(obj) if isinstance(obj,Generate_Object) else obj
        self.extracted = {}
        if obj:
            for key, value in self.data.items():
                if isinstance(value, Generate_Object):
                    self.extracted[key] = vars(value)
                elif isinstance(value,list) and len(value) > 0 and isinstance(value[0], Generate_Object):
                    vals = []
                    for v in value:
                        ex = vars(v)
                        if isinstance(ex,dict):
                            new_values = {}
                            for k,vl in ex.items():
                                if isinstance(vl,Generate_Object):
                                    new_values[k] = vars(vl)
                                elif isinstance(vl,list) and len(vl) > 0 and isinstance(vl[0], Generate_Object):
                                    new_values[k] = [vars(xv) for xv in vl]
                                else:
                                    new_values[k] = vl
                            vals.append(new_values)
                    self.extracted[key] = vals

                else:
                     self.extracted[key] = value
