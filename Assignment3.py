"""
Q1
variable: start_coordinates, end_coordinates, segment_distance_list, segment_time_list, speed
start_coordinates = []
end_coordinates = []
segment_distance_list = []
segment_time_list = []

start = last_end
if start == none, continue
end = current lat & lon(convert to value) -->function
total_dist = sum(segment_distance_list)
output_file1()

Q2
find_max_speed()
find_mean_speed()
output_file2()

Q3
variable: storm
storm = {}
for each row:
    calculate dist = distance btw storm eye & location
    if dist <= 5 and wind >=64 append storm ID to storm
    算location象限: 與颱風眼經緯度相減
    elif dist <= location象限的暴風半徑 (判斷是否落在該象限的風暴半徑內) append storm ID to storm
"""

"""
IS590 PR - Assignment 3

Instructor: Mr. Weible
Author:  
"""

"====================================================================================================================="
"MARK: Library"
from geographiclib.geodesic import Geodesic
from prettytable import PrettyTable
# import pdb
"====================================================================================================================="
"MARK: Constant"

Current_Latitude = "current_latitude"
Current_Longitude = "current_longitude"
Distance_List = "Distance_List"

Current_Date = "current_date"
Current_Time_mins = "current_time"
Time_List = "Time_List"
Speed_List = "Speed_List"

Question_1 = "Question_1"
Question_2 = "Question_2"

"====================================================================================================================="
"MARK: Function definition"

def process_storm_data(file_name, result_dict, impact_storms = [], target_lat = -999, target_lon = -999):
    """
    The main function to read the raw data line by line.
    Meanwhile, the function will find and calculate the five questions in the assignment - ID, name, start date, end date,
    highest Maximum sustained wind

    :param file_name: name of file in .txt format
    :param result_dict: an empty dictionary to gather the storm data for future use, such as print on console or output a file
    :return: None
    """
    geod = Geodesic.WGS84
    with open(file_name, 'r') as input_file:
        # initiate a dictionary for the storm
        storm_dict = reset_storm_dict()

        current_line_count = 0
        need_to_check_storm_hit = True

        for line in input_file:

            # Memorize the id and name, and decide how many lines need to read
            if line[0:2].isalpha():
                # 1. get the id and name
                # print('Storm system ID is ' , line[0:4])
                storm_dict["stormID"] = line[0:8]

                if line.find('UNNAMED', 18, 28) == -1:
                    # print('the name of the storm is ', line[18:28])
                    storm_dict["name"] = line[19:28].replace(" ", "")

                # set how many lines of this storm data
                current_line_count = int(line[33:36])

                continue

            # start count lines for this storm
            current_line_count -= 1

            # get the current latitude and longitude, add up distance (nautical miles) after calculation
            # print("--------------------")
            current_latitude = get_latitude(line)
            current_longitude = get_longitude(line)

            # Add up the total distance
            distance = calculate_the_distance(geod, storm_dict, current_latitude, current_longitude)
            storm_dict[Distance_List].append(distance)

            # Set the current coordinate
            storm_dict[Current_Latitude] = current_latitude
            storm_dict[Current_Longitude] = current_longitude


            # for speed calculation:
            current_date, current_time = line[0:8], line[10:14]

            hours = calculate_the_time(storm_dict, current_date, current_time)
            speed = round(calculate_the_speed(distance, hours), 2)
            # print(hours, distance, speed)

            # Add up the total times
            storm_dict[Time_List].append(hours)
            storm_dict[Speed_List].append(speed)

            # Set the current time
            storm_dict[Current_Date] = current_date
            storm_dict[Current_Time_mins] = current_time

            # 2. start date and end date of the storm
            if storm_dict["startDate"] is None:
                storm_dict["startDate"] = line[0:8]

            storm_dict["endDate"] = line[0:8]

            # 3. The highest Maximum sustained wind (in knots)
            current_sustained_wind = int(line[38:41])
            if current_sustained_wind != "-99" and current_sustained_wind > storm_dict["maxSustainedWind"]:
                storm_dict["maxSustainedWind"] = current_sustained_wind

            # 64 kt wind radii maximum extent in each quadrant
            storm_dict["NEradii"] = int(line[97:101])
            storm_dict["SEradii"] = int(line[103:107])
            storm_dict["SWradii"] = int(line[109:113])
            storm_dict["NWradii"] = int(line[115:119])

            # check whether the storm hit the location
            if target_lat != -999 and target_lon != -999 and need_to_check_storm_hit:
                did_hit = did_storm_hit_location(geod, storm_dict, target_lat, target_lon)
                if did_hit:
                    impact_storms.append(storm_dict["stormID"]+storm_dict["name"])
                    # print("impact_storms",impact_storms)
                    need_to_check_storm_hit = False
                    # print("need_to_check_storm_hit",need_to_check_storm_hit)

            # in the end of each storm section
            if 0 == current_line_count:
                # print_storm_detail(storm_dict)

                current_storm_id = storm_dict["startDate"] + storm_dict["stormID"] + storm_dict["name"]

                average_speed = 0.0
                if len(storm_dict[Time_List]) != 1:
                    average_speed = round((sum(storm_dict[Distance_List]) / sum(storm_dict[Time_List])), 2)

                if current_storm_id not in result_dict:
                    date_string = storm_dict["startDate"]
                    date_string = date_string[0:4] + "/" + date_string[4:6] + "/" + date_string[6:]
                    result_dict[current_storm_id] = [date_string,
                                                     storm_dict["stormID"],
                                                     storm_dict["name"],
                                                     round(sum(storm_dict[Distance_List]), 2),  # distance list
                                                     round(max(storm_dict[Speed_List]), 2),  # max of speed
                                                     average_speed
                                                     ]
                else:
                    print("[DEBUG] id is duplicated")

                need_to_check_storm_hit = True
                storm_dict = reset_storm_dict()


