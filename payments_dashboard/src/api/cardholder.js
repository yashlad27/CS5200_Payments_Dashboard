import axios from 'axios';

const API_URL = 'http://127.0.0.1:5000/api/cardholders';

export const getCardholders = async () => {
    try {
        const response = await axios.get(API_URL);
        return response.data;
    } catch (error) {
        console.error("Error fetching cardholders", error);
        return [];
    }
};