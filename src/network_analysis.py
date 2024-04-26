import argparse
import csv
import sys
import igraph as ig
import numpy as np
# import matplotlib.pyplot as plt

import save_files






# g.vs["label"] = g.vs["name"]


# fig, ax = plt.subplots()
# ig.plot(
#     g,
#     target=ax,
#     # layout="sugiyama",
#     vertex_size=15,
#     vertex_color="blue",
#     edge_color="#222",
#     edge_width=1,
# )
# plt.show()









def read_parsing_list(path):
    parsing_list = {}

    try:
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip the header
            for row in reader:
                if row:  # Check if row is not empty
                    username = row[0].strip()  # Remove any leading/trailing whitespace
                    status = int(row[1].strip())  # Convert status to integer
                    parsing_list[username] = status

    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    return parsing_list






def read_network(path):
    network = []

    try:
        with open(path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header
            for row in csv_reader:
                network.append((row[0], row[1]))  # Append each row as a tuple to the list
                
    except FileNotFoundError:
        # If the file is not found, print an error message and exit the program
        sys.exit(f"Error: The file at {path} was not found.") 
    except Exception as e: 
        # If any other exception occurs, exit the program
        sys.exit(f"Error: {e}") 
    return network
                







def clean_graph(list_path, network_path):

    parsing_list = read_parsing_list(list_path)

    network = read_network(network_path)


    final_graph = []


    for row in network:
        source, destination = row
        if destination in parsing_list:
            final_graph.append((source, destination))


    # Use a set to find unique sources
    unique_sources = set(source for source, destination in final_graph)
    # Count the number of unique source nodes
    number_of_sources = len(unique_sources)
    print("Number of source nodes:", number_of_sources)


    return final_graph









def calculate_and_save_pageranks(g):

    # Calculate the page ranking
    # TODO: pagerank = g.pagerank(damping=0.85)?
    pagerank = g.pagerank()


    # Pair ranks with usernames
    pagerank_list = []
    for vertex, score in zip(g.vs, pagerank):
        pagerank_list.append((vertex['name'], score))


    # Sort the list in ascending order
    sorted_pageranks_list = sorted(pagerank_list, key=lambda item: item[1])

    # TODO: Give proper comment
    scores = [score for name, score in sorted_pageranks_list]

    # Calculate percentiles
    p25 = np.percentile(scores, 25)
    p50 = np.percentile(scores, 50)
    p75 = np.percentile(scores, 75)

    min_score = np.min(scores)  # 0th percentile
    max_score = np.max(scores)  # 100th percentile


    # Initialize lists for each range
    range_0_25 = []
    range_26_50 = []
    range_51_75 = []
    range_76_100 = []


    # Assign tuples to each range based on their Page Rank
    for name, score in sorted_pageranks_list:
        if score <= p25:
            range_0_25.append((name, score))
        elif p25 < score <= p50:
            range_26_50.append((name, score))
        elif p50 < score <= p75:
            range_51_75.append((name, score))
        elif score > p75:
            range_76_100.append((name, score))



    # Save the results in .csv format
    save_files.save_25_percentile(range_0_25, min_score, p25)
    save_files.save_50_percentile(range_26_50, p25, p50)
    save_files.save_75_percentile(range_51_75, p50, p75)
    save_files.save_100_percentile(range_76_100, p75, max_score)



    





def main(parsing_list, network_list):

    cleaned_network = clean_graph(parsing_list, network_list)

    save_files.save_cleaned_network(cleaned_network)

    # Create a graph from the list of edges
    graph = ig.Graph.TupleList(cleaned_network, directed=True)

    calculate_and_save_pageranks(graph)

    print("Program ended succesfully")








if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("parsing_list")
    parser.add_argument("network_list")

    args = parser.parse_args()

    main(args.parsing_list, args.network_list)


