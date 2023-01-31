
def deractor(fn):
    def wrapper(request,*args,**kwargs):
        if request.method.lower() == 'post':
            return fn(request,*args,**kwargs)
        else:
            pass
    return wrapper