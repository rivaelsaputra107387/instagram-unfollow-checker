"""
Instagram Unfollowers Tracker
Flask web app untuk mengetahui siapa yang tidak follow back di Instagram.
Upload 1 file ZIP hasil export data Instagram.
"""

from flask import Flask, render_template, request
import json
import zipfile
import tempfile
import os

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 500 * 1024 * 1024  # Max 500MB upload


def extract_usernames(data):
    """
    Mengambil semua username dari struktur JSON followers Instagram.

    Struktur followers_1.json (array):
    [
        {
            "string_list_data": [
                { "value": "username", "timestamp": 123456789 }
            ]
        }
    ]
    """
    usernames = set()
    for item in data:
        for entry in item.get("string_list_data", []):
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
            { "title": "username", "string_list_data": [...] }
        ]
    }
    """
    usernames = set()
    for item in data.get("relationships_following", []):
        title = item.get("title", "")
        if title:
            usernames.add(title.strip().lower())
    return usernames


def process_zip(zip_file):
    """
    Mengekstrak dan memproses file ZIP export Instagram.

    1. Membuat temporary directory
    2. Mencari followers_1.json dan following.json di dalam ZIP
    3. Membaca dan mem-parse kedua file
    4. Membersihkan temporary files

    Args:
        zip_file: FileStorage object dari Flask request

    Returns:
        tuple: (followers_set, following_set) atau raise Exception jika gagal
    """
    # Validasi bahwa file adalah ZIP yang valid
    if not zipfile.is_zipfile(zip_file):
        raise ValueError("File yang diupload bukan file ZIP yang valid.")

    # Reset file pointer setelah is_zipfile membacanya
    zip_file.seek(0)

    followers_data = None
    following_data = None

    with tempfile.TemporaryDirectory() as tmp_dir:
        with zipfile.ZipFile(zip_file, "r") as zf:
            # Keamanan: cek path traversal
            for name in zf.namelist():
                if name.startswith("/") or ".." in name:
                    raise ValueError("File ZIP mengandung path yang tidak aman.")

            # Cari file followers_1.json dan following.json
            for name in zf.namelist():
                basename = os.path.basename(name)
                if basename == "followers_1.json":
                    zf.extract(name, tmp_dir)
                    filepath = os.path.join(tmp_dir, name)
                    with open(filepath, "r", encoding="utf-8") as f:
                        followers_data = json.load(f)

                elif basename == "following.json":
                    zf.extract(name, tmp_dir)
                    filepath = os.path.join(tmp_dir, name)
                    with open(filepath, "r", encoding="utf-8") as f:
                        following_data = json.load(f)

        # Validasi: pastikan kedua file ditemukan
        if followers_data is None:
            raise FileNotFoundError(
                "File 'followers_1.json' tidak ditemukan di dalam ZIP. "
                "Pastikan Anda mengupload file ZIP export Instagram yang benar."
            )

        if following_data is None:
            raise FileNotFoundError(
                "File 'following.json' tidak ditemukan di dalam ZIP. "
                "Pastikan Anda mengupload file ZIP export Instagram yang benar."
            )

    # Extract usernames
    followers_set = extract_usernames(followers_data)
    following_set = extract_following_usernames(following_data)

    return followers_set, following_set


@app.route("/", methods=["GET", "POST"])
def index():
    """Halaman utama untuk upload ZIP dan menampilkan hasil analisis."""
    results = None
    error = None
    stats = None

    if request.method == "POST":
        zip_file = request.files.get("zipfile")

        if not zip_file or zip_file.filename == "":
            error = "Harap upload file ZIP export Instagram."
        elif not zip_file.filename.lower().endswith(".zip"):
            error = "File harus berformat .zip"
        else:
            try:
                followers_set, following_set = process_zip(zip_file)

                # Cari yang tidak follow back
                not_following_back = sorted(following_set - followers_set)

                stats = {
                    "total_followers": len(followers_set),
                    "total_following": len(following_set),
                    "not_following_back": len(not_following_back),
                }
                results = not_following_back

            except ValueError as e:
                error = str(e)
            except FileNotFoundError as e:
                error = str(e)
            except json.JSONDecodeError:
                error = "Format file JSON di dalam ZIP tidak valid."
            except Exception as e:
                error = f"Terjadi kesalahan: {str(e)}"

    return render_template("index.html", results=results, error=error, stats=stats)


if __name__ == "__main__":
    app.run(debug=True)
