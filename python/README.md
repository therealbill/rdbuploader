# RDB Uploader

RDB Uploader is a system for uploading Redis Dump files to a remote server.

## Python Version

The python version has a few requirements-XXX.txt files. 

The command to import all required modules, useful if installing on a system
where various destination drivers may be used, is:

```shell
pip install -r requirements-all.txt
``` 


If you only need a specific driver, for example using Rackspace's CloudFiles:

```shell
pip install -r requirements-rackspace.txt
``` 

will pull in requirements for connecting to CloudFiles.


# Configuration

Regardless of language implementation, the same config file is used. See the
parent directory for an example.

# Running rdbuploader

Once configured, simply running "rdbuploader.py" (assuming it is in your PATH)
will upload the Redis dump file, logging to standard out.
