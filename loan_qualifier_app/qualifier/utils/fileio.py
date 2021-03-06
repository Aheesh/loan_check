# -*- coding: utf-8 -*-
"""Helper functions to load and save CSV data.

This contains a helper function for loading and saving CSV files.

"""
import csv


def load_csv(csvpath):
    """Reads the CSV file from path provided.

    Args:
        csvpath (Path): The csv file path.

    Returns:
        A list of lists that contains the rows of data from the CSV file.

    """
    with open(csvpath, "r") as csvfile:
        data = []
        csvreader = csv.reader(csvfile, delimiter=",")

        # Skip the CSV Header
        next(csvreader)

        # Read the CSV data
        for row in csvreader:
            data.append(row)
    return data


def write_to_csv(csvpath,data):
    """ Function to write to a CSV file to the parameter path provided at function call.
    
    Args:
        csvpath (Path): The CSV file path to save the file.
        data : The data to save in CSV.

    """
    with open(csvpath, 'w',newline='') as csvfile:
        csvwriter=csv.writer(csvfile)
        for row in data:
            csvwriter.writerow(row)
