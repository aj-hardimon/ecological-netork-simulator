"""
Author: AJ Hardimon

Date: 7/23/2025
"""
import csv
import networkx as nx

class Species:
    """ A class designed to hold the attributes of a species in Yosemitie
        to be used in a ecological relations graph.

        Class Attributes:
        species_name: str representation of the species name for that instance
        of Species
        common_name: str of the common name for the species
        category: str of the category of the species (ex: mammal)
        nativeness: boolean of whether the species is native to Yosemitie
    """

    def __init__(self, species_name):
        """Simple constructor containing that uses a scientific species name
            and uses data from Yosemitie National Park to fill in information
            about that species.
        """

        self.species_name = species_name.lower()
        self.common_name = ""
        self.category = ""
        self.nativeness = False

        file_path = "Data-Files/Species Full List with Details.csv"

        # Search through the csv file for species name
        with open(file_path, "r") as species_csv:
            csv_reader = csv.reader(species_csv)
            i = 0
            try:
                for line in csv_reader:
                    if (i >= 5 and len(line) >= 7):
                        line_species = line[3].lower()
                        if line_species == species_name:
                            # Species found in the csv file
                            self.common_name = line[4].title()
                            self.category = line[1]
                            if(line[7] == "Native"):
                                self.nativeness = True
                            break
                    i += 1
            except Exception as e:
                print(f"Error occured: {e}")
        

    @staticmethod
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

    def __repr__(self):
        """Return all class attributes and their values."""
        class_name = type(self).__name__
        return(
            f"{class_name} "
            f"(species_name='{self.species_name}', "
            f"common_name={self.common_name}, "
            f"category={self.category}, "
            f"nativeness={self.nativeness})"
            )

    def __str__(self):
        """ Return the common name, category, and nativeness in an easy
            to read form.
        """
        return(
            f"{self.common_name} " 
            f"is a {self.category if self.category[-1] != "s" else self.category[:-1]} "
            f"and is {"Native" if self.nativeness else "Non-Native"}"
            )


    def get_species_name(self):
        """Return species_name."""
        return self.species_name
    
    def get_common_name(self):
        """Return species_name."""
        return self.common_name
    
    def get_category(self):
        """Return category."""
        return self.category
    
    def get_nativeness(self):
        "Return nativeness."
        return self.nativeness