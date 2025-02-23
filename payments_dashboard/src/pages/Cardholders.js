import React, { useEffect, useState } from "react";
import { getCardholders } from "/Users/yashlad/Documents/GitHub/CS5200_Payments_Dashboard/payments_dashboard/src/api/cardholder.js";

const Cardholders = () => {
    const [cardholders, setCardholders] = useState([]);

    useEffect(() => {
        async function fetchData() {
            const data = await getCardholders();
            setCardholders(data);
        }
        fetchData();
    }, []);

    return (
        <div>
            <h2>Cardholders List</h2>
            <ul>
                {cardholders.map((c) => (
                    <li key={c.cardholder_id}>
                        {c.first_name} {c.last_name} - {c.email}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Cardholders;