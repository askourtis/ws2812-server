SHELL   = /bin/bash

.PHONY: all
all: service

.PHONY: service
service:
	@chmod +x ./*.sh && ./service.sh
