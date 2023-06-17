def reportEntity(report) -> dict:
    return {
        "id": str(report["_id"]),
        "user_id": str(report["user_id"]),
        "type": str(report["type"]),
        "title": str(report["title"]),
        "content": str(report["content"]),
        "attachment": str(report["attachment"]),
        "status": str(report["status"]),
        "operator_call": str(report["operator_call"]),
        "personal_data_source": str(report["personal_data_source"]),
        "pd_operator_relation": str(report["pd_operator_relation"])
        
    }


def reportResponseEntity(report) -> dict:
    return {
        "type": str(report["type"]),
        "title": str(report["title"]),
        "content": str(report["content"]),
        "attachment": str(report["attachment"]),
        "status": str(report["status"]),
        "operator_call": str(report["operator_call"]),
        "personal_data_source": str(report["personal_data_source"]),
        "pd_operator_relation": str(report["pd_operator_relation"])
        
    }