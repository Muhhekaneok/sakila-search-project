def get_limit():
    # limit_input = input("Enter max number of result (leave emtpy for all): ")
    # try:
    #     limit = int(limit_input) if limit_input.strip() else None
    # except ValueError:
    #     print("Invalid limit value")
    #     return None
    # return limit

    limit_input = input("Enter max number of result (leave emtpy for all): ")
    try:
        return int(limit_input) if limit_input.strip() else None
    except ValueError:
        print("Invalid limit value")
        return None