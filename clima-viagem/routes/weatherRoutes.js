const express = require('express');
const router = express.Router();
const { compareCities, getTravelSuggestions } = require('../controllers/weather');

// Compara clima entre duas cidades
router.get('/compare', compareCities);

// Sugere melhor época para viajar
router.get('/suggest', getTravelSuggestions);

module.exports = router;