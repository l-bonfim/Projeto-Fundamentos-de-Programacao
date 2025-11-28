import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Loading from "../components/Loading";

function EditProfile() {

  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    username: '',
    age: 0,
    height:0,
    weight: 0
  })
  const [loadingState, setLoadingState] = useState(false)
  const [passArea, setPassArea] = useState(false)
  const [message, setMessage] = useState('')

  const handleFormInput = (event, name) => {
    setFormData({
      ...formData,
      [name]: event.target.value
    })
  }

  const togglePassClick = (event) => {
    event.preventDefault()
    setPassArea(!passArea)
  }

  return(
    <div>
      <h1>
        Editar Usuário
      </h1>
      <form className="form-area">
        <input type="text" placeholder="Usuário" onChange={ (e) => handleFormInput(e, 'username') } value={formData.username} />
        <input type="text" placeholder="Email" onChange={ (e) => handleFormInput(e, 'email') } value={formData.email}  />
        <input type="text" placeholder="Nome Completo" onChange={ (e) => handleFormInput(e, 'name') } value={formData.name}  />
        Idade:
        <input type="number" placeholder="Idade" onChange={ (e) => handleFormInput(e, 'age') } value={formData.age}  />
        Altura (cm):
        <input type="number" placeholder="Altura (cm)" onChange={ (e) => handleFormInput(e, 'height') } value={formData.height}  />
        Peso (kg):
        <input type="number" placeholder="Peso (kg)" onChange={ (e) => handleFormInput(e, 'weight') } value={formData.weight}  />
        {
          passArea ? (
            <div>
              Senha atual:
              <input type="password" placeholder="Senha atual"/>
              <input type="password" placeholder="Digite novamente"/>
              Nova senha:
              <input type="password" placeholder="Nova senha"/>
              <button onClick={ togglePassClick } >Alterar Senha</button>
            </div>
          ) : 
          (
            <button onClick={ togglePassClick } >Alterar Senha</button>
          )
        }
        <button>Salvar</button>
      </form>
    </div>
  )
}

export default EditProfile;