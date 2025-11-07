import { useNavigate } from "react-router-dom";

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
