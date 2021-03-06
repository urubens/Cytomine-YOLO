import os
import sys

from cytomine import CytomineJob
from cytomine.models import ImageInstanceCollection, TermCollection, AnnotationCollection, Annotation, Property
from shapely.affinity import affine_transform
from shapely.geometry import box

CLASSES_FILENAME = "classes.names"
IMG_DIRECTORY = "images"
ANNOTATION_DIRECTORY = "labels"


def change_referential(geometry, height):
    matrix = [1, 0, 0, -1, 0, height]
    return affine_transform(geometry, matrix)



def yolo_to_geometry(geom, image_width, image_height):
    x_center, y_center, w, h = geom

    minx = image_width * (x_center - w/2)
    maxx = image_width * (x_center + w/2)
    miny = image_height * (y_center - h/2)
    maxy = image_height * (y_center + h/2)

    geom = box(minx, miny, maxx, maxy)
    # Change referential as Cytomine annotations are in a cartesian coordinate system
    geom = change_referential(geom, image_height)

    return geom


def run(argv):
    # CytomineJob.from_cli() uses the descriptor.json to automatically create the ArgumentParser
    with CytomineJob.from_cli(argv) as cj:
        cj.job.update(statusComment="Initialization...")
        id_project = cj.parameters.cytomine_id_project
        id_terms = cj.parameters.cytomine_id_terms
        id_tags_for_images = cj.parameters.cytomine_id_tags_for_images
        working_path = cj.parameters.working_path

        terms = TermCollection().fetch_with_filter("project", id_project)
        if id_terms:
            filtered_term_ids = [int(id_term) for id_term in id_terms.split(',')]
            filtered_terms = TermCollection()
            for term in terms:
                if term.id in filtered_term_ids:
                    filtered_terms.append(term)
        else:
            filtered_terms = terms

        # Associate YOLO class index to Cytomine term
        classes_filename = os.path.join(working_path, CLASSES_FILENAME)
        with open(classes_filename, 'r') as f:
            classes = f.readlines()
            indexes_terms = {}
            for i, _class in enumerate(classes):
                _class = _class.strip()
                indexes_terms[i] = filtered_terms.find_by_attribute("name", _class)

        cj.job.update(statusComment="Open model...", progress=1)
        # TODO...

        cj.job.update(statusComment="Predictions...", progress=5)
        images = ImageInstanceCollection(tags=id_tags_for_images).fetch_with_filter("project", id_project)
        for image in images:
            print("Prediction for image {}".format(image.instanceFilename))
            # TODO: get predictions from YOLO
            # TODO: I suppose here for the sake of the demo that the output format is the same as input, which is not sure
            # <class> <x_center> <y_center> <width> <height> <proba>
            sample_predictions = [
                (0, 0.604000000000, 0.493846153846, 0.105600000000, 0.461538461538, 0.9),
                (0, 0.409200000000, 0.606153846154, 0.050400000000, 0.095384615385, 0.5)
            ]

            ac = AnnotationCollection()
            for pred in sample_predictions:
                _class, xcenter, ycenter, width, height, proba = pred
                term_ids = [indexes_terms[_class].id] if _class in indexes_terms.keys() else None
                if term_ids is None:
                    print("No term found for class {}".format(_class))
                geometry = yolo_to_geometry((xcenter, ycenter, width, height), image.width, image.height)
                properties = [{"key": "probability", "value": proba}]
                ac.append(Annotation(id_image=image.id, id_terms=term_ids, location=geometry.wkt, properties=properties))

            ac.save()

        cj.job.update(statusComment="Finished", progress=100)


if __name__ == '__main__':
    argv = sys.argv[1:]
    run(argv)

