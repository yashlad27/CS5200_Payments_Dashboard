import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Cardholders from "./pages/Cardholders";

function App() {
    return (
        <Router>
            <Routes>
                <Route path="/cardholders" element={<Cardholders />} />
            </Routes>
        </Router>
    );
}

export default App;