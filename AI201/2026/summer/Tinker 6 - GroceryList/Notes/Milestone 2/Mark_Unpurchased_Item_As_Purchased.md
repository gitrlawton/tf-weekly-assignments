Try marking an unpurchased item as purchased:

curl -X PATCH \
  -H "Content-Type: application/json" \
  -d '{"user_id": "95d7aa73-7711-4e64-a5db-52374874c39d"}' \
  http://127.0.0.1:5000/lists/37653694-508a-43f2-bd6a-6ef1efdc92fd/items/d72bcb68-1f57-4805-9914-7bcd19681853

{
  "added_at": "2026-07-04T15:29:17.586466",
  "added_by": "95d7aa73-7711-4e64-a5db-52374874c39d",
  "category": "produce",
  "id": "d72bcb68-1f57-4805-9914-7bcd19681853",
  "is_purchased": true,
  "list_id": "37653694-508a-43f2-bd6a-6ef1efdc92fd",
  "name": "Bananas",
  "purchased_at": "2026-07-04T21:09:01.207826",
  "purchased_by": "95d7aa73-7711-4e64-a5db-52374874c39d",
  "quantity": 1.0,
  "unit": "bunch"
}


Run it again:

{
  "error": "Item 'd72bcb68-1f57-4805-9914-7bcd19681853' is already marked as purchased"
}


Try Requesting a Bad ID:

curl -X PATCH \
  -H "Content-Type: application/json" \
  -d '{"user_id": "95d7aa73-7711-4e64-a5db-52374874c39d"}' \
  http://127.0.0.1:5000/lists/37653694-508a-43f2-bd6a-6ef1efdc92fd/items/bad-item-id

{
  "error": "Item 'bad-item-id' not found in list '37653694-508a-43f2-bd6a-6ef1efdc92fd'"
}