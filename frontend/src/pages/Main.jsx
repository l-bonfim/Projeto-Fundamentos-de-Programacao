import { useNavigate } from "react-router-dom";
import Header from "../components/Header";

function Main() {

  const navigate = useNavigate();

  const handleRegisterClick = () => {
    navigate("/register")
  }

  const handleLoginClick = () => {
    navigate("/Login")
  }

  return (

    <div>
      <Header/>
      <h1>
        Bem-vindo!
      </h1>
      <button onClick={handleLoginClick}>
        Entrar
      </button>
      <button onClick={handleRegisterClick}>
        Registrar
      </button>
    </div>

  );
}

export default Main;
