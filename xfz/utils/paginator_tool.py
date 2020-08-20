class PaginatorTool:
    def page_control(self, paginator_obj, page_obj):
        pre_range = list()
        later_range = list()
        context_range = dict()
        count = 2
        for i in paginator_obj.page_range:
            if page_obj.has_previous():
                if i <= page_obj.previous_page_number():
                    pre_range.append(i)
                    if len(pre_range) > count:
                        pre_dot = True
                        context_range['pre_dot'] = pre_dot
                    else:
                        pre_dot = False
                        context_range['pre_dot'] = pre_dot
                        context_range['pre_range'] = pre_range

            if page_obj.has_next():
                if i >= page_obj.next_page_number():
                    later_range.append(i)
                    if len(later_range) > count:
                        later_dot = True
                        context_range['later_dot'] = later_dot
                    else:
                        later_dot = False
                        context_range['later_dot'] = later_dot
                        context_range['later_range'] = later_range
        return context_range

    def page_control2(self, paginator_obj, page_obj):
        count = 2
        pre_dot = False
        later_dot = False
        context_range = {}

        if page_obj.has_previous():
            pre_page_num = page_obj.previous_page_number()
            if pre_page_num > count:
                pre_dot = True
            else:
                pre_range = range(1, pre_page_num+1)
                context_range['pre_range'] = pre_range

        if page_obj.has_next():
            next_page_num = page_obj.next_page_number()
            if next_page_num + count < paginator_obj.page_range[-1]:
                later_dot = True
            else:
                later_range = range(next_page_num, paginator_obj.page_range[-1]+1)
                context_range['later_range'] = later_range

        context_range['later_dot'] = later_dot
        context_range['pre_dot'] = pre_dot

        return context_range
