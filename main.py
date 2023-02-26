import pandas as pd
import csv
from flask import Flask, request, jsonify, Response


app = Flask(__name__)

recipe = pd.read_csv("data.csv")
foods = []
table = recipe

def replace(string):
    return string.replace("-", " ").upper()

def path_to_image_html(path):
    if path == 'https://www.foodandwine.com/thmb/oNVXVUf4pFADXPCm5nYR-5Ww0nA=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/201501-xl-herbed-chickpea-bruschetta-2000-658549af2d1846ecb0de55885a6773f9.jpg':
        return '<a href="http://127.0.0.1:5000/recipe1"> <img src="'+ path + '" width="200" >'
    if path == 'https://www.foodandwine.com/thmb/rXFla_SwyGohKrjVh-P8-8-Isb8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/200208-r-xl-armenian-bean-and-walnut-pate-b4a917dc587b4a7c820b89915a523d1b.jpg':
        return '<a href="http://127.0.0.1:5000/recipe2"> <img src="'+ path + '" width="200" >'
    return '<a href="http://127.0.0.1:5000/recipe"> <img src="'+ path + '" width="200" >'


@app.route('/')
def start():
    with open("first.html") as f:
        html=f.read()
    return html

@app.route('/recipe')
def show():
    return "<html><p>&#128680;&#128679;&#128680;&#128679; UNDER CONSTRUCTION &#128679;&#128680;&#128679;&#128680;<p><html>"

@app.route('/recipe1')
def recipe1():
    with open("recipe1.html") as f:
        html=f.read()
    return html

@app.route('/recipe2')
def recipe2():
    with open("recipe2.html") as f:
        html=f.read()
    return html


@app.route('/fridge')
def fridge():
    global value
    with open("fridge.html") as f:
        html=f.read()
        for item in foods:
            num = html.find('</ul>')
            to_add = '<li>\n ' + str(item) + '\n </li>\n   '
            html = html[ : num] + to_add + html[num : ]
    return html

@app.route('/food', methods=["POST"])
def food():
    global foods
    food = str(request.data, "utf-8")
    foods.append(food)
    with open("file.txt", "a") as f: # open file in append mode
        f.write(food + "\n") # 2
    return jsonify(f"\U0001F608" + " Added! " + "\U0001F608")

@app.route('/result')
def result():
    
    global foods, table
    
    recipe["Food Name"] = recipe["Food Name"].apply(replace)

    #재료, total column 만들어주기
    for ing in foods:
        recipe[ing] = 0
    recipe["total"] = 0

    #loop 돌면서 ingredient 있는지 체크하기
    for ing in foods:
        for index in range(len(recipe)):
            if (ing in recipe.iloc[index]["Ingredients"]):
                recipe.loc[index, ing] = 1
                recipe.loc[index,"total"] += 1

    #조건충족된 음식뽑기
    output = recipe[recipe["total"] == len(foods)]
    df = output.loc[:,["Food Name", "Image","Total Time"]]
    #df.set_index('Food Name', inplace=True)
    df['Total Time'] = df['Total Time'].fillna('-')
    table = df.to_html(escape=False, formatters=dict(Image=path_to_image_html))
    table = table.replace('<tr style="text-align: right;">', '<tr style="text-align: center;">')
    with open("teble.html") as f:
        html=f.read()
        num = html.find('</table>')
        to_add = '\n ' + str(table)+ '\n   '
        html = html[ : num] + to_add + html[num : ]
    return html

    


if __name__ == '__main__':
    app.run(debug=True) # don't change this line!

# NOTE: app.run never returns (it runs for ever, unless you kill the process)
# Thus, don't define any functions after the app.run call, because it will
# never get that far.