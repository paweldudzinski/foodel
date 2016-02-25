from geopy.geocoders import Nominatim
from geopy.distance import vincenty, great_circle


class Geo(object):

    def __init__(self):
        self.geolocator = Nominatim()

    def zip_code_to_lang_lat(self, zip_code, to_tuple=True):
        location = self.geolocator.geocode("%s, Poland" % zip_code)
        if location and to_tuple:
            return (location.latitude, location.longitude)

    def distance_vincenty(self, origin, destination):
        distance = vincenty(origin, destination)
        return distance and distance.km

    def distance_great_circle(self, origin, destination):
        distance = great_circle(origin, destination)
        return distance and distance.km

    def filter_products(self, products, zip_code):
        zip_code_coordinates = self.zip_code_to_lang_lat(zip_code)
        distances = []
        for product in products:
            product_coordinates = product.get_coordinated()
            distance = self.distance_vincenty(
                product_coordinates,
                zip_code_coordinates)
            distances.append((product, distance))
        distances = sorted(distances, key=lambda tup: tup[1])
        result = []
        for distance in distances:
            if distance[1] > 60:
                continue
            product = distance[0]
            product.distance = distance[1]
            result.append(product)
        return result

geo = Geo()
