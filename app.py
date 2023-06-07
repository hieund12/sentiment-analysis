from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask_basicauth import BasicAuth

app = Flask(__name__)
CORS(app)
basic_auth = BasicAuth(app)

app.config['CORS_HEADERS'] = 'Content-Type'  # Xác định các tiêu đề CORS bạn muốn đặt
app.config['CORS_RESOURCES'] = {r'/api/*': {'origins': '*'}}  # Cấu hình tài nguyên CORS và nguồn gốc
app.config['BASIC_AUTH_USERNAME'] = 'username'  # Thay thế 'username' bằng tên đăng nhập của bạn
app.config['BASIC_AUTH_PASSWORD'] = 'password'  # Thay thế 'password' bằng mật khẩu của bạn

nltk.download('stopwords')
nltk.download('punkt')
nltk.download('vader_lexicon')


def preprocess_text(text):
    stop_words = set(stopwords.words('english'))
    words = [word for word in word_tokenize(text) if word.lower() not in stop_words]
    words = [word.lower() for word in words]
    processed_text = ' '.join(words)
    return processed_text


def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    sentiment_scores = analyzer.polarity_scores(text)
    if sentiment_scores['compound'] < 0:
        return "Negative"
    else:
        return "Positive"


@app.route('/sentiment-analysis', methods=['POST'])
@basic_auth.required  # Đặt chứng thực Basic Authen là bắt buộc cho tất cả các route liên quan đến API
def sentiment_analysis():
    data = request.get_json()
    comment = data['text']
    processed_comment = preprocess_text(comment)
    sentiment = analyze_sentiment(processed_comment)
    return jsonify({'sentiment': sentiment})


if __name__ == '__main__':
    app.run(port=8000)
