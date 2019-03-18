DOCKER_IMAGE := test/image:stable

REPORT_DIR ?= $(CURDIR)/../testout

.PHONY: build
build:
	docker build --rm --tag "$(DOCKER_IMAGE)" . --network host

REPORT_PATH ?= $(REPORT_DIR)

.PHONY: run
run:
	docker run --rm=true \
		-v $(CURDIR):/tests \
		-v $(REPORT_PATH):/testout \
		-w /tests \
		-e PYTHONPATH=/tests/api \
		--network host -it \
		$(DOCKER_IMAGE) \
		bash -c "make test"


.PHONY: test
test:
	python3 -m pytest autotests/






