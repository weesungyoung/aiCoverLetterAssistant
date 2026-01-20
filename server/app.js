const express = require('express');
const path = require('path');
const morgan = require('morgan');
const cors = require('cors');

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, '../app/dist')));

app.listen(PORT, () => {
    console.log("Start Server");
});