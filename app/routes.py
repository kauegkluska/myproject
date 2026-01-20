from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from flask.config import T
from app.models import Properties, Property_Features, Property_Images
from app import create_app, db
from werkzeug.utils import secure_filename
import os


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    print("FILTROS RECEBIDOS:", request.args)
   
    query = Properties.query
    #filtro
    #tipo
    type_ = request.args.get("type")
    if type_ and type_ != "all":
        query = query.filter(Properties.type == type_)
    #transacao
    transaction = request.args.get("transaction")
    if transaction and transaction != "all":
        query = query.filter(Properties.transaction == transaction)
    #cidade
    city = request.args.get("city")
    if city and city != "all":
        query = query.filter(Properties.city == city)    
    #max_preco
    max_price = request.args.get("maxPrice")
    
    if max_price:
        query = query.filter(Properties.price <= int(max_price))
        
    cities = (
        Properties.query
        .with_entities(Properties.city)
        .distinct()
        .order_by(Properties.city)
        .all()
    )
    cities = [c[0] for c in cities]

    properties = query.all()
        
    return render_template("index.html", properties = properties, filters = request.args, cities = cities)


@main_bp.route('/property-details/<int:property_id>')
def property_details(property_id):
    property = Properties.query.get_or_404(property_id)
    return render_template('property-details.html', property = property)


ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123456"

@main_bp.route("/admin/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("main.dashboard"))
        else:
            flash("Usuário ou senha incorretos!", "error")
            return redirect(url_for("main.login"))

    return render_template("login.html")

@main_bp.route("/admin/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("main.login"))
    
    properties = Properties.query.all()
    total_properties = len(properties)
    active_listings = len([p for p in properties if p.active])
    
    return render_template(
        "dashboard.html",
        properties=properties,
        total_properties=total_properties,
        active_listings=active_listings
    )
    
@main_bp.route("/admin/properties/add", methods=["POST"])
def add_property():
    if not session.get("admin_logged_in"):
        return redirect(url_for("main.login"))

    name = request.form.get("name")
    type_ = request.form.get("type")
    transaction = request.form.get("transaction")
    city = request.form.get("city")
    neighbourhood = request.form.get("neighbourhood")
    price = float(request.form.get("price"))
    beds = int(request.form.get("beds"))
    baths = int(request.form.get("baths"))
    sqmt = int(request.form.get("sqmt"))
    description = request.form.get("description")

    # Cria a propriedade
    new_property = Properties(
        name=name,
        type=type_,
        transaction=transaction,
        city=city,
        neighbourhood=neighbourhood,
        price=price,
        beds=beds,
        baths=baths,
        sqmt=sqmt,
        description=description,
        active=True
    )

    db.session.add(new_property)
    db.session.flush()  # necessario para pegar ID antes do commit

    # Salvar features
    features_str = request.form.get("features")  # "Pool, Garage"
    if features_str:
        features_list = [f.strip() for f in features_str.split(",") if f.strip()]
        for f in features_list:
            feature = Property_Features(feature=f, property_id=new_property.id)
            db.session.add(feature)

    # Salvar imagens
    uploaded_files = request.files.getlist("images")
    img_folder = os.path.join("app", "static", "img")
    for file in uploaded_files:
        if file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(img_folder, filename))
            img = Property_Images(image= '/static/img/'+filename, property_id=new_property.id)
            db.session.add(img)

    db.session.commit()
    flash("Property added successfully!", "success")
    return redirect(url_for("main.dashboard"))