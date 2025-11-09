import { Navigate, Route, Routes } from "react-router-dom";
import LotsPage from "./pages/lots/page";
import LotsLayout from "./pages/lots/layout";
import LotPage from "./pages/lots/[id]/page";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/lots" replace />} />
      <Route path="lots" element={<LotsLayout />}>
        <Route index element={<LotsPage />} />
        <Route path="/lots/:id" element={<LotPage />} />
      </Route>
    </Routes>
  );
}
export default App;
