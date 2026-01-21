from app import create_app, db
import os

app = create_app()
app.secret_key = "sua_chave_secreta_aqui"

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # usa a porta do Render ou 5000 local
    app.run(host="0.0.0.0", port=port, debug=True)
