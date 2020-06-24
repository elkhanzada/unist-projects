#ifndef ASSIGNMENT6_ADJACENCYLISTDIRECTEDGRAPH_H
#define ASSIGNMENT6_ADJACENCYLISTDIRECTEDGRAPH_H

#include <iostream>
#include <list>
#include <stdexcept>

using namespace std;

template<typename V, typename E>
class AdjacencyListDirectedGraph {

  // ---------------------------------------------------------------------------------
  // You *cannot* add any additional public or private member functions in this class.
  // You *cannot* add any additional public or private member variables in this class.
  // ---------------------------------------------------------------------------------

public:

  // Define public data types of Vertex and Edge and the associated iterators.

  class Vertex;
  class Edge;

  typedef list<Vertex> VertexList;
  typedef list<Edge> EdgeList;
  typedef typename VertexList::iterator VertexItor;
  typedef typename EdgeList::iterator EdgeItor;
  typedef typename VertexList::const_iterator VertexConstItor;
  typedef typename EdgeList::const_iterator EdgeConstItor;

private:

  // Define private data types of VertexObject and EdgeObject and the associated iterators.
  // The type of IncidenceEdgesList and its iterator are defined as well.

  struct VertexObject;
  struct EdgeObject;

  typedef list<VertexObject> VertexObjectList;
  typedef list<EdgeObject> EdgeObjectList;
  typedef list<EdgeList> IncidenceEdgesList;

  typedef typename VertexObjectList::iterator VertexObjectItor;
  typedef typename EdgeObjectList::iterator EdgeObjectItor;
  typedef typename IncidenceEdgesList::iterator IncidenceEdgesItor;
  /*
   * VertexObject stores data of a vertex.
   */
  struct VertexObject {
    V elt;                             // the element stored at this vertex
    VertexObjectItor pos;              // position in vertex_collection
    IncidenceEdgesItor inc_edges_pos;  // position in inc_edges_collection

    VertexObject(V _elt) : elt(_elt) {}  // pos and inc_edges_pos are initially "NULL".
  };

  /*
   * EdgeObject stores data of an edge.
   */
  struct EdgeObject {
    E elt;                          // the element stored at this edge
    Vertex origin_vertex;           // the vertex at the origin
    Vertex dest_vertex;             // the vertex at the destination
    EdgeObjectItor pos;             // position in edge_collection
    EdgeItor origin_inc_edges_pos;  // position in an edge list in inc_edges_collection
    EdgeItor dest_inc_edges_pos;    // position in an edge list in inc_edges_collection

    EdgeObject(const Vertex& v, const Vertex& w, E _elt) : origin_vertex(v), dest_vertex(w), elt(_elt) {} // pos origin_inc_edges_pos, and dest_inc_edges_pos are initially "NULL".
  };

  // ---------------------------------------------------------------------------------
  // This class should contain the following three member variables only:
  // vertex_collection, edge_collection, and inc_edges_collection
  // You are not allowed to define any other member variables (public or private).
  // ---------------------------------------------------------------------------------

  VertexObjectList vertex_collection;
  EdgeObjectList edge_collection;
  IncidenceEdgesList inc_edges_collection;

public:

  /*
   * Vertex is a position class of a vertex in AdjacencyListDirectedGraph.
   * Internally, a vertex is a pointer to an entry in vertex_collection.
   */
  class Vertex {

    VertexObject *v_obj;

  public:

    /*
     * The constructor of Vertex. This subsumes the default constructor.
     *
     * v - a pointer to a VertexObject
     */
    Vertex(VertexObject* v = NULL) : v_obj(v) {}


    /*
     * Return the element stored at this vertex.
     */
    V& operator*() const {
	return v_obj->elt;
    }

    /*
     * Return a list of edges incident to this vertex.
     */
    EdgeList incidentEdges() const {
		auto es = v_obj->inc_edges_pos;
		return *es;
    }

    /*
     * Check whether a vertex is adjacent to this vertex.
     * This means whether there is an edge that has this vertex
     * and the given vertex as the end points.
     *
     * v - the given vertex
     */
     //I traverse through the edges to find if vertex is adjacent
    bool isAdjacentTo(const Vertex& v) const {
	auto es = incidentEdges();
	for(auto it = es.begin(); it!=es.end(); it++){
		if(it->isIncidentOn(v))
			return true;
	}
	return false;

    }

