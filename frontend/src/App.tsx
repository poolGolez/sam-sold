import { Navigate, Route, Routes } from "react-router-dom";
import LotsPage from "./pages/lots/page";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/lots" replace />} />
      <Route path="/lots" element={<LotsPage />} />
      <Route path="/lots/:id" element={<LotsPage />} />
    </Routes>
  );
}
export default App;
