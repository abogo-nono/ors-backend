from app import create_app

# create the app
app = create_app()

# run the app if the file is not imported
if __name__ == "__main__":
    app.run(debug=True)
