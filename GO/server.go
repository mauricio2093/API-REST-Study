package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
)

var AllowedResources = map[string]bool{
	"books":   true,
	"authors": true,
	"genres":  true,
}

type Book struct {
	Titulo    string `json:"titulo"`
	Id_Autor  int    `json:"id_autor"`
	Id_gereno int    `json:"id_gereno"`
}

var Books = []Book{
	{
		Titulo:    "Lo que el viento se llevo",
		Id_Autor:  2,
		Id_gereno: 2,
	},
	{
		Titulo:    "El señor de los anillos",
		Id_Autor:  1,
		Id_gereno: 1,
	},
	{
		Titulo:    "La Odisea",
		Id_Autor:  1,
		Id_gereno: 3,
	},
}

func main() {
	http.Handle("/", http.HandlerFunc(ExampleHandler))
	http.HandleFunc("/books", books)
	http.HandleFunc("/book/", book)

	http.ListenAndServe(":8080", nil)
}

func book(w http.ResponseWriter, r *http.Request) {
	idstr := r.URL.Path[len("/book/"):]
	id, err := strconv.Atoi(idstr)
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		fmt.Fprint(w, "<h1>Bad Request</h1>")
		return
	}

	switch r.Method {
	case http.MethodGet:
		getBook(w, r, id)
	case http.MethodDelete:
		w.Write([]byte("DELETE"))
	}
}

func getBook(w http.ResponseWriter, r *http.Request, id int) {
	// Get a single book
	maxBooks := len(Books)

	if id >= maxBooks {
		w.WriteHeader(http.StatusNotFound)
		fmt.Fprint(w, "<h1>Not Found</h1>")
		return
	}

	book := Books[id]
	response, err := json.Marshal(book)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, "<h1>Internal Server Error</h1>")
		return
	}

	fmt.Fprint(w, string(response))
}

func books(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case "GET":
		getBooks(w, r)
	case "POST":
		postBooks(w, r)
	}
}

func getBooks(w http.ResponseWriter, r *http.Request) {
	respose, err := json.Marshal(Books)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		fmt.Fprint(w, "<h1>Internal Server Error</h1>")
		return
	}

	fmt.Fprint(w, string(respose))
}

func postBooks(w http.ResponseWriter, r *http.Request) {
	w.Write([]byte("POST"))
}
