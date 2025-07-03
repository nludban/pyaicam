all: sync-all

# hostname of the target raspberry pi (all overloaded meanings)
RPI	?= undefined

define SYNC_RULE
sync-$(RPI)/$(1): $(1)
	ssh pi@$(RPI) mkdir -p Project/pyaicam/$(dir $(1))
	scp $(1) pi@$(RPI):Project/pyaicam/$(1)
	mkdir -p sync-$(RPI).$(dir $(1))
	@cp -f $(1) sync-$(RPI)
endef

BACKEND_SRCS = \
	backend/requirements.txt		\
	backend/Dockerfile			\
	backend/docker-compose.yml		\
	backend/pyaicam-api/main.py

SYNC_SRCS = $(foreach src,$(BACKEND_SRCS),sync-$(RPI)/$(src))

$(foreach src,$(BACKEND_SRCS),$(eval $(call SYNC_RULE,$(src))))

test-sync-srcs:
	echo $(SYNC_SRCS)

sync-all: $(SYNC_SRCS)

#--#
