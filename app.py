from flask import Flask, jsonify, redirect, render_template, url_for
from flask import request
import requests
import json
app = Flask(__name__)

# функция получает данные и отправляет на две другие функции которые фильтруют данные и отправляют по двум запросам.
@app.route('/', methods=['GET', 'POST'])
def main():
    page= 1
    api_url = 'https://b7w2x7a.retailcrm.ru/api/v5/orders'
    request_params = {'apiKey': 'FjqFa87rUgdvxFhrhyPQQiy41kl5AnXq', 'page': page}
    r = requests.get(api_url, params=request_params)
    r_json = r.json()

    if request.method == 'POST':
        resp_data= add_site_data(r_json)
        resp_items= add_site_items(r_json)

        return render_template('result.html', resp_data=resp_data , resp_items= resp_items)
    return render_template('view.html', json=r_json)

# функция получает данные пробегаясь пагинацией по запросу и собирая большой массив отправляет на сервер
@app.route('/send', methods=['GET', 'POST'])
def send():
    page= 1
    api_url = 'https://b7w2x7a.retailcrm.ru/api/v5/orders'
    request_params = {'apiKey': 'FjqFa87rUgdvxFhrhyPQQiy41kl5AnXq', 'page': page}
    r = requests.get(api_url, params=request_params)
    r_json = r.json()
    total_list = r_json["orders"]
    # print(type(total_list))
    for page in range(2, r_json["pagination"]["totalPageCount"]+1):
        r = requests.get(api_url, params =f"apiKey=FjqFa87rUgdvxFhrhyPQQiy41kl5AnXq&page={page}")
        r_json = r.json()
        total_list.extend(r_json["orders"])
        # print(json)
    # print(len(total_list))
    if request.method == 'POST':
        # resp_data= add_site_data(r_json)
        resp_data= add_site_items_pagination(total_list)

        return render_template('result2.html',  resp_data= resp_data)
    return render_template('view2.html', json=total_list)

# функция отправки данных data
def add_site_data(json):
    orders_list = json.get('orders')
    user = "Богатырев Б.В."
    data_site_data = []
    for i in orders_list:
        if len(i.get("items")) != 0:
            for t in range(len(i.get("items"))):
                offer_id = str(i["items"][t]["offer"]["id"])
                bonusesCreditTotal = (i["bonusesCreditTotal"])
                bonusesChargeTotal = (i["bonusesChargeTotal"])
                externalId = (i["externalId"])
                orderType = (i["orderType"])
                orderMethod = (i["orderMethod"])
                privilegeType = (i["privilegeType"])
                countryIso = (i["countryIso"])
                createdAt = (i["createdAt"])
                statusUpdatedAt = (i["statusUpdatedAt"])
                summ = (i["summ"])
                totalSumm = (i["totalSumm"])
                prepaySum = (i["prepaySum"])
                purchaseSumm = (i["purchaseSumm"])
                markDatetime = (i["markDatetime"])
                lastName = (i["lastName"])
                firstName = (i["firstName"])
                phone = (i["phone"])
                email = (i["email"])
                call = (i["call"])
                expired = (i["expired"])
                site = (i["site"])
                status = (i["status"])
                # обработал исключение отсутсвия ключа.
                fullPaidAt = (i.get("fullPaidAt", "unknown"))
                fromApi = (i["fromApi"])
                shipmentStore = (i["shipmentStore"])
                shipped = (i["shipped"])
                currency = (i["currency"])

                my_dict_data = {"offer_id": offer_id,
                          "bonusesCreditTotal": bonusesCreditTotal,
                          "bonusesChargeTotal": bonusesChargeTotal,
                          "externalId": externalId,
                          "orderType": orderType,
                          "orderMethod": orderMethod,
                          "privilegeType": privilegeType,
                          "countryIso": countryIso,
                          "createdAt": createdAt,
                          "statusUpdatedAt": statusUpdatedAt,
                          "summ": summ,
                          "totalSumm": totalSumm,
                          "prepaySum": prepaySum,
                          "purchaseSumm": purchaseSumm,
                          "markDatetime": markDatetime,
                          "lastName": lastName,
                          "firstName": firstName,
                          "phone": phone,
                          "email": email,
                          "call": call,
                          "expired": expired,
                          "site": site,
                          "status": status,
                          "fullPaidAt": fullPaidAt,
                          "fromApi": fromApi,
                          "shipmentStore": shipmentStore,
                          "shipped": shipped,
                          "currency": currency, }
                data_site_data.append(my_dict_data)
    context = {"user": user, "data": data_site_data}
    # print(context)
    res = requests.post(
        'http://94.241.143.164:8000/site/add_site_data/', json=context)
    print(res.json())
    return res.json()

