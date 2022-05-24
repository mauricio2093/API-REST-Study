const express = require('express');
const app = express();
const bodyParser = require('body-parser');

// Middlewares para recibir JSON a traves del API en express
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Parametros permitidos para "resource_type"
const allowedResources = [
    'books',
    'authors',
    'genres'
];

// Array de objetos que contienen los libros
const books = [
    { title: 'Lo que el viento se llevo', id_author: 2, id_genre: 2 },
    { title: 'La Iliada', id_author: 1, id_genre: 1 },
    { title: 'La odisea', id_author: 1, id_genre: 1 }
];

app.get('/', (req, res) => {
  // Obtiene "resource_type" de los parámetros del URL
    const resourceType = req.query.resource_type;

  // Verifica si existe este parámetro en nuestro arreglo de permitidos
    if(allowedResources.indexOf(resourceType) === -1) {
        // Devuelve error si no se encuentra
        return res.json({ status: 'Failed', error: 'missing or invalid param: resource_type' });    
    }
  // Si sale todo bien, devuelve un ok junto a los libros
    res.json({ status: 'ok', books });
});

app.post('/books', (req, res) => {
  // Verifica si se envian datos por formulario
    if(req.body) {
    // Verifica si falta "title", "id_author" o "id_genre"
        if(!req.body.title || !req.body.id_author || !req.body.id_genre) {
        // Devuelve error si falta alguno
            return res.json({ status: 'failed', error: 'missing or invalid: data' });
        }
    // Inserta un nuevo objeto al array, y devuelve el id insertado 
    // (característica javascript)
        const insertCount = books.push({
            title: req.body.title,
            id_author: req.body.id_author,
            id_genre: req.body.id_genre
        })

        // Devuelve ok y el id insertado si todo salió bien
        res.json({ status: 'ok', insert_id: insertCount - 1, books })
    } else {
        // Devuelve un error si no se envian datos por formulario
        return res.json({ status: 'Failed', error: 'error no data' });
    }
})
app.put('/books/:id', (req, res) => {
    const paramId = req.params.id
    // Verifica si se ha puesto un id y que este exista
    if(paramId && books[paramId]) {
        const book = books[paramId];
  
      // Modificar solo los datos que se hayan enviado
        book.title = req.body.title || book.title;
        book.id_author = req.body.id_author || book.id_author;
        book.id_genre = req.body.id_genre || book.id_genre;
      // Esta sintaxis dice: 
      // "Es igual al dato enviado (req.body.title), 
      // Y si está vacío (||) dejar el valor por defecto (book.title)"
  
      // Guardar el libro modificado
        books[paramId] = book;

      // Envia un ok, el libro modificado y la colección de libros
        res.send({ status: 'ok', book, books })
    } else {
      // En caso de no encontrar, devuelve error
        res.json({ status: 'Failed', error: 'missing or invalid param: id' });
    }
})
// Iniciador del servidor, en el puerto 5000
app.listen(5000, () => {
    console.log('server on port 5000');
});
