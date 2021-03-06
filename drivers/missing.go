package drivers

import (
	"github.com/ncw/swift"
	//"io/ioutil"
	"log"
	//"time"
)

type MissingDriver struct {
	Name       string
	Username   string
	Apikey     string
	Authurl    string
	Connection swift.Connection
}

func (d *MissingDriver) Connect() bool {
	log.Println("Connect called on:", d.Name)
	log.Println("Username is:", d.Username)
	return false
}
func (d *MissingDriver) Authenticate() bool {
	log.Println("Authenticate called on:", d.Name)
	return false
}
func (d *MissingDriver) Upload() bool {
	log.Println("Upload called on:", d.Name)
	return false
}
