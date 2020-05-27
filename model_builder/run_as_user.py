import sys
from argparse import ArgumentParser

from cytomine import Cytomine

from model_builder.preprocessing import preprocess

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--cytomine_host', dest='host')
    parser.add_argument('--cytomine_public_key', dest='public_key')
    parser.add_argument('--cytomine_private_key', dest="private_key")
    parser.add_argument('--id_project')
    parser.add_argument('--id_terms',
                        help="List of terms to use for dataset, separated by comma. If unset, all terms are used.")
    parser.add_argument('--id_tags_for_images',
                        help="List of tags (id), separated by comma, that images must have to be used in dataset. "
                             "If unset, all images in the project are used.")
    parser.add_argument('--working_path')
    params, _ = parser.parse_known_args(sys.argv[1:])

    with Cytomine(host=params.host, public_key=params.public_key, private_key=params.private_key) as cytomine:
        preprocess(cytomine, params.working_path, params.id_project, params.id_terms, params.id_tags_for_images)
