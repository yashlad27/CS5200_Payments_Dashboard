import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend,
} from "recharts";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://127.0.0.1:5000/api";

const Dashboard = () => {
  const [cardholders, setCardholders] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [topMerchants, setTopMerchants] = useState([]);
  const [failedTransactions, setFailedTransactions] = useState(0);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      // Fetch Cardholders
      const cardholderRes = await axios.get(`${API_BASE_URL}/cardholders`);
      setCardholders(cardholderRes.data);

      // Fetch Transactions
      const transactionRes = await axios.get(`${API_BASE_URL}/transactions`);
      setTransactions(transactionRes.data);

      // Fetch Top Merchants
      const merchantRes = await axios.get(`${API_BASE_URL}/top-merchants`);
      const merchantsData = merchantRes.data.map(merchant => ({
        ...merchant,
        total_revenue: parseFloat(merchant.total_revenue || 0),
      }));
      setTopMerchants(merchantsData);

      // Fetch Failed Transactions Count
      const failedRes = await axios.get(`${API_BASE_URL}/failed-transactions`);
      setFailedTransactions(failedRes.data.length);
      
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  // Prepare data for transactions trend chart
  const transactionData = transactions.map((tx, index) => ({
    name: `Tx ${index + 1}`,
    amount: parseFloat(tx.amount || 0),
  }));

  return (
    <div className="bg-gray-100 min-h-screen flex flex-col items-center p-10">
      <h1 className="text-4xl font-bold text-blue-600 mb-5">Visa Payment Dashboard 💳</h1>

      {/* Summary Cards */}
      <div className="grid grid-cols-3 gap-6">
        <div className="bg-white shadow-lg rounded-lg p-6 w-60 text-center">
          <h2 className="text-xl font-semibold text-gray-700">Total Cardholders</h2>
          <p className="text-3xl text-blue-600 font-bold">{cardholders.length}</p>
        </div>
        <div className="bg-white shadow-lg rounded-lg p-6 w-60 text-center">
          <h2 className="text-xl font-semibold text-gray-700">Total Transactions</h2>
          <p className="text-3xl text-green-600 font-bold">{transactions.length}</p>
        </div>
        <div className="bg-white shadow-lg rounded-lg p-6 w-60 text-center">
          <h2 className="text-xl font-semibold text-gray-700">Failed Transactions</h2>
          <p className="text-3xl text-red-600 font-bold">{failedTransactions}</p>
        </div>
      </div>

      {/* Top Merchants */}
      <div className="mt-8 w-full max-w-3xl bg-white shadow-lg rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Top Merchants</h2>
        {topMerchants.length > 0 ? (
          <ul className="divide-y divide-gray-200">
            {topMerchants.map((merchant) => (
              <li key={merchant.merchant_name} className="py-2 flex justify-between">
                <span className="text-gray-700 font-medium">{merchant.merchant_name}</span>
                <span className="text-green-600 font-bold">${merchant.total_revenue.toFixed(2)}</span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-500 text-center">No merchant data available.</p>
        )}
      </div>

      {/* Transactions Trend */}
      <div className="mt-8 w-full max-w-3xl bg-white shadow-lg rounded-lg p-6">
        <h2 className="text-xl font-semibold text-gray-700 mb-4">Transactions Trend</h2>
        {transactionData.length > 0 ? (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={transactionData}>
              <CartesianGrid stroke="#e0dfdf" strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-20} textAnchor="end" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="amount" stroke="#007aff" strokeWidth={2} dot={{ r: 4 }} />
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p className="text-gray-500 text-center">No transaction data available.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard;