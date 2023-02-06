import os
import csv
import json
import datetime

journeys = []
start_stations = {}
end_stations = {}
unique_stations = {}
common_journeys = {}

first_date = None
last_date = None

longest_journey = {
    "Error": "You didn't take any Tube journeys.", "Journey Time": 0}
shortest_journey = {
    "Error": "You didn't take any Tube journeys.", "Journey Time": 99999}

latest_journey = {
    "Error": "You didn't take any Tube journeys.", "Mod Start Time": "00:00"}
earliest_journey = {
    "Error": "You didn't take any Tube journeys.", "Mod Start Time": "99:99"}

most_expensive_journey = {
    "Error": "You didn't take any Tube journeys.", "Charge": 0.0}
times_cap_hit = 0
times_didnt_tap = 0

bus_routes = {}
methods = {}

total_journeys = 0


def add_to_dict(dict, key):
    if key in dict:
        dict[key] += 1
    else:
        dict[key] = 1


def conv_time(time):
    return int(time[:2]) * 60 + int(time[3:5])


for filename in os.listdir('journey-history'):
    if filename.endswith('.csv'):
        with open('journey-history/' + filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Ignore auto top-ups and refunds
                if row['Journey/Action'].startswith('Auto'):
                    continue

                # GENERAL HANDLING
                total_journeys += 1

                # Convert row['Date'] to a datetime object. %d-%b-%Y is the format of the date in the CSV file.
                journey_date = datetime.datetime.strptime(
                    row['Date'], '%d-%b-%Y')

                if first_date == None or journey_date < first_date:
                    first_date = journey_date
                if last_date == None or journey_date > last_date:
                    last_date = journey_date

                if "We are not able to show where you touched out during this journey" in row['Note'] or "We are not able to show where you touched in during this journey" in row['Note'] or '[No touch' in row['Journey/Action']:
                    times_didnt_tap += 1

                if "This journey was cheaper or free today because you reached a daily cap" in row['Note']:
                    times_cap_hit += 1

                # Handle same-day journey things
                if int(row['Start Time'][:2]) < 4 or (int(row['Start Time'][:2]) == 4 and int(row['Start Time'][3:5]) < 30):
                    row['Mod Start Time'] = f"{int(row['Start Time'][:2]) + 24}:{row['Start Time'][3:5]}"
                    if row['End Time']:
                        row['Mod End Time'] = f"{int(row['End Time'][:2]) + 24}:{row['End Time'][3:5]}"
                elif row['End Time'] and (int(row['End Time'][:2]) < 4 or (int(row['End Time'][:2]) == 4 and int(row['End Time'][3:5]) < 30)):
                    row['Mod Start Time'] = row['Start Time']
                    row['Mod End Time'] = f"{int(row['End Time'][:2]) + 24}:{row['End Time'][3:5]}"
                else:
                    row['Mod Start Time'] = row['Start Time']
                    row['Mod End Time'] = row['End Time']

                # MODE SPECIFIC-HANDLING
                # Handle bus journeys
                if row['Journey/Action'].startswith('Bus journey'):
                    add_to_dict(methods, 'Bus')
                    route = row['Journey/Action'].split(
                        'Bus journey, route ')[-1]
                    add_to_dict(bus_routes, route)

                # Handle Tube, DLR, Overground, TfL Rail and Elizabeth Line journeys
                else:
                    add_to_dict(methods, 'Tube/Overground/DLR/EL')
                    row['Start Station'] = row['Journey/Action'].split(' to ')[
                        0].split(' [')[0].split(' DLR')[0]
                    row['End Station'] = row['Journey/Action'].split(
                        ' to ')[-1].split(' [')[0].split(' DLR')[0]
                    add_to_dict(start_stations, row['Start Station'])
                    add_to_dict(end_stations, row['End Station'])
                    add_to_dict(unique_stations, row['Start Station'])
                    add_to_dict(unique_stations, row['End Station'])
                    add_to_dict(
                        common_journeys, f"{row['Start Station']} to {row['End Station']}")

                    if row['Mod End Time']:
                        row['Journey Time'] = conv_time(
                            row['Mod End Time']) - conv_time(row['Mod Start Time'])
                        if longest_journey['Journey Time'] < row['Journey Time']:
                            longest_journey = row
                        if shortest_journey['Journey Time'] > row['Journey Time']:
                            shortest_journey = row

                if conv_time(row['Mod Start Time']) > conv_time(latest_journey['Mod Start Time']):
                    latest_journey = row
                if conv_time(row['Mod Start Time']) < conv_time(earliest_journey['Mod Start Time']):
                    earliest_journey = row

                if float(row['Charge']) > float(most_expensive_journey['Charge']):
                    most_expensive_journey = row

                journeys.append(row)
                pass


print(f"{start_stations=}")
print(f"{end_stations=}")
print(f"{common_journeys=}")
print(f"{longest_journey=}")
print(f"{shortest_journey=}")
print(f"{latest_journey=}")
print(f"{earliest_journey=}")
print(f"{most_expensive_journey=}")
print(f"{bus_routes=}")
print(f"{times_cap_hit=}")
print(f"{times_didnt_tap=}")
print(f"{total_journeys=}")

most_common_journey = max(common_journeys, key=common_journeys.get)
print(f"{most_common_journey=} {common_journeys[most_common_journey]} times")

most_common_start_station = max(start_stations, key=start_stations.get)
print(
    f"{most_common_start_station=} {start_stations[most_common_start_station]} times")

most_common_end_station = max(end_stations, key=end_stations.get)
print(
    f"{most_common_end_station=} {end_stations[most_common_end_station]} times")

most_common_bus_route = max(bus_routes, key=bus_routes.get)
print(f"{most_common_bus_route=} {bus_routes[most_common_bus_route]} times")

print(f"{round(times_didnt_tap / total_journeys * 100, 2)}% of journeys didn't tap")
print(f"{round(times_cap_hit / total_journeys * 100, 2)}% of journeys hit the cap")

print(f"Methods used: {methods}")

favourite_method = max(methods, key=methods.get)
print(f"Favourite method: {favourite_method}")

time_spent_travelling = sum(int(journey['Journey Time'])
                            for journey in journeys if "Journey Time" in journey)
print(f"Time spent travelling: {time_spent_travelling} minutes")

average_journey_time = round(time_spent_travelling / total_journeys, 1)
print(
    f"Average journey time: {average_journey_time} minutes")

raw_charge = sum(float(journey['Charge']) for journey in journeys)
total_charge = '{0:.2f}'.format(
    round(sum(float(journey['Charge']) for journey in journeys), 2))
print(f"Total charge: £{total_charge}")

average_charge = '{0:.2f}'.format(raw_charge / total_journeys)
print(f"Average charge: £{average_charge}")

export = {
    "start_stations": len(start_stations),
    "end_stations": len(end_stations),
    "unique_stations": len(unique_stations),
    "most_common_journey": {"journey": most_common_journey, "times": common_journeys[most_common_journey]},
    "longest_journey": longest_journey,
    "shortest_journey": shortest_journey,
    "latest_journey": latest_journey,
    "earliest_journey": earliest_journey,
    "most_expensive_journey": most_expensive_journey,
    "most_common_bus_route": {"route": most_common_bus_route, "times": bus_routes[most_common_bus_route]},
    "times_didnt_tap": times_didnt_tap,
    "times_cap_hit": times_cap_hit,
    "total_journeys": total_journeys,
    "methods_used": methods,
    "time_spent_travelling": time_spent_travelling,
    "average_journey_time": average_journey_time,
    "total_charge": total_charge,
    "average_charge": average_charge,
    # Create a new dict with the first and last dates in the format DD MMM YYYY
    "date_range": {"first": first_date.strftime("%d %b %Y"), "last": last_date.strftime("%d %b %Y"), "days_covered": (last_date - first_date).days + 1, "journeys_per_day": round(total_journeys / ((last_date - first_date).days + 1), 1)},
}

print(export)
with open('export.json', 'w') as f:
    json.dump(export, f)
