"""
Author: AJ Hardimon

Date: 7/23/2025
"""
import csv
import requests
import os
import time

class Species:
    """ A class designed to hold the attributes of a species to be used in a
    ecological relations graph.

        Class Attributes:
        species_name: str representation of the species name for that instance
        of Species
        common_name: str of the common name for the species
        category: str of the category of the species (ex: mammal)

        get_yosemitie_species(): returns a list of known species in Yosemitie
        accoring to the National Park Services
    """

    def __init__(self, species_name):
        """Simple constructor containing that uses a scientific species name
            and uses data from Yosemitie National Park to fill in information
            about that species.
        """

        self.species_name = species_name.lower()
        self.common_name = []
        self.category = None

        if Species.verify_iNat_token() == False:
            Species.get_iNat_token()


        url = f"https://api.inaturalist.org/v1/taxa?q={self.species_name}"


        headers = {
            "Authorizaton": f"{os.getenv("INATURALIST_API_TOKEN")}"
        }
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

        if sp_info_json:
            try:
                self.category = sp_info_json['results'][0]['iconic_taxon_name']
                for entry in sp_info_json['results']:
                    self.common_name.append(entry['preferred_common_name'])
            except Exception as e:
                print(f"Exception: {e}, for species {self.species_name}")


    @staticmethod
    def verify_iNat_token():
        """Verify the iNat API token and returns boolean result."""

        # Test API call
        test_url = "https://api.inaturalist.org/v1/taxa?q=canis%20lupus"
        headers = {
            "Authorization": os.getenv("INATURALIST_API_TOKEN")
        }

        try:
            response = requests.get(url=test_url, headers=headers)
            if response.status_code == 200:
                return True
            elif response.status_code == 401:
                print("Token is invalid or expired")
                return False
            else:
                print(f"Unexpected status code: {response.status_code}")
        except Exception as e:
            print(f"Error verifying iNat token: {e}")
            return False

    @staticmethod 
    def get_iNat_token():
        """Retrieve a new iNat API token."""

    url = "https://www.inaturalist.org/users/api_token"
    token_json = None
    try:
        response = requests.get(url=url)
        if response.status_code == 200:
            token_json = response.json()
            os.environ['INATURALIST_API_TOKEN'] = token_json['api_token']
        else:
            # Handles API fails
            print(f"Response Failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        # Handles API exceptions
        print(f"Error: {e}")
    

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
            f"category={self.category}"
            )

    def __str__(self):
        """ Return the common name and category in an easy
            to read form.
        """
        comm_name = (str(self.common_name)).rstrip("]").lstrip("[").replace("'", "")
        return(
            f"{comm_name} is a {self.category}"
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