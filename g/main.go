package main

import "os"
import "fmt"
import "gopkg.in/mgo.v2/bson"
import "shiroyuki/photos/dbal"
import "shiroyuki/photos/models"

// func main() {
//     url        := "mongodb://127.0.0.1:27017"
//     database   := "photos"
//     collection := "photographs"
//     // query      := nil
//
//     session, err := mgo.Dial(url)
//
//     if err != nil {
//         panic(err)
//     }
//
//     var result models.Photograph
//
//     query := bson.M{"aperture": 2.8, "model": "NIKON D810"}
//
//     err = session.DB(database).C(collection).Find(query).One(&result)
//
//     if err != nil {
//         fmt.Println(err)
//         os.Exit(1)
//     }
//
//     fmt.Println(result.Location)
//     fmt.Println(result.Model)
//     fmt.Println(result.Aperture)
//     fmt.Println(result.ExposureTime)
// }

func main() {
    var err        error
    var repository dbal.Repository
    var result     models.Photograph

    url        := "mongodb://127.0.0.1:27017"
    database   := "photos"
    collection := "photographs"
    // query      := nil

    repository = dbal.Repository{
        Url:            url,
        DatabaseName:   database,
        CollectionName: collection,
    }

    criteria := bson.M{"aperture": 2.8, "model": "NIKON D810"}

    repository.Activate()
    defer repository.Deactivate()

    query, err := repository.Query(criteria)

    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }

    err = query.One(&result)

    if err != nil {
        fmt.Println(err)
        os.Exit(1)
    }

    fmt.Println(result.Id)
    fmt.Println(result.Location)
    fmt.Println(result.Model)
    fmt.Println(result.Aperture)
    fmt.Println(result.ExposureTime)
}
