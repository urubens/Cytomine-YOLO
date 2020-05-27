import os
import sys
from argparse import ArgumentParser

from cytomine import Cytomine
from cytomine.models import TermCollection, ImageInstanceCollection, AnnotationCollection
from shapely import wkt
from shapely.affinity import affine_transform

CLASSES_FILENAME = "obj.names"


def change_referential(geometry, height):
    matrix = [1, 0, 0, -1, 0, height]
    return affine_transform(geometry, matrix)


def geometry_to_yolo(geom, image_width, image_height):
    """
    Convert a Cytomine geometry to YOLO format.
    :param geom: The geometry to convert
    :param image_width:
    :param image_height:
    :return:
    """
    # Change referential as Cytomine annotations are in a cartesian coordinate system
    geom = change_referential(geom, image_height)

    # https://shapely.readthedocs.io/en/latest/manual.html#object.bounds
    minx, miny, maxx, maxy = geom.bounds

    # <x_center> <y_center> <width> <height> -
    # float values relative to width and height of image, it can be equal from (0.0 to 1.0]
    x_center = float((minx + maxx)) / 2 / image_width
    y_center = float((miny + maxy)) / 2 / image_height
    w = float((maxx - minx)) / image_width
    h = float((maxy - miny)) / image_height
    return x_center, y_center, w, h


def preprocess(cytomine, working_path, id_project, id_terms=None, id_tags_for_images=None):
    if not os.path.exists(working_path):
        os.makedirs(working_path)

    terms = TermCollection().fetch_with_filter("project", id_project)
    if id_terms:
        filtered_term_ids = [int(id_term) for id_term in id_terms.split(',')]
        filtered_terms = [term for term in terms if term.id in filtered_term_ids]
    else:
        filtered_terms = terms
    terms_indexes = {term.id: i for i, term in enumerate(filtered_terms)}

    # https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects
    # Write obj.names
    with open(os.path.join(working_path, CLASSES_FILENAME), 'w') as f:
        for term in filtered_terms:
            f.write(term.name + os.linesep)

    # Download images
    image_tags = id_tags_for_images if id_tags_for_images else None
    images = ImageInstanceCollection(tags=image_tags).fetch_with_filter("project", id_project)
    for image in images:
        image.dump(os.path.join(working_path, "{id}.png"), override=False)

    # Create annotation files
    for image in images:
        annotations = AnnotationCollection()
        annotations.image = image.id
        annotations.terms = [t.id for t in filtered_terms] if id_terms else None
        annotations.showWKT = True
        annotations.showTerm = True
        annotations.fetch()

        with open(os.path.join(working_path, "{}.txt".format(image.id)), 'w') as f:
            for annotation in annotations:
                geometry = wkt.loads(annotation.location)
                x, y, w, h = geometry_to_yolo(geometry, image.width, image.height)
                for term_id in annotation.term:
                    # <object-class> <x_center> <y_center> <width> <height>
                    f.write("{} {:.6f} {:.6f} {:.6f} {:.6f}".format(terms_indexes[term_id], x, y, w, h) + os.linesep)