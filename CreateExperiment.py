import numpy as np
from qwanta import Xperiment, Configuration
import matplotlib.pyplot as plt
import pandas as pd
from math import radians, cos, sin, asin, sqrt
import dill
import requests
import sys
import pandas as pd

# %%

def execute(parameter):
    index = parameter['index']
    loss = parameter['loss rate'] # dB/km
    depo_prob = parameter['depolarizing rate']
    gate_error = parameter['gate error rate']
    measurement_error = parameter['measurement error']
    memory_time = parameter['memory error']
    repeat_th = parameter['trajectory']

    node_info = {
            'A': {'coordinate': (0, 0, 0)},
            'B': {'coordinate': (100, 0, 0)},
            'C': {'coordinate': (200, 0, 0)},
            'numPhysicalBuffer': 20,
            'numInternalEncodingBuffer': 20,
            'numInternalDetectingBuffer': 10,
            'numInternalInterfaceBuffer': 2,
        }

    Quantum_topology = {
            ('A', 'B'): {
            'connection-type': 'Space',
            'function': p_dep,
            'loss': loss,
            'light speed': 300000, # km/s
            'Pulse rate': 0.0001, # waiting time for next qubit (interval)
            'memory function': 1,
            'depolarlizing error': [1, 0, 0, 0],
            },
            ('B', 'C'): {
            'connection-type': 'Space',
            'function': p_dep,
            'loss': loss,
            'light speed': 300000,
            'Pulse rate': 0.0001,
            'memory function': 1,
            'depolarlizing error': [1, 0, 0, 0],
            },
            ('A', 'C'): {
            'connection-type': 'Space',
            'function': p_dep,
            'loss': loss,
            'light speed': 300000,
            'Pulse rate': 0.0001,
            'memory function': 1,
            'depolarlizing error': [1, 0, 0, 0],
            },
        }

    exps = Xperiment(
        timelines_path = f'exper_id3_selectedStats_2hops.xlsx',
        nodes_info_exp = node_info,
        edges_info_exp = Quantum_topology,
        gate_error = gate_error,
        measurement_error = measurement_error,
        memory_time = memory_time,
        experiment = f'p{index}_r{repeat_th}',
    )

    exps.execute(save_result=True)

    return True

# %%

loss_list =  np.array([0.1])
p_dep_list = np.array([0.025])
gate_error_list = np.array([0.0005])
mem_error_list = np.array([0.01])
measurement_error_list =  np.array([0])
number_of_hops_list = np.array([2]) 
num_trajectories = 5
exp_names = ['Sheet1']

parameters_set = []; index = 0
for hops in number_of_hops_list:
    for loss in loss_list:
        for p_dep in p_dep_list:
            for gate_error in gate_error_list:
                for mem_error in mem_error_list:
                    for measure_error in measurement_error_list:
                        for trajectory in range(num_trajectories):
                            parameters_set.append({
                                'index': int(index),
                                'loss rate': loss, 
                                'depolarizing rate': p_dep, 
                                'gate error rate': gate_error, 
                                'memory error': mem_error,
                                'measurement error': measure_error,
                                'number of hops': hops,
                                'trajectory': trajectory
                                })
                        index += 1



df = pd.DataFrame(parameters_set)
# %%

result = [execute(i) for i in parameters_set]