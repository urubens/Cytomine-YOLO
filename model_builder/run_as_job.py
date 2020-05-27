import sys

from cytomine import CytomineJob

from model_builder.preprocessing import preprocess

if __name__ == '__main__':
    params = sys.argv[1:]

    # CytomineJob.from_cli() uses the descriptor.json to automatically create the ArgumentParser
    with CytomineJob.from_cli(params) as cj:
        preprocess(cj, cj.parameters.working_path, cj.parameters.cytomine_id_project, cj.parameters.cytomine_id_terms,
                   cj.parameters.cytomine_id_tags_for_images)
