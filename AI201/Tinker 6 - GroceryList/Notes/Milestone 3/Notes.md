Running curl -X POST http://127.0.0.1:5000/lists/LIST_ID/purchase-all \
-H "Content-Type: application/json" \
-d '{"user_id": "MAYA_USER_ID"}' results in all purchased items being overwritten with Maya's ID, so Olive Oil which was purchased by Leo now says purchased by Maya.

Running curl -X POST http://127.0.0.1:5000/lists/LIST_ID/purchase-all \
-H "Content-Type: application/json" \
-d '{}'  with no user ID now changes the "purchased by" value to null for all the items.