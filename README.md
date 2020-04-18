# loop
Simple python program to help prioritize loans repayments

# Problem

Different loans have different interest rates and durations, therefore different returns for the banks.
In a situation where a client has an extra capital and wonder what loan should be paid off first, in order to 
minimize total interests paid, one usually goes for the loan with the highest interest rate first. 
However, there are situations when it would be better to split the capital and do the extra payment to multiple loans 
in a specific order. 

# Solution
Based on the amount of the extra capital it's iteratively calculated where and how much money should be put to what loan in order to pay off the loans as efficiently as possible.

# Notes
 - program does not take inflation into consideration
 - it is assumed that extra payments to loans are for free
 - it is assumed that monthly payments will be the same after the extra payment i.e. duration of the loan will decrease

# Usage

The program takes data from the JSON file (data.json) and stores result in result.json.

# Example
