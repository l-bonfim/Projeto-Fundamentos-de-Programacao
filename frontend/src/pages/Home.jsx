import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";

function Home() {

  const { id } = useParams();
  const [lodiangState, setLoadingState] = useState(true);


  return(
    <div>
      <section>
        Olá $USER,
        Aqui está sua área de hábitos:
      </section>
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