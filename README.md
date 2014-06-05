# What it is

A utility to upload a Redis dump file to a remote (non-Redis) server. It will
probably evolve to do more, but this is a good start.

# Why It Exists

I initially began writing this for a Tutorial on how to copy Redis dumps to
remote locations when I realized it would be more useful to make a utility and
write the tutorial on the utility. 

Why would you want to do that? First, offsite backup is a good idea. If that
isn't enough, consider some other scenarios. With this set up in, or used in
another script, you can have point in time recover for Redis data. The default
remote storage name is a timestamp based one.

It can also be used in a strategy where the master has persistence disabled, to
be handled by a "persistence slave".


# How to Use it

Go makes this part easy. Assuming you have your GOPATH environment variable set
up you simply run:

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


