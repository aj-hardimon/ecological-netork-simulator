# Ecological Network Simulator
The Ecological Network Simulator is a python project that takes a list of input species and produces a network with species as nodes and edges conveying
predator/prey relationships.

Relations between species are determined by the Global Biotic Interactions (GloBI) API. Only the predator --> prey relationship is shown in graph examples,
however the reverse is also supported through the get_prey_list and get_predator_list methods. Classification of species and their common names is provided 
by the iNaturalist API.

Graphs can be produced either by pyvis (prefered) or Plotly. Network graphs produced by Plotly are static, however they show the number of outdegree 
connections more clearly. Network graphs produced by pyvis network graph include the common name of each species as labels for nodes, the interaction 
(x eats y) as labels for edges, and color nodes by groups (Mammalia, Aves, etc.) The graph also supports neighbor highlighting based on nodes or edges, as 
well as the ability to search species nodes by their scientific name.

The network is constructed only between the species in the input list to limit API calls and scale. The network could be easily modified to propagate 
from an origin species if given enough time to run, or start from a list of species contained to another list of species.

Originally this project was designed to work for only species listed to be in Yosemite by the NPS, and this set of species is also what was used for the graph 
examples.  It was modified later to work with any set of input species, however due to some scientific species name resulting in many common names (Wolf, Eastern Wolf, 
Red Wolf, etc.) therefore visual appeal was sacrificed in order to avoid assuming what common name to use for a given species.