    /*
     * Check whether there is a directed edge connecting this vertex to the given vertex.
     *
     * v - the given vertex
     */
     //I traverse through the edges to find if vertex is destination of any
    bool isOutgoingTo(const Vertex& v) const {
	auto es = incidentEdges();
	for(auto it = es.begin(); it!=es.end(); it++){
		if(v==it->dest())
			return true;
	}
	return false;
    }

    /*
     * Return a directed edge connecting this vertex to the given vertex.
     * If the directed edge does not exist, throw an exception.
     *
     * v - the given vertex
     * Return the directed edge connecting this vertex to the given vertex.
     */
     //I traverse through the edges to find if vertex is destination of any and return that edge
    Edge outgoingEdge(const Vertex& v) const {
	auto es = incidentEdges();
	for(auto it = es.begin(); it!=es.end(); it++){
		if(v==it->dest())
			return *it;
	}
	throw runtime_error("Outgoing edge does not exist!");	
    }

    /*
     * Return the set of all directed edges connecting this vertex to any vertex.
     */
     //I create new list and add all the edges that are incident to vertex
    EdgeList outgoingEdges() const {
	auto es = incidentEdges();
	EdgeList elist;
	for(auto it = es.begin(); it!=es.end(); it++){
		if(it->origin()==v_obj)
			elist.push_back(*it);
	}
	return elist;
    }

    /*
     * Check whether this vertex is the same as the given vertex
     *
     * v - the given vertex
     * Return true if this vertex is the same as the given vertex
     */
    bool operator==(const Vertex& v) const {
		if(v_obj==v.v_obj)
			return true;
		return false;
    }

    /*
     * Declare friend to AdjacencyListDirectedGraph so that
     * AdjacencyListDirectedGraph can access to the private
     * member variables of this class.
     */
    friend class AdjacencyListDirectedGraph<V,E>;
  };

  /*
   * Edge is a position class of an edge in AdjacencyListDirectedGraph.
   * Internally, an edge is a pointer to an entry in edge_collection.
   */
  class Edge {

    EdgeObject *e_obj;

  public:

    /*
     * The constructor of Edge. This subsumes the default constructor.
     *
     * v - a pointer to a EdgeObject
     */
    Edge(EdgeObject* e = NULL) : e_obj(e) {}

    /*
     * Return the element stored at this edge.
     */
    E& operator*() const {
	return	e_obj->elt;
    }

    /*
     * Return the vertices of this directed edge.
     * The first element of the vertex list is the vertex of the origin.
     * The second element of the vertex list is the vertex of the destination.
     */
    VertexList endVertices() const {
	VertexList vList;
	vList.push_back(e_obj->origin_vertex);
	vList.push_back(e_obj->dest_vertex);
	return vList;
	
    }

    /*
     * Return the vertex of this edge that is different from the given vertex.
     * If the given vertex is origin, return destination.
     * If the given vertex is destination, return origin.
     * If the given vertex is neither origin nor destination, throw an exception.
     *
     * v - the given vertex
     * Return the other vertex of this edge
     */
    Vertex opposite(const Vertex& v) const {
	if(e_obj->origin_vertex==v)
		return e_obj->dest_vertex;
	else if(e_obj->dest_vertex==v)
		return e_obj->origin_vertex;
	throw runtime_error("Given vertex is neither origin nor destination!");
    }

    /*
     * Check whether a given edge is adjacent to this edge.
     * This means that whether the given edge and this edge
     * shared a vertex.
     *
     * edge - the given edge
     * Return true if the given edge is adjacent to this edge.
     */
    //I check whether if given edge has any connections with the requested one
    bool isAdjacentTo(const Edge& edge) const {
	if(e_obj->origin_vertex==edge.origin()||
		e_obj->origin_vertex==edge.dest()||
			e_obj->dest_vertex==edge.origin()||
				e_obj->dest_vertex==edge.dest())
			return true;
	return false;
    }

    /*
     * Check whether a vertex is incident on this edge.
     * This means that whether the vertex is a vertex of this edge.
     *
     * v - the given vertex
     * Return true if the given vertex is incident to this edge.
     */
    bool isIncidentOn(const Vertex& v) const {
	if(e_obj->origin_vertex==v||e_obj->dest_vertex==v)
		return true;
	return false;
    }

    /*
     * Return the vertex at the origin of this edge.
     */
    Vertex origin() const {
	return e_obj->origin_vertex;
    }

