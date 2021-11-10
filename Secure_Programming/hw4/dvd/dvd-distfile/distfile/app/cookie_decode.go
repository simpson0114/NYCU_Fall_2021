package main

import (
    "github.com/gorilla/securecookie"      
	"fmt"
    //you will need this later
    "net/http"
)

func main() {
	var s *securecookie.SecureCookie
    s = securecookie.New([]byte("d2908c1de1cd896d90f09df7df67e1d4"), nil)
	value := make(map[string]string)
	if err := s.Decode("cookie-name", "MTYzNjUzNjY1MHxEdi1CQkFFQ180SUFBUkFCRUFBQUpfLUNBQUVHYzNSeWFXNW5EQW9BQ0hWelpYSnVZVzFsQm5OMGNtbHVad3dIQUFWbmRXVnpkQT09fGO7vEMuZJTWAZn4F6D7HaTNMxCO8wIIRggtOzKIy6Qz", &value); err == nil {
		fmt.Println("The value of foo is %q", value)
	}
}
