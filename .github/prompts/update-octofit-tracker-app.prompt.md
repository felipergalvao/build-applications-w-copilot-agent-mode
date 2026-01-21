---
mode: agent
model: gpt-4.1
---

# Atualizações do Aplicativo Django - OctoFit Tracker

## Visão Geral

Atualizar e melhorar o aplicativo Django do OctoFit Tracker com configurações corretas, modelos robustos e uma API REST completa e funcional.

## Estrutura do Projeto

Todos os arquivos do projeto Django estão localizados em: `octofit-tracker/backend/octofit_tracker`

## Tarefas de Atualização

### 1. Atualizar `settings.py`
- Configurar conexão com MongoDB via Djongo
- Configurar Django REST Framework
- Adicionar CORS (Cross-Origin Resource Sharing)
- Configurar autenticação por token
- Habilitar suporte para múltiplos domínios (localhost e GitHub Codespaces)
- Adicionar aplicações necessárias (rest_framework, corsheaders, dj_rest_auth, allauth)

### 2. Atualizar `models.py`
Implementar modelos para suportar:
- **UserProfile**: Perfil estendido do usuário com bio e avatar
- **Team**: Equipes de fitness com membros
- **ActivityType**: Tipos de atividades (Running, Cycling, etc.)
- **Activity**: Log de atividades do usuário
- **Leaderboard**: Leaderboards por timeframe (daily, weekly, monthly, all_time)
- **LeaderboardEntry**: Entradas no leaderboard com ranking
- **WorkoutSuggestion**: Sugestões de treino personalizadas

Requisitos:
- Usar relacionamentos ForeignKey e ManyToMany apropriadamente
- Implementar métodos `__str__()` para todos os modelos
- Adicionar atributos de data (created_at, updated_at)
- Validações apropriadas

### 3. Atualizar `serializers.py`
- Criar serializers para cada modelo
- Implementar serialização de campos aninhados
- Converter ObjectId para strings (para MongoDB)
- Adicionar validação de dados
- Suportar leitura/escrita de dados complexos

### 4. Atualizar `views.py`
- Implementar ViewSets para cada modelo
- Adicionar permissões (IsAuthenticated, IsAuthenticatedOrReadOnly)
- Criar ações customizadas:
  - `add_member` e `remove_member` para Teams
  - `accept` para WorkoutSuggestion
  - `my_activities` para Activities
  - `me` para UserProfile
- Implementar filtros e buscas
- Adicionar paginação

### 5. Atualizar `urls.py`
- Configurar DefaultRouter para ViewSets
- Registrar todas as rotas de API
- Certificar que `/` aponta para a API
- Implementar `api_root` view como ponto de entrada
- Incluir URLs do tracker app
- Suportar variáveis de ambiente do GitHub Codespaces (CODESPACE_NAME)

### 6. Atualizar `admin.py`
- Registrar todos os modelos no admin
- Configurar list_display com campos relevantes
- Adicionar search_fields para buscas
- Configurar list_filter para filtros
- Adicionar fieldsets para melhor organização

### 7. Atualizar/Criar `tests.py`
- Criar testes para modelos
- Criar testes para serializers
- Criar testes para API endpoints
- Implementar testes de autenticação
- Testar permissões de acesso

## Funcionalidades Principais

### Autenticação
- Suportar Token Authentication e Session Authentication
- Endpoints públicos para activity types e leaderboards
- Endpoints protegidos para atividades do usuário e gerenciamento de equipe

### Gerenciamento de Equipes
- Criar, atualizar e deletar equipes
- Adicionar e remover membros
- Visualizar membros da equipe

### Rastreamento de Atividades
- Registrar novas atividades
- Atualizar atividades existentes
- Deletar atividades
- Filtrar atividades por usuário e tipo

### Leaderboards
- Criar leaderboards automáticos por equipe e timeframe
- Atualizar rankings com base em dados de atividade
- Suportar múltiplos critérios de ranking (calorias, distância, contagem de atividades)

### Sugestões de Treino
- Gerar sugestões personalizadas
- Aceitar ou rejeitar sugestões
- Rastrear histórico de sugestões

## Padrões e Convenções

- Usar Django REST Framework ViewSets
- Seguir convenções de nomeação PEP 8
- Implementar validação em nível de serializer
- Usar permissões do DRF apropriadamente
- Adicionar docstrings a classes e métodos

## Configuração de Banco de Dados

**Tipo**: MongoDB  
**Driver**: Djongo (Django ORM para MongoDB)  
**Host**: `mongodb://localhost:27017`  
**Database**: `octofit_db`

## Configuração de API

**Base URL**: `/api/`  
**Framework**: Django REST Framework  
**Autenticação**: Token e Session  
**Versão**: v1

## Endpoints Esperados

### Públicos (sem autenticação)
- `GET /api/activity-types/` - Listar tipos de atividade
- `GET /api/leaderboards/` - Listar leaderboards
- `GET /api/leaderboard-entries/` - Listar entradas do leaderboard
- `GET /api/teams/` - Listar equipes

### Protegidos (requer autenticação)
- `GET/POST /api/activities/` - Atividades do usuário
- `GET /api/profiles/me/` - Perfil do usuário atual
- `GET/POST /api/suggestions/` - Sugestões de treino
- `POST /api/teams/{id}/add_member/` - Adicionar membro à equipe
- `POST /api/teams/{id}/remove_member/` - Remover membro da equipe

## Dependências Necessárias

```
Django==4.1.7
djangorestframework==3.14.0
django-allauth==0.51.0
django-cors-headers==4.5.0
dj-rest-auth==2.2.6
djongo==1.3.6
pymongo==3.12
```

## Boas Práticas

1. Sempre validar entrada de dados
2. Implementar tratamento de erro apropriado
3. Usar transações para operações críticas
4. Implementar logging adequado
5. Adicionar comentários em código complexo
6. Manter modelos simples e coesos
7. Usar serializers para validação de dados

## Próximos Passos

- [ ] Implementar testes unitários
- [ ] Adicionar documentação da API com Swagger/DRF
- [ ] Configurar CI/CD
- [ ] Implementar rate limiting
- [ ] Adicionar caching
- [ ] Configurar monitoramento
- [ ] Preparar para produção

---

**Objetivo Final**: Ter um backend Django completamente funcional com API REST pronta para integração com o frontend React.
