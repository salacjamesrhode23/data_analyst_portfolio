KEY=gcp_key/data-analyst-sa.json
REGION=ASIA
DURATION=7d
BUCKET=gs://paysim_dataset/enriched_dataset
OUT_DIR=./enriched_dataset

download-transactions:
	@mkdir -p $(OUT_DIR)
	@URL=$$(gsutil signurl -d $(DURATION) -r $(REGION) $(KEY) $(BUCKET)/transactions.csv | tail -n 1 | sed 's/.*https/https/'); \
	curl -L "$$URL" -o $(OUT_DIR)/transactions.csv

download-customers:
	@mkdir -p $(OUT_DIR)
	@URL=$$(gsutil signurl -d $(DURATION) -r $(REGION) $(KEY) $(BUCKET)/customers.csv | tail -n 1 | sed 's/.*https/https/'); \
	curl -L "$$URL" -o $(OUT_DIR)/customers.csv

download-merchants:
	@mkdir -p $(OUT_DIR)
	@URL=$$(gsutil signurl -d $(DURATION) -r $(REGION) $(KEY) $(BUCKET)/merchants.csv | tail -n 1 | sed 's/.*https/https/'); \
	curl -L "$$URL" -o $(OUT_DIR)/merchants.csv

download-all: download-transactions download-customers download-merchants