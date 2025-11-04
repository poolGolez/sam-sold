import { Navigate, Route, Routes } from "react-router-dom";
import LotsPage from "./pages/lots/page";
import LotsLayout from "./pages/lots/layout";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/lots" replace />} />
      <Route path="lots" element={<LotsLayout />}>
        <Route index element={<LotsPage />} />
      </Route>
      {/* <Route path="/lots/:id" element={<LotsPage />} /> */}
    </Routes>
  );
}
export default App;
