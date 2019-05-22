
def images(df):
    im = []
    for item in df.Filepath:
        im.append(item)
    return im

def titles(df):
    ttls = []
    for item in df.Title:
        ttls.append(item)
    return ttls

def summaries(df):
    mmrs = []
    for item in df.Summary:
        mmrs.append(item)
    return mmrs

def numbers(df):
    ns = []
    for item in df.No:
        ns.append(item)
    return ns