import{ Route, Routes, BrowserRouter } from "react-router-dom";

import Main from "./Main";
import Login from "./Login";
import Register from "./Register";

const Router = () => {
  return(
    <BrowserRouter>
      <Routes>
        <Route Component={ Main } path="/" exact />
        <Route Component={ Login } path="/login" />
        <Route Component={ Register } path="/register" />
      </Routes>
    </BrowserRouter>
  )
}

export default Router;
