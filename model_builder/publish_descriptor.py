import sys
from argparse import ArgumentParser
from cytomine import Cytomine
from cytomine.utilities.descriptor_reader import read_descriptor

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--cytomine_host')
    parser.add_argument('--cytomine_public_key')
    parser.add_argument('--cytomine_private_key')
    params, _ = parser.parse_known_args(sys.argv[1:])

    with Cytomine(params.cytomine_host, params.cytomine_public_key, params.cytomine_private_key) as c:
        software = read_descriptor("descriptor.json")
        print("The software ID is: {}".format(software.id))
