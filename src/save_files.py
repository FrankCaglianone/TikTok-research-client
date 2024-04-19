import csv





#################### DATA SAVING FUNCTIONS FOR USER FOLLOWING QUERY ####################
"""
    Saves data from the `parsing_list` dictionary and the `queue` list into two separate CSV files.

    - The `parsing_list.csv` file will contain two columns: "Username" and "Parsed Status", 
      representing keys and values from the `parsing_list` dictionary, respectively. 
    - The `queue.csv` file will contain a single column: "Usernames to parse", 
      listing all usernames to still parse from the `queue` list.

    The file is saved in the `src/outputs` directory with no extra line spaces between rows.
"""
def save_to_csv(parsing_list, queue):
    # Save parsing_list to CSV
    with open('src/outputs/parsing_list.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Parsed Status"])  # Writing headers
        for username, parsed_status in parsing_list.items():
            writer.writerow([username, parsed_status])

    # Save queue to CSV
    with open('src/outputs/queue.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Usernames to parse"]) 
        for username in queue:
            writer.writerow([username])





"""
    Saves a dictionary of usernames and their associated list of time stamps into a CSV file named `time_stamps.csv`.

    The resulting CSV file will contain two columns: "Username" and "Time Stamp". 
    Each row after the header will contain a username and their associated time stamps. 
    If a username has multiple time stamps, all will be included in the same row, following the username.

    The file is saved in the `src/outputs` directory with no extra line spaces between rows.
"""
def save_time_stamps(time_stamps):
    with open('src/outputs/time_stamps.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Time Stamp"])  # Writing headers
        for username, timestamps in time_stamps.items():
            # If timestamps is None or not a list, log an error or handle it as you see fit
            if timestamps is None:
                print(f"Error: No timestamps found for username {username}.")
                continue  # Skip this username
            elif not isinstance(timestamps, list):
                print(f"Error: Timestamps for username {username} is not a list.")
                continue  # Skip this username

            # Writing username and all its timestamps in one row
            row = [username] + timestamps
            writer.writerow(row)





"""
    Saves a dictionary of usernames and their associated JSON responses into a CSV file named `saved_jsons.csv`.

    The resulting CSV file will have two columns: "Username" and "Json_response". 
    Each row after the header will contain a username and the corresponding JSON response as a single string. 

    The file is saved in the `src/outputs` directory. 
    The CSV format is chosen for ease of use in spreadsheets and other data analysis tools.
"""
def save_jsons(jsons):
    with open('src/outputs/saved_jsons.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Username", "Json_response"])  # Writing headers
        for username, data in jsons.items():
            writer.writerow([username, data])





"""
    Saves the global network graph to a CSV file.

    This function iterates over the global `network_graph` variable, which is expected to be a list of tuples. 
    Each tuple represents a directional relationship between two users (i.e., a source user and their followee, the destination user). 
    It writes these relationships to a CSV file, creating a representation of the social network.

    The CSV file will have two columns: "Source" and "Destination", corresponding to the user and their followee, respectively. 
    Each row after the header represents one such relationship in the network.

    Notes:
    - The function writes the CSV file to 'src/outputs/network.csv'. It will overwrite any existing file at this location.
"""
def save_network(network_graph):
    with open('src/outputs/network.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Destination"])
        # Write each tuple in the network list to the file
        for connection in network_graph:
            writer.writerow(connection)










#################### DATA SAVING FUNCTIONS FOR NETWORK ANALYSIS ####################
def save_pagerankings(range_0_25, range_26_50, range_51_75, range_76_100):
    # Open a new CSV file
    with open('src/network_analysis_outputs/ranges.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Write the headers
        writer.writerow(['0% - 25%', '26% - 50%', '51% - 75%', '76% - 100%'])

        # Since the lists can have different lengths, find the maximum length of the lists
        max_length = max(len(range_0_25), len(range_26_50), len(range_51_75), len(range_76_100))


        for i in range(max_length):
            # Initialize the row with empty strings for each column
            row = ['', '', '', '']
            
            # For each range, if there is data for the row index, add it to the row
            if i < len(range_0_25):
                row[0] = ': '.join(map(str, range_0_25[i]))
            if i < len(range_26_50):
                row[1] = ': '.join(map(str, range_26_50[i]))
            if i < len(range_51_75):
                row[2] = ': '.join(map(str, range_51_75[i]))
            if i < len(range_76_100):
                row[3] = ': '.join(map(str, range_76_100[i]))
                
            # Write the row to the CSV file
            writer.writerow(row)
     