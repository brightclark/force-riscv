#
# Copyright (C) [2020] Futurewei Technologies, Inc.
#
# FORCE-RISCV is licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY OR
# FIT FOR A PARTICULAR PURPOSE.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Provide a bitstream utility

class Bitstream(object):

    def __init__(self, bitstream=""):
        self.bitstream = bitstream
    
    def stream(self):
        if self.bitstream.startswith('0x'):
            return self.convertHexToBin();
        else:
            return self.convert()
        
    def append(self, bitstream):
        self.bitstream += bitstream
        return self
        
    def prepend(self, bitstream):
        self.bitstream = bitstream + self.bitstream
        return self
    
    def value(self):
        val = ""
        for i in self.bitstream:
            if i == "1" or i == "0":
                val += i
            elif i == "X":
                val += "0000"
            elif i == "x":
                val += "0"
        return int(val, 2)
    
    def mask(self):
        m = ""
        for i in self.bitstream:
            if i == "1" or i == "0":
                m += "1"
            elif i == "X":
                m += "0000"
            elif i == "x":
                m += "0"
        return int(m, 2)
        
    def valueMask(self):
        val = ""
        m = ""
        for i in self.bitstream:
            if i == "1" or i == "0":
                val += i
                m += "1"
            elif i == "X":
                val += "0000"
                m += "0000"
            elif i == "x":
                val += "0"
                m += "0"
        val_str = "0x{0:x}".format(int(val,2))
        m_str = "0x{0:x}".format(int(m,2))
        return val_str+"/"+m_str
        
    def convert(self):
        stream = ""
        for i in self.bitstream:
            if i == "1" or i == "0" or i == "x":
                stream += i
            elif i == "X":
                stream += "xxxx"
        return stream
        
    def bits(self, bits_string):
        stream = ""
        for item in bits_string.split(","):
            if item.find("-") != -1:
                myList = item.split("-")
                stream += self.strWithin(int(myList[0]), int(myList[1]))
            else:
                stream += self.strAt(int(item))
        return stream
        
    def strWithin(self, begin, end):
        stream = self.convert()
        start = len(stream)-1-begin
        stop = len(stream)-1-end
        step = 1
        if start > stop:
            step = -1
            stop -= 1
            if stop <= -1:
                stop = None
        else:
            stop += 1
        return stream[start:stop:step]
        
    def strAt(self, pos):
        stream = self.convert()
        if pos < len(stream) and pos >= 0:
            return stream[len(stream)-1-pos]
        return ""
    
    def __getitem__(self, args):
        if isinstance(args, str):
            return self.bits(args)
        #elif isinstance(args, int):
        #    return self.strAt(args)
        return ""
    
    def convertHexToBin(self):
        stream = ""
        for i in self.bitstream[2:]:
            if i == "_":
                continue
            stream += "{0:04b}".format(int(i,16))
        self.bitstream = stream
        return stream
            
