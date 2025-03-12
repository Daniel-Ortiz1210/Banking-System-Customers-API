import requests

from abc import ABC, abstractmethod

class StudioGhibliService(ABC):
    """
    Abstract base class for interacting with the Studio Ghibli API.
    This class provides the basic structure for fetching data from the Studio Ghibli API.
    Subclasses must implement the abstract methods to fetch all records or fetch a specific record by ID.
    Attributes:
        BASE_URL (str): The base URL for the Studio Ghibli API.
    Methods:
        fetch_all():
            Abstract method to fetch all records from the API.
        fetch_by_id(id):
            Abstract method to fetch a specific record by its ID from the API.
    """

    BASE_URL = 'https://ghibliapi.vercel.app'
    
    @abstractmethod
    def fetch_all(self):
        pass
    
    @abstractmethod
    def fetch_by_id(self, id):
        pass


class FilmsServices(StudioGhibliService):

    
    def fetch_all(self):
        url = f'{super().BASE_URL}/films'
        response = requests.get(url)
        return response.json()
    
    def fetch_by_id(self, id):
        url = f'{super().BASE_URL}/films/{id}'
        response = requests.get(url)
        return response.json()
    

class PeopleServices(StudioGhibliService):
    
    def fetch_all(self):
        url = f'{super().BASE_URL}/people'
        response = requests.get(url)
        return response.json()
    
    def fetch_by_id(self, id):
        url = f'{super().BASE_URL}/people/{id}'
        response = requests.get(url)
        return response.json()
    

class LocationsServices(StudioGhibliService):
    
    def fetch_all(self):
        url = f'{super().BASE_URL}/locations'
        response = requests.get(url)
        return response.json()
    
    def fetch_by_id(self, id):
        url = f'{super().BASE_URL}/locations/{id}'
        response = requests.get(url)
        return response.json()
    

class SpeciesServices(StudioGhibliService):
    
    def fetch_all(self):
        url = f'{super().BASE_URL}/species'
        response = requests.get(url)
        return response.json()
    
    def fetch_by_id(self, id):
        url = f'{super().BASE_URL}/species/{id}'
        response = requests.get(url)
        return response.json()
    

class VehiclesServices(StudioGhibliService):
    
    def fetch_all(self):
        url = f'{super().BASE_URL}/vehicles'
        response = requests.get(url)
        return response.json()
    
    def fetch_by_id(self, id):
        url = f'{super().BASE_URL}/vehicles/{id}'
        response = requests.get(url)
        return response.json()
    

class AdminAccessService:

    def __init__(self):
        self.vehicles = VehiclesServices()
        self.species = SpeciesServices()
        self.locations = LocationsServices()
        self.people = PeopleServices()
        self.films = FilmsServices()


    def fetch_all(self, service):
        if service == 'films':
            return self.films.fetch_all()
        elif service == 'people':
            return self.people.fetch_all()
        elif service == 'locations':
            return self.locations.fetch_all()
        elif service == 'species':
            return self.species.fetch_all()
        elif service == 'vehicles':
            return self.vehicles.fetch_all()
        else:
            return None
    
    def fetch_by_id(self, service, id):
        if service == 'films':
            return self.films.fetch_by_id(id)
        elif service == 'people':
            return self.people.fetch_by_id(id)
        elif service == 'locations':
            return self.locations.fetch_by_id(id)
        elif service == 'species':
            return self.species.fetch_by_id(id)
        elif service == 'vehicles':
            return self.vehicles.fetch_by_id(id)
        else:
            return None


class ServicesFactory:
    
    @staticmethod
    def get_service(role: str) -> StudioGhibliService | AdminAccessService:
        if role == 'admin':
            return AdminAccessService()
        elif role == 'vehicles':
            return VehiclesServices()
        elif role == 'species':
            return SpeciesServices()
        elif role == 'locations':
            return LocationsServices()
        elif role == 'people':
            return PeopleServices()
        elif role == 'films':
            return FilmsServices()
        else:
            return None
        