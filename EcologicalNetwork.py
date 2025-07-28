"""
Author: AJ Haridmon

Date: 7/25/2025
"""

import networkx as nx
import matplotlib.pyplot as plt
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
            graph.
        """
        self.species_list = species_list
        self.network = nx.DiGraph()

        
        for species in species_list:
            self.network.add_node(species)
            prey_list = EcologicalNetwork.get_prey_list(species=species)

            for prey in prey_list:
                if(prey is not None and prey in species_list):
                    self.network.add_node(prey)
                    self.network.add_edge(species, prey)
        

        self.network.add_node(species_list[0])
        prey_list = EcologicalNetwork.get_prey_list(species=species_list[0])
        print(species_list[0])

        for prey in prey_list:
            print(prey)
            if(prey is not None and prey in species_list):
                self.network.add_node(prey)
                self.network.add_edge(species_list[0], prey)


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
                        prey_list.append(prey)
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
                    yosemitie_species_lst.append(line[3])
                i += 1
        except IndexError:
            print("Index Error")
            return None
        else:
            return yosemitie_species_lst
        
species_lst = get_yosemitie_species()



network_test = EcologicalNetwork(species_list=species_lst)
nx.draw(network_test.network, with_labels=True)
plt.show()