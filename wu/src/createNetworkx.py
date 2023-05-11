import copy 
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# - - - - - - - - - - - - - - 
DICT_REVIT_RES = r'C:\dev\teaching\bscelvira\super-constraints\wu\data' # to change
DICT_ANALYSIS_RES = r'C:\dev\teaching\bscelvira\super-constraints\wu\res' # to change

TOPO_OBJECT_NAME = "\collected_topology_wall_"
TOPO_SPACE_NAME = "\collected_topology_space_"
TOPO_PARAMETER_NAME = "\collected_topology_GP_"

FILE_OBJECT_HOST = DICT_REVIT_RES + TOPO_OBJECT_NAME + 'host.txt'
FILE_OBJECT_WALLS = DICT_REVIT_RES + TOPO_OBJECT_NAME + 'walls.txt'
FILE_OBJECT_SLABS = DICT_REVIT_RES + TOPO_OBJECT_NAME + 'slabs.txt'
FILE_OBJECT_INSERTS = DICT_REVIT_RES + TOPO_OBJECT_NAME + 'inserts.txt'

FILE_SPACE_HOST = DICT_REVIT_RES + TOPO_SPACE_NAME + 'host.txt'
FILE_SPACE_WALLS = DICT_REVIT_RES + TOPO_SPACE_NAME + 'walls.txt'
FILE_SPACE_DOORS = DICT_REVIT_RES + TOPO_SPACE_NAME + 'doors.txt'

FILE_PARAMETER_HOST = DICT_REVIT_RES + TOPO_PARAMETER_NAME + 'host.txt'
FILE_PARAMETER_OBJECTS = DICT_REVIT_RES + TOPO_PARAMETER_NAME + 'objects.txt'

# - - - - - - - - - - - - - - 
def flatten(list):
    return [item for sublist in list for item in sublist]


def get_data_from_h5(h5doc, key):
    """
    Collect data from .h5 file by specifying the store key.
    """

    allData = pd.HDFStore(h5doc, 'r')
    data = allData[key]
    return data


def split_guids(guids, separator=','):
    """
    """
    
    guid_multilist = copy.deepcopy(guids)
    for ii in range(len(guid_multilist)):
        if separator in guid_multilist[ii]:
            guid_multilist[ii] = guid_multilist[ii].split(separator)
        elif guid_multilist[ii]:
            guid_multilist[ii] = [guid_multilist[ii]]
        else:
            continue

    return guid_multilist


def build_guid_edges(lst_host,lst_targets,set_sort=True):
    """
    """
    
    all_edges = []
    if len(lst_host) != len(lst_targets):
        return all_edges
    else:
        for host,targets in zip(lst_host,lst_targets):
            edges_per_host = []
            actual_targets = [tt for tt in targets if (tt != host[0] and tt)]
            edges_per_host = [[host[0],target] for target in actual_targets]
            all_edges.append(edges_per_host)
    
    all_edges = flatten(all_edges)
    if set_sort:
        all_edges = [sorted(x, key = lambda x:x[0]) for x in all_edges]
    all_edges = [list(i) for i in set(map(tuple, all_edges))]
    return all_edges


def build_networkx_graph(all_df_edges, all_dict_attrs=[]):
    """
    """

    G_all = []
    for df in all_df_edges:
        G = nx.Graph()
        G = nx.from_pandas_edgelist(df, 'host', 'target')
        G_all.append(G)
    
    G_all = nx.compose_all(G_all)

    if all_dict_attrs:
        for dict_attrs in all_dict_attrs:
            nx.set_node_attributes(G_all, dict_attrs)

    return G_all


def update_graph_nodes(G, nn, label):
    """
    update the networkx graph with additonal nodes.
    """

    df_update = pd.DataFrame(nn, columns = ['node_name'])
    df_update['classification'] = label
    df_update = df_update.set_index('node_name')
    df_update = df_update[~df_update.index.duplicated(keep='first')]
    attrs = df_update.to_dict(orient = 'index')
    nx.set_node_attributes(G, attrs)


