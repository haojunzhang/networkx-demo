import matplotlib.pyplot as plt
import networkx as nx
from models import Account, Transaction, AccountRelation
import random
import uuid


def get_accounts():  # 帳戶, 交易資料
    accounts = []
    for i in range(8):
        accounts.append(Account('a' + str(i)))
    return accounts


def random_2_number_not_repeat(fr, to):  # 隨機兩數字不重複
    if fr == to:
        return fr, to
    i1 = random.randint(fr, to)
    i2 = random.randint(fr, to)
    while i1 == i2:
        i2 = random.randint(fr, to)
    return i1, i2


def random_money():  # 隨機金額(10,000 ~ 1,000,000)
    return random.randint(1, 100) * 10000


def generate_transactions(count):  # 產生交易紀錄
    accounts = get_accounts()
    transactions = []
    for i in range(count):  # 產生count次交易紀錄
        i1, i2 = random_2_number_not_repeat(0, len(accounts)-1)
        from_account = accounts[i1]
        to_account = accounts[i2]
        amount = random_money()
        transactions.append(Transaction(from_account, to_account, amount))
    return transactions


def calculate_account_relation(accounts, transactions):  # 計算每個帳戶與其他帳戶的關係
    account_relations = []

    # 先塞滿
    for a in accounts:
        relative_account = {}
        for a2 in accounts:
            if a != a2:  # 跳過自己
                relative_account[a2.name] = 0
        account_relations.append(AccountRelation(a, relative_account))

    # 將transactions分配到
    for t in transactions:

        # 累積from_account與to_account交易關係
        for ar in account_relations:
            if ar.account == t.from_account:
                ar.relative_account[t.to_account.name] += t.amount

        # 累積to_account與from_account交易關係
        for ar in account_relations:
            if ar.account == t.to_account:
                ar.relative_account[t.from_account.name] += t.amount

    return account_relations


def get_total_amount_from_2_accounts(ar1, ar2, account_relations):
    for ar in account_relations:
        if ar == ar1:
            return ar.relative_account[ar2.account.name]
    return 0


accounts = get_accounts()
transactions = generate_transactions(1000)
account_relations = calculate_account_relation(accounts, transactions)

for ar in account_relations:
    print(ar)

G = nx.Graph()  # Create a graph object called G

total_amounts = []
for ar in account_relations:
    G.add_node(ar.account.name)
    total_amounts.append(ar.get_total_amount())

max_amount = max(total_amounts)
min_amount = min(total_amounts)
delta_amount = max_amount - min_amount
total_amount = sum(total_amounts)

# Note: You can also try a spring_layout
pos = nx.circular_layout(G)

sizes = []
for amount in total_amounts:
    my_delta = amount - min_amount + 1 
    
    weight = my_delta * 1.0 / delta_amount  # 0~1
    
    # 100~2000
    size = weight * 1900 + 100

    sizes.append(size)
    print(my_delta, weight, size)
nx.draw_networkx_nodes(G,
                        pos,
                        node_color='green',
                        node_size=sizes)

# 3. If you want, add labels to the nodes
labels = {}
for ar in account_relations:
    labels[ar.account.name] = ar.account.name
nx.draw_networkx_labels(G, pos, labels, font_size=16)

for i in range(len(account_relations)-1):
    for j in range(i+1, len(account_relations)-1):
        G.add_edge(account_relations[i].account.name,
                   account_relations[j].account.name,
                   weight=get_total_amount_from_2_accounts(account_relations[i], account_relations[j], account_relations))

all_weights = []
for (node1, node2, data) in G.edges(data=True):
    all_weights.append(data['weight'])

unique_weights = list(set(all_weights))

for weight in unique_weights:
    weighted_edges = [(node1, node2) for (node1, node2, edge_attr) in G.edges(
        data=True) if edge_attr['weight'] == weight]
    # width=1~20
    width = weight * 1.0 / sum(all_weights) * 19 + 1
    nx.draw_networkx_edges(G, pos, edgelist=weighted_edges, width=width)

plt.axis('off')
plt.savefig("chess_legends.png")
plt.show()
