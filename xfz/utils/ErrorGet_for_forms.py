class ErrorGet(object):
    def get_error(self):
        new_errors_data = {}
        error_data = self.errors.get_json_data()
        for fields, errors_list in error_data.items():
            messages = []
            for error_message in errors_list:
                messages.append(error_message['message'])
            new_errors_data[fields] = messages
            # 最后得到的数据：
            # {'password:['xxx','xxx'],'telephone':['xxx','xxx']}
        return new_errors_data
