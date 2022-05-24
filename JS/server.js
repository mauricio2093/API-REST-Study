const express = require("express");
const bodyParser = require("body-parser");
const router = express.Router();

var app = express();
app.use(bodyParser.json());

app.use(router);

const books = [
    {
        titulo : 'Lo que el viento se llevo',
        id_autor : '2',
        id_genero : '2'
    },
    {
        titulo : 'La Iliada',
        id_autor : '1',
        id_genero : '1'
    },
    {
        titulo : 'La Odisea',
        id_autor : '1',
        id_genero : '1'
    }]


router.get("/", function(req, res) {
    console.log(req.query);
    console.log(req.body);

    res.json(books)
});

app.listen(3000);

console.log("La aplicacion esta escuchando en http://localhost:3000");
