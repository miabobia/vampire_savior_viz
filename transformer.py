# from reader import start_reading

def get_values():
    return parse_json(start_reading())

def parse_json(player_dict: dict):
    #s = "hello".encode("utf-8").hex()
    # print(len(player_dict.keys()))
    return [v for k,v in player_dict.items()]
    # for k, v in player_dict.items():
    #     print(v)


# if __name__ == '__main__':
#     parse_json(start_reading())