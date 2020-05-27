import sys

from cytomine import CytomineJob

from model_builder.preprocessing import preprocess

if __name__ == '__main__':
    params = sys.argv[1:]

    # CytomineJob.from_cli() uses the descriptor.json to automatically create the ArgumentParser
    with CytomineJob.from_cli(params) as cj:
        cj.job.update(statusComment="Preprocessing...", progress=1)
        result = preprocess(cj, cj.parameters.working_path, cj.parameters.cytomine_id_project, cj.parameters.cytomine_id_terms,
                   cj.parameters.cytomine_id_tags_for_images)

        classes_filename, image_filenames, annotation_filenames = result
        print("The classes are in file: {}".format(classes_filename))
        print("There are {} images".format(len(image_filenames)))
        print("There are {} annotation files".format(len(annotation_filenames)))

        # Train YOLO
        cj.job.update(statusComment="Start to train YOLO", progress=5)
        # TODO

        # Save model
        cj.job.update(statusComment="Saving model", progress=95)
        # TODO

        cj.job.update(statusComment="Finished", progress=100)
