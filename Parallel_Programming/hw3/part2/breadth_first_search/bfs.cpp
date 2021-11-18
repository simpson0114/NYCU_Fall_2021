#include "bfs.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cstddef>
#include <omp.h>

#include "../common/CycleTimer.h"
#include "../common/graph.h"

#define ROOT_NODE_ID 0
#define NOT_VISITED_MARKER -1

void vertex_set_clear(vertex_set *list)
{
    list->count = 0;
}

void vertex_set_init(vertex_set *list, int count)
{
    list->max_vertices = count;
    list->vertices = (int *)malloc(sizeof(int) * list->max_vertices);
    vertex_set_clear(list);
}

// Take one step of "top-down" BFS.  For each vertex on the frontier,
// follow all outgoing edges, and add all neighboring vertices to the
// new_frontier.
void top_down_step(
    Graph g,
    vertex_set *frontier,
    vertex_set *new_frontier,
    int *distances,
    bool *bu_frontier)
{
    #pragma omp parallel 
    {
        /*  set local frontier and count to avoid synchronization   */
        int local_count = 0;
        Vertex* local_frontier = new Vertex[g->num_nodes];

        #pragma omp for
        for (int i = 0; i < frontier->count; i++)
        {

            int node = frontier->vertices[i];

            int start_edge = g->outgoing_starts[node];
            int end_edge = (node == g->num_nodes - 1)
                            ? g->num_edges
                            : g->outgoing_starts[node + 1];

            // attempt to add all neighbors to the new frontier
            for (int neighbor = start_edge; neighbor < end_edge; neighbor++)
            {
                int outgoing = g->outgoing_edges[neighbor];
                if (distances[outgoing] == NOT_VISITED_MARKER)
                {
                    __sync_bool_compare_and_swap(&distances[outgoing], NOT_VISITED_MARKER, distances[node] + 1);
                    // distances[outgoing] = distances[node] + 1;
                    // int index = __sync_add_and_fetch(&new_frontier->count, 1);
                    // new_frontier->vertices[index-1] = outgoing;
                    local_frontier[local_count++] = outgoing;
                    if(bu_frontier)
                        bu_frontier[outgoing] = 1;
                }
            }
        }
        #pragma omp critical
        {
            memcpy(new_frontier->vertices+new_frontier->count, local_frontier, sizeof(int)*local_count);
            new_frontier->count += local_count;
        }
        delete [] local_frontier;
    }
}

bool botton_up_step(
    Graph g,
    bool *frontier,
    bool *new_frontier,
    int *distances)
{
    bool end = true;

    #pragma omp parallel for schedule(dynamic, 1024)
    for (int node = 0; node < g->num_nodes; node++)
    {
        if (distances[node] == NOT_VISITED_MARKER)
        {
            int start_edge = g->incoming_starts[node];
            int end_edge = (node == g->num_nodes - 1)
                           ? g->num_edges
                           : g->incoming_starts[node + 1];
            
            for(int neighbor = start_edge; neighbor < end_edge; neighbor++)
            {
                int incoming = g->incoming_edges[neighbor];

                if(frontier[incoming])
                {
                    new_frontier[node] = 1;
                    distances[node] = distances[incoming] + 1;
                    end = 0;
                    break;
                }
            }
        }
    }
    return end;
}



// Implements top-down BFS.
//
// Result of execution is that, for each node in the graph, the
// distance to the root is stored in sol.distances.
void bfs_top_down(Graph graph, solution *sol)
{

    vertex_set list1;
    vertex_set list2;
    vertex_set_init(&list1, graph->num_nodes);
    vertex_set_init(&list2, graph->num_nodes);

    vertex_set *frontier = &list1;
    vertex_set *new_frontier = &list2;

    // initialize all nodes to NOT_VISITED
    #pragma omp parallel for
    for (int i = 0; i < graph->num_nodes; i++)
        sol->distances[i] = NOT_VISITED_MARKER;

    // setup frontier with the root node
    frontier->vertices[frontier->count++] = ROOT_NODE_ID;
    sol->distances[ROOT_NODE_ID] = 0;

    while (frontier->count != 0)
    {

#ifdef VERBOSE
        double start_time = CycleTimer::currentSeconds();
#endif

        vertex_set_clear(new_frontier);

        top_down_step(graph, frontier, new_frontier, sol->distances, nullptr);

#ifdef VERBOSE
        double end_time = CycleTimer::currentSeconds();
        printf("frontier=%-10d %.4f sec\n", frontier->count, end_time - start_time);
#endif

        // swap pointers
        vertex_set *tmp = frontier;
        frontier = new_frontier;
        new_frontier = tmp;
    }
}

