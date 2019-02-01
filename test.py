from collections import defaultdict

applicants_data = [
    ('CSC', 'MS', 'REJECT', 1), 
    ('CSC', 'MS', 'ACCEPT', 2),
    ('CSC', 'MS', 'PENDING', 3),
    ('CSC', 'PhD', 'REJECT', 1),
    ('CSC', 'PhD', 'ACCEPT', 2), 
    ('CSC', 'PhD', 'PENDING', 3),
    ('PHY', 'MS', 'REJECT', 1),
    ('PHY', 'MS', 'ACCEPT', 2),
    ('PHY', 'MS', 'PENDING', 3),
    ('PHY', 'MS', 'REJECT', 1),
    ('PHY', 'PhD', 'ACCEPT', 2),
    ('PHY', 'PhD', 'PENDING', 3)
    ]
lst = [(1,'Hello','WOrld',112),(2,'Hello','People',42)]

d = defaultdict(lst)

for k,*v in applicants_data:
    print(k)
print(d)