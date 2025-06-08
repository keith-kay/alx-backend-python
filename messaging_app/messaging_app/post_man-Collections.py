{
  "info": {
    "name": "Messaging App API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "JWT Login",
      "request": {
        "method": "POST",
        "header": [{ "key": "Content-Type", "value": "application/json" }],
        "url": { "raw": "{{base_url}}/api/token/", "host": ["{{base_url}}"], "path": ["api", "token"] },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"username\": \"{{username}}\",\n  \"password\": \"{{password}}\"\n}"
        }
      }
    },
    {
      "name": "Create Conversation",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": { "raw": "{{base_url}}/api/conversations/", "host": ["{{base_url}}"], "path": ["api", "conversations"] },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"participants\": [1, 2]\n}"
        }
      }
    },
    {
      "name": "Send Message",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": { "raw": "{{base_url}}/api/messages/", "host": ["{{base_url}}"], "path": ["api", "messages"] },
        "body": {
          "mode": "raw",
          "raw": "{\n  \"conversation_id\": 1,\n  \"content\": \"Hello!\"\n}"
        }
      }
    },
    {
      "name": "Fetch Conversations",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": { "raw": "{{base_url}}/api/conversations/", "host": ["{{base_url}}"], "path": ["api", "conversations"] }
      }
    },
    {
      "name": "Fetch Messages (Paginated)",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Authorization", "value": "Bearer {{access_token}}" }
        ],
        "url": {
          "raw": "{{base_url}}/api/messages/?conversation_id=1&page=1",
          "host": ["{{base_url}}"],
          "path": ["api", "messages"],
          "query": [
            { "key": "conversation_id", "value": "1" },
            { "key": "page", "value": "1" }
          ]
        }
      }
    },
    {
      "name": "Unauthorized Fetch Conversations",
      "request": {
        "method": "GET",
        "header": [],
        "url": { "raw": "{{base_url}}/api/conversations/", "host": ["{{base_url}}"], "path": ["api", "conversations"] }
      }
    }
  ]
}