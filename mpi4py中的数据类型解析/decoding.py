# decoding.py

"""
Demonstrates the usage of datatype decoding.

Run this with 1 processes like:
$ mpiexec -n 1 python decoding.py
or
$ python decoding.py
"""

from mpi4py import MPI


comm = MPI.COMM_WORLD

Int = MPI.INT
Ihvec = MPI.INT.Create_hvector(2, 3, 4*4)
Ihvec4 = Ihvec.Create_contiguous(4)

for dtyp, typ_name in [ (Int, 'MPI.INT'), (Ihvec, 'Ihvec'), (Ihvec4, 'Ihvec4') ]:
    print '%s.Get_envelope: %s' % (typ_name, dtyp.Get_envelope())
    print '%s.envelope: %s' % (typ_name, dtyp.envelope)
    print '%s.combiner: %s' % (typ_name, dtyp.combiner)
    try:
        print '%s.Get_contents: %s' % (typ_name, dtyp.Get_contents())
        print '%s.contents: %s' % (typ_name, dtyp.contents)
    except MPI.Exception as e:
        print e.error_string
    print '%s.decode: %s' % (typ_name, dtyp.decode())
    print '%s.is_named: %s' % (typ_name, dtyp.is_named)
    print '%s.is_predefined: %s' % (typ_name, dtyp.is_predefined)
    print '%s.name: %s' % (typ_name, dtyp.name)
    print