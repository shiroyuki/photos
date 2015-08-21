package main

import "os"
import "fmt"
import "time"
import "gopkg.in/mgo.v2"
import "gopkg.in/mgo.v2/bson"

type Photograph struct {
    Id                     bson.ObjectId `bson:"_id"`
    ExposureTime           string        `bson:"exposure_time"`// : "10/6400",
	Date_time              time.Time //: "2014:09:11 21:28:08",
	Original_focal_length  []uint32  //: [10, 6400],
	Orientation            uint8     //: 1,
	Original_aperture      []uint8   //: [240, 10],
	Manufacture            string    // : "NIKON CORPORATION",
	Focal_length_35mm      uint8     // : 24,
	Flash                  uint8     // : 16,
	Metering_mode          uint8     // : 5,
	Hashsum                string    // : "d8ab9b8984f9f0a7bcc3bf1b3e3d5a5da20392c7",
	Height                 uint32    // : 4912,
	Width                  uint32    // : 7360,
	White_balance          uint8     // : 0,
	Iso                    uint8     // : 64,
	Location               string    // : "/Volumes/Sonata/Photography/Lightroom/Class A/2014.09 - Japan/09.12/DSC_3101.JPG",
	Focal_length           uint8     // : 24,
	Aperture               float32   // : 2.8,
	Model                  string    // : "NIKON D810",
	Original_exposure_time []uint32  // : [28, 10]
}

func main() {
    url        := "mongodb://127.0.0.1:27017"
    database   := "photos"
    collection := "photographs"
    // query      := nil

    session, err := mgo.Dial(url)

    if err != nil {
        panic(err)
    }

    var result Photograph

    query := bson.M{"aperture": 2.8, "model": "NIKON D810"}

    err = session.DB(database).C(collection).Find(query).One(&result)

    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }

    fmt.Println(result.Location)
    fmt.Println(result.Model)
    fmt.Println(result.Aperture)
    fmt.Println(result.ExposureTime)
}
