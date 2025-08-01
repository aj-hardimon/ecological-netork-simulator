"""
Author: AJ Hardimon

Date: 7/23/2025
"""
import csv
import requests
import time

class Species:
    """ A class designed to hold the attributes of a species to be used in a
        ecological relations graph. The common name and category fields are
        populated by API calls to iNaturalist in the constructor.

        Class Attributes:
        species_name: str representation of the species name for that instance
        of Species
        common_name: str of the common name for the species
        category: str of the category of the species (ex: Mammalia, Aves)

        get_yosemitie_species(): returns a list of known species in Yosemitie
        accoring to the National Park Services
        get_species_name: return self.species_name
        get_common_name: return self.common_name
        get_category: return self.category
    """

    def __init__(self, species_name):
        """ Constructor that takes a scientific species name as input and
            uses the iNaturalist API to fill in common names and the
            category for that species.
        """

        self.species_name = species_name.lower()
        self.common_name = []
        self.category = None

        url = f"https://api.inaturalist.org/v1/taxa?q={self.species_name}"
        
        # Get info about species from iNaturalist
        sp_info_json = None
        try:
            response = requests.get(url)
            if response.status_code == 200:
                sp_info_json = response.json()
                # iNat API needs 1 second of delay between calls
                time.sleep(1)
            else:
                print(f"Response failed: {response.status_code}")
        except Exception as e:
            print(f"Exception: {e}")

        # Double check json file is found
        if sp_info_json:
            try:
                if len(sp_info_json['results'].keys()) >= 1:
                    # Category of species is the same no matter the source
                    self.category = sp_info_json['results'][0]['iconic_taxon_name']
                for entry in sp_info_json['results']:
                    if 'preferred_common_name' in entry.keys():
                        # Add common name to list if found
                        self.common_name.append(entry['preferred_common_name'])
            except Exception as e:
                print(f"Exception: {e}, for species {self.species_name}")

    @staticmethod
    def get_yosemitie_species():
        """ Uses a csv file to create a list of species within Yosemitie National
            Park.
        """

        yosemitie_species_lst = []
        file_path = "Data-Files/Species Full List with Details.csv"

        with open(file_path, "r") as species_csv:
            csv_reader = csv.reader(species_csv)
            i = 0
            try:
                for line in csv_reader:
                    # First 5 lines of csv aren't needed
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
            f"category={self.category}"
            )

    def __str__(self):
        """ Return the common name and category in an easy
            to read form.
        """
        comm_name = (str(self.common_name)).rstrip("]").lstrip("[").replace("'", "")
        return(f"{comm_name} is in the {self.category} class.")


    def get_species_name(self):
        """Return species_name."""
        return self.species_name
    
    def get_common_name(self):
        """Return species_name."""
        return self.common_name
    
    def get_category(self):
        """Return category."""
        return self.category