def plot_networkx_per_rule(
        path, G, nodesize_map, nodecolor_map):
    """
    plot the networkx graph with specified maps for node size and node color.
    """

    fig = plt.figure(figsize=(30, 18))
    ax = plt.axes((0.05, 0.05, 0.90, 0.90))
    G_nodes = G.nodes()
    G_nodes_sizes = [nodesize_map[G.nodes[n]['classification']] for n in G_nodes]
    G_nodes_colors = [nodecolor_map[G.nodes[n]['classification']] for n in G_nodes]

    nx.draw_networkx(
        G,
        # pos = nx.nx_agraph.graphviz_layout(G, prog="neato"), # doesnot work
        pos = nx.kamada_kawai_layout(G, scale=0.75),
        with_labels=False,
        node_size=G_nodes_sizes,
        node_shape="o",
        node_color=G_nodes_colors,
        linewidths=0.1,
        width=0.5,
        alpha=0.80,
        edge_color='black')
    ax.title.set_position([.5, 0.975])

    for kk in list(nodecolor_map.keys()):
        plt.scatter([],[], c=nodecolor_map[kk], label=kk)

    plt.legend()
    plt.savefig(path + '\\' + 'G.png', dpi=200)

# - - - - - - - - - - - - - - 
# wall-based
guid_wall_host, guid_wall_inserts, guid_wall_walls, guid_wall_slabs = [],[],[],[]
with open(FILE_OBJECT_HOST) as file:
    for line in file:
        guid_wall_host.append(line.rstrip())
with open(FILE_OBJECT_WALLS) as file:
    for line in file:
        guid_wall_walls.append(line.rstrip())
with open(FILE_OBJECT_SLABS) as file:
    for line in file:
        guid_wall_slabs.append(line.rstrip())
with open(FILE_OBJECT_INSERTS) as file:
    for line in file:
        guid_wall_inserts.append(line.rstrip())

### to solve 
# ISSUE: miss the last line for guid_wall_inserts
guid_wall_inserts.append('')
### to solve 

# space-based
guid_space_host, guid_space_walls, guid_space_doors= [],[],[]
with open(FILE_SPACE_HOST) as file:
    for line in file:
        guid_space_host.append(line.rstrip())
with open(FILE_SPACE_WALLS) as file:
    for line in file:
        guid_space_walls.append(line.rstrip())
with open(FILE_SPACE_DOORS) as file:
    for line in file:
        guid_space_doors.append(line.rstrip())

# GP-based
guid_parameter_host, guid_parameter_objects = [],[]
with open(FILE_PARAMETER_HOST) as file:
    for line in file:
        guid_parameter_host.append(line.rstrip())
with open(FILE_PARAMETER_OBJECTS) as file:
    for line in file:
        guid_parameter_objects.append(line.rstrip())

# - - - - - - - - - - - - - - 
# Build networkx edges 
# wall-based edges.
guid_wall_host_indi = split_guids(guid_wall_host)
guid_wall_walls_indi = split_guids(guid_wall_walls)
guid_wall_inserts_indi = split_guids(guid_wall_inserts)
guid_wall_slabs_indi = split_guids(guid_wall_slabs)

edges_wall_h_walls = build_guid_edges(guid_wall_host_indi, guid_wall_walls_indi)
edges_wall_h_inserts = build_guid_edges(guid_wall_host_indi, guid_wall_inserts_indi)
edges_wall_h_slabs = build_guid_edges(guid_wall_host_indi, guid_wall_slabs_indi)

df_edges_wall_h_walls = pd.DataFrame.from_records(edges_wall_h_walls, columns = ['host','target'])
df_edges_wall_h_inserts = pd.DataFrame.from_records(edges_wall_h_inserts, columns = ['host','target'])
df_edges_wall_h_slabs = pd.DataFrame.from_records(edges_wall_h_slabs, columns = ['host','target'])

