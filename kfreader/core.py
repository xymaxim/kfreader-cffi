import os.path

from cffi import FFI


TYPEDECLS = {
    1: 'int[]',
    2: 'double[]',
    3: 'char *',
}

ffi = FFI()
ffi.cdef("""
#define KF_T_STRING        3

typedef struct _ArrayList {
    void **data;
    int allocatedSize;
    int length;
} ArrayList;

typedef struct _KFFile {
   char *name;
   ArrayList sections;
   int fd;
   int byteOrder;
   int integerSize;
   int isOpen;
   int indexHeaderLength;
   int indexEntryLength;
   int superIndexHeaderLength;
   int superIndexEntryLength;
   int typeSize[5];
} KFFile;

int     openKFFile              (KFFile *kf, const char *name);
void    closeKFFile             (KFFile *kf);
int     getKFVariableLength     (KFFile *kf, const char *name);
int     getKFVariableUsedLength (KFFile *kf, const char *name);
int     getKFVariableType       (KFFile *kf, const char *name);
int     getKFData               (KFFile *kf, const char *name, void *buf);
""")

here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
C = ffi.dlopen(here('../lib/libkfreader.so'))


class KFReader:
    def __init__(self, filename):
        self._kf = ffi.new('KFFile *')
        C.openKFFile(self._kf, filename.encode())

    def get_data(self, section, variable):
        name = '{}%{}'.format(section, variable).encode()
        length = C.getKFVariableLength(self._kf, name)
        atype = C.getKFVariableType(self._kf, name)

        if atype == C.KF_T_STRING:
            cdata = ffi.new('char*')
            C.getKFData(self._kf, name, cdata)
            return ffi.string(cdata).decode().rstrip()
        else:
            cdata = ffi.new(TYPEDECLS[atype], length)
            C.getKFData(self._kf, name, cdata)
            return cdata[0] if length == 1 else list(cdata)

    def close(self):
        C.closeKFFile(self._kf)
