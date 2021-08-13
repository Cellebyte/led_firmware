py_files_raw := $(wildcard *.py) $(wildcard **/*.py)
py_files := $(filter-out "apiserver/api.py",${py_files_raw})
api_files := apiserver/api.py
mpy_files := $(patsubst %.py, %.mpy, $(api_files))
directories := 
device := /dev/ttyUSB0
baud_rate := 115200
architecture := xtensa
.PHONY: all clean

all: build

build: $(mpy_files)
%.mpy: %.py
	@echo "Compile $< to $@"
	mpy-cross -march=${architecture} -v $<

upload: upload_py
upload_py: 
	rsync -av --include="*/" --include="*.py" --exclude="*" . /run/media/$$USER/CIRCUITPY

clean:
	@echo "Cleaning up..."
	rm -rvf $(mpy_files)


