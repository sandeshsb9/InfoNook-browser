from flask import Flask, request, render_template_string
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            search_url = f"https://www.google.com/search?q={query}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
            response = requests.get(search_url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            for item in soup.find_all('div', class_='g'):
                title = item.find('h3')
                link = item.find('a', href=True)
                snippet = item.find('span', class_='aCOpRe')
                if title and link:
                    results.append({
                        'title': title.get_text(),
                        'link': link['href'],
                        'snippet': snippet.get_text() if snippet else ''
                    })

    return render_template_string(TEMPLATE, results=results)

TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>InfoNook</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: black;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 100vh; /* Ensure full height */
        }

        .border {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
            margin: 10% auto 0;
            width: 90%; /* Default width for mobile */
            height: auto; /* Adjust height based on content */
            background: linear-gradient(0deg, black, rgb(44, 42, 42));
        }

        .glow::before, .glow::after {
            content: '';
            position: absolute;
            left: -2px;
            top: -2px;
            background: linear-gradient(45deg, #e6fb04, #ff3300, #ff00ff, #ff0099, #6e0dd0, #ff3300, #e6fb04, #ff00ff);
            background-size: 400%;
            width: calc(100% + 5px);
            height: calc(100% + 5px);
            z-index: -1;
            animation: animate 20s linear infinite;
        }

        @keyframes animate {
            0% {
                background-position: 0 0;
            }
            50% {
                background-position: 400% 0;
            }
            100% {
                background-position: 0 0;
            }
        }

        .glow::after {
            filter: blur(40px);
            opacity: 0.99;
        }

        .border h1 {
            color: white;
            font-weight: bold;
            font-style: italic;
            text-shadow: 2px 2px 4px rgb(255, 0, 0);
            margin: 20px 0;
            text-align: center; /* Center the text */
        }

        form {
            display: flex;
            flex-direction: column; /* Stack input and button vertically */
            gap: 10px;
            width: 100%;
            max-width: 350px; /* Default max width */
        }

        input[type="text"] {
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 4px;
            width: 100%; /* Full width input */
            box-sizing: border-box; /* Include padding and border in width */
        }

        button {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }

        button:hover {
            background-color: #0056b3;
        }

        ul {
            list-style-type: none;
            padding: 0;
            width: 90%;
            max-width: 800px;
            margin-top: 20px;
        }

        li {
            background: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            margin: 10px 0;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        a {
            text-decoration: none;
            color: #007bff;
            font-size: 18px;
            display: block;
            margin-bottom: 5px;
        }

        a:hover {
            text-decoration: underline;
        }

        p {
            color: #666;
            font-size: 14px;
            margin: 0;
        }

        /* Responsive styles */
        @media (max-width: 480px) {
            .border {
                width: 90%; /* Full width on mobile */
            }

            input[type="text"] {
                max-width: 100%; /* Ensure full width on mobile */
            }

            button {
                width: 100%; /* Full width button */
            }

            ul {
                width: 100%; /* Full width list */
            }
        }

        @media (min-width: 481px) and (max-width: 767px) {
            .border {
                width: 80%; /* Adjust width for tablets */
            }

            form {
                flex-direction: column; /* Stack vertically */
            }

            input[type="text"] {
                max-width: 100%; /* Ensure full width */
            }

            button {
                width: auto; /* Natural width */
            }
        }

        @media (min-width: 768px) {
            .border {
                width: 70%; /* Adjust width for laptops and larger screens */
            }

            form {
                flex-direction: row; /* Align input and button horizontally */
                gap: 10px;
            }

            input[type="text"] {
                max-width: 500px; /* Increase max width for larger screens */
            }

            button {
                width: auto; /* Natural width */
            }
        }
    </style>
</head>
<body>
    <div class="border glow">
        <h1>InfoNook</h1>
        <form method="post">
            <input type="text" name="query" placeholder="Search..." required>
            <button type="submit">Search</button>
        </form>
        <ul>
            {% for item in results %}
                <li>
                    <a href="{{ item.link }}">{{ item.title }}</a>
                    <p>{{ item.snippet }}</p>
                </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
