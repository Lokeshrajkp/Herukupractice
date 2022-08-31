from flask import Flask,request,render_template,jsonify
from flask_cors import CORS,cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
app=Flask(__name__)
@app.route('/',methods=['GET'])
@cross_origin()
def homepage():
    return render_template("index.html")
@app.route('/review',methods=['GET','POST'])
@cross_origin()
def index():
    if request.method=='POST':
        try:
            searchstring=request.form['content'].replace(" ","")
            flipkart_url="https://www.flipkart.com/search?q="+searchstring
            uclient=uReq(flipkart_url)
            flipkartPage=uclient.read()
            uclient.close()
            flipkart_html=bs(flipkartPage,"html.parser")
            bigboxes=flipkart_html.find_all('div',{"class":"_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box=bigboxes[0]
            productlink="https://www.flipkart.com"+box.div.div.div.a['href']
            prodres=requests.get(productlink)
            prodres.encoding='utf-8'
            prod_html=bs(prodres.text,"html.parser")
            print(prod_html)
            comment_boxes=prod_html.findall('div',{"class":"_16PBlm"})
            filename=searchstring+".csv"
            fw=filename.open(filename,"w")
            headers="price,product,customer name,rating,heading,comment\n"
            fw.write(headers)
            reviews=[]
            for comment_box in comment_boxes:
                try:
                    price = prod_html.find_all('div', {"class":"_30jeq3 _16Jk6d"})[0].text
               except:
                    price='No price'
                try:
                    name=comment_box.div.div.find_all('p',{"class":"_2sc7ZR _2V5EHH"})[0].text
                except:
                    name='No Name'
                try:
                    customerrating=comment_box.div.div.div.div.text
                except:
                    rating='No rating'
                try:
                    commenthead=comment_box.div.div.div.p.text
                except:
                    commmenthead= 'No heading'
                try:
                    comtag=comment_box.div.div.find_all('div',{"class":""})
                    custcomment=comment[0].div.text
                except Exception as e:
                    print('Exception while creating dictionary: ",e')
                mydict={"price":price,"product":searchstring,"Name":name,"Rating":rating,"commenthead":commenthead,"comment":customcomment}
                reviews.append(mydict)
            return render_template("results.html",reviews=reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('The Exception message is: ', e)
            return 'something is wrong'
    else:
        return render_template("index.html")
if __name__=='__main__':
    app.run(debug=True)




