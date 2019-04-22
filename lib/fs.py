def readfile(filename):
    f = open(filename)
    content = f.read()
    f.close()
    return content