def output_storm_result(result_dict, question_type):
    """
    Output the result of the storm statistics to a .txt file for the last question with the help of PrettyTable library
    :param result_dict:
    :return: None
    """

    result_table = PrettyTable()

    out_put_title = 'Assignment_3_question_1.txt'
    start_point = 3
    stop_point = 4

    if question_type == Question_1:
        result_table.field_names = ["Date", "Storm ID", "Name", "Distance"]
    elif question_type == Question_2:
        start_point = 4
        stop_point = 6
        result_table.field_names = ["Date", "Storm ID", "Name", "Max Speed", "Avg Speed"]
        out_put_title = 'Assignment_3_question_2.txt'

    for storm in result_dict:
        each_storm_data = result_dict[storm][0:3] + result_dict[storm][start_point:stop_point]
        result_table.add_row(each_storm_data)

    print(result_table)

    with open(out_put_title, 'w') as output_file:
        output_file.write(result_table.get_string())


def calculate_the_distance(geod, storm_dict, current_latitude: float, current_longitude: float) -> float:
    """
    Calculate the nautical miles from last coordinate to current coordinate
    :param geod: Geodesic.WGS84 object
    :param storm_dict: The customized dictionary for memorize the necessary storm data,
    :param current_latitude: current latitude
    :param current_longitude: current longitude
    :return: The distance (nautical miles) from last coordinate to current coordinate
    """
    last_latitude = storm_dict[Current_Latitude]
    last_longitude = storm_dict[Current_Longitude]

    if -999.0 == last_latitude or -999.0 == last_longitude:
        return 0.0

    distance = round(geod.Inverse(last_latitude, last_longitude, current_latitude, current_longitude)['s12'] / 1852.0, 2)
    # print("the distance(nautical miles) between current coordinate and last coordinate: ", distance)

    return distance


def get_latitude(line: str) -> float:
    """
    Get the latitude from each storm data string
    :param line: the storm data string
    :return: the latitude in float type; positive means north, negative means south
    """
    is_north = 1
    if line[27: 28] == "N":
        is_north = 1
    elif line[27: 28] == "S":
        is_north = -1
    else:
        return 0.0

    latitude = float(line[23:27]) * is_north
    # print("latitude = ", latitude)
    return latitude


def get_longitude(line: str) -> float:
    """
    Get the longitude each storm data string
    :param line: the storm data string
    :return: the longitude in float type; positive means east, negative means west
    """
    is_east = 1
    if line[35: 36] == "E":
        is_east = 1
    elif line[35: 36] == "W":
        is_east = -1
    else:
        return 0.0

    longitude = float(line[30:35]) * is_east
    # print("longitude = ", longitude)
    return longitude


