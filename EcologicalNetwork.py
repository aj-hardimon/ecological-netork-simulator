"""
Author: AJ Haridmon

Date: 7/25/2025
"""

import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pyvis.network import Network
import csv
import requests


class EcologicalNetwork():
    """ A class that creates a graph of species with directed edges indicating
        one species eating the other. These relationships will be used to
        simulate population shifts.

        Class Attributes:
        species_list: list of species in the network
        network: dict graph of eating relation between species
    """

    def __init__(self, species_list):
        """ Constructor that takes a list of species to be included into the
            graph and creates a network between those species.
        """
        self.species_list = species_list
        self.network = nx.DiGraph()

    def create_network(self):
        i = 0
        lst_len = len(self.species_list)
        for species in ['canis lupus', 'procyon lotor', 'lynx rufus']:
            species = species.lower()
            self.network.add_node(species)
            prey_list = EcologicalNetwork.get_prey_list(species=species)
            if prey_list is not None:
                for prey in prey_list:
                    if(prey is not None and prey in self.species_list):
                        self.network.add_node(prey)
                        self.network.add_edge(species, prey)
            i += 1
            print(f"{i}/{lst_len} completed")


    @staticmethod
    def get_prey_list(species):
        """ Static method that takes a species and returns a list of all the
            prey of that species.
        """
        prey_list = []
        prey_json = EcologicalNetwork._get_prey_json(species=species)

        if prey_json:
            try:
                for list in prey_json["data"]:
                    for prey in list[2]:
                        prey_l = prey.lower().rstrip(".-")
                        if(list[1] == "eats" or list[1] == "preysOn" and species == list[0].lower()):
                            prey_list.append(prey_l)
                return prey_list
            except:
                print("Error Occured")
                return None

    @staticmethod
    def _get_prey_json(species):
        """ Static method that grabs the json file of all of the species the
            input species eats.
        """
        url = f"https://api.globalbioticinteractions.org/taxon/{species}/eats"

        try:
            response = requests.get(url=url)

            if response.status_code == 200:
                prey_json = response.json()
                return prey_json
            else:
                # Handles API fails
                print(f"Response Failed: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            # Handles API exceptions
            print(f"Error: {e}")
            return None
        
    @staticmethod
    def get_predator_list(species):
        """ Static method that takes a species and returns a list of all the
            predators of that species.
        """
        predator_list = []
        predator_json = EcologicalNetwork._get_predator_jsond(species=species)

        if predator_json:
            try:
                for list in predator_json["data"]:
                    for predator in list[2]:
                        predator_l = predator.lower().rstrip(".-")
                        if(list[1] == "eatenBy" or list[1] == "preyedUponBy" and species == list[0].lower()):
                            predator_list.append(predator_l)
                return predator_list
            except:
                print("Error Occured")
                return None

    @staticmethod
    def _get_predator_json(species):
        """ Static method that grabs the json file of all of the species the
            input species is eaten by.
        """
        url = f"https://api.globalbioticinteractions.org/taxon/{species}/preyedUponBy"

        try:
            response = requests.get(url=url)

            if response.status_code == 200:
                prey_json = response.json()
                return prey_json
            else:
                # Handles API fails
                print(f"Response Failed: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            # Handles API exceptions
            print(f"Error: {e}")
            return None

    def draw_graph(self):
        """ Method to draw the network as a Plotly graph."""
        
        edge_x = []
        edge_y = []
        pos = nx.spring_layout(self.network)

        for u, v in self.network.edges():
            x0, y0 = pos[u]
            x1, y1 = pos[v]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, 
            y=edge_y,
            line=dict(width=0.8, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        node_text = []
        node_adj = []
        node_size = []


        for node in self.network.nodes():
            if(self.network.in_degree(node) > 0 or self.network.out_degree(node) > 0):
                x, y = pos[node]
                node_x.append(x)
                node_y.append(y)
                node_text.append(node)
                node_adj.append(self.network.out_degree(node))
                node_size.append(20 + 0.2 * self.network.out_degree(node))


        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                # colorscale options
                #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
                #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
                #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
                colorscale='Rainbow',
                reversescale=False,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title=dict(
                        text='Node Connections',
                        side='right'
                    ),
                    xanchor='left',
                ),
                line_width=2))
        
        node_adjacencies = []
        
        for node, adjacencies in enumerate(self.network.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            

        node_trace.marker.color = node_adj
        node_trace.marker.size = node_size
        node_trace.text = node_text

        fig = go.Figure(data=[edge_trace, node_trace],
            layout=go.Layout(
                title=dict(
                    text="<br>Species interactions in Yosemitie National Park",
                    font=dict(
                        size=16
                    )
                ),
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[dict(
                    text="GitHub: <a href='https://github.com/aj-hardimon/ecological-netork-simulator'> https://github.com/aj-hardimon/ecological-netork-simulator",
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )
        
        fig.show(renderer="browser")


def get_yosemitie_species():
    """ Uses a csv file to create a list of species within Yosemitie Natinoal
        Park
    """

    yosemitie_species_lst = []
    file_path = "Data-Files/Species Full List with Details.csv"

    with open(file_path, "r") as species_csv:
        csv_reader = csv.reader(species_csv)
        i = 0
        try:
            for line in csv_reader:
                if i >= 5 and len(line) >= 4:
                    yosemitie_species_lst.append(line[3].lower())
                i += 1
        except IndexError:
            print("Index Error")
            return None
        else:
            return yosemitie_species_lst
        
species_lst = get_yosemitie_species()


network_test = EcologicalNetwork(species_list=species_lst)
network_test.create_network()

network_test.draw_graph()

#nx.draw_networkx(network_test.network, with_labels=True, node_size=100, font_size=4, pos=nx.spring_layout(network_test.network) )
#plt.show()