from flask import Flask,request,jsonify,make_response
import snowflake.connector
from flask_caching import Cache
app=Flask(__name__)

def get_snowflake_connection():
    return snowflake.connector.connect(
        user='YASH044',
        password='@Yashu_094',
        account='en40192.central-india.azure',
        warehouse='COMPUTE_WH',
        database='MULTILINGUAL_PROJECT',
        schema='PUBLIC'
    )


app.config['CACHE_TYPE'] = 'simple'  
cache = Cache(app)

@app.route('/translations', methods=['GET'])
@cache.cached(timeout=60)  
def get_translations():
    language = request.args.get('language')
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM multilingual_data WHERE NATIVE_LANG = '{language}' LIMIT 10"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    cursor.close()
    conn.close()
    return jsonify(result)
@app.route('/translations', methods=['POST'])
def add_translation():
    data = request.json
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO multilingual_data (TALK_ID, NATIVE_LANG, TRANSCRIPT, SPEAKER_1, RECORDED_DATE, TITLE, VIEWS, DURATION)
    VALUES (%(TALK_ID)s, %(NATIVE_LANG)s, %(TRANSCRIPT)s, %(SPEAKER_1)s, %(RECORDED_DATE)s, %(TITLE)s, %(VIEWS)s, %(DURATION)s)
    """
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Translation added successfully!"})
@app.route('/analytics', methods=['GET'])
def get_analytics():
    # Get the 'type' query parameter, default to 'language' if not provided
    query_type = request.args.get('type', 'language')

    conn = get_snowflake_connection()
    cursor = conn.cursor()

    if query_type == 'language':
        query = """
        SELECT NATIVE_LANG, COUNT(*) as translation_count
        FROM multilingual_data
        GROUP BY NATIVE_LANG
        ORDER BY translation_count DESC
        LIMIT 10
        """
    elif query_type == 'period':
        query = """
        SELECT RECORDED_DATE, COUNT(*) as translation_count
        FROM multilingual_data
        GROUP BY RECORDED_DATE
        ORDER BY translation_count DESC
        LIMIT 10
        """
    else:
        return jsonify({"error": "Invalid query type. Use 'language' or 'period'"}), 400
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]
    result = [dict(zip(columns, row)) for row in rows]
    cursor.close()
    conn.close()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)