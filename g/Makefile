build: install_deps compile
	@echo "Done"

install_deps:
	go get gopkg.in/mgo.v2

compile:
	GOPATH=${GOPATH}:`pwd` go build main.go

clean:
	rm main
