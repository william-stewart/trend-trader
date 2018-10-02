package main

import (
	"fmt"
	"os"

	_ "github.com/go-sql-driver/mysql"
	"github.com/william-stewart/av"
)

func main() {
	// Call the AV API
	avClient := av.NewClient(avApiKey)
	queryInterval(avClient, "SBUX", 1)

	//mysqlclient.QueryDb("INSERT INTO ttimeseries VALUES ( 'TESTER2','2018-10-11 13:23:44', 34.22, 38.21, 33.56, 37.98, 1200.0 )")
}

func queryInterval(client *av.Client, symbol string, timeInterval av.TimeInterval) {
	res, err := client.StockTimeSeriesIntraday(timeInterval, symbol)
	if err != nil {
		ErrorF("error loading intraday series %s: %v", timeInterval, err)
		return
	}

	//quick print for a quick win
	sum := 0
	for i := 0; i < len(res); i++ {
		sum += i
		fmt.Println(res[i])
	}
}

func ErrorF(format string, args ...interface{}) {
	fmt.Fprintf(os.Stderr, fmt.Sprintf("%s\n", format), args...)
}
