import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:5000/api";
console.log("API BASE URL:", API_BASE_URL);

// Fetch all cardholder;
export const fetchCardHolders = async() => {
    try {
        const response = await axios.get(`${API_BASE_URL}/cardholders`);
        return response.data;
    } catch (error) {
        console.error('Error fetching cardholders: ', error);
        return [];
    }
}

// fetch all transactions:
export const fetchTransactions = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/transactions`);
        return response.data;
    } catch (error) {
        console.error('Error fetching transactions: ', error);
        return [];
    }
}

export const fetchTopMerchants = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/top-merchants`);
        return response.data;
    } catch (error) {
        console.error('Error fetching top merchants:', error);
        return [];
    }
};