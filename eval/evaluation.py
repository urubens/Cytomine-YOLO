import sys
from argparse import ArgumentParser
from cytomine import Cytomine
from cytomine.models import ImageInstanceCollection, AnnotationCollection

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--cytomine_host')
    parser.add_argument('--cytomine_public_key')
    parser.add_argument('--cytomine_private_key')
    parser.add_argument('--cytomine_id_tags_for_images',
                        help="List of tags (id), separated by comma, that images must have to be used in dataset. "
                             "If unset, all images in the project are used.")
    parser.add_argument('--cytomine_id_job')
    params, _ = parser.parse_known_args(sys.argv[1:])

    with Cytomine(params.cytomine_host, params.cytomine_public_key, params.cytomine_private_key) as c:
        id_tags_for_images = params.cytomine_id_tag_for_images
        id_project = params.cytomine_id_project

        image_tags = id_tags_for_images if id_tags_for_images else None
        images = ImageInstanceCollection(tags=image_tags).fetch_with_filter("project", id_project)
        image_ids = [image.id for image in images]

        groundtruths = AnnotationCollection()
        groundtruths.showTerm = True
        groundtruths.showWKT = True
        groundtruths.images = image_ids
        groundtruths.fetch()

        predictions = AnnotationCollection()
        predictions.showTerm = True
        predictions.showWKT = True
        predictions.images = True
        predictions.job = params.cytomine_id_job
        predictions.fetch()

        print("There are  {} groundtruths and {} predictions".format(len(groundtruths), len(predictions)))
