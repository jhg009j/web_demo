var xfzalert = {
    'BasicMessage': function (msg) {
        Swal.fire(msg);
    },
    'QuestionMessage': function (title, text) {
        Swal.fire(
            title,
            text,
            'question'
        )
    },
    'InputMessage': function (title, msg, func) {
        Swal.fire({
            title: title,
            input: 'text',
            inputPlaceholder: msg,
            showConfirmButton: true,
            showCancelButton: true,
            confirmButtonText: '确认',
            cancelButtonText: '取消',
            preConfirm: func,
            inputValidator: (value) => {
                if (!value) {
                    return '请输入分类名！'
                }
            }

        });
    },
    'WarningMessage': function (title, text, func) {
        Swal.fire({
            title: title,
            text: text,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: '删除',
            cancelButtonText: '取消',
            preConfirm: func
        })
    },
    'Close': function () {
        Swal.close();
    },
    'SuccessMessage': function () {
        Swal.fire({
            position: 'top-end',
            icon: 'success',
            title: '操作成功！',
            showConfirmButton: false,
            timer: 1500,
            width: '400px',
            height:'200px'
        })
    },
    'SuccessBox': function (title,text, func) {
        Swal.fire({
            title: title,
            text: text,
            icon: 'success',
            preConfirm: func
        })
    },
};

