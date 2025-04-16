## API для библиотеки
### Клонируем и подготавливаемся
```bash
git clone https://github.com/ImOneDollarBun/LibraryAPI.git
git cd LibraryAPI
```

Редактируем файл окружения под нужды (на убунте)
```bash
nano .env
```

### Собираем контейнер и запускаемся
```bash
docker-compose up --build
```

Доку смотрим по адресу fastapi приложения и порту, например
```url
http://localhost:5000/docs
```