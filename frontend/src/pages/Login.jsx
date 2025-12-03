import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Loading from "../components/Loading";
import Header from "../components/Header";

function Login() {

  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })
  const [loadingState, setLoadingState] = useState(false);
  const [message, setMessage] = useState('')

  const handleFormInput = (event, name) => {
    setFormData({
      ...formData,
      [name]: event.target.value
    })
  }

  const handleLogin = async (event) => {
    try{
      setLoadingState(true)
      event.preventDefault()
      const login = await fetch('http://127.0.0.1:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      const loginData = await login.json()
      if (loginData.edited === false) {
        navigate(`/profile/${ loginData.username }/edit`, {
          state : {
            id: loginData.id,
            edited: loginData.edited,
            username: loginData.username
          }
        })
      } else if (loginData.edited === true) {
        navigate(`/home/${ loginData.username }`, {
          state : {
            id: loginData.id,
            edited: loginData.edited,
            username: loginData.username
          }
        })
      } else {
        setMessage(loginData.message)
      }
      setLoadingState(false)
    } catch (err) {
      console.log(err)
    }
  }

  return(
    <div>
      <Header/>
      {
        loadingState ? (<Loading/>) : (
        <form className="form-area">
          <h2>Login</h2>
          <input placeholder="E-mail" type="text" value={formData.email} onChange={(e) => {handleFormInput(e, 'email')}} />
          <input placeholder="Senha" type="password" value={formData.password} onChange={(e) => {handleFormInput(e, 'password')}} />
          <button onClick={ handleLogin }>Entrar</button>
          {message === '' ? (true) : (
            <span>
              { message }
            </span>
          )}
        </form>
        )}
      
    </div>
  )
}

export default Login;