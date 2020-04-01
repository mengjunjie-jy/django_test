import random
import requests

main_url = "http://127.0.0.1:8000"


def random_name():

    xing = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    ming = '豫章故郡洪都新府星分翼轸地接衡庐襟三江而带五湖四海'
    X = random.choice(xing)
    M = "".join(random.choice(ming) for i in range(2))
    print(X)
    print(M)
    print(X + M)
    return X + M


class FractionTest(object):
    def __init__(self):
        self.post_name = random_name()

    def post(self):
        data = {
            "client_name": self.post_name,
            "fraction": random.randrange(1, 10000000),
        }
        response = requests.post(main_url + "/fraction/", data=data)
        print(response.json())
        json_response = response.json()
        assert response.status_code == 200
        assert json_response.get("code") == "200"
        assert json_response.get("message") == "ok"

        data = {
            "client_name": random_name(),
            "fraction": random.randrange(1, 10000000),
        }
        response = requests.post(main_url + "/fraction/", data=data)
        print(response.json())
        json_response = response.json()
        assert response.status_code == 200
        assert json_response.get("code") == "200"
        assert json_response.get("message") == "ok"

    def get(self):
        data = {
            "client_name": self.post_name,
            "fraction": 15,
        }
        request_params = []
        for k, v in data.items():
            request_params.append(f"{k}={v}")

        print(request_params)
        response = requests.get(main_url + "/fraction/?{}".format("&".join(request_params)))
        print(response.json())
        json_response = response.json()
        assert response.status_code == 200
        assert json_response.get("code") == "200"
        assert json_response.get("message") == "ok"
        assert json_response.get("data", {}).get("page") == 1
        print(json_response.get("data", {}).get("count"))
        assert json_response.get("data", {}).get("count") == 10
        assert isinstance(json_response.get("data", {}).get("data"), list)
        assert json_response.get("data", {}).get("data")[-1], self.post_name

        data = {
            "client_name": random_name(),
            "fraction": 15,
            "page": 1,
            "count": 10,
        }
        request_params = []
        for k, v in data.items():
            request_params.append(f"{k}={v}")

        response = requests.get(main_url + "/fraction/?{}".format("&".join(request_params)))
        print(response.json())
        json_response = response.json()
        assert response.status_code == 200
        assert json_response.get("code") == "200"
        assert json_response.get("message") == "ok"
        assert json_response.get("data", {}).get("page") == 1
        assert isinstance(json_response.get("data", {}).get("data"), list)


if __name__ == '__main__':
    f = FractionTest()
    f.post()
    f.get()
