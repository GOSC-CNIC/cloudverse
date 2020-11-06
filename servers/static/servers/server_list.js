;(function () {

    //
    // 页面刷新时执行
    window.onload = function() {
        update_vms_status(get_vm_list_uuid_array());
    };

    /*
     * 拼接params对象为url参数字符串
     * @param {Object} obj - 待拼接的对象
     * @returns {string} - 拼接成的query参数字符串
     */
    function encode_params(obj) {
        const params = [];

        Object.keys(obj).forEach((key) => {
            let value = obj[key];
            // 如果值为undefined我们将其置空
            if (typeof value === 'undefined') {
                value = ''
            }
            // 对于需要编码的文本我们要进行编码
            params.push([key, encodeURIComponent(value)].join('='))
        });

        return params.join('&');
    }

    //
    // 全选/全不选
    //
    $(":checkbox[data-check-target]").on('click', function () {
        let target = $(this).attr('data-check-target');
        if ($(this).prop('checked')) {
            $(target).prop('checked', true); // 全选
            $(target).parents('tr').addClass('bg-warning'); // 选中时添加 背景色类
        } else {
            $(target).prop('checked', false); // 全不选
            $(target).parents('tr').removeClass('bg-warning');// 不选中时移除 背景色类
        }
    });

    //
    // 表格中每一行单选checkbox
    //
    $(".item-checkbox").on('click', function () {
        if ($(this).prop('checked')){
            $(this).parents('tr').addClass('bg-warning');
        }else{
            $(this).parents('tr').removeClass('bg-warning');
        }
    });

    // 有多少虚拟机被选中
    function get_checked_vm_count() {
        return $(".item-checkbox:checked").length
    }

    //
    // 检测是否有选中项
    //
    function is_exists_checked() {
        return get_checked_vm_count() !== 0
    }

    //
    // 获取所有的当前选中的虚拟机的uuid数组
    //
    function get_checked_vm_uuid_array() {
        var arr = [];
        let bucket_list_checked = $(".table-vm-list :checkbox:checked.item-checkbox");
        bucket_list_checked.each(function (i) {
            arr.push($(this).val());
        });

        return arr;
    }

    //
    // 获取table中所有的虚拟机的uuid数组
    //
    function get_vm_list_uuid_array() {
        var arr = [];
        let bucket_list_checked = $(".table-vm-list :checkbox.item-checkbox");
        bucket_list_checked.each(function (i) {
            arr.push($(this).val());
        });

        return arr;
    }

    // 获取并设置虚拟机的运行状态
    function get_vm_status(url, vmid) {
        let node_status = $("#vm_status_" + vmid);
        node_status.html(`<i class="fa fa-spinner fa-pulse"></i>`);
        $.ajax({
            url: url,
            type: 'get',
            cache:false,
            success: function(data) {
                node_status.html('<span class="badge  badge-' + VM_STATUS_LABEL[data.status.status_code] + '">' + VM_STATUS_CN[data.status.status_code] + "</span>");
            },
            error: function (xhr) {
                node_status.html('<span class="badge  badge-danger">查询失败</span>');
            }
        });
    }

    function update_vms_status(vmids){
        for(let i in vmids) {
            let api = build_vm_status_api(vmids[i]);
            get_vm_status(api, vmids[i]);
        }
    }

    // 刷新虚拟机状态点击事件
    $(".btn-update-vm-status").click(function (e) {
        e.preventDefault();
        update_vms_status(get_vm_list_uuid_array());
    });

    // 虚拟机运行状态api构建
    function build_vm_status_api(vm_uuid){
        let url = 'api/server/' + vm_uuid + '/status/';
        return build_absolute_url(url);
    }

    // 虚拟机vnc api构建
    function build_vm_vnc_api(vm_uuid){
        let url = 'api/server/' + vm_uuid + '/vnc/';
        return build_absolute_url(url);
    }

    function start_vm(vm_uuid){
        let node_vm_task = $("#vm_task_" + vm_uuid);
        start_vm_ajax(vm_uuid, function () {
            node_vm_task.html(VM_TASK_CN["start"]);
        }, function () {
            node_vm_task.html("");
            let api = build_vm_status_api(vm_uuid);
            get_vm_status(api, vm_uuid);
        });
    }

    // 启动虚拟机点击事件
    $(".btn-vm-start").click(function (e) {
        e.preventDefault();

        let vm_uuid = $(this).attr('data-server-id');
        start_vm(vm_uuid);
    });

    function reboot_vm(vm_uuid){
        let node_vm_task = $("#vm_task_" + vm_uuid);
        reboot_vm_ajax(vm_uuid, function () {
            node_vm_task.html(VM_TASK_CN["reboot"]);
        }, function () {
            node_vm_task.html("");
            let api = build_vm_status_api(vm_uuid);
            get_vm_status(api, vm_uuid);
        });
    }
    // 重启虚拟机点击事件
    $(".btn-vm-reboot").click(function (e) {
        e.preventDefault();
        if(!confirm('确定重启虚拟机？'))
		    return;

        let vm_uuid = $(this).attr('data-server-id');
        reboot_vm(vm_uuid);
    });

    function shutdown_vm(vm_uuid){
        let node_vm_task = $("#vm_task_" + vm_uuid);
        shutdown_vm_ajax(vm_uuid, function () {
            node_vm_task.html(VM_TASK_CN["shutdown"]);
        }, function () {
            let api = build_vm_status_api(vm_uuid);
            node_vm_task.html("");
            get_vm_status(api, vm_uuid);
        });
    }
    // 关机虚拟机点击事件
    $(".btn-vm-shutdown").click(function (e) {
        e.preventDefault();

        if(!confirm('确定关闭虚拟机？'))
		    return;

        let vm_uuid = $(this).attr('data-server-id');
        shutdown_vm(vm_uuid);
    });

    function poweroff_vm(vm_uuid){
        let node_vm_task = $("#vm_task_" + vm_uuid);
        poweroff_vm_ajax(vm_uuid, function () {
            node_vm_task.html(VM_TASK_CN["poweroff"]);
        }, function () {
            node_vm_task.html("");
            let api = build_vm_status_api(vm_uuid);
            get_vm_status(api, vm_uuid);
        });
    }
    // 强制断电虚拟机点击事件
    $(".btn-vm-poweroff").click(function (e) {
        e.preventDefault();

        if(!confirm('确定强制断电虚拟机？'))
		    return;

        let vm_uuid = $(this).attr('data-server-id');
        poweroff_vm(vm_uuid);
    });

    function delete_vm(vm_uuid, op){
        let node_vm_task = $("#vm_task_" + vm_uuid);
        delete_vm_ajax(vm_uuid, op,
            function () {
                node_vm_task.html(VM_TASK_CN[op]);
            },
            function () {
                node_vm_task.parents('tr').remove();
            },
            function () {
                node_vm_task.html("");
                let api = build_vm_status_api(vm_uuid);
                get_vm_status(api, vm_uuid);
            }
        );
    }
    // 删除虚拟机点击事件
    $(".btn-vm-delete").click(function (e) {
        e.preventDefault();

        if(!confirm('确定删除虚拟机？'))
		    return;

        let vm_uuid = $(this).attr('data-server-id');
        delete_vm(vm_uuid, 'delete');
    });

    // 强制删除虚拟机点击事件
    $(".btn-vm-delete-force").click(function (e) {
        e.preventDefault();

        if(!confirm('确定强制删除虚拟机？'))
		    return;

        let vm_uuid = $(this).attr('data-server-id');
        delete_vm(vm_uuid, 'delete_force');
    });


    // 批量启动选中的所有虚拟机
    $("#id-btn-batch-vm-start").click(function (e) {
        e.preventDefault();
        if(!is_exists_checked())
            return;
        if(!confirm('确定启动所有选中的虚拟机？'))
		    return;

        let vm_uuids = get_checked_vm_uuid_array();
        for (let i=0, len=vm_uuids.length; i < len; i++){
            start_vm(vm_uuids[i]);
        }
    });

    // 批量关机选中的所有虚拟机
    $("#id-btn-batch-vm-shutdown").click(function (e) {
        e.preventDefault();
        if(!is_exists_checked())
            return;
        if(!confirm('确定关闭所有选中的虚拟机？'))
		    return;

        let vm_uuids = get_checked_vm_uuid_array();
        for (let i=0, len=vm_uuids.length; i < len; i++){
            shutdown_vm(vm_uuids[i]);
        }
    });

    // 批量断电选中的所有虚拟机
    $("#id-btn-batch-vm-poweroff").click(function (e) {
        e.preventDefault();
        if(!is_exists_checked())
            return;
        if(!confirm('确定强制断电所有选中的虚拟机？'))
		    return;

        let vm_uuids = get_checked_vm_uuid_array();
        for (let i=0, len=vm_uuids.length; i < len; i++){
            poweroff_vm(vm_uuids[i]);
        }
    });

    // 批量删除选中的所有虚拟机
    $("#id-btn-batch-vm-delete").click(function (e) {
        e.preventDefault();
        if(!is_exists_checked())
            return;
        if(!confirm('确定删除所有选中的虚拟机？'))
		    return;

        let vm_uuids = get_checked_vm_uuid_array();
        for (let i=0, len=vm_uuids.length; i < len; i++){
            delete_vm(vm_uuids[i], 'delete');
        }
    });

    // 批量删除选中的所有虚拟机
    $("#id-btn-batch-vm-delete-force").click(function (e) {
        e.preventDefault();
        if(!is_exists_checked())
            return;
        if(!confirm('确定强制删除所有选中的虚拟机？'))
		    return;

        let vm_uuids = get_checked_vm_uuid_array();
        for (let i=0, len=vm_uuids.length; i < len; i++){
            delete_vm(vm_uuids[i], 'delete_force');
        }
    });

    // 获取虚拟机vnc url
    function get_vm_vnc_url(vm_uuid){
        let api = build_vm_vnc_api(vm_uuid);
        $.ajax({
            url: api,
            type: 'get',
            success: function (data, status_text) {
                let vnc = data.vnc.url;
                window.open(vnc, '_blank');
            },
            error: function (xhr, msg, err) {
                msg = '打开vnc失败，请确认是否启动云主机';
                try {
                    let data = xhr.responseJSON;
                    if (data.hasOwnProperty('message')) {
                        msg = '打开vnc失败，请确认是否启动云主机。' + data.message;
                    }
                }catch (e) {}
                alert(msg);
            }
        });
    }

    // 打开vnc点击事件
    $(".btn-vnc-open").click(function (e) {
        e.preventDefault();
        let vm_uuid = $(this).attr('data-server-id');
        get_vm_vnc_url(vm_uuid);
    });

    $('.edit_vm_remark').click(function (e) {
        e.preventDefault();

        let div_show = $(this).parent();
        div_show.hide();
		div_show.next().show();
    });

    $('.save_vm_remark').click(function (e) {
        e.preventDefault();
        let vm_uuid = $(this).attr('data-server-id');
        let dom_remark = $(this).prev();
        let remark = dom_remark.val();
        let div_edit = dom_remark.parent();
        let div_show = div_edit.prev();

        let query_str = encode_params({remark:remark});
        $.ajax({
			url: '/api/server/' + vm_uuid + '/remark/?' + query_str,
			type: 'patch',
			success:function(data){
			    div_show.children("span:first").text(remark);
			},
            error: function(e){
			    alert('修改失败');
            },
			complete:function() {
				div_show.show();
				div_edit.hide();
			}
		});

    });

})();