def calculate_the_speed(distance, hours):
    if hours == 0: return 0
    speed = distance / hours

    return speed


def get_hours(current_date, current_time, last_date, last_time):
    '''
    input: current_time
    output: hours between rows
    '''
    current_hour, last_hour = int(current_time[0:2]), int(last_time[0:2])
    current_minute, last_minute = int(current_time[2:4]), int(last_time[2:4])

    hours = (current_hour - last_hour) + (current_minute - last_minute)/60

    if current_date != last_date:
        hours = hours + 24

    return hours


def calculate_the_time(storm_dict, current_date, current_time):

    last_date = storm_dict[Current_Date]
    last_time = storm_dict[Current_Time_mins]

    if int(last_date) == 0:
        return 0


    return get_hours(current_date, current_time, last_date, last_time)



def reset_storm_dict():
    """
    Reset the storm dictionary to original state
    :return: a dictionary of storm-related data
    """
    storm_dict = {
        "stormID": None,
        "name": "UNNAMED",
        "startDate": None,
        "endDate": None,
        "maxSustainedWind": 0,
        Current_Latitude: -999.0,
        Current_Longitude: -999.0,
        Distance_List: [],
        Current_Date: 0,
        Current_Time_mins: 0,
        Time_List: [],
        Speed_List:[],
        "NEradii": -999, # to be added into "process_storm_data" function
        "SEradii": -999, # to be added into "process_storm_data" function
        "SWradii": -999, # to be added into "process_storm_data" function
        "NWradii": -999 # to be added into "process_storm_data" function
    }
    return storm_dict


def did_storm_hit_location(geod, storm_dict, location_latitude: float, location_longitude: float) -> bool:
    """
    Determine whether the storm hit the location
    :param geod: Geodesic.WGS84 object
    :param storm_dict: a dictionary storing storm data
    :param location_latitude: location latitude
    :param location_longitude: location longitude
    :return: a Boolean value; True means the storm hit the location, False means the storm did not hit the location
    """
    storm_latitude = storm_dict[Current_Latitude]
    storm_longitude = storm_dict[Current_Longitude]
    loc_storm_distance = round(geod.Inverse(storm_latitude, storm_longitude,
                                location_latitude, location_longitude)['s12'] / 1852.0, 2)
    if loc_storm_distance <= 5 and storm_dict["maxSustainedWind"] >= 64:
        return True

    location_quadrant = find_location_quadrant(storm_latitude, storm_longitude, location_latitude, location_longitude)
    if location_quadrant == "NE" and loc_storm_distance <= storm_dict["NEradii"]:
        return True
    elif location_quadrant == "SE" and loc_storm_distance <= storm_dict["SEradii"]:
        return True
    elif location_quadrant == "SW" and loc_storm_distance <= storm_dict["SWradii"]:
        return True
    elif location_quadrant == "NW" and loc_storm_distance <= storm_dict["NWradii"]:
        return True

    return False



def find_location_quadrant(storm_latitude: float, storm_longitude: float, location_latitude: float, location_longitude: float) -> str:
    """
    Find the quadrant of the location compared to the storm eye
    :param storm_latitude: storm eye latitude
    :param storm_longitude: storm eye longitude
    :param location_latitude: location latitude
    :param location_longitude: location longitude
    :return: a Boolean value; True means the storm hit the location, False means the storm did not hit the location
    """
    latitude_diff = location_latitude - storm_latitude
    longitude_diff = location_longitude - storm_longitude
    quadrant = "N" if latitude_diff > 0 else "S"
    quadrant += "E" if longitude_diff > 0 else "W"
    return quadrant

def find_hurricanes_hitting_location(lat: float, lon: float) -> list:
    result_dict = {}
    impact_storms = []
    process_storm_data("hurdat2-1851-2018-120319.txt", result_dict, impact_storms, lat, lon)
    process_storm_data("hurdat2-nepac-1949-2018-122019.txt", result_dict, impact_storms, lat, lon)
    print(impact_storms)
    return impact_storms
"====================================================================================================================="
"MARK: Program execution"
#
#result_dict = {}
#process_storm_data("hurdat2-1851-2018-120319.txt", result_dict)
# output_storm_result(result_dict, Question_1)
# output_storm_result(result_dict, Question_2)
find_hurricanes_hitting_location(32.31, -64.75)
