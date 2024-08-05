### IMPORTS From Modules ###
from website import create_app

app = create_app()

### Run the website ####
if __name__ == '__main__':
    app.run(debug=True)