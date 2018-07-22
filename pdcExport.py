

import os, sys, struct

class BinaryFileWriter:
    def __init__(self, filename):
        self.__f = file(filename, "wb")
    def WriteByte(self, b):
        self.__f.write(struct.pack('>B', b))
    def WriteInt(self, i):
        self.__f.write(struct.pack('>i', int(i)))
    def WriteUint(self, i):
        self.__f.write(struct.pack('>I', int(i)))
    def WriteString(self, str, size):
        fmt = "<%is" % size
        self.__f.write(struct.pack(fmt, str))
    def WriteFloat(self, f):
        self.__f.write(struct.pack('>f', float(f)))
    def WriteDouble(self, d):
        self.__f.write(struct.pack('>d', float(d)))
    def Close(self):
        self.__f.close()

def pdcExport():
    #exportparmsdir = os.environ["SHOT_PATH_"] + "/maya/particles/pt/"
    #cmd = "unix mkdir -p " + exportparmsdir
    #hou.hscript(cmd)
    startfrm = hou.hscriptExpression("$RFSTART")
    endfrm = hou.hscriptExpression("$RFEND")
    frm = startfrm
    src = hou.node("/obj/pdc_export1/processing/swate")
    geo = src.geometry()
    ptlist = list()


    #while frm <= endfrm:

    #set frame
    frm=hou.frame()
    cmd = "fcur " + str(int(frm))
    hou.hscript(cmd)
    
    ptframe=str(250*frm)
    ptframe=ptframe.replace('.0','')
    #filepath='/jobs/canon_stars/sequences/rnd/rnd001/maya/particles/pt/particleShape2.'+ptframe+'.pdc'
    filepath='C:/Users/hiro/Desktop/houdiniptShape.'+ptframe+'.pdc'
    
    bfw=BinaryFileWriter(filepath)
    #header
    #format
    bfw.WriteString("PDC ",4)
    #format version
    bfw.WriteInt(1)
    #byteOrder
    bfw.WriteInt(1)
    #extra
    bfw.WriteInt(0)
    #extra
    bfw.WriteInt(0)
    
    #num of Particles
    bfw.WriteInt(len(geo.points()))
    #num of Attr
    
    #attrList={'position':'translate','rotationPP':'rotate','scalePP':'scale'}
    attrList={'position':{'attrName':'translate','attrType':5},\
                #'rotationPP':{'attrName':'rotate','attrType':5},\
                'scalePP':{'attrName':'scale','attrType':5},\
                'particleId':{'attrName':'id','attrType':3}}\
                #'velocity':{'attrName':'v','attrType':5}}
    attrNum=len(attrList)
    bfw.WriteInt(attrNum)
    
    #print 'start'
    for attr in attrList:
        #attrNameLength
        bfw.WriteInt(len(attr))
        #attrName
        bfw.WriteString(attr,len(attr))
        #attrType
        type=attrList[attr]['attrType']
        bfw.WriteInt(type)    
    
        #print attr
        #print attrList[attr]['attrName']
        #print type
        #integer:Per-Obj
        if type==0:
            break
        #integer array:Per-Particle
        elif type==1:
            for point in geo.points():
                buff=point.attribValue(attrList[attr]['attrName'])
                #print("test")
                bfw.WriteInt(buff)
        #double:Per-Obj
        elif type==2:
            break
        #double array:Per-Particle
        elif type==3:
            for point in geo.points():
                #print("darray_test")
                #buff=point.attribValue('id')
                buff=point.attribValue(attrList[attr]['attrName'])
                #print attrList[attr]['attrName']
                #print buff
                bfw.WriteDouble(buff)
        #vector:Per-Obj
        elif type==4:
            break
        #vector array:Per-Particle
        elif type==5:
            for point in geo.points():
                buff=point.floatListAttribValue(attrList[attr]['attrName'])
                #print("varray_test")
                bfw.WriteDouble(buff[0])
                bfw.WriteDouble(buff[1])
                bfw.WriteDouble(buff[2])
        else:
            break

        #bfw.Close()
        #frm +=1
