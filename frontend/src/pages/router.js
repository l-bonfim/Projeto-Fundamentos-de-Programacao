import{ Route, Routes, BrowserRouter } from "react-router-dom";

import Home from "./Home";
import Login from "./Login";
import Register from "./Register";

const Router = () => {
  return(
    <BrowserRouter>
      <Routes>
        <Route Component={ Home } path="/" exact />
        <Route Component={ Login } path="/login" />
        <Route Component={ Register } path="/register" />
      </Routes>
    </BrowserRouter>
  )
}

export default Router;
