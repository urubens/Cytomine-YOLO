# YOLO model builder (sample)

This model builder software is a toy software to demonstrate how to get data from Cytomine to train YOLO.
It prepares data in YOLO format, following https://github.com/eriklindernoren/PyTorch-YOLOv3#train-on-custom-dataset

In a given directory, it
* creates an `obj.names` with one class per line
* downloads all requestes images
* creates, for each image, a `txt` file with the same name of the related images where annotations are in the form:
```
    <class> <x_center> <y_center> <width> <height>
```
where 
* `<class>` is the index of the class in the `obj.names` files
* `<x_center>` and `<y_center>` are the center of the annotation, relative to the image size
* `<width>` and `<height>`are the sizes of the annotations, relative to the image size


## Execute as a regular user

To get data from Cytomine as a regular user, use the script `run_as_user.py`

    python run_as_user.py --cytomine_host https://research.cytomine.be --cytomine_public_key XXX --cytomine_private_key XXX --cytomine_id_project 123
    
## Execute as a Cytomine software

The model builder could have additional parameters used in YOLO training. They can be stored in Cytomine with a Cytomine software.
Every execution of this software is a Cytomine Job and its execution parameters are stored in the platform.
The inputs of your Cytomine software are described in the `descriptor.json` file.

More info on how to create a Cytomine software: https://doc.uliege.cytomine.org/display/ALGODOC/%5BHOWTO%5D+Create+a+local+software

### Publish the descriptor to Cytomine

    python publish_descriptor.py --cytomine_host https://research.cytomine.be --cytomine_public_key XXX --cytomine_private_key XXX
   
This script gives you the ID of your newly added Cytomine software.

### Run a job
The `run_as_job.py` file is pretty identical to `run_as_user.py` except that its execution will be done as a Cytomine job and the associated parameters will be linked to the platform.

    python run_as_job.py --cytomine_host https://research.cytomine.be --cytomine_public_key XXX --cytomine_private_key XXX --cytomine_id_project 123 --cytomine_id_software 456
    
