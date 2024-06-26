import os

def list_files(path, d=0):
    #print('\n'+path, end = '')
    nlines = 0
    if os.path.isfile(path):
        if path[-3:]=='.py':
            nlines = len(open(path).readlines())
            while len(path) > 25:
                path = path[1:]
            while len(path) < 25:
                path = ' '+path
            print(path+' '+str(nlines))
            return nlines
    elif '.' not in path and '__' not in path:
        for sub in (os.listdir(path) if path else os.listdir()):
            sub = os.path.join(path, sub)
            nlines += list_files(sub, d+1)
    return nlines

print(' '*(25-len('total'))+'total '+str(list_files('',-1)))
