const express = require('express');
const router = express.Router();
const { compareCities, getTravelSuggestions } = require('../controllers/weatherController');

router.get('/compare', compareCities);

router.get('/suggest', getTravelSuggestions);

module.exports = router;