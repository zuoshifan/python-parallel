/* helloworld.h */

#define MPICH_SKIP_MPICXX 1
#define OMPI_SKIP_MPICXX  1

#include <mpi.h>

void sayhello(MPI_Comm comm);