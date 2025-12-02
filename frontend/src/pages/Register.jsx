import { useState } from "react";
import Loading from "../components/Loading";

function Register() {
  const [formData, setFormData] = useState({
    username: '',
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
  
  const validateUser = () => {
    const user = formData.username
    let testUser = false
    if (user.length <= 3) {
      testUser = true
    }
    return testUser
  }

  const validateEmail = () => {
    const email = formData.email
    let testEmail = false
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
      if (emailRegex.test(email) === false) {
        testEmail = true
  }
  return testEmail
  }

  const validatePass = () => {
    const pass = formData.password
    let testPass = false
      if (pass.length <= 5) {
        testPass = true
  }
  return testPass
  }

  const validateSubmit = () => {
    if (!validateUser() && !validateEmail() && !validatePass()) {
      return false
    }
    return true
  }

  const handleFormSubmit = async (event) => {
    try{
      setLoadingState(true)
      event.preventDefault()
      const res = await fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      const resData = await res.json()
      setMessage(resData.message)
      setLoadingState(false)
    } catch (err) {
      console.log(err)
    }
  }

  return(
    <div>
      <a href="/">
        Home
      </a>
      {loadingState ? (
        <Loading/>
      ) : (<form>
        <h1>
          Registro de novo usuario:
        </h1>
        <input placeholder="Usuario" type="text" value={formData.username} onChange={(e) => {handleFormInput(e, 'username')}} />
        {
          validateUser() ? (
            <span>Usuário deve ter 4 caracteres ou mais.</span>
          ) : (
            false
          )
        }
        <input placeholder="E-mail" type="text" value={formData.email} onChange={(e) => {handleFormInput(e, 'email')}} />
        {
          validateEmail() ? (
            <span>Digite um email válido.</span>
          ) : (
            false
          )
        }
        <input placeholder="Senha" type="password" value={formData.password} onChange={(e) => {handleFormInput(e, 'password')}} />
        {
          validatePass() ? (
            <span>Sua senha deve ter pelo menos 6 digitos.</span>
          ) : (
            false
          )
        }
        {message === '' ? (true) : (
            <span>
              { message }
            </span>
          )}
        <button disabled={ validateSubmit() } onClick={ handleFormSubmit } >Registrar</button>
      </form>)}
    </div>
    
  )
}

export default Register;