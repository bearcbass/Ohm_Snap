import json
from six.moves.urllib.request import urlopen
from functools import wraps
from PIL import Image

from flask import (
    Flask,
    redirect,
    request,
    jsonify,
    _request_ctx_stack,
    flash,
    send_file,
)
from flask_cors import cross_origin, CORS

from werkzeug.utils import secure_filename
from jose import jwt

import os
from io import BytesIO
from sam.create_model import embed_image, load_model
from sam.create_model import mask_query

# SAM

AUTH0_DOMAIN = "ttps://ohm-snap-auth0.com"
API_AUDIENCE = "https://ohm-snap-auth0.com"
ALGORITHMS = ["RS256"]

APP = Flask(__name__)
CORS(APP)
model = load_model()


# Error handler
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@APP.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response


# /server.py


# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            401,
        )
    elif len(parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found"}, 401
        )
    elif len(parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            },
            401,
        )

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://" + AUTH0_DOMAIN + "/",
                )
            except jwt.ExpiredSignatureError:
                raise AuthError(
                    {"code": "token_expired", "description": "token is expired"}, 401
                )
            except jwt.JWTClaimsError:
                raise AuthError(
                    {
                        "code": "invalid_claims",
                        "description": "incorrect claims,"
                        "please check the audience and issuer",
                    },
                    401,
                )
            except Exception:
                raise AuthError(
                    {
                        "code": "invalid_header",
                        "description": "Unable to parse authentication" " token.",
                    },
                    401,
                )

            _request_ctx_stack.top.current_user = payload
            return f(*args, **kwargs)
        raise AuthError(
            {"code": "invalid_header", "description": "Unable to find appropriate key"},
            401,
        )

    return decorated


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
        token_scopes = unverified_claims["scope"].split()
        for token_scope in token_scopes:
            if token_scope == required_scope:
                return True
    return False


# Controllers API


# This doesn't need authentication
@APP.route("/api/public")
@cross_origin(headers=["Content-Type", "Authorization"])
def public():
    response = (
        "Hello from a public endpoint! You don't need to be authenticated to see this."
    )
    return jsonify(message=response)


# This needs authentication
@APP.route("/api/private")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private():
    response = (
        "Hello from a private endpoint! You need to be authenticated to see this."
    )
    return jsonify(message=response)


# This needs authorization
@APP.route("/api/private-scoped")
@cross_origin(headers=["Content-Type", "Authorization"])
@requires_auth
def private_scoped():
    if requires_scope("read:messages"):
        response = "Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this."
        return jsonify(message=response)
    raise AuthError(
        {
            "code": "Unauthorized",
            "description": "You don't have access to this resource",
        },
        403,
    )


ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@APP.route("/mask", methods=["POST", "GET"])
def mask():
    if request.method == "POST":
        if "image" not in request.files or "data" not in request.files:
            flash("No file part")
            return redirect(request.url)
        print(request.files["data"])
        data = json.load(request.files["data"])
        image = request.files["image"]
        upload_file = image
        if upload_file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if "coordinates" not in data:
            flash("No selected file")
            return redirect(request.url)
        coordinates = data["coordinates"]
        if "x" not in coordinates or "y" not in coordinates:
            flash("Json data incorrect")
            return redirect(request.url)
        # save image, embed image
        if allowed_file(upload_file.filename):
            point = (int(coordinates["x"]), int(coordinates["y"]))
            filename = secure_filename(upload_file.filename)
            img_path = os.path.join("", filename)
            upload_file.save(img_path)
            stripped = filename.rsplit(".", 1)[0]
            mask_images = mask_query(img_path, point, model)
            # embed_image(img_path, stripped + ".npy")
            # save to mongodb
            length = len(mask_images)
            im = mask_images[1]
            bytes_io = BytesIO()
            im.save(bytes_io, "JPEG")
            bytes_io.seek(0)
            return send_file(bytes_io, mimetype="image/JPEG")
        # return redirect(url_for("uploaded_file", filename=filename))


# @APP.route("/band_masks", methods=["POST", "GET"])
# def mask():
#     if request.method == "POST":
#         if "image" not in request.files:
#             flash("No file part")
#             return redirect(request.url)
#         image = request.files["image"]
#         upload_file = image
#         if upload_file.filename == "":
#             flash("No selected file")
#             return redirect(request.url)
#         # save image, embed image
#         if allowed_file(upload_file.filename):
#             request.get_json()
#             filename = secure_filename(upload_file.filename)
#             img_path = os.path.join("", filename)
#             upload_file.save(img_path)
#             stripped = filename.rsplit(".", 1)[0]
#             mask_img_query(
#                 img_path,
#                 point,
#             )
#             # embed_image(img_path, stripped + ".npy")
#             # save to mongodb
#             return "Success"
#             # return redirect(url_for("uploaded_file", filename=filename))


@APP.route("/image", methods=["GET", "POST"])
# @requires_auth
def image():
    MAX_CONTENT_SIZE = 50000000

    # save image, embed image
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        upload_file = request.files["file"]
        # TODO additional checks -https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/
        if upload_file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if allowed_file(upload_file.filename):
            filename = secure_filename(upload_file.filename)
            img_path = os.path.join("", filename)
            upload_file.save(img_path)
            # TODO eventually we need the color band function here
            stripped = filename.rsplit(".", 1)[0]
            embed_image(img_path, stripped + ".npy")
            # save to mongodb
            return "Success"
            # return redirect(url_for("uploaded_file", filename=filename))
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=env.get("PORT", 3010))
