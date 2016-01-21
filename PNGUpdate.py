#encoding:utf-8
from struct import *
from zlib import *
import stat
import sys
import os
import argparse
class PNGproccess():
    def __init__(self,filepath):
        self.filepath=filepath
    def getFile(self):
        _dir=[]
        pngs=[]
        path=self.filepath
        files= os.listdir(str(path))
        for file in files:
                filepath=os.path.join(path,file)
                if file[-4:].lower()=='.png':
                    pngs.append(filepath)
        return pngs
    def setPNG(self,path):
        pngheader = "\x89PNG\r\n\x1a\n"

        file = open(path, "rb")
        oldPNG = file.read()
        file.close()

        if oldPNG[:8] != pngheader:
            return None

        newPNG = oldPNG[:8]

        chunkPos = len(newPNG)

    # For each chunk in the PNG file
        while chunkPos < len(oldPNG):

        # Reading chunk
            chunkLength = oldPNG[chunkPos:chunkPos+4]
            chunkLength = unpack(">L", chunkLength)[0]
            chunkType = oldPNG[chunkPos+4 : chunkPos+8]
            chunkData = oldPNG[chunkPos+8:chunkPos+8+chunkLength]
            chunkCRC = oldPNG[chunkPos+chunkLength+8:chunkPos+chunkLength+12]
            chunkCRC = unpack(">L", chunkCRC)[0]
            chunkPos += chunkLength + 12

        # Parsing the header chunk
            if chunkType == "IHDR":
                width = unpack(">L", chunkData[0:4])[0]
                height = unpack(">L", chunkData[4:8])[0]

        # Parsing the image chunk
            if chunkType == "IDAT":
                try:
                # Uncompressing the image chunk
                    bufSize = width * height * 4 + height
                    chunkData = decompress( chunkData, -8, bufSize)

                except Exception, e:
                # The PNG image is normalized
                    return None

            # Swapping red & blue bytes for each pixel
                newdata = ""
                for y in xrange(height):
                    i = len(newdata)
                    newdata += chunkData[i]
                    for x in xrange(width):
                        i = len(newdata)
                        newdata += chunkData[i+2]
                        newdata += chunkData[i+1]
                        newdata += chunkData[i+0]
                        newdata += chunkData[i+3]

            # Compressing the image chunk
                chunkData = newdata
                chunkData = compress( chunkData )
                chunkLength = len( chunkData )
                chunkCRC = crc32(chunkType)
                chunkCRC = crc32(chunkData, chunkCRC)
                chunkCRC = (chunkCRC + 0x100000000) % 0x100000000

        # Removing CgBI chunk
            if chunkType != "CgBI":
                newPNG += pack(">L", chunkLength)
                newPNG += chunkType
                if chunkLength > 0:
                    newPNG += chunkData
                newPNG += pack(">L", chunkCRC)

        # Stopping the PNG file parsing
            if chunkType == "IEND":
                break

        return newPNG
    def lastsetPNG(self,path):
        data = self.setPNG(path)
        if data != None:
            file = open(path, "wb")
            file.write(data)
            file.close()
            return True
        return data
    def main(self):
        pngs=self.getFile()
        complicated=0
        if len(pngs)==0:
            sys.exit()
        while 1 :
            for ipng in xrange(len(pngs)):
                perc= (float(ipng)/len(pngs))*100.0
                print "%.2f%% %s" % (perc, pngs[ipng])
                if self.lastsetPNG(pngs[ipng]):
                    complicated +=1
            break


if __name__=="__main__":
    parse= argparse.ArgumentParser()
    parse.add_argument('-d','--dir',dest='Path',help='file path',action='store')
    #args=['-d','C:\Users\haha\Desktop\\123\Payload\CpicJczc.app']
    args=parse.parse_args()
    if args.Path:
        pn=PNGproccess(args.Path)
        pn.main()
    else:
        print'''
        Useage : input you file path
        '''
        sys.exit()

