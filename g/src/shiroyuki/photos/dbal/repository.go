package dbal

import "gopkg.in/mgo.v2"

type Repository struct {
    Url            string
    DatabaseName   string
    CollectionName string
    sessionApi     *mgo.Session
    databaseApi    *mgo.Database
    collectionApi  *mgo.Collection
}

type StartupError struct {
    msg string
}

func (e *StartupError) Error() string {
    return e.msg
}

type InactiveRepositoryError struct {
    msg string
}

func (e *InactiveRepositoryError) Error() string {
    return e.msg
}

func (self *Repository) Activate() error {
    var err error

    if self.sessionApi == nil {
        self.sessionApi, err = mgo.Dial(self.Url)
    }

    if err != nil {
        return &StartupError{msg: err.Error()}
    }

    if self.databaseApi == nil {
        self.databaseApi = self.sessionApi.DB(self.DatabaseName)
    }

    if self.collectionApi == nil {
        self.collectionApi = self.databaseApi.C(self.CollectionName)
    }

    return nil
}

func (self *Repository) Deactivate() {
    if !self.IsActive() {
        return
    }

    // Dereference to API objects
    self.collectionApi = nil
    self.databaseApi   = nil

    // Close the session
    self.sessionApi.Close()
}

func (self *Repository) IsActive() bool {
    return self.collectionApi != nil
}

func (self *Repository) PreFlightCheck() error {
    if !self.IsActive() {
        return &InactiveRepositoryError{"InactiveRepositoryError: Failed at the pre-flight check. The repository must be active before this operation."}
    }

    return nil
}

func (self *Repository) Query(criteria interface{}) (*mgo.Query, error) {
    if err := self.PreFlightCheck(); err != nil {
        return nil, err
    }

    return self.collectionApi.Find(criteria), nil
}
