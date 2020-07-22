from dist.louvain import community as community_louvain
import matplotlib.pyplot as plt
import networkx as nx
import collections

# Variables
SIZE = 100
m = 3


def draw_degree_dist(G, title):
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    fig, ax = plt.subplots()
    plt.bar(deg, cnt, width=0.6, color='b')
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    ax.set_xticks([d + 0.4 for d in deg])
    ax.set_xticklabels(deg)
    plt.title(title)


def draw_subnetworks(G, title, turn):
    plt.subplot(3, 5, turn)
    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)
    degreeCount = collections.Counter(degree_sequence)
    deg, cnt = zip(*degreeCount.items())
    plt.bar(deg, cnt, width=0.6, color='b')
    plt.title("Degree Histogram")
    plt.ylabel("Count")
    plt.xlabel("Degree")
    plt.title(title)


# 1. Generating Network
G = nx.barabasi_albert_graph(SIZE, m)

# 2. Drawing Degree Distribution
draw_degree_dist(G, 'Network Degree Distribution')
plt.show()

# 3. Finding Communities in the Network
partition = community_louvain.best_partition(G)

# 4. Printing the Number of Communities
partition_set = set(partition.values())
print('Number of communities: ', len(partition_set))

# 5. Naming Communities
community_dict = {}
for i in range(len(partition_set)):
    string = 'community{}'
    string = string.format(i)
    community_dict[string] = []
for node, comm in partition.items():
    string = 'community{}'
    string = string.format(comm)
    community_dict[string].append(node)

# 6. Printing Size and Nodes of Communities
print('community name   ' + '   community size   ' + '   nodes in the community')
for com_str, node_list in community_dict.items():
    print(com_str + '          ' + str(len(node_list)) + '                   ' + str(node_list))

# 7. Drawing the Colored Network
pos = nx.spring_layout(G)
nx.draw(G, pos, node_color=list(partition.values()), with_labels=True, node_size=250)
plt.show()

# 8. Assigning Communities to Networks
subnetwork_dict = {}
i = 0
for com_str, node_list in community_dict.items():
    new_graph = G.subgraph(node_list)
    string = 'sub_network{}'
    string = string.format(i)
    subnetwork_dict[string] = new_graph
    i += 1

# 9. Drawing Degree Distributions of Subnetworks
i = 1
fig = plt.figure()
for subnetwork_name, graph in subnetwork_dict.items():
    draw_subnetworks(graph, subnetwork_name + ' Degree Distribution', i)
    i += 1
fig.text(.5, .05,
         'Communities in the network seem to be similar structure as original network. Meaning because our initial network is a scale-free network, communities also seem to be scale-free.',
         ha='center', fontsize=12)
fig.text(.5, .025,
         '(it can be seen when selecting network size big enough)',
         ha='center', fontsize=12)
plt.show()