# функция отправки данных items
def add_site_items(json):
    orders_list = json.get('orders')
    user = "Богатырев Б.В."
    data_site_items = []
    for i in orders_list:
        if len(i.get("items")) != 0:
            for t in range(len(i.get("items"))):
                bonusesChargeTotal = (i["items"][t]["bonusesChargeTotal"])
                bonusesCreditTotal = (i["items"][t]["bonusesCreditTotal"])
                initialPrice = (i["items"][t]["initialPrice"])
                discountTotal = (i["items"][t]["discountTotal"])
                vatRate = int(float(i["items"][t]["vatRate"]))
                createdAt = (i["items"][t]["createdAt"])
                quantity_1 = (i["items"][t]["quantity"])
                status = (i["items"][t]["status"])
                purchasePrice = str(i["items"][t]["purchasePrice"])
                ordering = (i["items"][t]["ordering"])
                offer_displayName = (i["items"][t]["offer"]["displayName"])
                offer_id = str(i["items"][t]["offer"]["id"])
                offer_externalId = (i["items"][t]["offer"]["externalId"])
                offer_xmlId = (i["items"][t]["offer"]["xmlId"])
                offer_name = (i["items"][t]["offer"]["name"])
                offer_article = (i["items"][t]["offer"]["article"])
                offer_vatRate = (i["items"][t]["offer"]["vatRate"])
                offer_properties_type = (
                    i["items"][t]["offer"]["properties"]["type"])
                offer_unit_code = (i["items"][t]["offer"]["unit"]["code"])
                offer_unit_name = (i["items"][t]["offer"]["unit"]["name"])
                offer_unit_sym = (i["items"][t]["offer"]["unit"]["sym"])
                price = (i["items"][t]["prices"][0]["price"])
                my_dict_items = {
                    "bonusesChargeTotal": bonusesChargeTotal,
                    "bonusesCreditTotal": bonusesCreditTotal,
                    "initialPrice": initialPrice,
                    "discountTotal": discountTotal,
                    "vatRate": vatRate,
                    "createdAt": createdAt,
                    "quantity_1": quantity_1,
                    "status": status,
                    "purchasePrice": purchasePrice,
                    "ordering": ordering,
                    "offer_displayName": offer_displayName,
                    "offer_id": offer_id,
                    "offer_externalId": offer_externalId,
                    "offer_xmlId": offer_xmlId,
                    "offer_name": offer_name,
                    "offer_article": offer_article,
                    "offer_vatRate": offer_vatRate,
                    "offer_properties_type": offer_properties_type,
                    "offer_unit_code": offer_unit_code,
                    "offer_unit_name": offer_unit_name,
                    "offer_unit_sym": offer_unit_sym,
                    "price": price,
                }
                data_site_items.append(my_dict_items)
    context = {"user":user, "data":data_site_items}
    # print(context)
    res = requests.post('http://94.241.143.164:8000/site/add_site_items/', json = context)
    print(res.json())
    return res.json()

def add_site_items_pagination(json):
    orders_list = json
    user = "Богатырев Б.В."
    data_site_data = []
    for i in orders_list:
        if len(i.get("items")) != 0:
            for t in range(len(i.get("items"))):
                offer_id = str(i["items"][t]["offer"]["id"])
                bonusesCreditTotal =(i.get("bonusesCreditTotal", "unknown"))
                bonusesChargeTotal = (i.get("bonusesChargeTotal", "unknown"))
                externalId = (i.get("externalId", "unknown"))
                orderType = (i.get("orderType", "unknown"))
                orderMethod = (i.get("orderMethod", "unknown"))
                privilegeType = (i.get("privilegeType", "unknown"))
                countryIso = (i.get("countryIso", "unknown"))
                createdAt = (i.get("createdAt", "unknown"))
                statusUpdatedAt = (i.get("statusUpdatedAt", "unknown"))
                summ = int(float(i.get("summ", "unknown")))
                totalSumm = int(float(i.get("totalSumm", "unknown")))
                prepaySum = int(float(i.get("prepaySum", "unknown")))
                purchaseSumm = int(float(i.get("purchaseSumm", "unknown")))
                markDatetime = (i.get("markDatetime", "unknown"))
                lastName = (i.get("lastName", "unknown"))
                firstName = (i.get("firstName", "unknown"))
                phone = (i.get("phone", "unknown"))
                email = (i.get("email", "unknown"))
                call = (i.get("call", "unknown"))
                expired = (i.get("expired", "unknown"))
                site = (i.get("site", "unknown"))
                status = (i.get("status", "unknown"))
                # обработал исключение отсутсвия ключа.
                fullPaidAt = (i.get("fullPaidAt", "unknown"))
                fromApi = (i.get("fromApi", "unknown"))
                shipmentStore = (i.get("shipmentStore", "unknown"))
                shipped = (i.get("shipped", "unknown"))
                currency = (i.get("currency", "unknown"))

                my_dict_data = {"offer_id": offer_id,
                          "bonusesCreditTotal": bonusesCreditTotal,
                          "bonusesChargeTotal": bonusesChargeTotal,
                          "externalId": externalId,
                          "orderType": orderType,
                          "orderMethod": orderMethod,
                          "privilegeType": privilegeType,
                          "countryIso": countryIso,
                          "createdAt": createdAt,
                          "statusUpdatedAt": statusUpdatedAt,
                          "summ": summ,
                          "totalSumm": totalSumm,
                          "prepaySum": prepaySum,
                          "purchaseSumm": purchaseSumm,
                          "markDatetime": markDatetime,
                          "lastName": lastName,
                          "firstName": firstName,
                          "phone": phone,
                          "email": email,
                          "call": call,
                          "expired": expired,
                          "site": site,
                          "status": status,
                          "fullPaidAt": fullPaidAt,
                          "fromApi": fromApi,
                          "shipmentStore": shipmentStore,
                          "shipped": shipped,
                          "currency": currency, }
                data_site_data.append(my_dict_data)
    context = {"user": user, "data": data_site_data}
    # print(context)
    res = requests.post(
        'http://94.241.143.164:8000/site/add_site_data/', json=context)
    print(res.json())
    return res.json()


if __name__ == '__main__':
    app.run(debug=True)
