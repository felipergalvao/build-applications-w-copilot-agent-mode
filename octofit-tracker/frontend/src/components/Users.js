import React, { useState, useEffect } from 'react';

function Users({ apiBaseUrl }) {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      setLoading(true);
      const url = `${apiBaseUrl}/profiles/`;
      console.log('📡 Buscando usuários de:', url);
      
      const response = await fetch(url);
      const data = await response.json();
      
      console.log('✅ Dados dos usuários recebidos:', data);
      
      // Handle both paginated (.results) and simple array responses
      const usersList = data.results || (Array.isArray(data) ? data : []);
      setUsers(usersList);
      setError(null);
    } catch (err) {
      console.error('❌ Erro ao buscar usuários:', err);
      setError(err.message);
      setUsers([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="users-container">
      <h2>👤 Usuários</h2>
      
      {loading && <div className="alert alert-info">Carregando usuários...</div>}
      {error && <div className="alert alert-danger">Erro: {error}</div>}
      
      {!loading && users.length === 0 && (
        <div className="alert alert-warning">Nenhum usuário encontrado</div>
      )}
      
      {!loading && users.length > 0 && (
        <div className="table-responsive">
          <table className="table table-striped table-hover">
            <thead>
              <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Email</th>
                <th>Pontos</th>
                <th>Streak</th>
              </tr>
            </thead>
            <tbody>
              {users.map((user) => (
                <tr key={user.id}>
                  <td>{user.id}</td>
                  <td>{user.user?.first_name || user.first_name || 'N/A'} {user.user?.last_name || user.last_name || ''}</td>
                  <td>{user.user?.email || user.email || 'N/A'}</td>
                  <td>{user.total_points || 0}</td>
                  <td>{user.current_streak || 0}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Users;
