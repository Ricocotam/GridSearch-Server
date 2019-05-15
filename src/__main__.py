import itertools
import json

from argparse import ArgumentParser

from fabric import Connection

from .utils import LockedIterator
from .gridsearch import product, listing
from .generator import CommandGenerator
from .machines import Server, GPU


def get_formating_function(string):
    return lambda params, gpu: string.format(gpu=gpu, **params)


def get_param_sets(filename):
    with open(filename, "r") as f:
        a = json.load(f)
    params = a["parameters"]
    iterators = []
    for conf in params:
        if conf["type"] == "listing":
            iterators.append(listing(*conf["parameters"]))
        elif conf["type"] == "product":
            iterators.append(product(**conf["parameters"]))
    
    iterator = itertools.chain(*iterators)
    formating_function = get_formating_function(a["format"])
    return iterator, formating_function


def get_servers_gpus(filename, generator):
    with open(filename, "r") as f:
        a = json.load(f)
    
    servers = {
        server["name"]:
                Server(server["name"], generator, 
                       Connection(server["name"]), server["prefixs"])
        for server in a["servers"]
    }
 
    gpus = [
        GPU(gpu["name"], gpu["max_xp"], servers[server["name"]])
        for server in a["servers"]
        for gpu in server["gpus"]
    ]
    return servers.values(), gpus


def main(paramset_file, server_file):
    iterator, formating_function = get_param_sets(paramset_file)
    iterator = LockedIterator(iterator)
    generator = CommandGenerator(iterator, formating_function)
    
    servers, gpus = get_servers_gpus(server_file, generator)

    print(len(gpus), "gpus and", len(servers), "servers")

    for server in servers:
        server.start()
    
    for gpu in gpus:
        gpu.start()


if __name__ == "__main__":
    main(paramset_file="params.json", server_file="servers.json")
