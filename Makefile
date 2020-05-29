HOST=https://research.cytomine.be
PUBKEY=XXX
PRIVKEY=XXX

WORKING_PATH=data

ID_PROJECT=156585393
ID_TERMS=156585427
ID_TRAIN_TAG=155359903
ID_TEST_TAG=155359909

ID_SOFTWARE_TRAIN=156573814
ID_SOFTWARE_PREDICT=156587029


train_as_user:
	python model_builder/run_as_user.py --cytomine_host $(HOST) --cytomine_public_key $(PUBKEY) --cytomine_private_key $(PRIVKEY) --cytomine_id_project $(ID_PROJECT) --working_path $(WORKING_PATH) --cytomine_id_terms $(ID_TERMS) --cytomine_id_tags_for_images $(ID_TRAIN_TAG)

train_as_job:
	python model_builder/run_as_job.py --cytomine_host $(HOST) --cytomine_public_key $(PUBKEY) --cytomine_private_key $(PRIVKEY) --cytomine_id_project $(ID_PROJECT) --cytomine_id_software $(ID_SOFTWARE_TRAIN) --working_path $(WORKING_PATH) --cytomine_id_tags_for_images $(ID_TRAIN_TAG) --cytomine_id_terms $(ID_TERMS)

publish_descriptor_train:
	python model_builder/publish_descriptor.py --cytomine_host $(HOST) --cytomine_public_key $(PUBKEY) --cytomine_private_key $(PRIVKEY)

predict_as_job:
	python predictor/run_as_job.py --cytomine_host $(HOST) --cytomine_public_key $(PUBKEY) --cytomine_private_key $(PRIVKEY) --cytomine_id_project $(ID_PROJECT) --cytomine_id_software $(ID_SOFTWARE_PREDICT) --working_path $(WORKING_PATH) --cytomine_id_tags_for_images $(ID_TEST_TAG) --cytomine_id_terms $(ID_TERMS)

publish_descriptor_predict:
	python predictor/publish_descriptor.py --cytomine_host $(HOST) --cytomine_public_key $(PUBKEY) --cytomine_private_key $(PRIVKEY)
