all: all-protos sync-all

# hostname of the target raspberry pi (all overloaded meanings)
RPI	?= undefined

define MKDIR_RULE
sync-$(RPI)/$(1):
	ssh pi@$(RPI) mkdir -p Project/pyaicam/$(1)
	mkdir -p sync-$(RPI)/$(1)
endef

define SYNC_RULE
sync-$(RPI)/$(1): $(1)
	scp $(1) pi@$(RPI):Project/pyaicam/$(1)
	@cp -f $(1) sync-$(RPI)/$(1)
endef

BACKEND_SRCS = \
	backend/requirements.txt				\
	backend/Dockerfile					\
	backend/docker-compose.yml				\
	backend/pyaicam/__init__.py				\
	backend/pyaicam/presentation/__init__.py		\
	backend/pyaicam/presentation/cameraproxy.py		\
	backend/pyaicam/presentation/sensorcaps.py		\
	backend/pyaicam/presentation/camera2_pb2.py		\
	backend/pyaicam/presentation/camera2_pb2_grpc.py	\
	backend/pyaicam/application/__init__.py			\
	backend/pyaicam/application/logging.py			\
	backend/pyaicam/application/network.py			\
	backend/pyaicam/control/__init__.py			\
	backend/pyaicam/control/cameracontroller.py		\
	backend/pyaicam/data/__init__.py			\
	backend/pyaicam/data/cameradriver.py			\
	backend/pyaicam/main.py					\
	backend/bin/cam-agent					\
	backend/bin/cam-capture					\
	backend/bin/serve-api					\
	backend/libexec/cam-agent.py				\
	backend/libexec/cam-capture.py

# Unique subdirs extracted from SRCS
BACKEND_DIRS = $(sort $(foreach path,				\
			$(BACKEND_SRCS),			\
			$(dir $(path))))

# Generate sync rule for each subdir
$(foreach subdir,						\
	$(BACKEND_DIRS),					\
	$(eval $(call MKDIR_RULE,$(subdir))))

# Generate sync rule for each src
$(foreach src,							\
	$(BACKEND_SRCS),					\
	$(eval $(call SYNC_RULE,$(src))))

# Generate lists for local dependencies
SYNC_DIRS	= $(foreach dir,$(BACKEND_DIRS),sync-$(RPI)/$(dir))
SYNC_SRCS	= $(foreach src,$(BACKEND_SRCS),sync-$(RPI)/$(src))

# Would prefer order-only-prerequisites
sync-dirs: $(SYNC_DIRS)

# Add lint checks?
sync-srcs: $(SYNC_SRCS)

sync-all: defined-rpi sync-dirs sync-srcs

.PHONY: defined-pri sync-dirs sync-srcs sync-all

defined-rpi:
	if [ "${RPI}" = "undefined" ]; then	\
		echo "RPI must be defined";	\
		exit 1;				\
	fi


# Debugs
test-backend-dirs:
	@echo $(BACKEND_DIRS)

test-sync-srcs:
	@echo $(SYNC_SRCS)



all-protos: \
	backend/pyaicam/presentation/helloworld_pb2.pyi \
	backend/pyaicam/presentation/camera2_pb2.pyi

PROTOC  = python -m grpc_tools.protoc
PROTOC_FLAGS = -Ibackend/protos \
		--python_out=backend/pyaicam/presentation \
		--pyi_out=backend/pyaicam/presentation \
		--grpc_python_out=backend/pyaicam/presentation

# https://github.com/grpc/grpc/issues/29459
#import helloworld_pb2 as helloworld__pb2
#from . import helloworld_pb2 as helloworld__pb2

backend/pyaicam/presentation/helloworld_pb2.pyi:	\
		backend/protos/helloworld.proto
	${PROTOC} ${PROTOC_FLAGS} backend/protos/helloworld.proto
	./backend/tools/grpc-import-fix.py \
		backend/pyaicam/presentation/helloworld_pb2_grpc.py

backend/pyaicam/presentation/camera2_pb2.pyi:		\
		backend/protos/camera2.proto
	${PROTOC} ${PROTOC_FLAGS} backend/protos/camera2.proto
	./backend/tools/grpc-import-fix.py \
		backend/pyaicam/presentation/camera2_pb2_grpc.py

#--#
