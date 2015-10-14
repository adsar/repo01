#include <stdio.h>
#include <stdlib.h>
#include "network.h"
#include "readgml.h"

// Function to export to tsv (destructive for undirected networks)

void export_network(NETWORK *network, FILE *stream)
{
  printf("\nExporting data to .tsv\n");
  int i, j, k, tot_degree = 0;
  fprintf(stream, "source\tsource_val\ttarget\ttarget_val\tvalue\n");
  for (i=0; i<network->nvertices; i++) {
    //printf("vertex label: %s  -  degree: %d\n", network->vertex[i].label, network->vertex[i].degree);
    for (j=0; j<network->vertex[i].degree; j++) {
      int vt = network->vertex[i].edge[j].target;
      //printf("source:%d (%s),  target:%d (%s),  value:%d\n", network->vertex[i].id, network->vertex[i].label, network->vertex[vt].id, network->vertex[vt].label, (int)network->vertex[i].edge[j].weight);

      // in undirected networks avoid printing double arc
      if (vt == -1) continue;
      if (network->directed==0)
      {
          for (k=0; k<network->vertex[vt].degree; k++) {
            if (network->vertex[vt].edge[k].target == i) {
                network->vertex[vt].edge[k].target = -1;
            }
          }
      }
      tot_degree += 1;
      fprintf(stream, "%s\t%s\t%s\t%s\t%d\n", network->vertex[i].label, network->vertex[i].value, network->vertex[vt].label, network->vertex[vt].value, (int)network->vertex[i].edge[j].weight);
    }
  }
  printf("...exported %d vertices and %d edges.\n", network->nvertices, tot_degree);
}

void usage()
{
    printf("\n./readgml file.gml file.tsv\n");
}

int main(int argc, char* argv[])
{
    if (argc != 3) {
        usage();
        return 1;
    }

    NETWORK node;
    NETWORK *network = &node;
    FILE *stream = fopen(argv[1], "r");
    read_network(network, stream);
    printf("%d vertices read from .gml file.\n", network->nvertices);

    FILE *csv_stream = fopen(argv[2], "w");
    export_network(network, csv_stream);

    free_network(network);
    return 0;
}
