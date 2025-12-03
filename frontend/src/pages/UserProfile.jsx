import { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import Loading from "../components/Loading";
import Header from "../components/Header";

function UserProfile(){

  const navigate = useNavigate()
  const location = useLocation()
  const { state } = location
  const { username, id } = state
  const [loadingState, setLoadingState] = useState(false)
  const [formData, setFormData] = useState({
      email: '',
      password: '',
      name: '',
      username: '',
      age: 0,
      height:0,
      weight: 0,
      id: id
  })

  useEffect(() => {
    const colectingUserData = async () => {
      setLoadingState(true)
      const fetchingUserData = await fetch(`http://127.0.0.1:5000/profile/${ username }`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      })
      const userData = await fetchingUserData.json()
      if (userData.id === id) {
        setFormData(userData)
      }
      setLoadingState(false)
    }

    colectingUserData()
  }, [id, username])

  const edit_button = (event) => {
    event.preventDefault()
    navigate(`/profile/${ formData.username }/edit`, {
        state : {
          id: formData.id,
          edited: formData.edited,
          username: formData.username
        }
      })
  }


  return(
      <div>
        <Header/>
        <h1>
            Dados de Usuários
        </h1>
        {
          loadingState ? (
            <Loading/>
          ) : (
            <div>
              <form className="form-area">
                Usuário:
                <p>{ formData.username }</p>
                Nome:
                <p>{ formData.name }</p>
                Email:
                <p>{ formData.email }</p>
                Idade:
                <p>{ formData.age }</p>
                Altura (cm):
                <p>{ formData.height }</p>
                Peso (kg):
                <p>{ formData.weight }</p>
              </form>
            </div>
          )}
        <button onClick={ edit_button }>
          Editar
        </button>
      </div>
  )
}

export default UserProfile;