import React, { useState, useEffect } from 'react';

function Activities({ apiBaseUrl }) {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    fetchActivities();
  }, []);

  const fetchActivities = async () => {
    try {
      setLoading(true);
      const url = `${apiBaseUrl}/activities/`;
      console.log('📡 Buscando atividades de:', url);
      
      const response = await fetch(url);
      const data = await response.json();
      
      console.log('✅ Dados das atividades recebidos:', data);
      
      // Handle both paginated (.results) and simple array responses
      const activitiesList = data.results || (Array.isArray(data) ? data : []);
      setActivities(activitiesList);
      setError(null);
    } catch (err) {
      console.error('❌ Erro ao buscar atividades:', err);
      setError(err.message);
      setActivities([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="activities-container">
      <h2>📋 Atividades</h2>
      
      {loading && <div className="alert alert-info">Carregando atividades...</div>}
      {error && <div className="alert alert-danger">Erro: {error}</div>}
      
      {!loading && activities.length === 0 && (
        <div className="alert alert-warning">Nenhuma atividade encontrada</div>
      )}
      
      {!loading && activities.length > 0 && (
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Usuário</th>
                <th>Tipo</th>
                <th>Data</th>
                <th>Duração (min)</th>
                <th>Calorias</th>
              </tr>
            </thead>
            <tbody>
              {activities.map((activity) => (
                <tr key={activity.id}>
                  <td>{activity.id}</td>
                  <td>{activity.user?.username || 'N/A'}</td>
                  <td>{activity.activity_type?.name || activity.activity_type || 'N/A'}</td>
                  <td>{new Date(activity.activity_date).toLocaleDateString('pt-BR')}</td>
                  <td>{activity.duration}</td>
                  <td>{activity.calories_burned || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Activities;
