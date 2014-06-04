# What it is

A set of scripts demonstrating how to upload a Redis dump file to a remote
(non-Redis) server

# Why It Exists

I initially began writing this for a Tutorial on how to copy Redis dumps to
remote locations when I realized it would be more useful to make a utility and
write the tutorial on the utility. The initial idea was to write it for Python
and Go, and since I am learning Go I figured I'd continue it in both languages.
They both do the same things, and use the same config file.

# How to Use it

Since I've not yet written the setup.py, I'll go through using the Go version.

## Installation

Go makes this part easy. Assuming you have your GOPATH environment variable set up you simply run:

`
go get github.com/TheRealBill/rdbuploader/go/rdbuploader
`

Now, if $GOPATH/bin is in your path you can run `rdbuploader` and it will
complain about the config file being absent.

## Configuration

To get the default file in place:

`
mkdir /etc/redis 
cp $GOPATH/src/github.com/TheRealBill/rdbuploader/config/rdbuploader.cfg /etc/redis/
`

Now you'll need to modify it to have your credentials and remote-specific
settings. For details on the configuration of rdbuploader see [the config doc](docs/configuration.md).


