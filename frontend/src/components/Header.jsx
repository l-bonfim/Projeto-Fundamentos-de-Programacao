import { useLocation, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import logo from "../assets/img/logo.jpeg"

function Header() {

  const navigate = useNavigate()
	const location = useLocation()
  const [navBarConfig, setNavBarConfig] = useState(false)
  const { state } = location
  const [username, setUsername] = useState('')

  useEffect(() => {
    const headerConfig = async () => {
      
      if ( state !== null ) {
        setNavBarConfig(false)
        setUsername(state.username)
      } else {
        setNavBarConfig(true)
      }
    }

    headerConfig()
  }, [state])

  const handleHomeClick = () => {
    navigate("/")
  }

  const handleRegisterClick = () => {
    navigate("/register")
  }

  const handleLoginClick = () => {
    navigate("/Login")
  }

	return(
		<header>
			<nav>
        {
          navBarConfig ? (
            <div className="header-area">
              <img className="logo" src={ logo } alt="logo" />
              <h1>HabitPlanner</h1>
              <nav>
                <button onClick={handleHomeClick}>
                  Home
                </button>
                <button onClick={handleLoginClick}>
                  Entrar
                </button>
                <button onClick={handleRegisterClick}>
                  Registrar
                </button>
              </nav>
            </div>
          ) : (
            <div className="header-area">
              <img className="logo" src={ logo } alt="logo" />
              <h1>HabitPlanner</h1>
              <h2>
                Bem-Vindo { username }!
              </h2>
              <nav>
                <a href="/">Home</a>
                <a href="/login">Login</a>
                <a href="/resgiter">Cadastrar</a>
              </nav>
            </div>
          )
        }
			</nav>
		</header>
	)
}

export default Header;