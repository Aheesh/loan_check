# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
from qualifier.utils.fileio import write_to_csv
import sys
import fire
import questionary
from pathlib import Path

from qualifier.utils.fileio import load_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(qualifying_loans):
    """ Function checks if there are 1 or more qualifying bank loans it provides user a choice to save this list in a CSV file.
    If the user doesn't qualify for any loan option to save in CSV doesn't apply.
    On users approval the function saves the qualifying loans to a CSV file else will display the results on the terminal output screen.
         

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # @TODO: Complete the usability dialog for savings the CSV Files.
    # YOUR CODE HERE!
    
    # Check if there is 1 or more qualifying loans
   # Check if there is 1 or more qualifying loans
    if(len(qualifying_loans)>0):
        print(f"You qualify for {len(qualifying_loans)} loan(s).")
        # collect user response on save results to CSV Yes/No?
        save_to_csv=questionary.confirm("Would you like to save the list of qualified bank(s) and loan(s) to a CSV file?").ask()
        # save to csv scenario
        if(save_to_csv):
            print(f"Call function to save to csv")
            result_path=questionary.text("Where would you like to save the CSV ?").ask()
            result_path=result_path+"/bank_loans_list.csv"
            print(result_path)
            print("loans*****",qualifying_loans)
            # call the write to csv fileio function
            # write_to_csv(result_path,qualifying_loans)
            save_csv(result_path,qualifying_loans)

        # display results on the console screen.
        else:
            print("List of qualified bank loans below ")
            print(qualifying_loans)
    # No qualifying loans to list.
    else:
        print()
        print("********************************* SORRY ****************************************************")
        print("Based on the information provided there are no loan options available from the banks. Please check back for new financing options next calendar month")
        print("********************************************************************************************")
        print()


def save_csv(path,list):
    """ Function to write the results to a csv file. Utilized the module in fileio.py to write to the csv file.         

    Args:
        path , and list : the path to the save the file and list is the results that need to be saved in a csv.
    """
    write_to_csv(path,list)



def run():
    """The main function for running the script."""

    # Load the latest Bank data
    bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)
