#!/users/eprakash/anaconda2/bin/python

def fillPlaceholders(filename, s):
        tmpfilename = filename+".tmp"
        print filename
        fp=open(filename)
        tmpfp=open(tmpfilename, "w+")
        for line in fp:
                line=line.replace('_place_holder', s)
                tmpfp.write(line)
        fp.close()
        tmpfp.close()

fillPlaceholders('testfile', 'replaced!')
