SRCROOT   = $(CURDIR)

default: tests

include makefile.vars

tests: check_binaries
	$(bin_env) PYTHONPATH=$(CURDIR)/src $(bin_nose) $(CURDIR)/src/tests $(noseflags)

clean:
	$(bin_find) -type f -name \*.pyc -o -name \*.pyo -exec rm -f \{\} \;
