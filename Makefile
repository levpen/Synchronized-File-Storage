.PHONY: server
server:
	python3 server/server.py

.PHONY: package
package:
	chmod +x client/usr/bin/sfsclient && \
	dpkg-deb --build client && \
	dpkg -i client.deb

.PHONY: client
client:
	python3 client/var/sfsclient/main.py $(ARGS)
