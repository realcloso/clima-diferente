const express = require('express');
const router = express.Router();
const { compareCities, getTravelSuggestions } = require('../controllers/weatherController');

// Compara clima entre duas cidades
router.get('/compare', compareCities);

// Sugere melhor época para viajar
router.get('/suggest', getTravelSuggestions);

module.exports = router;