from flask import Flask, request, jsonify
from packaging.version import Version, InvalidVersion

app = Flask(__name__)


@app.route('/checkversion', methods=['GET'])
def checkversion():
    '''
    METHOD
    GET /checkversion

    ARGUMENTS
    takes 2 args *ver1* and *ver2*, specified in PEP440 format

    RETURNS:
    json indicating if the first string is before, after, or equal to the second string.

    ERRORS:
    422: If any one of *ver1* or *ver2* is absent, or if non conformant version values are provided
    '''
    response = {}
    ver1 = request.args.get("ver1", None)
    ver2 = request.args.get("ver2", None)

    # Check if user sent both versions
    if not ver1 or not ver2:
        response["error"] = f"send both versions ver1:{ver1} ver2:{ver2}"
        response["message"] = f"sample request: http://127.0.0.1:5000/checkversion?ver1=2.0&ver2=1.0"
        response = jsonify(response)
        response.status_code = 422
        return response

    try:
        check = compare_versions(ver1, ver2)
        response["ver1"] = ver1
        response["ver2"] = ver2
        response["result"] = f"{ver1} {check} {ver2}"
        response = jsonify(response)
    except InvalidVersion as e:
        response["error"] = str(e)
        response["message"] = f"Version numbers doesnt conform to PEP440 ref: https://www.python.org/dev/peps/pep-0440/#version-scheme"
        response = jsonify(response)
        response.status_code = 422

    return response


@app.route('/')
def index():
    return """
    <h1>Version Checker</h1>

    <pre>
    METHOD:
    GET /checkversion

    Compare version strings in PEP440 format
    ref: https://www.python.org/dev/peps/pep-0440/#version-scheme

    eg:  http://127.0.0.1:5000/checkversion?ver1=2.0&ver2=1.0.0

    ARGUMENTS:
    takes 2 args *ver1* and *ver2*, specified in PEP440 format

    RESPONE:
    json indicating if the first string is before, after, or equal to the second string.
    eg: {
      "result": "2.0 Equal 2.0",
      "ver1": "2.0",
      "ver2": "2.0"
    }

    ERRORS:
    422: If any one of *ver1* or *ver2* is absent, or if non conformant version values are provided
    eg: {
      "error": "Invalid version: '2.0.'",
      "message": "Version numbers doesnt conform to PEP440 ref: https://www.python.org/dev/peps/pep-0440/#version-scheme"
    }
    </pre>
    """


def compare_versions(ver1, ver2):
    v1 = Version(ver1)
    v2 = Version(ver2)

    if v1 < v2:
        return "Before"
    elif v1 > v2:
        return "After"
    else:
        return "Equal"


@app.errorhandler(404)
def page_not_found(e):
    response = jsonify({'error': 'supported methods are /checkversion?ver1=2.0&ver2=1.0'})
    response.status_code = 404
    return response


if __name__ == '__main__':
    app.run(threaded=True, port=5000)
