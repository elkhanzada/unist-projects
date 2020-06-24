#include <iostream>
#include <string>
#include <stdexcept>
#include <queue>
#include <list>
#include <vector>
#include <map>
#include <limits>
#include "AdjacencyListDirectedGraph.h"
#include "FlightMap.h"

//After making the route string, I traverse the route by assigning first as origin and second as destination till the second one does not exist
//From there, i take edge weight from origin to dest and I add it to my distance variable
//In case if error happens, I catch it and return -1
//In the end I return it
double FlightMap::calcRouteDistance(const list<string> route) {
	auto origin = route.begin();
	if(*origin==*route.end())
		return 0;
	auto dest = route.begin();
	dest++;
	double distance = 0;
	while(dest!=route.end()){
		try{
			auto v = findOrCreateAirport(*origin);
			auto u = findOrCreateAirport(*dest);
			auto e = v.outgoingEdge(u);
			distance+=*e;
		}catch(...){
			return -1;
		}
		origin++;
		dest++;
			
	}
	return distance;				

}

//In this function I applied Djikstra algorithm
//mapDis maps vertex values to its distances
//rMapDis maps distances to its vertex values
//q is used to keep track of minimal distance
//shortestAdjV is used to keep track of adjacent vertices where there is minimal distance
//At first I initiate mapDis and rMapDis by considering the distances as infinity except origin
//Then while in the loop I find the vertex that has minimal distance by the help of rMapDis and q
//From there I get its adjacent vertices and check if the path is less than the distance they have currently
//If it is less I push it to q and change the values at mapDis as well as rMapDis
//I add it to shortestAdjV as well
//After this algorithm I create string list
//I find the route by the help of shortestAdjV then return it but if there is no such route I return empty object
list<string> FlightMap::findShortestRoute(const string &airport1, const string &airport2) {
	auto allV = flight_graph.vertices();	
	auto startV = findOrCreateAirport(airport1);
	auto endV = findOrCreateAirport(airport2);
	if(startV==endV) return {};
	map<string, double> mapDis;
	map<double, string> rMapDis;
	map<string, string> shortestAdjV;
	priority_queue<double, vector<double>, greater<double>> q;
	int counter=100000000;
	for(auto it = allV.begin(); it!=allV.end(); it++){
		if(startV==*it){
			mapDis.insert({**it, 0});
			rMapDis.insert({0, **it});
		}else{
			mapDis.insert({**it, 10000000000});
			rMapDis.insert({counter++, **it});
		}
	}
	q.push(0);
	auto curV = startV;
	while(!q.empty()){
		if(rMapDis.find(q.top())!=rMapDis.end())
			curV = findOrCreateAirport(rMapDis.at(q.top()));
		else{	
			q.pop();
			continue;
		}
		q.pop();
		auto edges = curV.outgoingEdges();
		for(auto it = edges.begin();it!=edges.end();it++){
			auto adjV = (*it).dest();
			double altPath = mapDis.at(*curV)+(**it);
			if(altPath<mapDis.at(*adjV)){
				mapDis.at(*adjV)=altPath;
				shortestAdjV[*adjV] = *curV;
				q.push(altPath);
				for(auto t = rMapDis.begin();t!=rMapDis.end();t++)
					if(t->second==(*adjV)){
						rMapDis.erase(t->first);
						rMapDis.insert({altPath, *adjV});
						break;
					}
			}
		}
	}
	list<string> route;
		auto temp = *endV;
		while(temp!=*startV){
			if(shortestAdjV.find(temp)==shortestAdjV.end()){
					return {};
	    		}
	    		route.push_front(temp);
	    		temp = shortestAdjV.at(temp);
	    		
		}
	    	if(route.size()>=1){
	    		route.push_front(*startV);
	    		return route;
	    	}
	
	}	


//I traverse the all vertices in order to find minimal distances from origin to those vertices
//It is easily done with the help of findShortestRoute and calcRouteDistance 
void FlightMap::printAllShortestRoutes(const string &airport) {
	auto allV = flight_graph.vertices();
	list<string> route;
	for(auto it = allV.begin(); it!=allV.end(); it++){
		route = findShortestRoute(airport,**it);
		if(!route.empty()){ 
			printRoute(route);
			cout<<"  (Distance = "<<calcRouteDistance(route)<<")";
	    		cout<<"\n";
	    	}
	}	
}

