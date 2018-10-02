package mysqlclient

import (
	"database/sql"

	_ "github.com/go-sql-driver/mysql"
)

var dbConnectionStr = dbUser + ":" + dbPassword + "@tcp(" + dbServer + ")/" + dbName

func QueryDb(queryString string) {
	db, err := sql.Open(dbType, dbConnectionStr)
	if err != nil {
		panic(err.Error()) // Need to handle error
	}
	defer db.Close()

	err = db.Ping()
	if err != nil {
		panic(err.Error()) // Need to handle error
	}

	insert, err := db.Query(queryString)
	if err != nil {
		panic(err.Error()) // Need to handle error
	}

	defer insert.Close()
}
