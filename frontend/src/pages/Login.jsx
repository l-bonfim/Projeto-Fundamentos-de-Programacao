// import { useNavigate } from "react-router-dom";
import { useState } from "react";

function Login() {

  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })
  const [loadingState, setLoadingState] = useState(false);

  const handleFormInput = (event, name) => {
    setFormData({
      ...formData,
      [name]: event.target.value
    })
  }

  return(
    <div>
      <a href="/">
        Home
      </a>
      <input placeholder="E-mail" type="text" />
      <input placeholder="Senha" type="password" />
      <button>Entrar</button>
    </div>
  )
}

export default Login;