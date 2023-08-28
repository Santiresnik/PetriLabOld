// Import packages
const express = require("express");
//const home = require("./routes/home");

// Middlewares
const app = express();
app.use(express.json());

// Routes
app.get("/home", (req, res) => {
    res.status(200).send("Hello World!");
});

// connection
module.exports = app;