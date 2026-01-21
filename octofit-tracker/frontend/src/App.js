import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Activities from './components/Activities';
import Teams from './components/Teams';
import Users from './components/Users';
import Leaderboard from './components/Leaderboard';
import Workouts from './components/Workouts';

function App() {
  const codespaceNameFromEnv = process.env.REACT_APP_CODESPACE_NAME;
  const apiBaseUrl = codespaceNameFromEnv 
    ? `https://${codespaceNameFromEnv}-8000.app.github.dev/api`
    : 'http://localhost:8000/api';

  console.log('🚀 OctoFit Tracker App iniciado');
  console.log('📡 REACT_APP_CODESPACE_NAME:', codespaceNameFromEnv);
  console.log('🔗 API Base URL:', apiBaseUrl);

  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
          <div className="container-fluid">
            <Link className="navbar-brand" to="/">
              🐙 OctoFit Tracker
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Atividades</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Equipes</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Usuários</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <div className="container mt-4">
          <Routes>
            <Route path="/" element={<Home apiBaseUrl={apiBaseUrl} />} />
            <Route path="/activities" element={<Activities apiBaseUrl={apiBaseUrl} />} />
            <Route path="/teams" element={<Teams apiBaseUrl={apiBaseUrl} />} />
            <Route path="/users" element={<Users apiBaseUrl={apiBaseUrl} />} />
            <Route path="/leaderboard" element={<Leaderboard apiBaseUrl={apiBaseUrl} />} />
            <Route path="/workouts" element={<Workouts apiBaseUrl={apiBaseUrl} />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

function Home({ apiBaseUrl }) {
  return (
    <div className="jumbotron">
      <h1 className="display-4">Bem-vindo ao OctoFit Tracker 🐙💪</h1>
      <p className="lead">Rastreie suas atividades, gerencie equipes e compita no leaderboard!</p>
      <hr className="my-4" />
      <p>API Base URL: <code>{apiBaseUrl}</code></p>
      <p className="text-muted">Selecione um item no menu para começar.</p>
    </div>
  );
}

export default App;
