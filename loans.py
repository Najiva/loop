import matplotlib.pyplot as plt
import numpy as np
import math
import json


def rate(loan):
    try:
        return loan['rentRate']
    except KeyError:
        return -1


def loadLoans():
    with open('data.json') as json_file:
        data = json.load(json_file)
        # TODO validate data
        # 1. There are at least two loans
        return data['data']


def dumpLoans(data):
    with open('results/result.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


def monthly(ir, duration, principal):
    val = abs(np.pmt(ir / 12, duration, principal))
    return val

def interests(payment, duration, principal):
    cost = payment * duration - principal
    return cost


# Function to calculate monthly payment, total interests paid and rentRate for each loan
# Function sorts loans based on rentRate
def analyzeLoans(data):
    loans = data['loans']
    totalInterests = 0
    stats = {
        'current': {
        },
        'optimized': {
        }
    }
    for p in loans:
        payment = monthly(p['ir'], p['n'], p['p'])
        p['monthly'] = payment
        p['cost'] = interests(payment, p['n'], p['p'])
        p['rentRate'] = p['cost'] / p['p']
        totalInterests += p['cost']
    stats['current']['totalInterests'] = totalInterests
    data['stats'] = stats
    # Sort loans based on the rentRate
    loans.sort(reverse=True, key=rate)


def showRentRateDrop(loans):
    for loan in loans:
        x = []
        y = []
        for i in range(1, loan['p'] + 1):
            newBalance = loan['p'] - i
            l1 = math.log(1 - ((loan['ir'] / 12) * newBalance) / loan['monthly'])
            l2 = math.log(1 + loan['ir'] / 12)
            newn = abs(l1 / l2)
            interests = (loan['monthly'] * newn - (newBalance))
            rentRate = interests / loan['p']
            x.append(i)
            y.append(rentRate)
        plt.plot(x, y, label=loan['name'])
    plt.legend()
    plt.show()


def optimize(rr, data):
    loans = data['loans']
    totalExtra = 0.0
    totalInterests = 0.0
    for loan in loans:
        x = np.asarray([0, loan['n']], dtype=np.float32)
        y = np.asarray([0, loan['rentRate']], dtype=np.float32)
        # How long should I pay to decrease return to rr?
        xmin = np.interp(rr, y, x)
        # How much should I pay so that I decrease duration to xmin
        mir = 1.0 + (loan['ir'] / 12)
        a = 1.0 - pow(mir, (-1.0) * xmin)
        b = loan['p'] / (1 - pow(mir, (-1.0) * loan['n']))
        extraPayment = loan['p'] - (a * b)
        totalExtra += extraPayment

        # TODO this must not be recalculated every time
        newPrincipal = loan['p'] - extraPayment
        payment = monthly(loan['ir'], xmin, newPrincipal)
        cost = interests(payment, xmin, newPrincipal)
        totalInterests += cost
        optimized = {
            'extra': extraPayment,
            'n': xmin,
            'cost': cost
        }
        loan['optimized'] = optimized
    data['stats']['optimized']['totalInterests'] = totalInterests

    return totalExtra


def main():
    ITERATIONS = 100

    data = loadLoans()

    analyzeLoans(data)

    # Optimization
    minrr = data['loans'][-1]['rentRate']
    maxrr = data['loans'][0]['rentRate']
    rr = (minrr + maxrr) / 2
    needed = 0.0
    for i in range(1, ITERATIONS):
        needed = optimize(rr, data)
        if needed < data['extra']:
            maxrr = rr
            rr = (rr + minrr) / 2
        else:
            minrr = rr
            rr = (rr + maxrr) / 2

    dumpLoans(data)


if __name__ == "__main__":
    main()


# for p in loans:
#     x = []
#     y = []
#     for i in range(1, p['n'] + 1):
#         x.append(i)
#         monthlyPayment = np.pmt(p['ir'] / 12, i, p['p'])
#         u = abs(monthlyPayment) * i - p['p']
#         rentRate = u / p['p']
#         y.append(rentRate)
#         if i == p['n']:
#             p['monthly'] = abs(monthlyPayment)
#             p['cost'] = u
#             p['rentRate'] = rentRate
#             p['x'] = np.asarray(x, dtype=np.float32)
#             p['y'] = np.asarray(y, dtype=np.float32)
#     plt.plot(x, y, label=p['name'])

# # Calculate new payment durations such that all loans will have the best rent rate
# print("---------Loop method---------")
# # What duration is best for me based on rentrate i can afford
# # In this case rent rate of the best loan + 0.0469
# targerRentRate = loans[-1]['rentRate'] + 0.013
# print("Target rent rate: " + str(targerRentRate))
# plt.axhline(y=targerRentRate, color='r', linestyle='-')
# totalExtra = 0.0
# for p in loans:
#     print('+++' + p['name'] + '+++')
#     p['bestDuration'] = np.interp(targerRentRate, p['y'], p['x'])
#     # TODO what if the best duration is the same as original duration
#     print("Best duration: " + str(p['bestDuration']))
#     mir = 1.0 + (p['ir'] / 12)
#     a = 1.0 - pow(mir, (-1.0) * p['bestDuration'])
#     b = p['p'] / (1 - pow(mir, (-1.0) * p['n']))
#     p['extraPayment'] = p['p'] - (a * b)
#     p['newp'] = p['p'] - p['extraPayment']
#     totalExtra += p['extraPayment']
#     print("Extra payment for " + p['name'] + ": " + str(p['extraPayment']))
# print("Total extra payments: " + str(totalExtra))

# Now calculate new total interests paid
# newTotalInterests = 0.0
# for p in loans:
#     monthlyPayment = np.pmt(p['ir'] / 12, p['bestDuration'], p['newp'])
#     u = (abs(monthlyPayment) * p['bestDuration'] - p['newp'])
#     newTotalInterests += u
# print("Total interest after extra payments: " + str(newTotalInterests))
# saving = data['stats']['current']['totalInterests'] - newTotalInterests
# print("Saving interests: " + str(saving))

# Now calculate if the extra payment went to pay for the biggest interest loan first
# print("---------Avalanche method---------")
# t = 0.0
# for p in loans:
#     if p['name'] != 'po2':
#         t += p['cost']
#     else:
#         print("Post od po2 not counted.")
# print("Total interest after extra payments only to po2: " + str(t))
# print("Saving interests: " + str(totalInterests-t))

# print("+++++How much i would save if I paid 7009 to auto.+++++")
# for p in loans:
#     extra = 7009.0
#     if p['name'] == 'po1':
#         # Calculate duration of loan with extra payment
#         newP = p['p'] - extra
#         l1 = math.log(
#             1-((p['ir']/12) * newP)/p['monthly']
#             )
#         l2 = math.log(1+p['ir']/12)
#         newn = abs(l1/l2)
#         u = (p['monthly']*newn - (newP))
#         print("Cost withou extra payment: " + str(p['cost']))
#         print("Saving interests: " + str(p['cost'] - u))
#         print("Difference saved between loop and car first: " + str(saving - (p['cost'] - u)))

# plt.legend()
# plt.show()