# space-based edges.
guid_space_host_indi = split_guids(guid_space_host)
guid_space_walls_indi = split_guids(guid_space_walls)
guid_space_doors_indi = split_guids(guid_space_doors)

edges_space_h_walls = build_guid_edges(guid_space_host_indi, guid_space_walls_indi)
edges_space_h_doors = build_guid_edges(guid_space_host_indi, guid_space_doors_indi)

df_edges_space_h_walls = pd.DataFrame.from_records(edges_space_h_walls, columns = ['host','target'])
df_edges_space_h_doors = pd.DataFrame.from_records(edges_space_h_doors, columns = ['host','target'])

# GP-based edges.
guid_parameter_host_indi = split_guids(guid_parameter_host)
guid_parameter_objects_indi = split_guids(guid_parameter_objects)
edges_parameter_h_objects = build_guid_edges(guid_parameter_host_indi, guid_parameter_objects_indi, set_sort=False)
df_edges_parameter_h_objects = pd.DataFrame.from_records(edges_parameter_h_objects, columns = ['host','target'])

# - - - - - - - - - - - - - - 
# Build networkx attributes
# object attributes
df_doorinstances = pd.read_csv(DICT_REVIT_RES+'\df_Doors.csv', index_col ='ifcguid')
df_windowinstances = pd.read_csv(DICT_REVIT_RES+'\df_Windows.csv', index_col ='ifcguid')
df_wallinstances = pd.read_csv(DICT_REVIT_RES+'\df_Walls.csv', index_col ='ifcguid')
df_slabinstances = pd.read_csv(DICT_REVIT_RES+'\df_Slabs.csv', index_col ='ifcguid')

attrs_door = df_doorinstances.to_dict(orient = 'index')
attrs_window = df_windowinstances.to_dict(orient = 'index')
attrs_wall = df_wallinstances.to_dict(orient = 'index')
attrs_slab = df_slabinstances.to_dict(orient = 'index')

# space attributes
df_spaceinstances = pd.read_csv(DICT_REVIT_RES+'\df_Spaces.csv', index_col ='ifcguid')
attrs_space = df_spaceinstances.to_dict(orient = 'index')

# GP attibutes
df_gp_instances = pd.read_csv(DICT_REVIT_RES+'\df_Parameters.csv', index_col ='name')
attrs_gp = df_gp_instances.to_dict(orient = 'index')

# all edges.
all_df_edges_object = [df_edges_wall_h_walls, df_edges_wall_h_slabs] # df_edges_wall_h_inserts
all_df_edges_space = [df_edges_space_h_walls] #df_edges_space_h_doors
all_df_edges_parameter = [df_edges_parameter_h_objects]
all_df_edges = all_df_edges_object + all_df_edges_space + all_df_edges_parameter

# all attributes
all_dict_attrs = [attrs_door, attrs_window, attrs_wall, attrs_slab, attrs_space, attrs_gp] 
G_all = build_networkx_graph(all_df_edges, all_dict_attrs)

# - - - - - - - - - - - - - - 
# visualization
nodesize_map_by_object_type = {
    'Element_Door':50,
    'Element_Window':50,
    'Element_Wall':50,
    'Element_Slab':50,
    'Space':150,
    'Parameter_Global':30,
    }

nodecolor_map_by_object_type = {
    'Element_Door':'green',
    'Element_Window':'skyblue',
    'Element_Wall':'darkorange',
    'Element_Slab':'yellow',
    'Space':'navy',
    'Parameter_Global':'grey',
    }

# - - - - - - - - - - - - - - 
#plot the networkx.
plot_networkx_per_rule(
    DICT_ANALYSIS_RES, G_all, nodesize_map_by_object_type, nodecolor_map_by_object_type)
