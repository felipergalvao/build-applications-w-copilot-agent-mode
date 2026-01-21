import React, { useState, useEffect } from 'react';

function Leaderboard({ apiBaseUrl }) {
  const [entries, setEntries] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const url = `${apiBaseUrl}/leaderboard-entries/`;
      console.log('📡 Buscando leaderboard de:', url);
      
      const response = await fetch(url);
      const data = await response.json();
      
      console.log('✅ Dados do leaderboard recebidos:', data);
      
      // Handle both paginated (.results) and simple array responses
      const entriesList = data.results || (Array.isArray(data) ? data : []);
      setEntries(entriesList);
      setError(null);
    } catch (err) {
      console.error('❌ Erro ao buscar leaderboard:', err);
      setError(err.message);
      setEntries([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="leaderboard-container">
      <h2>🏆 Leaderboard</h2>
      
      {loading && <div className="alert alert-info">Carregando leaderboard...</div>}
      {error && <div className="alert alert-danger">Erro: {error}</div>}
      
      {!loading && entries.length === 0 && (
        <div className="alert alert-warning">Nenhuma entrada encontrada no leaderboard</div>
      )}
      
      {!loading && entries.length > 0 && (
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead>
              <tr>
                <th>🥇 Posição</th>
                <th>Usuário</th>
                <th>Pontos</th>
                <th>Equipe</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry) => (
                <tr key={entry.id}>
                  <td>
                    {entry.rank === 1 && '🥇'}
                    {entry.rank === 2 && '🥈'}
                    {entry.rank === 3 && '🥉'}
                    {entry.rank > 3 && `#${entry.rank}`}
                  </td>
                  <td>{entry.user?.username || entry.user || 'N/A'}</td>
                  <td>{entry.points || 0}</td>
                  <td>{entry.leaderboard?.name || 'N/A'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Leaderboard;
