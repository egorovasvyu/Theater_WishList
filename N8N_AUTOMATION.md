# N8N automation для театрального wishlist

Цель: отправлять ссылку или заметку в Telegram-бот, а n8n должен разобрать сообщение, найти/заполнить карточку спектакля и сохранить её в Supabase.

## Общая схема

```text
Telegram Trigger
→ Edit Fields
→ AI Agent
→ Code in JavaScript
→ Split Out
→ Supabase: Get many rows
→ If
  → True: Telegram reply, что карточка уже есть
  → False: Supabase Insert
          → Telegram reply, что карточка добавлена
```

## 1. Telegram Trigger

Триггер получает сообщение из Telegram-бота.

Поддерживаем два сценария:

- сообщение написано вручную от себя;
- сообщение переслано из канала/от человека.

## 2. Edit Fields

Нужно вывести минимум два поля:

```text
text
source_channel
```

### text

```text
={{ $json.message.text || $json.message.caption || '' }}
```

### source_channel

```text
={{
  $json.message.forward_origin?.chat?.title
  || $json.message.forward_from_chat?.title
  || [
    $json.message.forward_origin?.sender_user?.first_name,
    $json.message.forward_origin?.sender_user?.last_name
  ].filter(Boolean).join(' ')
  || [
    $json.message.forward_from?.first_name,
    $json.message.forward_from?.last_name
  ].filter(Boolean).join(' ')
  || $json.message.forward_sender_name
  || 'Я'
}}
```

## 3. AI Agent

Агент получает текст и источник и возвращает JSON с карточками спектаклей.

### System Message

```text
Ты AI Agent для личного театрального wishlist.

На вход приходит Telegram-сообщение: ссылка, текст, пересланный пост или заметка.
Также приходит источник рекомендации.

Твоя задача: извлечь одну или несколько карточек спектаклей.

Верни строго JSON без пояснений, без markdown:

{
  "items": [
    {
      "title": "",
      "theater": "",
      "director": "",
      "city": "Москва",
      "category": "adult",
      "status": "want",
      "link": "",
      "source": "",
      "note": "",
      "tags": []
    }
  ]
}

Правила:
- source всегда бери из поля "Источник".
- category только "adult" или "kids".
- Если спектакль детский, ставь "kids".
- Если явно не понятно, ставь "adult".
- status по умолчанию "want".
- city по умолчанию "Москва".
- link сохрани исходную ссылку, если она есть.
- Если есть #NY, #НовыйГод, Новый год, Щелкунчик, Двенадцать месяцев или новогодний смысл — добавь тег "#NY".
- Если есть слова подростки, подростковый, 12+, 14+, 16+ — добавь тег "#подростки".
- Если театр неясен, оставь пустую строку.
- Если сообщение содержит несколько спектаклей, верни несколько объектов в items.
- note: сделай короткое саммари из сообщения на русском языке, 1 короткое предложение.
- Если в сообщении почти нет описания, а есть только ссылка, note оставь пустой строкой.
- Не копируй весь текст сообщения в note.
```

### Prompt / User Message

```text
Обработай это Telegram-сообщение.

Текст:
{{ $json.text }}

Источник:
{{ $json.source_channel }}
```

## 4. Tool для агента: Tavily Search

Используем Tavily, если агенту нужно найти официальную страницу спектакля.

### Query

```text
{{ $fromAI("query", "Поисковый запрос для поиска официальной страницы спектакля", "string") }}
```

### Tool Description

```text
Ищи в интернете официальную страницу спектакля на сайте театра или площадки.
Используй этот инструмент, если в сообщении нет ссылки или нужно проверить ссылку.
В финальный link можно ставить только официальный сайт театра/площадки.
Не используй агрегаторы и афиши: Яндекс, Афиша, Ticketland, Timepad, Kassir, KudaGo, 2ГИС, соцсети и новостные статьи.
```

## 5. Structured Output Parser

Пример JSON:

