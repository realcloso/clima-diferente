const { fetchWeatherData } = require('../services/weatherService');

const compareCities = async (req, res) => {
    const { city1, city2, days = 5 } = req.query;

    try {
        const [weatherCity1, weatherCity2] = await Promise.all([
            fetchWeatherData(city1, days),
            fetchWeatherData(city2, days),
        ]);

        res.json({
            city1: weatherCity1,
            city2: weatherCity2,
            comparison: `Comparação entre ${city1} e ${city2} nos próximos ${days} dias.`,
        });
    } catch (error) {
        res.status(500).json({ error: "Erro ao buscar dados." });
    }
};

const getTravelSuggestions = async (req, res) => {
    const { city, month } = req.query;
    res.json({ suggestion: `Melhor época para ${city}: ${month || 'Abril a Outubro'}` });
};

module.exports = { compareCities, getTravelSuggestions };