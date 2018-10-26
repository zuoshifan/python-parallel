/* helloworld.c */

#include <mpi.h>
#include <Python.h>

int main(int argc, char *argv[])
{
  const char *fname = "./helloworld.py";
  FILE *fp;

  MPI_Init(&argc, &argv);
  Py_Initialize();

  fp = fopen(fname, "r");
  PyRun_SimpleFile(fp, fname);

  MPI_Finalize(); /* MPI should be finalized */
  Py_Finalize();  /* after finalizing Python */

  return 0;
}