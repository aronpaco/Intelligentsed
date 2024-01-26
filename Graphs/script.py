import csv
from geopy.distance import geodesic
import folium

radius = 1000
capitals = []
with open('capitals.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)
    for row in reader:
        try:
            latitude = float(row[2][:-1]) if row[2][-1] == 'N' or row[2][-1] == 'S' else None
            longitude = float(row[3][:-1]) if row[3][-1] == 'E' or row[3][-1] == 'W' else None
            if latitude is not None and longitude is not None:
                capitals.append({
                    'city': row[0],
                    'country': row[1],
                    'latitude': latitude if row[2][-1] == 'N' else -latitude,
                    'longitude': longitude if row[3][-1] == 'E' else -longitude,
                })
            else:
                print(f"Skipped line: {row}")
        except ValueError as e:
            print(f"Error processing line {row}: {e}")

def haversine(coord1, coord2):
    return geodesic(coord1, coord2).kilometers

def find_capitals_within_radius(start, end, radius_km):
    route = [start]
    current_location = start

    while current_location != end:
        nearest_capitals = [capital for capital in capitals if capital['city'] != current_location['city'] and haversine(
            (capital['latitude'], capital['longitude']), (current_location['latitude'], current_location['longitude'])
        ) <= radius_km]
        
        if not nearest_capitals:
            print("No capitals within a", radius, " km radius")
            break

        nearest_capitals.sort(key=lambda capital: haversine(
            (capital['latitude'], capital['longitude']), (end['latitude'], end['longitude'])
        ))

        current_location = nearest_capitals[0]
        route.append(current_location)

    return route

def main():
    start_city = input("Enter the starting city: ")
    end_city = input("Enter the destination city: ")

    start = next((capital for capital in capitals if capital['city'].lower() == start_city.lower()), None)
    end = next((capital for capital in capitals if capital['city'].lower() == end_city.lower()), None)

    if start is None or end is None:
        print("City not found.")
    else:
        route = find_capitals_within_radius(start, end, radius)
        print("Route:")
        for capital in route:
            print(f"{capital['city']}, {capital['country']}")

        visualize_route(route)

def visualize_route(route):
    map_center = (route[0]['latitude'], route[0]['longitude'])
    m = folium.Map(location=map_center, zoom_start=4)

    for capital in route:
        folium.Marker(location=(capital['latitude'], capital['longitude']),
                      popup=f"{capital['city']}, {capital['country']}").add_to(m)

    folium.PolyLine([(capital['latitude'], capital['longitude']) for capital in route],
                    color="blue", weight=2.5, opacity=1).add_to(m)

    m.save("route_map.html")


if __name__ == "__main__":
    main()
