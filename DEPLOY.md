# Публикация в GitHub и Replit

## 0. Проверить папку

Проект должен лежать здесь:

```text
/Users/svetlanasoloveva/Documents/WishList
```

Внутри должны быть файлы:

```text
theatre-wishlist.html
index.html
README.md
DEPLOY.md
.replit
.gitignore
```

## 1. Создать Git в правильной папке

Открой Terminal и вставь:

```bash
cd "/Users/svetlanasoloveva/Documents/WishList"
pwd
```

После `pwd` должно быть:

```text
/Users/svetlanasoloveva/Documents/WishList
```

Только если путь правильный, запускай:

```bash
git init
git add .
git commit -m "Publish theatre wishlist"
```

Важно: не запускай `git add .` из домашней папки `~`.

## 2. Добавить в GitHub Desktop

1. Открой GitHub Desktop.
2. `File` -> `Add Local Repository...`
3. Выбери:

```text
/Users/svetlanasoloveva/Documents/WishList
```

4. Нажми `Add Repository`.
5. Нажми `Publish repository`.
6. Название репозитория можно поставить:

```text
theatre-wishlist
```

Можно оставить репозиторий приватным.

## 3. Подключить Replit

1. Открой Replit.
2. `Create App`.
3. Выбери `Import from GitHub`.
4. Выбери репозиторий `theatre-wishlist`.
5. Если Replit спросит команду запуска, используй:

```bash
python3 -m http.server 3000
```

Файл `.replit` уже содержит эту команду.

## 4. Проверка после публикации

На опубликованной странице должно быть:

```text
Загружено карточек: ...
```

Если карточки не появились, проверь:

- Supabase-ключ в `theatre-wishlist.html`;
- доступность таблицы `performances`;
- Row Level Security policies в Supabase;
- нет ли ошибки под поисковой строкой.

## 5. Бэкап

Перед большими правками делай архив:

```bash
cd "/Users/svetlanasoloveva/Documents/WishList"
zip -r "theatre-wishlist-backup-$(date +%Y%m%d-%H%M%S).zip" .
```

