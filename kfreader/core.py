import os
from contextlib import contextmanager

from cffi import FFI


TYPEDECLS = {
    1: 'int[]',
    2: 'double[]',
    3: 'char *',
    4: 'int *'
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

this_dir = os.path.abspath(os.path.dirname(__file__))
C = ffi.dlopen(os.path.join(this_dir, 'vendor/libkfreader.so'))


class KFFileReadingError(Exception):
    pass


class KFReader:
    def __init__(self, filename=None):
        if filename is not None:
            self.open(filename)

    def open(self, filename):
        self._kf = ffi.new('KFFile *')
        # TODO Suppress stderr messages while opening a file.
        if -1 == C.openKFFile(self._kf, filename.encode()):
            msg = "File does not exist or has unexpected format"
            raise KFFileReadingError(msg)

    def _get_string(self, name, length, is_continuous):
        cdata = ffi.new('char[]', length)
        C.getKFData(self._kf, name, cdata)
        data = ffi.string(cdata).decode()

        num_blocks = length // 160
        if num_blocks == 1:
            rv = data.rstrip()
        else:
            lines = []
            for i in range(0, length, 160):
                line = data[i:i+160]
                lines.append(line.rstrip())
            rv = ''.join(lines) if is_continuous else ','.join(lines)

        return rv

    def get_data(self, section, var, is_str_continuous=False):
        name = '{}%{}'.format(section, var).encode()
        length = C.getKFVariableLength(self._kf, name)
        if length == -1:
            msg = "Could not find variable '{}' in section '{}'"
            raise RuntimeError(msg.format(var, section))
        atype = C.getKFVariableType(self._kf, name)

        if atype == C.KF_T_STRING:
            return self._get_string(name, length, is_str_continuous)
        else:
            cdata = ffi.new(TYPEDECLS[atype], length)
            C.getKFData(self._kf, name, cdata)
            return cdata[0] if length == 1 else list(cdata)

    def close(self):
        C.closeKFFile(self._kf)


@contextmanager
def kfropen(filename):
    kfr = KFReader()

    # Does this hurt? No?
    try:
        kfr.open(filename)
        yield kfr
    except KFFileReadingError as e:
        raise(e)
    except Exception as e:
        kfr.close()
        raise(e)
    else:
        kfr.close()
