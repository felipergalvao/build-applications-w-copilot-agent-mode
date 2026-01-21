import React, { useState, useEffect } from 'react';

function Teams({ apiBaseUrl }) {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      const url = `${apiBaseUrl}/teams/`;
      console.log('📡 Buscando equipes de:', url);
      
      const response = await fetch(url);
      const data = await response.json();
      
      console.log('✅ Dados das equipes recebidos:', data);
      
      // Handle both paginated (.results) and simple array responses
      const teamsList = data.results || (Array.isArray(data) ? data : []);
      setTeams(teamsList);
      setError(null);
    } catch (err) {
      console.error('❌ Erro ao buscar equipes:', err);
      setError(err.message);
      setTeams([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="teams-container">
      <h2>👥 Equipes</h2>
      
      {loading && <div className="alert alert-info">Carregando equipes...</div>}
      {error && <div className="alert alert-danger">Erro: {error}</div>}
      
      {!loading && teams.length === 0 && (
        <div className="alert alert-warning">Nenhuma equipe encontrada</div>
      )}
      
      {!loading && teams.length > 0 && (
        <div className="row">
          {teams.map((team) => (
            <div key={team.id} className="col-md-6 mb-4">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">{team.name}</h5>
                  <p className="card-text">{team.description}</p>
                  <div className="mb-3">
                    <strong>Criada por:</strong> {team.created_by?.username || 'N/A'}
                  </div>
                  <div>
                    <strong>Membros ({team.members?.length || 0}):</strong>
                    <ul className="list-group mt-2">
                      {team.members?.map((member) => (
                        <li key={member.id} className="list-group-item">
                          {member.first_name} {member.last_name} (@{member.username})
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Teams;
