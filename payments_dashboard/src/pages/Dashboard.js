import React, { useEffect, useState } from "react";
import { fetchCardHolders, fetchTransactions } from "../api/api";

const Dashboard = () => {
    const [cardholders, setCardholders] = useState([]);
    const [transactions, setTransactions] = useState([]);

    useEffect(() => {
        const loadData = async() => {
            setCardholders(await fetchCardHolders());
            setTransactions(await fetchTransactions());
        };
        loadData();
    }, []);

    return (
        <div>
            <h1>Visa Payment Dashboard</h1>
            <h2>Total Cardholders: {cardholders.length}</h2>
            <h2>Total Transactions: {transactions.length}</h2>
        </div>
    );
};

export default Dashboard;