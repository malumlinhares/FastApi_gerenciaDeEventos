import { useEffect, useState } from "react";
import axios from "axios";

const AutenticadorList = () => {
  const [autenticadores, setAutenticadores] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/autenticadores") // Atualize a URL se necessário
      .then(response => {
        setAutenticadores(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Erro ao buscar autenticadores:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div>
      <h2>Lista de Autenticadores</h2>
      {loading ? (
        <p>Carregando...</p>
      ) : (
        <ul>
          {autenticadores.map((autenticador) => (
            <li key={autenticador.id}>
              {autenticador.nome} - {autenticador.descricao}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default AutenticadorList;
