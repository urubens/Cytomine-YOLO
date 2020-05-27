import sys
from argparse import ArgumentParser

from cytomine import Cytomine

from model_builder.preprocessing import preprocess

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--cytomine_host')
    parser.add_argument('--cytomine_public_key')
    parser.add_argument('--cytomine_private_key')
    parser.add_argument('--cytomine_id_project')
    parser.add_argument('--cytomine_id_terms',
                        help="List of terms to use for dataset, separated by comma. If unset, all terms are used.")
    parser.add_argument('--cytomine_id_tags_for_images',
                        help="List of tags (id), separated by comma, that images must have to be used in dataset. "
                             "If unset, all images in the project are used.")
    parser.add_argument('--working_path')
    params, _ = parser.parse_known_args(sys.argv[1:])

    with Cytomine(host=params.cytomine_host, public_key=params.cytomine_public_key, private_key=params.cytomine_private_key) as cytomine:
        result = preprocess(cytomine, params.working_path, params.cytomine_id_project, params.cytomine_id_terms, params.cytomine_id_tags_for_images)

        classes_filename, image_filenames, annotation_filenames = result
        print("The classes are in file: {}".format(classes_filename))
        print("There are {} images".format(len(image_filenames)))
        print("There are {} annotation files".format(len(annotation_filenames)))
