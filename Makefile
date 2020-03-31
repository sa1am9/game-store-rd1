admin:
	PYTHONPATH=".:${PYTHONPATH}" python -m game_store.admin.app

test:
	PYTHONPATH=".:${PYTHONPATH}" pytest tests/
