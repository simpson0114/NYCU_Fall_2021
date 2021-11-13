#ifndef __GRAPH_INTERNAL_H__
#define __GRAPH_INTERNAL_H__

#include <stdlib.h>
#include <cstdio>
#include "contracts.h"

static inline int num_nodes(const Graph graph)
{
  REQUIRES(graph != NULL);
  return graph->num_nodes;
}

static inline int num_edges(const Graph graph)
{
  REQUIRES(graph != NULL);
  return graph->num_edges;
}

static inline const Vertex* outgoing_begin(const Graph g, Vertex v)
{
  REQUIRES(g != NULL);
  REQUIRES(0 <= v && v < num_nodes(g));
  return g->outgoing_edges + g->outgoing_starts[v];
}

static inline const Vertex* outgoing_end(const Graph g, Vertex v)
{
  REQUIRES(g != NULL);
  REQUIRES(0 <= v && v < num_nodes(g));
  int offset = (v == g->num_nodes - 1) ? g->num_edges : g->outgoing_starts[v + 1];
  return g->outgoing_edges + offset;
}

static inline int outgoing_size(const Graph g, Vertex v)
{
  REQUIRES(g != NULL);
  REQUIRES(0 <= v && v < num_nodes(g));
  if (v == g->num_nodes - 1) {
    return g->num_edges - g->outgoing_starts[v];
  } else {
    return g->outgoing_starts[v + 1] - g->outgoing_starts[v];
  }
}

static inline const Vertex* incoming_begin(const Graph g, Vertex v)
{
  REQUIRES(g != NULL);
  REQUIRES(0 <= v && v < num_nodes(g));
  return g->incoming_edges + g->incoming_starts[v];
}

static inline const Vertex* incoming_end(const Graph g, Vertex v)
{
  REQUIRES(g != NULL);
  REQUIRES(0 <= v && v < num_nodes(g));
  int offset = (v == g->num_nodes - 1) ? g->num_edges : g->incoming_starts[v + 1];
  return g->incoming_edges + offset;
}

static inline int incoming_size(const Graph g, Vertex v)
{
  REQUIRES(g != NULL);
  REQUIRES(0 <= v && v < num_nodes(g));
  if (v == g->num_nodes - 1) {
    return g->num_edges - g->incoming_starts[v];
  } else {
    return g->incoming_starts[v + 1] - g->incoming_starts[v];
  }
}

static inline void print_graph(const Graph g)
{
  for (int i=0; i<num_nodes(g); i++) {
    // Vertex is typedef'ed to an int. Vertex* points into g.outgoing_edges[]
    const Vertex* start = outgoing_begin(g, i);
    const Vertex* end = outgoing_end(g, i);
    for (const Vertex* v=start; v!=end; v++)
        printf("Edge %u %u\n", i, *v);
  }
}


#endif // __GRAPH_INTERNAL_H__
