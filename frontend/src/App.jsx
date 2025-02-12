import React from 'react';
import './App.css';
import AutenticadorList from './components/Autenticador';

const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Autenticador Management App</h1>
      </header>
      <main>
        <AutenticadorList />
      </main>
    </div>
  );
};

export default App;