package main

import (
	"flag"
	"log"
	"os"

	"code.google.com/p/gcfg"
	drivers "github.com/TheRealBill/rdbuploader/go/drivers"
)

type Config struct {
	// Define the config file structure
	Main struct {
		Driver      string
		Maxfilesize int64
	}

	DestinationFormat struct {
		Python string
		Go     string
	}

	Redis struct {
		Dumpfile string
	}

	Rackspacecf struct {
		Username      string
		Apikey        string
		Containername string
	}

	Amazons3 struct {
		Username      string
		Apikey        string
		Containername string
	}
}

func getDriver(config Config) drivers.Driver {
	switch config.Main.Driver {
	case "rackspacecf":
		mydriver := new(drivers.CloudFilesDriver)
		mydriver.Name = config.Main.Driver
		mydriver.Username = config.Rackspacecf.Username
		mydriver.Apikey = config.Rackspacecf.Apikey
		mydriver.Authurl = "https://auth.api.rackspacecloud.com/v1.0"
		mydriver.Origin = config.Redis.Dumpfile
		mydriver.Layout = config.DestinationFormat.Go
		mydriver.Containername = config.Rackspacecf.Containername
		return mydriver

	case "amazons3":
		mydriver := new(drivers.AmazonS3Driver)
		mydriver.Name = config.Main.Driver
		mydriver.Username = config.Amazons3.Username
		mydriver.Apikey = config.Amazons3.Apikey
		mydriver.Origin = config.Redis.Dumpfile
		mydriver.Layout = config.DestinationFormat.Go
		mydriver.Containername = config.Amazons3.Containername
		return mydriver
	}

	return new(drivers.MissingDriver)
}

func main() {
	// The main stuff happens here
	var conf Config
	var configfilename string
	flag.StringVar(&configfilename, "conf", "/etc/redis/rdbuploader.cfg", "Config file to use")
	flag.Parse()

	err := gcfg.ReadFileInto(&conf, configfilename)
	if err != nil {
		log.Fatal(err)
	}
	td := getDriver(conf)
	td.Connect()
	td.Authenticate()

	origin, _ := os.Open(conf.Redis.Dumpfile)
	fi, _ := origin.Stat()
	if fi.Size() >= conf.Main.Maxfilesize {
		log.Fatal(conf.Redis.Dumpfile, " is too large, aborting")
	}
	filesizemb := fi.Size() / 1024.0
	log.Printf("Origin file is %.2f Kb ", float64(filesizemb))

	td.Upload()
}
