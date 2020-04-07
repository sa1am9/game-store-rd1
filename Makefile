admin:
	PYTHONPATH=".:${PYTHONPATH}" python -m game_store.admin.app --config configs/admin-dev.yml

test:
	PYTHONPATH=".:${PYTHONPATH}" pytest tests/
