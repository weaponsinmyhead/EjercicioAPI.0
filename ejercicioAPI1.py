
from flask import Flask, jsonify, request
from products import products
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

@app.route('/ping')
def ping():
    return jsonify({'message': 'pong!'})
   
@app.route('/products')    
def getProducts():
    return jsonify({"products":products, "message": "Product's List"})

@app.route('/products/<string:product_name>')
def getProduct(product_name):
    productFound= [product for product in products if product['name']== product_name]
    if (len(productFound)> 0): 
        return jsonify({"product": productFound[0]})
    return jsonify({"message":"product not found"})

@app.route('/products', methods=['POST'])
def addProduct():
    newProduct = { 
        "name": request.json['name'],
        "price": request.json['price'],
        "quantity": request.json['quantity']
    }
    products.append(newProduct)
    print(request.json)
    return jsonify({"message":"Product Addedd Succesfully", "products": products})

@app.route('/products/<string:product_name>', methods=['PUT'])
def editProduct(product_name):
    productFound= [product for product in products if product['name']== product_name]
    if (len(productFound)>0):
        productFound[0]['name'] = request.json['name']
        productFound[0]['price'] = request.json['price']
        productFound[0]['quantity'] = request.json['quantity']
        return jsonify({
            "message":"Product Update",
            "product": productFound[0]
        })
    return jsonify({"message": "Product not found"}) 

@app.route('/products/<string:product_name>', methods=['DELETE'])
def deleteProduct(product_name):
    productsFound= [product for product in products if product['name']== product_name]
    if (len(productsFound)>0):
        products.remove(productsFound[0])

      
        return jsonify({
            "message":"Product Deleted",
            "products": products
        })
    return jsonify({"message": "Product not found"}) 


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return jsonify({"error":"Error, vuelva a ingresar los datos"})

if __name__ == "__main__":
    app.run(debug= True, port = 4000)