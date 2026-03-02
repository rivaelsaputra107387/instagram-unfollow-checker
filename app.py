"""
Instagram Unfollowers Tracker
Flask web app untuk mengetahui siapa yang tidak follow back di Instagram.
"""

from flask import Flask, render_template, request
import json

app = Flask(__name__)


def extract_usernames(data):
    """
    Mengambil semua username dari struktur JSON export Instagram.
    
    Struktur followers_1.json (array):
    [
        {
            "string_list_data": [
                {
                    "href": "...",
                    "value": "username",
                    "timestamp": 123456789
                }
            ]
        }
    ]
    
    Args:
        data: list of dict dari JSON followers Instagram
    
    Returns:
        set: kumpulan username
    """
    usernames = set()
    for item in data:
        string_list = item.get("string_list_data", [])
        for entry in string_list:
            value = entry.get("value", "")
            if value:
                usernames.add(value.strip().lower())
    return usernames


def extract_following_usernames(data):
    """
    Mengambil semua username dari struktur JSON following Instagram.
    
    Struktur following.json (object):
    {
        "relationships_following": [
            {
                "title": "username",
                "string_list_data": [...]
            }
        ]
    }
    
    Args:
        data: dict dari JSON following Instagram
    
    Returns:
        set: kumpulan username
    """
    usernames = set()
    following_list = data.get("relationships_following", [])
    for item in following_list:
        title = item.get("title", "")
        if title:
            usernames.add(title.strip().lower())
    return usernames


@app.route("/", methods=["GET", "POST"])
def index():
    """Halaman utama untuk upload dan menampilkan hasil analisis."""
    results = None
    error = None
    stats = None

    if request.method == "POST":
        followers_file = request.files.get("followers")
        following_file = request.files.get("following")

        # Validasi file
        if not followers_file or not following_file:
            error = "Harap upload kedua file (followers_1.json dan following.json)."
        else:
            try:
                # Parse JSON
                followers_data = json.load(followers_file)
                following_data = json.load(following_file)

                # Extract usernames
                followers_set = extract_usernames(followers_data)
                following_set = extract_following_usernames(following_data)

                # Cari yang tidak follow back
                # (orang yang kamu follow tapi tidak follow kamu balik)
                not_following_back = sorted(following_set - followers_set)

                stats = {
                    "total_followers": len(followers_set),
                    "total_following": len(following_set),
                    "not_following_back": len(not_following_back),
                }

                results = not_following_back

            except json.JSONDecodeError:
                error = "Format file JSON tidak valid. Pastikan file yang diupload benar."
            except Exception as e:
                error = f"Terjadi kesalahan saat memproses file: {str(e)}"

    return render_template("index.html", results=results, error=error, stats=stats)


if __name__ == "__main__":
    app.run(debug=True)