void bfs_bottom_up(Graph graph, solution *sol)
{
    // For PP students:
    //
    // You will need to implement the "bottom up" BFS here as
    // described in the handout.
    //
    // As a result of your code's execution, sol.distances should be
    // correctly populated for all nodes in the graph.
    //
    // As was done in the top-down case, you may wish to organize your
    // code by creating subroutine bottom_up_step() that is called in
    // each step of the BFS process.

    bool *frontier = (bool*)calloc(graph->num_nodes, sizeof(bool));
	bool *new_frontier = (bool*)calloc(graph->num_nodes, sizeof(bool));

    #pragma omp parallel for
	for (int i = 0 ; i < graph->num_nodes ; i++)
    {
    	sol->distances[i] = NOT_VISITED_MARKER;
        frontier[i] = false;
    }
    
    sol->distances[ROOT_NODE_ID] = 0;
    frontier[ROOT_NODE_ID] = 1;

    bool end = 0;

    while(!end)
    {
        #pragma omp parallel for
        for (int i = 0 ; i < graph->num_nodes ; i++)
            new_frontier[i] = false;

        end = botton_up_step(graph, frontier, new_frontier, sol->distances);

        bool *tmp = frontier;
		frontier = new_frontier;
		new_frontier = tmp;
    }
}

void bfs_hybrid(Graph graph, solution *sol)
{
    // For PP students:
    //
    // You will need to implement the "hybrid" BFS here as
    // described in the handout.

    vertex_set list1;
    vertex_set list2;
    vertex_set_init(&list1, graph->num_nodes);
    vertex_set_init(&list2, graph->num_nodes);

    vertex_set *frontier = &list1;
    vertex_set *new_frontier = &list2;

    bool *bu_frontier = (bool*)calloc(graph->num_nodes, sizeof(bool));
	bool *bu_new_frontier = (bool*)calloc(graph->num_nodes, sizeof(bool));

    // initialize all nodes to NOT_VISITED
    #pragma omp parallel for
    for (int i = 0; i < graph->num_nodes; i++)
    {
        sol->distances[i] = NOT_VISITED_MARKER;
        bu_frontier[i] = false;
        bu_new_frontier[i] = false;
    }
    // setup frontier with the root node
    frontier->vertices[frontier->count++] = ROOT_NODE_ID;
    sol->distances[ROOT_NODE_ID] = 0;

    bool end = 0;
    bool button_up = 0;

    while(!end && frontier->count != 0) 
    {
        if(!button_up && (float)(frontier->count)/(float)(graph->num_nodes) < 0.1)
        {
            #pragma omp parallel for
            for (int i = 0 ; i < graph->num_nodes ; i++)
                bu_frontier[i] = false;
            vertex_set_clear(new_frontier);
            top_down_step(graph, frontier, new_frontier, sol->distances, bu_frontier);
        }
        else
        {
            #pragma omp parallel for
            for (int i = 0 ; i < graph->num_nodes ; i++)
                bu_new_frontier[i] = false;
            end = botton_up_step(graph, bu_frontier, bu_new_frontier, sol->distances);
            button_up = 1;
        }
        
        vertex_set *tmp = frontier;
		frontier = new_frontier;
		new_frontier = tmp;

		if(button_up)
        {
			bool *tmp = bu_frontier;
			bu_frontier = bu_new_frontier;
			bu_new_frontier = tmp;

		}
    }
}
