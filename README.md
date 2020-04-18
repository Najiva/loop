# loop
Simple python program to help prioritize loan repayments.

# Problem

Different loans have different interest rates and durations, therefore different returns for the banks.
In a situation where a client has an extra capital and wonder what loan should be paid off first, in order to 
minimize total interests paid, one usually goes for the loan with the highest interest rate first. 
However, there are situations when it would be better to split the capital and do the extra payment to multiple loans 
in a specific order. 

# Solution
Based on the amount of the extra capital it's iteratively calculated where and how much money should be put to what loan in order to pay off the loans as efficiently as possible.

## Notes
 - program does not take inflation into consideration
 - it is assumed that extra payments to loans are for free
 - it is assumed that monthly payments will be the same after the extra payment i.e. duration of the loan will decrease
 - there must be at least two loans

## Usage

The program takes data from the JSON file (data.json) and stores result in result.json.

## Example

Let's say John has spare 3700 Euro. For example, because he did not go for a vacation this year due to coronavirus. He decides to use the money to repay one of his loans. He has 2 loans.

 1. Loan for a car has a current principal of 11,000 Euro, an annual interest rate of 6 % and he has 62 monthly payments remaining.
 2. Loan for a bike has a current principal of 3,700 Euro, an annual interest rate of 7.5 % and he has 30 months to go.

The loan for the bike has a higher interest rate, so he decides to pay it off, which will save him *370,-* Euro on interests during the period of 30 months. Now if he chooses to do the extra payment to the car loan, he will be able to pay the car loan 2 years faster and will save him *1120,-* Euro over a period of 39 months.

### data.json
```json
{
    "data": {
        "id": "John",
        "extra": 3700,
        "loans": [
            {
                "name": "car",
                "ir": 0.06,
                "n": 62,
                "p": 11000
            },
            {
                "name": "bike",
                "ir": 0.075,
                "n": 30,
                "p": 3700
            },
        ]
    }
}
```
