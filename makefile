all: listen lvcgcnd.service
lvcgcnd: lvcgcnd.service
.PHONY: all listen install uninstall clean

service_dir=/etc/systemd/system
conf_dir=/etc/lvcgcn
awk_script='BEGIN {FS="="; OFS="="}{if ($$1=="ExecStart") {$$2=exec_path} if (substr($$1,1,1) != "\#") {print $$0}}'

listen: setup.py torosgcn/*.py
	pip install .

lvcgcnd.service: lvcgcnd.service.template torosgcn/listen.py
# awk is needed to replace the absolute path of the scheduler script in the .service file
	awk -v exec_path=$(shell which lvcgcn) $(awk_script) $< > $@

$(conf_dir):
	mkdir -p $@

$(service_dir)/lvcgcnd.service:
	cp lvcgcnd.service $(service_dir)

$(conf_dir)/lvcgcn-conf.yaml:
	cp lvcgcn-conf.yaml $(conf_dir)

install: $(service_dir) $(conf_dir) lvcgcnd.service lvcgcn-conf.yaml $(service_dir)/lvcgcnd.service $(conf_dir)/lvcgcn-conf.yaml
	systemctl enable lvcgcnd
	@echo "Installation complete."

uninstall:
	-systemctl stop lvcgcnd
	-pip uninstall -y torosgcn
	-rm $(service_dir)/lvcgcnd.service
	rm -r $(conf_dir)

clean:
	-rm lvcgcnd.service