```json
{
  "items": [
    {
      "title": "Азбука эмоций",
      "theater": "МАМТ",
      "director": "",
      "city": "Москва",
      "category": "kids",
      "status": "want",
      "link": "https://stanmus.ru/shows/azbuka-emotsij/",
      "source": "Я",
      "note": "Детский камерный концерт про эмоции и музыку.",
      "tags": []
    }
  ]
}
```

## 6. Code in JavaScript

Если AI Agent возвращает JSON строкой в поле `output`, распарсить так:

```javascript
const raw = $json.output;
const parsed = typeof raw === 'string' ? JSON.parse(raw) : raw;

return [
  {
    json: parsed
  }
];
```

## 7. Split Out

Field To Split Out:

```text
items
```

После этого каждый спектакль идёт отдельной карточкой.

## 8. Supabase: Get many rows

Проверяем дубль до добавления.

Таблица:

```text
performances
```

Фильтры:

```text
title ILIKE {{ '*' + $json.title + '*' }}
theater ILIKE {{ '*' + $json.theater + '*' }}
```

Settings:

```text
Always Output Data = ON
```

Если дубля нет, Supabase вернёт пустой объект `{}`.

## 9. If

Условие:

```text
{{ String(Boolean($json.id)) }}
```

Operator:

```text
is equal to
```

Value:

```text
true
```

Логика:

- True — похожая карточка уже есть.
- False — карточки нет, можно добавлять.

## 10. Supabase Insert

Таблица:

```text
performances
```

Поля:

```text
id = {{ 'tg_' + Date.now() + '_' + Math.random().toString(36).slice(2, 7) }}
title = {{ $('Split Out').item.json.title || '' }}
theater = {{ $('Split Out').item.json.theater || '' }}
director = {{ $('Split Out').item.json.director || '' }}
source = {{ $('Split Out').item.json.source || 'Telegram' }}
city = {{ $('Split Out').item.json.city || 'Москва' }}
category = {{ ['kids','детский','children','child','kid'].includes(($('Split Out').item.json.category || '').trim().toLowerCase()) ? 'kids' : 'adult' }}
status = {{ ['want','verywant','bought','seen','postponed'].includes(($('Split Out').item.json.status || '').trim()) ? $('Split Out').item.json.status.trim() : 'want' }}
link = {{ $('Split Out').item.json.link || '' }}
note = {{ $('Split Out').item.json.note || '' }}
display_order = {{ Math.floor(Date.now() / 1000) }}
data = {{ { tags: $('Split Out').item.json.tags || [] } }}
```

## 11. Telegram reply: дубль найден

Parse Mode:

```text
HTML
```

Текст:

```html
<b>Уже есть похожая карточка</b>

🎭 {{ $json.title }}
🏛 {{ $json.theater }}
🔗 {{ $json.link || 'ссылка не указана' }}

<b>Новая заявка:</b>
🎭 {{ $('Split Out').item.json.title }}
🏛 {{ $('Split Out').item.json.theater }}
🔗 {{ $('Split Out').item.json.link || 'ссылка не указана' }}

<b>Что делаем?</b>
1. Если это дубль — ничего не надо
2. Если это другой спектакль — добавь вручную на сайте или пришли уточнение
```

## 12. Telegram reply: карточка добавлена

```html
<b>Добавила спектакль в театральный wishlist</b>

🎭 {{ $('Split Out').item.json.title }}
🏛 {{ $('Split Out').item.json.theater }}
🔗 {{ $('Split Out').item.json.link || 'ссылка не указана' }}

Проверяй на странице театральной доски.
```

## 13. Частые ошибки

### Could not find the `data` column

В Supabase нужно добавить колонку:

```sql
alter table public.performances
add column if not exists data jsonb default '{}'::jsonb;

notify pgrst, 'reload schema';
```

### invalid input syntax for type integer

Для `display_order` использовать:

```text
{{ Math.floor(Date.now() / 1000) }}
```

### category violates check constraint

Использовать нормализацию:

```text
{{ ['kids','детский','children','child','kid'].includes(($('Split Out').item.json.category || '').trim().toLowerCase()) ? 'kids' : 'adult' }}
```

