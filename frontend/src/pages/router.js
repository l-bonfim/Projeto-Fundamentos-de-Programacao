import{ Route, Routes, BrowserRouter } from "react-router-dom";

import Main from "./Main";
import Login from "./Login";
import Register from "./Register";
import Home from "./Home";
import UserProfile from "./UserProfile"
import EditProfile from "./EditProfile";


const Router = () => {
  return(
    <BrowserRouter>
      <Routes>
        <Route Component={ Main } path="/" exact />
        <Route Component={ Login } path="/login" />
        <Route Component={ Register } path="/register" />
        <Route Component={ Home } path="/home/:username" />
        <Route Component={ UserProfile } path="/profile/:username" />
      </Routes>
    </BrowserRouter>
  )
}

export default Router;
