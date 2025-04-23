const axios = require('axios');
const NodeCache = require('node-cache');
const cache = new NodeCache({ stdTTL: 600 }); // Cache de 10 minutos

const fetchWeatherData = async (city, days) => {
    const cacheKey = `${city}-${days}`;
    const cachedData = cache.get(cacheKey);

    if (cachedData) {
        console.log("Retornando dados do cache.");
        return cachedData;
    }

    try {
        // Chamando SUA API de clima local (ex: rodando em http://localhost:4000)
        const response = await axios.get(
            `http://localhost:4000/api/weather?city=${city}&days=${days}`
        );

        const weatherData = {
            city,
            forecast: response.data.forecast.map(day => ({
                date: day.date,
                temp: day.temp,
                condition: day.condition,
            })),
        };

        cache.set(cacheKey, weatherData);
        return weatherData;
    } catch (error) {
        throw new Error("Falha ao buscar dados da sua API de clima.");
    }
};

module.exports = { fetchWeatherData };