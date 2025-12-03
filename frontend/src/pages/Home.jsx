import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header";

function Home() {

  const { id } = useParams();
  const [lodiangState, setLoadingState] = useState(true);


  return(
    <div>
      <Header/>
      <div>
        Habitos:
        <button>Adicionar hábito</button>
      </div>
      <div>
        Registros:
        <button>Adicionar Registro</button>
      </div>
      <button>Relatórios</button>
    </div>
  )
}

export default Home;