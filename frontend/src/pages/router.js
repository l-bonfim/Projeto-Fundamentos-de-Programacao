import{ Route, Routes, BrowserRouter } from "react-router-dom";

import Main from "./Main";
import Login from "./Login";
import Register from "./Register";
import Home from "./Home";

const Router = () => {
  return(
    <BrowserRouter>
      <Routes>
        <Route Component={ Main } path="/" exact />
        <Route Component={ Login } path="/login" />
        <Route Component={ Register } path="/register" />
        <Route Component={ Home } path="/home/:id" />
      </Routes>
    </BrowserRouter>
  )
}

export default Router;
