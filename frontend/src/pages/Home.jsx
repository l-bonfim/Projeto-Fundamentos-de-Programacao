import { useNavigate } from "react-router-dom";

function Home() {

  const navigate = useNavigate();

  const handleRegisterClick = () => {
    navigate("/register")
  }

  const handleLoginClick = () => {
    navigate("/Login")
  }

  const test_connect = async () => {
    fetch('http://127.0.0.1:5000', {
      method: ['GET']
    })
      .then(response => response.json())
      .then(data => {
        console.log(data)
      })
      .catch(error => {
        console.error(error)
      })
      fetch('http://127.0.0.1:5000', {
        method: "POST",
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
          teste2: "teste2"
      }),
      })
      .then(response => response.json())
      .then(data => {
        console.log(data)
      })
      .catch(error => {
        console.error(error)
      })
  }

  test_connect()

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

export default Home;
