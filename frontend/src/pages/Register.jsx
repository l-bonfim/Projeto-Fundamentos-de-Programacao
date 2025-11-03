// import { useNavigate } from "react-router-dom";

function Register() {

  return(
    <div>
      <a href="/">
        Home
      </a>
      <form>
        <h1>
          Registro de novo usuario:
        </h1>
        <input placeholder="Nome" type="text" />
        <input placeholder="E-mail" type="text" />
        <input placeholder="Senha" type="password" />
        <button>Registrar</button>
      </form>
    </div>
    
  )
}

export default Register;