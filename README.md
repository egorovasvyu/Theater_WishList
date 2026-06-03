# Theatre Wishlist

Личная театральная доска Светланы: спектакли, статусы, ссылки на покупку билетов, заметки, теги и просмотренные спектакли с сердечками.

## Что внутри

- `theatre-wishlist.html` — основная страница.
- `index.html` — стартовая страница для Replit, сразу открывает `theatre-wishlist.html`.
- `.replit` — команда запуска для Replit.
- `.gitignore` — файлы, которые не нужно отправлять в Git.
- `N8N_AUTOMATION.md` — документация по Telegram/n8n/Supabase-автоматизации.
- `theatre-wishlist-rescue-fixed.zip` — текущий архив проекта.
- `theatre-wishlist-backup-*.zip` — ручной бэкап на случай восстановления.

## Как открыть локально

Открой файл:

```text
/Users/svetlanasoloveva/Documents/WishList/theatre-wishlist.html
```

Или запусти локальный сервер из папки проекта:

```bash
python3 -m http.server 3000
```

После этого открой:

```text
http://localhost:3000
```

## Данные

Карточки спектаклей загружаются из Supabase:

```text
https://xvqcymdplylrfepveqsi.supabase.co
```

Таблица:

```text
performances
```

Если страница открылась, но карточек нет, сначала смотри строку статуса под поиском: там будет либо `Загружено карточек: ...`, либо текст ошибки.

## Режим редактирования

PIN:

```text
2702
```

Без PIN страница работает как режим чтения.

## Публикация

Инструкция по GitHub и Replit лежит в:

```text
DEPLOY.md
```
