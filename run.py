from dissertation import create_app

'''
Runs the app
'''
app = create_app()

if __name__ == '__main':
    app.run(debug=False, use_reloader=False)
