from flask import Flask, render_template, request, make_response, jsonify
import re

from document_classification import ModelPredication

app = Flask(__name__)
token_key = "dc_token"
token_list = {"NrVvPG07nmraB7hW4jUc","YihxvSTMH5lolmZ9WAzj","FkPvzyAsjs1SQyjRuJLG"}

pickle_file = "classfier.pickle"
mp = ModelPredication(pickle_file)

@app.route('/')
def portal():
    return render_template('welcome.html')


@app.route('/prediction', methods=['POST'])
def prediction():
    
    response = {}
    header = request.headers
    if token_key not in header:
        response["error_code"] = "you need a token to use the api, please contact the administrator"
        return make_response(jsonify(response),403)
    else:
        if header[token_key] not in token_list:
            response["error_code"]  = "Invalid token"
            return make_response(jsonify(response),401)
        
    params = request.args
    
    if "words" not in params:
        response["error_code"] = "No document provided"
        return make_response(jsonify(response),406)
        
    words = params["words"]
    data = []
    if re.match('^[\w\s]+$', words) is not None:
        data.append(words.replace("\n", ""))
        res = mp.predict(data)
        response["prediction"] = res[0]
        response["confidence"] = res[1]
        return make_response(jsonify(response),200)
        
    else:
        response["error_code"] = "the document can only contains alphanumeric and space"
        return make_response(jsonify(response),417)
                
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)