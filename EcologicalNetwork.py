"""
Author: AJ Haridmon

Date: 7/25/2025
"""

import networkx as nx
import matplotlib.pyplot as plt
import csv



class EcologicalNetwork():
    """ A class that creates a graph of species with directed edges indicating
        one species eating the other. These relationships will be used to
        simulate population shifts
    """

    def __init__(self, species_list):
        """Constructor that takes a list of species to be included into the graph"""
        self.species_list = species_list
        self.graph = {}


def get_yosemitie_species():
    """ Uses a csv of species within Yosemitie National Park"""

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