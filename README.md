# Cytomine for YOLO

The repository gives a starting point to work with YOLO in Cytomine.

## Model builder

The model builder software is a toy software to demonstrate how to get data from Cytomine to train YOLO.
It prepares data in YOLO format, following https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects

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

## Predictor

The predictor software is a toy software to demonstrate how to add output predictions as analysis annotations to Cytomine.

## Evaluation

The evalution script shows how to get groundtruths and output predictions for a given execution in order to make a further offline evaluation analysis.