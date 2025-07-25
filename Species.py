"""
Author: AJ Hardimon

Date: 7/23/2025
"""

class Species:
    """ A class designed to hold the attributes of a species to be
        used in a graph for ecological simulation.

        Class Attributes:
        species_name: str representation of the species name for that instance of Species
        population: int of the population of the instance
        r_val: float representing how quickly the instance of species repopulates


    """

    def __init__(self, species_name, population, r_val=1.0):
        """simple constructor containing str species_name, int population, and float r_val."""

        self.species_name = species_name
        self.population = population
        self.r_val = r_val

    def __repr__(self):
        """__repr__ method that shows all class attributes and their values."""
        class_name = type(self).__name__
        return(f"{class_name}(species_name='{self.species_name}', population={self.population}, r-val={self.r_val})")

    def __str__(self):
        """__str__ method that displays the species and its population in an easy to read manner."""
        return(f"{self.species_name} has a population of {self.population}")


    def get_name(self):
        """Return species_name."""
        return self.species_name

    def get_population(self):
        """Return population."""
        return self.species_name

    def get_r_val(self):
        """Return r_val."""
        return self.r_val

    def set_population(self, new_population):
        """Set population."""
        self.population = new_population