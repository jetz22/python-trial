from app import create_app

app = create_app()
print('ROUTES:')
for rule in sorted(app.url_map.iter_rules(), key=lambda r: (r.rule, r.endpoint)):
    print(f'{rule.rule} -> {rule.endpoint}')
