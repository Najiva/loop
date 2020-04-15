import matplotlib.pyplot as plt
import numpy as np        

loans = [
    {
        'name': 'auto',
        'ir': 0.049,
        'n': 70,
        'p': 17000
    },
    {
        'name': 'hypo',
        'ir': 0.0159,
        'n': 134,
        'p': 22095
    },
    {
        'name': 'hypo2',
        'ir': 0.0159,
        'n': 126,
        'p': 91900
    },
    {
        'name': 'po1',
        'ir': 0.06,
        'n': 71,
        'p': 11600
    },
    {
        'name': 'po2',
        'ir': 0.075,
        'n': 39,
        'p': 4740
    }
]

# Calculate how expensie renting the money is
totalInterests = 0
for p in loans:
    x = []
    y = []
    for i in range(1,p['n']+1):
        x.append(i)
        monthlyPayment = np.pmt(p['ir']/12, i, p['p']);
        u = (abs(monthlyPayment)*i- p['p'])
        rentRate = u/ p['p']
        y.append(rentRate)
        if i == p['n']:
            print("Last iteration")
            p['monthly'] = monthlyPayment
            p['cost'] = u 
            p['rentRate'] = rentRate
            totalInterests+=u
    plt.plot(x, y, label=p['name'])
       
print("Total interests: " + str(totalInterests))

# Try to optimize loans such that the they are as good as the best loan
bestRentRate = loans[0]['rentRate']
bestLoan = loans[0]['name']
for p in loans:
    if p['rentRate'] < bestRentRate:
        bestRentRate = p['rentRate']
        bestLoan = p['name']
print("Best loan: " + bestLoan + '(' + str(bestRentRate) + ')')
plt.axhline(y=bestRentRate, color='r', linestyle='-')

plt.legend()
plt.show()

    

