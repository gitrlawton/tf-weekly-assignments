Test error handling with HTTP code:

curl http://127.0.0.1:5000/lists/000/stats -i

Question:
Recall what GET /lists/<list_id>/items returns for a bad list ID, Is the PR's behavior consistent with the existing app?

Answer:
No, GET /lists/<list_id>/items returns `404 Not Found` for a bad list ID, but GET /lists/<list_id>/stats returns `200 OK`.