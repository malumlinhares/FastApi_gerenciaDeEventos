import React, { useState } from 'react';

const AddAutenticadorForm = ({ addAutenticador }) => {
  const [autenticadorName, setAutenticadorName] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    if (autenticadorName.trim()) {
      addAutenticador(autenticadorName);
      setAutenticadorName('');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={autenticadorName}
        onChange={(e) => setAutenticadorName(e.target.value)}
        placeholder="Digite o nome do autenticador"
      />
      <button type="submit">Adicionar Autenticador</button>
    </form>
  );
};

export default AddAutenticadorForm;
