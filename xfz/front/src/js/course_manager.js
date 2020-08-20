function DateChooser() {
    this.start_date = $('#InputStartDate');
    this.end_date = $('#InputEndDate');
    var today = new Date();
    var current_year = today.getFullYear();
    var current_month = today.getMonth();
    var current_day = today.getDate();
    this.todayStr = current_year + "-" + (current_month + 1) + "-" + current_day;
}

DateChooser.prototype.DatePicker = function () {
    var self = this;
    var todayStr = self.todayStr;
    self.start_date.daterangepicker({
        "singleDatePicker": true,
        "locale": {
            "format": "YYYY-MM-DD",
            "applyLabel": "Apply",
            "cancelLabel": "Cancel",
            "fromLabel": "From",
            "toLabel": "To",
            "customRangeLabel": "Custom",
            "weekLabel": "W",
            "daysOfWeek": [
                "日",
                "一",
                "二",
                "三",
                "四",
                "五",
                "六"
            ],
            "monthNames": [
                "一月",
                "二月",
                "三月",
                "四月",
                "五月",
                "六月",
                "七月",
                "八月",
                "九月",
                "十月",
                "十一月",
                "十二月"
            ],
            "firstDay": 1,
        },
        "showCustomRangeLabel": false,
        "startDate": "2020-2-25",
        "minDate": "2020-2-25",
        "maxDate": todayStr
    }, function (start, end, lable) {

    });
    self.end_date.daterangepicker({
        "singleDatePicker": true,
        "locale": {
            "format": "YYYY-MM-DD",
            "applyLabel": "Apply",
            "cancelLabel": "Cancel",
            "fromLabel": "From",
            "toLabel": "To",
            "customRangeLabel": "Custom",
            "weekLabel": "W",
            "daysOfWeek": [
                "日",
                "一",
                "二",
                "三",
                "四",
                "五",
                "六"
            ],
            "monthNames": [
                "一月",
                "二月",
                "三月",
                "四月",
                "五月",
                "六月",
                "七月",
                "八月",
                "九月",
                "十月",
                "十一月",
                "十二月"
            ],
            "firstDay": 1,
        },
        "showCustomRangeLabel": false,
        "minDate": "2020-2-25",
        "maxDate": todayStr
    }, function (start, end, lable) {

    })
};

function CourseManager() {
    this.ClearBtn = $('.clear-search');
    var today = new Date();
    var current_year = today.getFullYear();
    var current_month = today.getMonth();
    var current_day = today.getDate();
    this.todayStr = current_year + "-" + (current_month + 1) + "-" + current_day;
}

CourseManager.prototype.ClearSearchInfo = function () {
    var self = this;
    self.ClearBtn.click(function () {
        var startDate = $('#InputStartDate');
        var endDate = $('#InputEndDate');
        var keyword = $('#InputKeyword');
        var category = $('#InputCategory');
        var todayStr = self.todayStr;
        startDate.val('2020-2-25');
        endDate.val(todayStr);
        keyword.val('');
        category.val(0);
    })
};

CourseManager.prototype.DeleteNews = function () {
    var self = this;
    var DelBtn = $('.del-btn');
    DelBtn.click(function () {
        var currentBtn = $(this);
        var tr = currentBtn.parent().parent();
        var courseid = tr.attr('course-id');
        xfzalert.WarningMessage('删除课程', '请注意，删除后将无法恢复！', function () {
            xfzajax.post({
                'url': '',
                'data': {
                    'pk': courseid
                },
                'success': function (result) {
                    if (result['code'] === 200) {
                        xfzalert.SuccessBox('删除课程', '课程删除成功！', function () {
                            window.location.reload();
                        })
                    } else {
                        xfzajax.success(result['message'])
                    }
                }
            })
        })
    })
};

$(function () {
    var datechooser = new DateChooser();
    datechooser.DatePicker();
    var couesemanager = new CourseManager();
    couesemanager.ClearSearchInfo();
    couesemanager.DeleteNews();
});