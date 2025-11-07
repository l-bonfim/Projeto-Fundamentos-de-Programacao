import { useState } from "react";

function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  })

  const handleFormInput = (event, name) => {
    setFormData({
      ...formData,
      [name]: event.target.value
    })
  }

  const handleFormSubmit = async (event) => {
    try{
      event.preventDefault()
      const response = await fetch('http://127.0.0.1:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      })
      const json = await response.json()
      console.log(response.status)
      console.log(json)
    } catch (err) {
      console.log(err)
    }
  }

  return(
    <div>
      <a href="/">
        Home
      </a>
      <form>
        <h1>
          Registro de novo usuario:
        </h1>
        <input placeholder="Nome" type="text" value={formData.name} onChange={(e) => {handleFormInput(e, 'name')}} required />
        <input placeholder="E-mail" type="text" value={formData.email} onChange={(e) => {handleFormInput(e, 'email')}}  required />
        <input placeholder="Senha" type="password" value={formData.password} onChange={(e) => {handleFormInput(e, 'password')}}  required />
        <button onClick={handleFormSubmit} >Registrar</button>
      </form>
    </div>
    
  )
}

export default Register;