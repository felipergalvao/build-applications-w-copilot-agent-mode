import React, { useState, useEffect } from 'react';

function Workouts({ apiBaseUrl }) {
  const [workouts, setWorkouts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    fetchWorkouts();
  }, []);

  const fetchWorkouts = async () => {
    try {
      setLoading(true);
      const url = `${apiBaseUrl}/suggestions/`;
      console.log('📡 Buscando sugestões de treinos de:', url);
      
      const response = await fetch(url);
      const data = await response.json();
      
      console.log('✅ Dados dos treinos recebidos:', data);
      
      // Handle both paginated (.results) and simple array responses
      const workoutsList = data.results || (Array.isArray(data) ? data : []);
      setWorkouts(workoutsList);
      setError(null);
    } catch (err) {
      console.error('❌ Erro ao buscar treinos:', err);
      setError(err.message);
      setWorkouts([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="workouts-container">
      <h2>💪 Sugestões de Treinos</h2>
      
      {loading && <div className="alert alert-info">Carregando sugestões de treinos...</div>}
      {error && <div className="alert alert-danger">Erro: {error}</div>}
      
      {!loading && workouts.length === 0 && (
        <div className="alert alert-warning">Nenhuma sugestão de treino encontrada</div>
      )}
      
      {!loading && workouts.length > 0 && (
        <div className="row">
          {workouts.map((workout) => (
            <div key={workout.id} className="col-md-6 mb-4">
              <div className="card">
                <div className="card-body">
                  <h5 className="card-title">
                    {workout.workout_type || 'Treino'} - Nível {workout.difficulty_level || 'N/A'}
                  </h5>
                  <p className="card-text">{workout.description}</p>
                  <div className="mb-2">
                    <strong>Usuário:</strong> {workout.user?.username || 'N/A'}
                  </div>
                  <div className="mb-2">
                    <strong>Duração:</strong> {workout.estimated_duration || '-'} minutos
                  </div>
                  <div>
                    <strong>Data:</strong> {new Date(workout.created_at).toLocaleDateString('pt-BR')}
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

export default Workouts;
