def userEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": str(user["first_name"]),
        "last_name": str(user["last_name"]),
        "company": str(user["company"]),
        "phone_number": str(user["phone_number"]),
        "email": str(user["email"]),
        "password": str(user["password"]),
        "active": str(user["active"])
    }


def userResponseEntity(user) -> dict:
    return {
        "id": str(user["_id"]),
        "first_name": user["first_name"],
        "last_name": str(user["last_name"]),
        "company": str(user["company"]),
        "phone_number": str(user["phone_number"]),
        "email": str(user["email"]),
        "role": str(user["role"]),
        "created_at": user["created_at"],
        "updated_at": user["updated_at"],
        "active": str(user["active"])
    }




