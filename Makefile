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

upload: upload_mpy upload_py
upload_py: 
	for file in $(py_files); do \
		echo $$file; \
		pyboard.py -b ${baud_rate} --device ${device} -f mkdir $(dir "$file"); \
		pyboard.py -b ${baud_rate} --device ${device} -f cp "$$file" ":$$file"; \
	done

upload_mpy: $(mpy_files)
	pyboard.py -b ${baud_rate} --device ${device} -f mkdir $(dir $<) | true;
	pyboard.py -b ${baud_rate} --device ${device} -f cp "$<" ":$<";

clean:
	@echo "Cleaning up..."
	rm -rvf $(mpy_files)


