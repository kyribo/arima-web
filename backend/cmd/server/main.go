package main

import (
	"backend/internal/database"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	// Initialize Database
	database.Connect()

	r := gin.Default()
	r.SetTrustedProxies(nil)

	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})

	r.Run() // listen and serve on 0.0.0.0:8080
}
