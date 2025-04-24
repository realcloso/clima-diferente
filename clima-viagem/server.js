const express = require('express');
const cors = require('cors');
const axios = require('axios');
const rotas = require('./routes/weatherRoutes.js'); 

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

// Rotas
app.use('/api', rotas);

app.listen(PORT, () => {
    console.log(`Servidor rodando em http://localhost:${PORT}`);
});