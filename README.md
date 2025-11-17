# UCar - Incident API Service

API-сервис для учета инцидентов

### Запуск проекта
```bash
# Клонировать репозиторий
git clone https://github.com/PanDanil-prog/UCar.git
cd UCar

# Запустить сервисы
docker-compose up --build -d
```
Сваггер: http://localhost:8000/docs

## Основные эндпоинты

### Создать инцидент
```bash
POST http://localhost:8000/api/v1/incidents/
Content-Type: application/json

{
  "description": "Самокат не в сети уже 2 часа",
  "source": "operator"
}
```

### Получить список инцидентов
```bash
GET http://localhost:8000/api/v1/incidents/?status=open&skip=0&limit=10
```

### Обновить статус инцидента
```bash
PATCH http://localhost:8000/api/v1/incidents/1
Content-Type: application/json

{
  "status": "in_progress"
}
```

### Получить инцидент по ID
```bash
GET http://localhost:8000/api/v1/incidents/1
```

### Удалить инцидент
```bash
DELETE http://localhost:8000/api/v1/incidents/1
```