    /*
     * Return the vertex at the destination of this edge.
     */
    Vertex dest() const {
	return e_obj->dest_vertex;
    }

    /*
     * Return true if this is a directed edge.
     * In this class, it should always return true.
     */
    bool isDirected() const {
	return true;
    }

    /*
     * Check whether this edge is the same as the given edge.
     *
     * edge - the given edge
     * Return true if this edge is the same as the given edge.
     */
    bool operator==(const Edge& edge) const {
	if(e_obj==edge.e_obj)
		return true;
	return false;
    }

    /*
     * Declare friend to AdjacencyListDirectedGraph so that
     * AdjacencyListDirectedGraph can access to the private
     * member variables of this class.
     */
    friend class AdjacencyListDirectedGraph<V,E>;
  };


public:

  /*
   * Return the list of vertices in this graph.
   */
   //I create new list and add all the vertices from vertex_collection
  VertexList vertices() {
	VertexList vList;
	for(auto it = vertex_collection.begin(); it!=vertex_collection.end(); it++){
		Vertex temp = Vertex(&(*it));
		vList.push_back(temp);		
	}

	return vList;
	
  }

  /*
   * Return the list of edges in this graph.
   */
   //I create new list and add all the edges from edge_collection
  EdgeList edges() {
	EdgeList eList;
	for(auto it = edge_collection.begin(); it!=edge_collection.end(); it++){
		Edge temp = Edge(&(*it));
		eList.push_back(temp);		
	}

	return eList;
  }

  /*
   * Add a new vertex to this graph.
   *
   * x - the element to be stored in the new vertex.
   * Return the newly created vertex.
   */
   //I add the vertex to vertex_collection by first creating one and then connect it with inc_edges_pos
  Vertex insertVertex(const V& x) {
	vertex_collection.push_back(VertexObject(x));
	vertex_collection.back().pos = --(vertex_collection.end());
	inc_edges_collection.push_back(EdgeList());
	vertex_collection.back().inc_edges_pos=--(inc_edges_collection.end());
	Vertex v = Vertex(&vertex_collection.back());
	return v;
  }

  /*
   * Add a new edge to this graph. Throw an exception
   * if an edge has already existed between v and w.
   *
   * v - the vertex at the origin
   * w - the vertex at the destination
   * x - the element to be stored in the new edge.
   * Return the newly created edge.
   */
   //I create a directed edge and add it to edge_collection, then connect it with its origin and dest inc edges pos
  Edge insertDirectedEdge(const Vertex& v, const Vertex& w, E x) {
	EdgeObject eo = EdgeObject(v, w, x);
	edge_collection.push_back(eo);
	edge_collection.back().pos = --(edge_collection.end());
	auto vit = v.v_obj->inc_edges_pos;
	auto wit = w.v_obj->inc_edges_pos;
	auto orig = (*vit).insert((*vit).end(), Edge(&edge_collection.back()));
	auto dest = (*wit).insert((*wit).end(), Edge(&edge_collection.back()));
	edge_collection.back().origin_inc_edges_pos = orig;
	edge_collection.back().dest_inc_edges_pos = dest;
	Edge e = Edge(&edge_collection.back());
	return e;
  }

  /*
   * Remove a vertex from this graph. All edges that contain
   * v as one of their vertices are also removed.
   *
   * v - a vertex
   */
   //I first delete all the edges that have that vertex and then delete the vertex from vertex_collection
  void eraseVertex(const Vertex& v) {
	auto es = v.incidentEdges();
	for(auto it = es.begin(); it!=es.end(); it++){
		eraseEdge(*it);
	}
	inc_edges_collection.erase((v.v_obj)->inc_edges_pos);
	vertex_collection.erase((v.v_obj)->pos);
  }

  /*
   * Remove an edge from this graph.
   *
   * e - an edge
   */
   //I get the details about the edge and erase it from vertex's inc_edges_pos. Then I delete it from edge_collection
  void eraseEdge(const Edge& e) {
	auto voriginO = e.origin().v_obj;
	auto vdestO = e.dest().v_obj;
	auto eo = e.e_obj;
	voriginO->inc_edges_pos->erase(eo->origin_inc_edges_pos);
	vdestO->inc_edges_pos->erase(eo->dest_inc_edges_pos);
	edge_collection.erase(eo->pos);

  }

};


#endif //ASSIGNMENT6_ADJACENCYLISTDIRECTEDGRAPH_H
